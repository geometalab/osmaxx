import argparse
import time

from django_rq import job

from converters import osm_cutter, options
from converters.gis_converter.bootstrap import bootstrap
from converters.gis_converter.extract.excerpt import Excerpt
from converters.osm_cutter import GEOMETRY_CLASSES_ACTION
from converters.boundaries import BBox


@job
def convert(geometry, format_options, output_directory=None):
    """
    Starts converting an excerpt for the specified format options

    :param geometry: osm_cutter.BBox or TBD
    :param format_type_options: TBD
    :param output_directory: where results are being stored
        uses '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S") for default
    :return: resulting paths/urls for created file
    """

    # sanity check of input param
    klass = geometry.__class__
    if klass not in GEOMETRY_CLASSES_ACTION:
        raise NotImplementedError(klass.__name__ + ' has not been implemented yet')

    if not output_directory:
        output_directory = '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S")

    pbf_path = osm_cutter.cut_osm_extent(geometry)
    bootstrap.boostrap(pbf_path)

    # strip trailing slash
    if output_directory[-1] == '/':
        output_directory = output_directory[:-1]

    formats = format_options['formats']
    excerpt = Excerpt(formats=formats, output_dir=output_directory)
    excerpt.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a extent (BoundingBox) to given formats. Use -h for help. '
                    'Usage: converter_job.py '
                    '-w 29.525547623634335 -s 40.77546776498174 -e 29.528980851173397 -n 40.77739734768811 '
                    '-f fgdb -f spatialite -f shp -f gpkg')
    parser.add_argument('--west', '-w', type=float, help='west coordinate of bounding box', required=True)
    parser.add_argument('--south', '-s', type=float, help='south coordinate of bounding box', required=True)
    parser.add_argument('--east', '-e', type=float, help='east coordinate of bounding box', required=True)
    parser.add_argument('--north', '-n', type=float, help='north coordinate of bounding box', required=True)
    parser.add_argument('-f', '--format',
                        action='append',
                        dest='formats',
                        default=[],
                        help='Add (repeated) output formats',
                        choices=options.get_output_formats(),
                        required=True,
                        )
    args = parser.parse_args()
    bounding_box = args.west, args.south, args.east, args.north
    geometry = BBox(*bounding_box)
    convert(geometry=geometry, format_options=args.formats)
