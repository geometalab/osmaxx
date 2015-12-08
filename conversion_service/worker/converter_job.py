import argparse
import logging
import os

from django_rq import get_connection
from rest_framework.reverse import reverse
import rq
import requests

from converters import osm_cutter, converter_options
from converters.converter import Options
from converters.gis_converter.bootstrap import bootstrap
from converters.gis_converter.extract.excerpt import Excerpt
from converters.boundaries import BBox
from shared import ConversionProgress

logger = logging.getLogger(__name__)


def set_progress_on_job(progress):  # pragma: nocover
    job = rq.get_current_job(connection=get_connection())
    if job:
        job.meta['progress'] = progress
        job.save()
    else:
        logger.info('status changed to: ' + str(progress))


class Notifier(object):
    def __init__(self, callback_url, status_url):
        self.callback_url = callback_url
        self.status_url = status_url
        self.noop = False
        if callback_url is None:
            self.noop = True

    def try_or_notify(self, function, *args, **kwargs):  # pragma: nocover
        try:
            return function(*args, **kwargs)
        except:
            set_progress_on_job(ConversionProgress.ERROR)
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
        if not self.noop:  # pragma: nocover
            data = {'status': self.status_url} if self.status_url is not None else {}
            try:
                requests.get(self.callback_url, params=data)
            except:
                pass


def convert(geometry, format_options, output_directory, callback_url, protocol, host=None):
    """
    Starts converting an excerpt for the specified format options

    :param geometry: osm_cutter.BBox or TBD
    :param format_options: TBD
    :param output_directory: where results are being stored
    :param callback_url: TBD
    :return: resulting paths/urls for created file
    """

    job = rq.get_current_job(connection=get_connection())
    if job is not None and host is not None:
        status_url = '{0}://'.format(protocol) + host + \
                     reverse(viewname='conversion_job_result-detail', kwargs={'rq_job_id': job.id})
    else:
        status_url = None
    notifier = Notifier(callback_url, status_url)

    set_progress_on_job(ConversionProgress.STARTED)
    notifier.notify()

    pbf_path = notifier.try_or_notify(osm_cutter.cut_osm_extent, geometry)
    notifier.try_or_notify(bootstrap.boostrap, pbf_path)

    # strip trailing slash
    if output_directory[-1] == '/':
        output_directory = output_directory[:-1]

    formats = format_options.get_output_formats()
    excerpt = Excerpt(formats=formats, output_dir=output_directory)
    notifier.try_or_notify(excerpt.start_format_extraction)
    set_progress_on_job(ConversionProgress.SUCCESSFUL)
    notifier.notify()


def _command_line_arguments():  # pragma: nocover
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
                        choices=converter_options.get_output_formats(),
                        required=True,
                        )
    return parser.parse_args()


if __name__ == '__main__':  # pragma: nocover
    args = _command_line_arguments()
    bounding_box = args.west, args.south, args.east, args.north
    geometry = BBox(*bounding_box)
    convert(
        geometry=geometry,
        format_options=Options({'output_formats': args.formats}),
        output_directory=os.path.dirname(__file__),
        callback_url=None,
    )
