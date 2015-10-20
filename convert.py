#!/usr/bin/env python
import os
import sys
import subprocess
import argparse

from extract.excerpt import Excerpt


def boostrap(west, south, east, north):
    os.chdir('bootstrap/')
    boostrap_cmd = 'sh', 'main-bootstrap.sh', str(west), str(south), str(east), str(north)
    subprocess.check_call(boostrap_cmd)
    os.chdir('..')


def name_generator(basename='osmaxx_excerpt'):
    filename = '_'.join(
        basename,
        time.strftime("%Y-%m-%d"),
        time.strftime("%H%M%S"),
    )
    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--format',
        action='append',
        dest='formats',
        default=[],
        help='Add (repeated) output formats',
        choices=['fgdb','shp','gpkg','spatialite'],
    )
    parser.add_argument('xmin', help='Min Longitude/Left/West', type=float)
    parser.add_argument('ymin', help='Min Latitude/Bottom/South', type=float)
    parser.add_argument('xmax', help='Max Longitude/Right/East', type=float)
    parser.add_argument('ymax', help='Max Latitude/Top/North', type=float)

    args = parser.parse_args()

    bounding_box = args.xmin, args.ymin, args.xmax, args.ymax
    boostrap(*bounding_box)

    excerpt = Excerpt(*bounding_box, formats=args.formats)
    excerpt.start()
