import os
import shutil
import subprocess
import time

from converters import garmin_converter
from converters import gis_converter
from converters.gis_converter.bootstrap import bootstrap
from utils import chg_dir_with


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
            with chg_dir_with(os.path.dirname(__file__)):
                # only create statistics once and remove it when done with all formats
                self._get_statistics(self.tmp_statistics_filename)
                for format in formats:
                    file_basename = '_'.join([self.filename_prefix, format])
                    self._copy_statistics_file_to_format_dir(file_basename)
                    self._export_from_db_to_format(file_basename, format)
                # remove the temporary statistics file
                os.remove(os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'))

    def _create_garmin_export(self, formats):
        if len(formats) == 1:
            garmin_format = formats[0]
            path_to_mkgmap = os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'garmin_converter', 'command_line_utils', 'mkgmap', 'mkgmap.jar')
            )
            garmin_out_dir = os.path.join(self.output_dir, garmin_format)
            os.makedirs(garmin_out_dir, exist_ok=True)
            subprocess.check_call([
                'java', '-Xms32m', '-Xmx4096m',
                '-jar', path_to_mkgmap,
                '--output-dir={0}'.format(garmin_out_dir),
                '--input-file={0}'.format(self.pbf_path),
            ])
            subprocess.check_call(["zip", "-r", "--move", '.'.join([garmin_out_dir, 'zip']), garmin_out_dir])

    # Export files of the specified format (file_format) from existing database
    def _export_from_db_to_format(self, file_basename, file_format):
        extract_base_dir = os.path.join(os.path.dirname(__file__), 'gis_converter', 'extract')
        extract_format_file_path = os.path.join(extract_base_dir, 'extract', 'extract_format.sh')
        extra_data_dir = os.path.join(extract_base_dir, 'static')

        dbcmd = 'sh', extract_format_file_path, self.output_dir, file_basename, file_format, extra_data_dir
        dbcmd = [str(arg) for arg in dbcmd]
        subprocess.check_call(dbcmd)

    # Extract Statistics
    def _get_statistics(self, filename):
        extract_statistics_file_path = os.path.join(
            os.path.dirname(__file__), 'gis_converter', 'extract', 'extract', 'extract_statistics.sh'
        )
        statcmd = 'bash', extract_statistics_file_path, self.output_dir, filename
        statcmd = [str(arg) for arg in statcmd]
        subprocess.check_call(statcmd)

    def _copy_statistics_file_to_format_dir(self, file_basename):  # pragma: nocover
        shutil.copyfile(
            os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'),
            os.path.join(self.output_dir, 'tmp', file_basename + '_STATISTICS.csv')
        )

    def _split_formats(self):
        garmin_formats = [garmin_format for garmin_format in self.formats
                          if garmin_format in garmin_converter.options.get_output_formats()]
        gis_formats = [gis_format for gis_format in self.formats
                       if gis_format in gis_converter.options.get_output_formats()]
        return garmin_formats, gis_formats
