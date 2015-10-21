#!/usr/bin/env python
import argparse
import time
from converters import osm_cutter

from converters.gis_converter import options
from converters.gis_converter.bootstrap.bootstrap import boostrap
from converters.gis_converter.extract.excerpt import Excerpt


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
        choices=options.get_output_formats(),
        required=True,
    )
    parser.add_argument('-o', '--out-dir',
        help='directory in which the resulting file(s) should be stored',
        type=str,
        default='/tmp/' + time.strftime("%Y-%m-%d_%H%M%S")
    )

    args = parser.parse_args()

    bounding_box = osm_cutter.BBox(args.xmin, args.ymin, args.xmax, args.ymax)
    pbf_path = osm_cutter.cut_osm_extent(bounding_box)
    boostrap(pbf_path)
    # strip trailing slash
    if args.out_dir[-1] == '/':
        args.out_dir = args.out_dir[:-1]
    excerpt = Excerpt(formats=args.formats, output_dir=args.out_dir)
    excerpt.start()
