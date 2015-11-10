import os
import shutil
import subprocess
import time

from utils import chg_dir_with


class Excerpt(object):
    def __init__(self, formats, output_dir, basename='osmaxx_excerpt'):
        self.formats = formats
        self.output_dir = output_dir
        self.filename_prefix = '_'.join([
            basename,
            time.strftime("%Y-%m-%d_%H%M%S"),
        ])
        self.tmp_statistics_filename = self.filename_prefix + '_tmp'

    def start_format_extraction(self):
        with chg_dir_with(os.path.dirname(__file__)):
            # only create statistics once and remove it when done with all formats
            self._get_statistics(self.tmp_statistics_filename)
            for format in self.formats:
                file_basename = '_'.join([self.filename_prefix, format])
                self._copy_statistics_file_to_format_dir(file_basename)
                self._export_from_db_to_format(file_basename, format)
            # remove the temporary statistics file
            os.remove(os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'))

    # Export files of the specified format (file_format) from existing database
    def _export_from_db_to_format(self, file_basename, file_format):  # pragma: nocover
        dbcmd = 'sh', './extract/extract_format.sh', self.output_dir, file_basename, file_format
        dbcmd = [str(arg) for arg in dbcmd]
        subprocess.check_call(dbcmd)

    # Extract Statistics
    def _get_statistics(self, filename):  # pragma: nocover
        statcmd = 'bash', './extract/extract_statistics.sh', self.output_dir, filename
        statcmd = [str(arg) for arg in statcmd]
        subprocess.check_call(statcmd)

    def _copy_statistics_file_to_format_dir(self, file_basename):  # pragma: nocover
        shutil.copyfile(
            os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'),
            os.path.join(self.output_dir, 'tmp', file_basename + '_STATISTICS.csv')
        )
