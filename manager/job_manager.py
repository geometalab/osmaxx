import django_rq
from converters import converter_settings
from converters.osm_cutter import BBox
from worker.converter_job import convert


class ConversionJobManager:
    """

    :param geometry:
    :param format_options:
    """

    result_directory = converter_settings.OSMAXX_CONVERSION_SERVICE['RESULTDIR']

    def __init__(self,
                 geometry=BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811),
                 format_options={'formats':['fgdb', 'spatialite', 'shp', 'gpkg']}):
        self.geometry = geometry
        self.format_options = format_options

    def start_conversion(self):
        return django_rq.enqueue(
            convert,
            geometry=self.geometry,
            format_options=self.format_options,
            output_directory=self.result_directory,
        )
