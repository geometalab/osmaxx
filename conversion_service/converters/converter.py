import tempfile

import os
import shutil
import time

from converters import garmin_converter
from converters import gis_converter
from converters.gis_converter.bootstrap import bootstrap
from converters.gis_converter.extract.db_to_format.extract import extract_to
from converters.gis_converter.extract.db_to_format.zip import zip_folders_relative
from converters.gis_converter.extract.statistics.statistics import gather_statistics
from utils import changed_dir


class Conversion(object):
    def __init__(self, formats, output_dir, osm_pbf_path, basename='osmaxx_excerpt'):
        self.formats = formats
        self.output_dir = output_dir
        self.filename_prefix = '_'.join([
            basename,
            time.strftime("%Y-%m-%d_%H%M%S"),
        ])
        self.tmp_statistics_filename = self.filename_prefix + '_tmp'
        self.pbf_path = osm_pbf_path

    def start_format_extraction(self):
        garmin_formats, gis_formats = self._split_formats()
        self._create_garmin_export(garmin_formats)
        self._extract_postgis_formats(gis_formats)

    def _extract_postgis_formats(self, formats):
        if len(formats) > 0:
            bootstrap.boostrap(self.pbf_path)
            with changed_dir(os.path.dirname(__file__)):
                # only create statistics once and remove it when done with all formats
                self._create_statistics()
                for format in formats:
                    file_basename = '_'.join([self.filename_prefix, format])
                    self._copy_statistics_file_to_format_dir(file_basename)
                    self._export_from_db_to_format(file_basename, format)
                # remove the temporary statistics file
                os.remove(self._get_statistics_file_path())

    def _create_garmin_export(self, formats):
        assert len(formats) <= 1
        if len(formats) == 1:
            # FIXME: pass the area name to get a better identification instead of just `Garmin`
            garmin = garmin_converter.Garmin(self.output_dir, self.pbf_path, 'Garmin')
            garmin.create_garmin_export()

    # Export files of the specified format (file_format) from existing database
    def _export_from_db_to_format(self, file_basename, file_format):
        extract_base_dir = os.path.join(os.path.dirname(__file__), 'gis_converter', 'extract')

        tmp_dir = tempfile.mkdtemp()
        try:
            data_work_dir = os.path.join(tmp_dir, 'data')
            os.mkdir(data_work_dir)
            extract_to(to_format=file_format, output_dir=data_work_dir, base_filename=file_basename)

            zip_result_path = os.path.join(self.output_dir, file_basename + '.zip')
            extra_data_dir = os.path.join(extract_base_dir, 'static')
            zip_folders_relative([tmp_dir, extra_data_dir], zip_out_file_path=zip_result_path)
        finally:
            shutil.rmtree(tmp_dir)

    # Extract Statistics
    def _create_statistics(self):
        os.makedirs(os.path.join(self.output_dir, 'tmp'), exist_ok=True)
        gather_statistics(self._get_statistics_file_path())

    def _copy_statistics_file_to_format_dir(self, file_basename):  # pragma: nocover
        shutil.copyfile(
            self._get_statistics_file_path(),
            os.path.join(self.output_dir, 'tmp', file_basename + '_STATISTICS.csv')
        )

    def _split_formats(self):
        garmin_formats = [garmin_format for garmin_format in self.formats
                          if garmin_format in garmin_converter.options.get_output_formats()]
        gis_formats = [gis_format for gis_format in self.formats
                       if gis_format in gis_converter.options.get_output_formats()]
        return garmin_formats, gis_formats

    def _get_statistics_file_path(self):
        return os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv')
