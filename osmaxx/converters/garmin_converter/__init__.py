from osmaxx.converters import Options
from .to_garmin import Garmin

options = Options(
    output_formats=['garmin', ],
)

__all__ = [
    'options',
    'Garmin',
]
