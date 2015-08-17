__author__ = 'dhruv'
import time, subprocess, os, argparse
import math
path = os.path.dirname(os.path.realpath(__file__))


def name_generator():
    filename='osmaxx_excerpt_'+time.strftime("%Y-%m-%d")+'_'+time.strftime("%H%M%S")
    return filename


def to_mercator(mercator_x_lon, mercator_y_lat):
    if math.fabs(mercator_x_lon) > 180 or math.fabs(mercator_y_lat) > 90:
        return
    num = mercator_x_lon * 0.017453292519943295
    x_value = 6378137.0 * num
    additional = mercator_y_lat * 0.017453292519943295
    mercator_x_lon = x_value
    mercator_y_lat = 3189068.5 * \
                     math.log((1.0 + math.sin(additional)) /
                              (1.0 - math.sin(additional)))
    return [mercator_x_lon, mercator_y_lat]


def get_statistics(data, name):
    statcmd = 'bash', './extract/extract_statistics', data[0], data[1], data[2], data[3], name
    subprocess.check_call(statcmd)


def call_db(data, name, form):
    get_statistics(data, name)
    dbcmd = 'sh', './extract/extract_db.sh', data[0], data[1], data[2], data[3], name, form
    subprocess.check_call(dbcmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--format',choices=['fgdb','shp','gpkg','spatialite'], default='fgdb', help= 'output formats')
    parser.add_argument('xmin', help='Min Longitude/Left/West', type=float)
    parser.add_argument('ymin', help='Min Latitude/Bottom/South', type=float)
    parser.add_argument('xmax', help='Max Longitude/Right/East', type=float)
    parser.add_argument('ymax', help='Max Latitude/Top/North', type=float)
    args = parser.parse_args()
    min_xy=to_mercator(args.xmin, args.ymin)
    max_xy=to_mercator(args.xmax, args.ymax)
    name=name_generator()
    call_db([str(min_xy[0]), str(min_xy[1]), str(max_xy[0]), str(max_xy[1])], name, args.format)
    print name+' have been completed in '+args.format+' format.'
