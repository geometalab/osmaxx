import os
import subprocess
import tempfile

import time

_path_to_commandline_utils = os.path.join(os.path.dirname(__file__), 'command_line_utils')


class Garmin:
    def __init__(self, output_directory, pbf_path, map_description):
        os.makedirs(output_directory, exist_ok=True)

        self.output_directory = output_directory
        self.pbf_path = pbf_path
        self.map_description = map_description
        self.timestamped_outfile_base_name = '{}-{}'.format(
            time.strftime("%Y-%m-%d_%H%M%S"),
            'garmin',
        )

    def create_garmin_export(self):
        self._to_garmin()

    def _to_garmin(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out_dir = os.path.join(tmp_dir, 'garmin')
            config_file_path = self._split(tmp_dir)
            self._produce_garmin(config_file_path, tmp_dir, tmp_out_dir)
            resulting_zip_file_path = self._zip_and_move(tmp_out_dir)

        return resulting_zip_file_path

    def _split(self, workdir):
        _splitter_path = os.path.abspath(os.path.join(_path_to_commandline_utils, 'splitter', 'splitter.jar'))
        subprocess.check_call([
            'java',
            '-jar', _splitter_path,
            '--output-dir={0}'.format(workdir),
            '--description={0}'.format(self.map_description),
            self.pbf_path,
        ])
        config_file_path = os.path.join(workdir, 'template.args')
        return config_file_path

    def _produce_garmin(self, config_file_path, workdir, out_dir):
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

    def _zip_and_move(self, workdir):
        resulting_zip_file_path = os.path.join(
            self.output_directory, '.'.join([self.timestamped_outfile_base_name, 'zip'])
        )
        subprocess.check_call(["zip", "-r", "--move", resulting_zip_file_path, workdir])
        return resulting_zip_file_path
