import tempfile

import os

import shutil
from enum import Enum
from fractions import Fraction

from django.utils import timezone

from jinja2 import Environment, PackageLoader
from rq import get_current_job

from osmaxx.conversion._settings import odb_license
from osmaxx.conversion.converters.converter_gis.bootstrap import BootStrapper
from osmaxx.conversion.converters.converter_gis.extract.db_to_format.extract import extract_to
from osmaxx.conversion.converters.utils import zip_folders_relative, recursive_getsize
from osmaxx.conversion_api.formats import FORMAT_DEFINITIONS


def perform_export(
        *, conversion_format, output_zip_file_path, filename_prefix, out_srs, osmosis_polygon_file_string, detail_level,
        **__):
    gis = GISConverter(
        conversion_format=conversion_format,
        output_zip_file_path=output_zip_file_path,
        base_file_name=filename_prefix,
        out_srs=out_srs,
        polyfile_string=osmosis_polygon_file_string,
        detail_level=detail_level
    )
    gis.create_gis_export()


QGIS_DISPLAY_SRID = 3857  # Web Mercator


class ScaleLevel(Enum):
    m1 = Fraction(1, 2500)
    m3 = Fraction(1, 10000)
    m4 = Fraction(1, 25000)


class GISConverter:
    def __init__(
            self, *, conversion_format, output_zip_file_path, base_file_name, out_srs, polyfile_string, detail_level):
        """
        Converts a specified pbf into the specified format.

        Args:
            output_zip_file_path: path to where the zipped result should be stored, directory must already exist
            conversion_format: One of 'fgdb', 'shapefile', 'gpkg', 'spatialite'
            base_file_name: base for created files inside the zip file

        Returns:
            the path to the resulting zip file
        """
        self._base_file_name = base_file_name
        self._out_zip_file_path = output_zip_file_path
        self._polyfile_string = polyfile_string
        self._conversion_format = conversion_format
        self._out_srs = out_srs
        dir = os.path.abspath(os.path.dirname(__file__))
        self._static_directory = os.path.join(dir, 'static')
        self._symbology_directory = os.path.join(dir, 'symbology')
        self._env = Environment(loader=PackageLoader(__package__, os.path.join('symbology', 'templates')))
        self._env.globals.update(zip=zip)
        self._detail_level = detail_level
        self._start_time = None

    def create_gis_export(self):
        self._start_time = timezone.now()

        _bootstrapper = BootStrapper(self._polyfile_string, detail_level=self._detail_level)
        _bootstrapper.bootstrap()
        geom_in_qgis_display_srs = _bootstrapper.geom.transform(QGIS_DISPLAY_SRID, clone=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            data_dir = os.path.join(tmp_dir, 'data')
            data_location = self._dump_gis_data(data_dir, tmp_dir)
            unzipped_result_size = recursive_getsize(data_dir)

            symbology_dir = os.path.join(tmp_dir, 'symbology')
            self._dump_qgis_symbology(data_location, geom_in_qgis_display_srs, target_dir=symbology_dir)

            zip_folders_relative([tmp_dir], zip_out_file_path=self._out_zip_file_path)

        job = get_current_job()
        if job:
            total_duration = timezone.now() - self._start_time
            job.meta['duration'] = total_duration
            job.meta['unzipped_result_size'] = unzipped_result_size
            job.save()
        return self._out_zip_file_path

    def _dump_gis_data(self, data_dir, target_dir):
        static_dir = os.path.join(target_dir, 'static')
        os.makedirs(data_dir)
        shutil.copytree(self._static_directory, static_dir)
        shutil.copy(odb_license, static_dir)
        data_location = extract_to(
            to_format=self._conversion_format,
            output_dir=data_dir,
            base_filename=self._base_file_name,
            out_srs=self._out_srs
        )
        return data_location

    def _dump_qgis_symbology(self, data_location, geom_in_qgis_display_srs, target_dir):
        qgis_symbology_dir = os.path.join(target_dir, 'QGIS')
        os.makedirs(qgis_symbology_dir)
        qgis_symbology_readme = os.path.join(self._symbology_directory, 'README.rst')
        shutil.copy(qgis_symbology_readme, qgis_symbology_dir)
        for scale_level in ScaleLevel:
            template = self._env.get_template('OSMaxx_{}.qgs.jinja2'.format(scale_level.name.upper()))
            format_definition = FORMAT_DEFINITIONS[self._conversion_format]
            template.stream(
                data_location=os.path.basename(data_location),
                separator=format_definition.qgis_datasource_separator,
                extension=format_definition.layer_filename_extension,
                extent=geom_in_qgis_display_srs.extent
            ).dump(os.path.join(qgis_symbology_dir, 'OSMaxx_{}.qgs'.format(scale_level.name.upper())))
        shutil.copytree(
            os.path.join(self._symbology_directory, 'OSMaxx_point_symbols'),
            os.path.join(target_dir, 'OSMaxx_point_symbols'),
        )
