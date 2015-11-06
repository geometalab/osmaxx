from converters import converter_settings
from converters.boundaries import BBox
from manager.rq_helper import rq_enqueue_with_settings
from worker.converter_job import convert


class ConversionJobManager:
    """

    :param geometry:
    :param format_options:
    """

    result_directory = converter_settings.OSMAXX_CONVERSION_SERVICE['RESULTDIR']

    def __init__(self,
                 geometry=BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811),
                 format_options={'formats': ['fgdb', 'spatialite', 'shp', 'gpkg']}):
        self.geometry = geometry
        self.format_options = format_options

    def start_conversion(self):
        # todo: ensure job is cleaned up after files have been requested -> in rest_api
        return rq_enqueue_with_settings(
            convert,
            geometry=self.geometry,
            format_options=self.format_options,
            output_directory=self.result_directory,
        )
