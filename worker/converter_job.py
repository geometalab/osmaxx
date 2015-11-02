import argparse
import time

from django_rq import job
import requests

from converters import osm_cutter, options
from converters.gis_converter.bootstrap import bootstrap
from converters.gis_converter.extract.excerpt import Excerpt
from converters.boundaries import BBox


class Notifier(object):
    def __init__(self, callback_url):
        self.callback_url = callback_url

    def try_or_notify(self, function, *args, **kwargs):
        try:
            return function(args, kwargs)
        except:
            self.notify()
            raise

    def notify(self):
        self._notify_status_change()

    def _notify_status_change(self):
        """
        fire and forget, and don't care when exceptions occur.

        :param callback_url:
        :return: nothing
        """
        try:
            requests.get(self.callback_url)
        except:
            pass


@job
def convert(geometry, format_options, output_directory=None, callback_url=None):
    """
    Starts converting an excerpt for the specified format options

    :param geometry: osm_cutter.BBox or TBD
    :param format_type_options: TBD
    :param callback_url: TBD
    :param output_directory: where results are being stored
        uses '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S") for default
    :return: resulting paths/urls for created file
    """

    notifier = Notifier(callback_url)

    if not output_directory:
        output_directory = '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S")

    pbf_path = notifier.try_or_notify(osm_cutter.cut_osm_extent, geometry)
    notifier.try_or_notify(bootstrap.boostrap, pbf_path)

    # strip trailing slash
    if output_directory[-1] == '/':
        output_directory = output_directory[:-1]

    formats = format_options['formats']
    excerpt = Excerpt(formats=formats, output_dir=output_directory)
    notifier.try_or_notify(excerpt.start_format_extraction)
    notifier.notify()


def _command_line_arguments():
    global args
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
    return parser.parse_args()


if __name__ == '__main__':
    args = _command_line_arguments()
    bounding_box = args.west, args.south, args.east, args.north
    geometry = BBox(*bounding_box)
    convert(geometry=geometry, format_options={'formats': args.formats})
