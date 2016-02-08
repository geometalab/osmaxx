from django.utils.translation import gettext_lazy as _

from osmaxx.converters import garmin_converter
from osmaxx.converters import gis_converter

CONVERTER_OPTIONS = gis_converter.options + garmin_converter.options

CONVERTER_CHOICES = dict(
    output_formats=[(format, _(format)) for format in CONVERTER_OPTIONS.get_output_formats()],
)
