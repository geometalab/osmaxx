import tempfile

import os

import shutil
from django.utils import timezone

from rq import get_current_job

from osmaxx.conversion.converters.converter_gis.bootstrap import bootstrap
from osmaxx.conversion.converters.converter_gis.extract.db_to_format.extract import extract_to
from osmaxx.conversion.converters.utils import zip_folders_relative, recursive_getsize


class GISConverter:
    def __init__(self, *, conversion_format, out_zip_file_path, base_file_name, out_srs, polyfile_string, detail_level):
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
        self._detail_level = detail_level

    def create_gis_export(self):
        start_time = timezone.now()
        bootstrap.boostrap(self._polyfile_string, detail_level=self._detail_level)
        end_time = timezone.now()
        bootstrap_duration = end_time - start_time

        with tempfile.TemporaryDirectory() as tmp_dir:
            data_dir = os.path.join(tmp_dir, 'data')
            static_dir = os.path.join(tmp_dir, 'static')
            os.makedirs(data_dir)
            shutil.copytree(self._static_directory, static_dir)
            start_time = timezone.now()
            extract_to(
                to_format=self._conversion_format,
                output_dir=data_dir,
                base_filename=self._base_file_name,
                out_srs=self._out_srs
            )
            end_time = timezone.now()
            unzipped_result_size = recursive_getsize(data_dir)
            extraction_duration = end_time - start_time
            zip_folders_relative([tmp_dir], zip_out_file_path=self._out_zip_file_path)
        total_duration = bootstrap_duration + extraction_duration
        job = get_current_job()
        if job:
            job.meta['duration'] = total_duration
            job.meta['unzipped_result_size'] = unzipped_result_size
            job.save()
        return self._out_zip_file_path
