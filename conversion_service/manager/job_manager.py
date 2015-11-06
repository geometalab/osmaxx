import random
import string

from converters.boundaries import BBox
from converters import converter_settings
from converters.converter import Options
from manager.rq_helper import rq_enqueue_with_settings
from worker.converter_job import convert


class ConversionJobManager:
    """

    :param geometry:
    :param format_options:
    """

    result_directory = converter_settings.OSMAXX_CONVERSION_SERVICE['RESULTDIR']

    # FIXME: do not allow None for required kwargs
    def __init__(self, geometry=None, format_options=None):
        self.geometry = geometry if geometry else BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811)
        self.format_options = format_options if format_options else Options(output_formats=['fgdb', 'spatialite', 'shp', 'gpkg'])

    def start_conversion(self, callback_url):
        output_directory = self.result_directory + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        # todo: ensure job is cleaned up after files have been requested -> in conversion_service
        return rq_enqueue_with_settings(
            convert,
            callback_url=callback_url,
            geometry=self.geometry,
            format_options=self.format_options,
            output_directory=output_directory,
        )
