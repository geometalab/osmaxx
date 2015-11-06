from django.utils.translation import gettext_lazy as _

from converters.gis_converter import options as gis_options

converter_options = gis_options

CONVERTER_CHOICES = dict(
    output_formats=[(format, _(format)) for format in converter_options.get_output_formats()],
)

__all__ = [
    'converter_options',
    'CONVERTER_CHOICES',
]
