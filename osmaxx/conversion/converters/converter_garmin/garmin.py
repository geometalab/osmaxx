import shutil

import os
import tempfile
from django.utils import timezone
from rq import get_current_job

from osmaxx.conversion._settings import CONVERSION_SETTINGS, odb_license, copying_notice, creative_commons_license
from osmaxx.conversion.converters.converter_pbf.to_pbf import cut_pbf_along_polyfile

from osmaxx.conversion.converters.utils import zip_folders_relative, recursive_getsize, logged_check_call

_path_to_commandline_utils = os.path.join(os.path.dirname(__file__), 'command_line_utils')
_path_to_bounds_zip = os.path.join(CONVERSION_SETTINGS['SEA_AND_BOUNDS_ZIP_DIRECTORY'], 'bounds.zip')
_path_to_sea_zip = os.path.join(CONVERSION_SETTINGS['SEA_AND_BOUNDS_ZIP_DIRECTORY'], 'sea.zip')
_path_to_geonames_zip = os.path.join(os.path.dirname(__file__), 'additional_data', 'cities1000.txt')


class Garmin:
    def __init__(self, *, out_zip_file_path, area_name, polyfile_string):
        self._resulting_zip_file_path = out_zip_file_path
        self._map_description = area_name
        self._osmosis_polygon_file = tempfile.NamedTemporaryFile(suffix='.poly', mode='w')
        self._osmosis_polygon_file.write(polyfile_string)
        self._osmosis_polygon_file.flush()
        self._polyfile_path = self._osmosis_polygon_file.name
        self._start_time = None
        self._unzipped_result_size = None
        self._area_polyfile_string = polyfile_string

    def create_garmin_export(self):
        self._start_time = timezone.now()
        self._to_garmin()
        self._osmosis_polygon_file.close()
        job = get_current_job()
        if job:
            job.meta['duration'] = timezone.now() - self._start_time
            job.meta['unzipped_result_size'] = self._unzipped_result_size
            job.save()

    def _to_garmin(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out_dir = os.path.join(tmp_dir, 'garmin')
            config_file_path = self._split(tmp_dir)
            self._produce_garmin(config_file_path, tmp_out_dir)
            self._create_zip(tmp_out_dir)

    def _split(self, workdir):
        memory_option = '-Xmx7000m'
        _splitter_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'splitter', 'splitter.jar'))
        _pbf_file_path = os.path.join('/tmp', 'pbf_cutted.pbf')
        cut_pbf_along_polyfile(self._area_polyfile_string, _pbf_file_path)
        logged_check_call([
            'java',
            memory_option,
            '-jar', _splitter_path,
            '--output-dir={0}'.format(workdir),
            '--description={0}'.format(self._map_description),
            '--geonames-file={0}'.format(_path_to_geonames_zip),
            '--polygon-file={}'.format(self._polyfile_path),
            _pbf_file_path,
        ])
        config_file_path = os.path.join(workdir, 'template.args')
        return config_file_path

    def _produce_garmin(self, config_file_path, out_dir):
        out_dir = os.path.join(out_dir, 'garmin')  # hack to get a subdirectory in the zipfile.
        os.makedirs(out_dir, exist_ok=True)

        shutil.copy(copying_notice, out_dir)
        shutil.copy(odb_license, out_dir)
        shutil.copy(creative_commons_license, out_dir)

        _mkgmap_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'mkgmap', 'mkgmap.jar'))
        mkg_map_command = ['java', '-jar', _mkgmap_path]
        output_dir = ['--output-dir={0}'.format(out_dir)]
        config = [
            '--bounds={0}'.format(_path_to_bounds_zip),
            '--precomp-sea={0}'.format(_path_to_sea_zip),
            '--read-config={0}'.format(config_file_path),
            '--gmapsupp',
            '--route',
        ]

        logged_check_call(
            mkg_map_command +
            output_dir +
            config
        )
        self._unzipped_result_size = recursive_getsize(out_dir)

    def _create_zip(self, data_dir):
        zip_folders_relative([data_dir], self._resulting_zip_file_path)


def perform_export(_output_zip_file_path, _area_name, _polyfile_string):
    garmin = Garmin(
        out_zip_file_path=_output_zip_file_path,
        area_name=_area_name,
        polyfile_string=_polyfile_string,
    )
    garmin.create_garmin_export()
