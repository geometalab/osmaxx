import subprocess

import os
import tempfile

from osmaxx.conversion._settings import CONVERSION_SETTINGS

from osmaxx.conversion.converters.utils import zip_folders_relative

_path_to_commandline_utils = os.path.join(os.path.dirname(__file__), 'command_line_utils')


class Garmin:
    def __init__(self, *, out_zip_file_path, area_name, polyfile_string):
        self._resulting_zip_file_path = out_zip_file_path
        self._map_description = area_name
        self._osmosis_polygon_file = tempfile.NamedTemporaryFile(suffix='.poly', mode='w')
        self._osmosis_polygon_file.write(polyfile_string)
        self._osmosis_polygon_file.flush()
        self._polyfile_path = self._osmosis_polygon_file.name

    def create_garmin_export(self):
        self._to_garmin()
        self._osmosis_polygon_file.close()

    def _to_garmin(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out_dir = os.path.join(tmp_dir, 'garmin')
            config_file_path = self._split(tmp_dir)
            self._produce_garmin(config_file_path, tmp_out_dir)
            resulting_zip_file_path = self._create_zip(tmp_out_dir)
        return resulting_zip_file_path

    def _split(self, workdir):
        _splitter_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'splitter', 'splitter.jar'))
        subprocess.check_call([
            'java',
            '-jar', _splitter_path,
            '--output-dir={0}'.format(workdir),
            '--description={0}'.format(self._map_description),
            '--polygon-file={}'.format(self._polyfile_path),
            CONVERSION_SETTINGS.get('PBF_PLANET_FILE_PATH'),
        ])
        config_file_path = os.path.join(workdir, 'template.args')
        return config_file_path

    def _produce_garmin(self, config_file_path, out_dir):
        out_dir = os.path.join(out_dir, 'garmin')  # hack to get a subdirectory in the zipfile.
        os.makedirs(out_dir, exist_ok=True)

        _mkgmap_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'mkgmap', 'mkgmap.jar'))
        mkg_map_command = ['java', '-jar', _mkgmap_path]
        output_dir = ['--output-dir={0}'.format(out_dir)]
        config = ['--read-config={0}'.format(config_file_path)]

        subprocess.check_call(
            mkg_map_command +
            output_dir +
            config
        )

    def _create_zip(self, data_dir):
        zip_folders_relative([data_dir], self._resulting_zip_file_path)
        return self._resulting_zip_file_path
