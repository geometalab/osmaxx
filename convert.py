#!/usr/bin/env python
import os
import subprocess
import argparse
import time

from worker.gis_converter.extract.excerpt import Excerpt


def boostrap(west, south, east, north):
    old_cur_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(__file__), 'worker', 'gis_converter', 'bootstrap'))
    boostrap_cmd = 'sh', 'main-bootstrap.sh', str(west), str(south), str(east), str(north)
    subprocess.check_call(boostrap_cmd)
    os.chdir(old_cur_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xmin', help='Min Longitude/Left/West', type=float)
    parser.add_argument('ymin', help='Min Latitude/Bottom/South', type=float)
    parser.add_argument('xmax', help='Max Longitude/Right/East', type=float)
    parser.add_argument('ymax', help='Max Latitude/Top/North', type=float)
    parser.add_argument('-f', '--format',
        action='append',
        dest='formats',
        default=[],
        help='Add (repeated) output formats',
        choices=['fgdb','shp','gpkg','spatialite'],
        required=True,
    )
    parser.add_argument('-o', '--out-dir',
        help='directory in which the resulting file(s) should be stored',
        type=str,
        default='/tmp/' + time.strftime("%Y-%m-%d_%H%M%S")
    )

    args = parser.parse_args()

    bounding_box = args.xmin, args.ymin, args.xmax, args.ymax
    boostrap(*bounding_box)
    # strip trailing slash
    if args.out_dir[-1] == '/':
        args.out_dir = args.out_dir[:-1]
    excerpt = Excerpt(*bounding_box, formats=args.formats, output_dir=args.out_dir)
    excerpt.start()
