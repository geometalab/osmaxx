import tempfile

import os

import shutil

from osmaxx.conversion.converters.converter_gis.bootstrap import bootstrap
from osmaxx.conversion.converters.converter_gis.extract.db_to_format.extract import extract_to
from osmaxx.conversion.converters.converter_gis.extract.statistics.statistics import gather_statistics
from osmaxx.conversion.converters.utils import zip_folders_relative


class GISConverter:
    def __init__(self, *, conversion_format, out_zip_file_path, base_file_name, out_srs, polyfile_string):
        """
        Converts a specified pbf into the specified format.

        Args:
            out_zip_file_path: path to where the zipped result should be stored, directory must already exist
            conversion_format: One of 'fgdb', 'shapefile', 'gpkg', 'spatialite'
            base_file_name: base for created files inside the zip file

        Returns:
            the path to the resulting zip file
        """
        self._base_file_name = base_file_name
        self._out_zip_file_path = out_zip_file_path
        self._polyfile_string = polyfile_string
        self._conversion_format = conversion_format
        self._out_srs = out_srs
        self._static_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')

    def create_gis_export(self):
        bootstrap.boostrap(self._polyfile_string)

        with tempfile.TemporaryDirectory() as tmp_dir:
            data_dir = os.path.join(tmp_dir, 'data')
            static_dir = os.path.join(tmp_dir, 'static')
            os.makedirs(data_dir)
            shutil.copytree(self._static_directory, static_dir)
            gather_statistics(os.path.join(tmp_dir, self._base_file_name + '_STATISTICS.csv'))
            extract_to(
                to_format=self._conversion_format,
                output_dir=data_dir,
                base_filename=self._base_file_name,
                out_srs=self._out_srs
            )
            zip_folders_relative([tmp_dir], zip_out_file_path=self._out_zip_file_path)
        return self._out_zip_file_path
