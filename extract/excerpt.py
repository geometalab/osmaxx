import time
import math
import subprocess
import os


class Excerpt(object):
    def __init__(self, xmin, ymin, xmax, ymax, formats, basename='osmaxx_excerpt'):
        self.formats = formats
        self.filename = '_'.join([
            basename,
            time.strftime("%Y-%m-%d_%H%M%S"),
        ])
        self.xmin, self.ymin = self._pseudo_mercator_to_mercator(xmin, ymin)
        self.xmax, self.ymax = self._pseudo_mercator_to_mercator(xmax, ymax)

    def start(self):
        old_cur_dir = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        for format in self.formats:
            self.export_from_db_to_format(format)
        os.chdir(old_cur_dir)

    #Calls the shell script that exports files of the specified format(file_format) from existing database
    def export_from_db_to_format(self, file_format):
        self._get_statistics()
        dbcmd = 'sh', './extract/extract_format.sh', self.xmin, self.ymin, self.xmax, self.ymax, self.filename, file_format
        dbcmd = [str(arg) for arg in dbcmd]
        subprocess.check_call(dbcmd)

    #Extract Statistics
    def _get_statistics(self):
        statcmd = 'bash', './extract/extract_statistics.sh', self.xmin, self.ymin, self.xmax, self.ymax, self.filename
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
