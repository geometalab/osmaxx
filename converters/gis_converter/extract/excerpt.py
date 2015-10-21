import time
import math
import subprocess
import shutil
import os
from utils import chg_dir_with


class Excerpt(object):
    def __init__(self, xmin, ymin, xmax, ymax, formats, output_dir, basename='osmaxx_excerpt'):
        self.formats = formats
        self.output_dir = output_dir
        self.filename = '_'.join([
            basename,
            time.strftime("%Y-%m-%d_%H%M%S"),
        ])
        self.xmin, self.ymin = self._pseudo_mercator_to_mercator(xmin, ymin)
        self.xmax, self.ymax = self._pseudo_mercator_to_mercator(xmax, ymax)
        self.tmp_statistics_filename = self.filename + '_tmp'

    def start(self):
        with chg_dir_with(os.path.dirname(__file__)):
            # only create statistics once and remove it when done with all formats
            self._get_statistics(self.tmp_statistics_filename)
            for format in self.formats:
                shutil.copyfile(
                    os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'),
                    os.path.join(self.output_dir, 'tmp', self.filename + '_STATISTICS.csv')
                )
                self.export_from_db_to_format(format)
            # remove the temporary statistics file
            os.remove(os.path.join(self.output_dir, 'tmp', self.tmp_statistics_filename + '_STATISTICS.csv'))

    #Calls the shell script that exports files of the specified format(file_format) from existing database
    def export_from_db_to_format(self, file_format):
        dbcmd = 'sh', './extract/extract_format.sh', self.xmin, self.ymin, self.xmax, self.ymax, self.output_dir, self.filename, file_format
        dbcmd = [str(arg) for arg in dbcmd]
        subprocess.check_call(dbcmd)

    #Extract Statistics
    def _get_statistics(self, filename):
        statcmd = 'bash', './extract/extract_statistics.sh', self.xmin, self.ymin, self.xmax, self.ymax, self.output_dir, filename
        statcmd = [str(arg) for arg in statcmd]
        subprocess.check_call(statcmd)

    #Converts the OSM map projection to mercator projection
    @staticmethod
    def _pseudo_mercator_to_mercator(pseudo_mercator_x_lon, pseudo_mercator_y_lat):
        if math.fabs(pseudo_mercator_x_lon) > 180 or math.fabs(pseudo_mercator_y_lat) > 90:
            return
        num = pseudo_mercator_x_lon * 0.017453292519943295
        x_value = 6378137.0 * num
        additional = pseudo_mercator_y_lat * 0.017453292519943295
        mercator_x_lon = x_value
        mercator_y_lat = 3189068.5 * \
                         math.log((1.0 + math.sin(additional)) /
                                  (1.0 - math.sin(additional)))
        return [mercator_x_lon, mercator_y_lat]
