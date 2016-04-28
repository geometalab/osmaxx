import os

from django.conf import settings

POLYFILE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'polyfiles')

# only needed for testing
if hasattr(settings, '_OSMAXX_POLYFILE_LOCATION'):
    POLYFILE_LOCATION = settings._OSMAXX_POLYFILE_LOCATION
