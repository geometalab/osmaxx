import time
import subprocess
import shutil
import os
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

    def start(self):
        with chg_dir_with(os.path.dirname(__file__)):
            # only create statistics once and remove it when done with all formats
            self._get_statistics(self.tmp_statistics_filename)
            for format in self.formats:
                file_basename = '_'.join([self.filename_prefix, format])
                shutil.copyfile(
                    os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'),
                    os.path.join(self.output_dir, 'tmp', file_basename + '_STATISTICS.csv')
                )
                self.export_from_db_to_format(format)
            # remove the temporary statistics file
            os.remove(os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'))

    #Calls the shell script that exports files of the specified format(file_format) from existing database
    def export_from_db_to_format(self, file_format):
        file_basename = '_'.join([self.filename_prefix, file_format])
        dbcmd = 'sh', './extract/extract_format.sh', self.output_dir, file_basename, file_format
        dbcmd = [str(arg) for arg in dbcmd]
        subprocess.check_call(dbcmd)

    #Extract Statistics
    def _get_statistics(self, filename):
        statcmd = 'bash', './extract/extract_statistics.sh', self.output_dir, filename
        statcmd = [str(arg) for arg in statcmd]
        subprocess.check_call(statcmd)
