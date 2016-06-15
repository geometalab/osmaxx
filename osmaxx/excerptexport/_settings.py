import os
from datetime import timedelta

from django.conf import settings

POLYFILE_LOCATION = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'polyfiles'))
OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL = timedelta(hours=1)  # default every hour
RESULT_FILE_AVAILABILITY_DURATION = timedelta(days=14)  # default to two weeks

if hasattr(settings, 'OSMAXX'):
    if hasattr(settings.OSMAXX, 'OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL'):
        OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL = settings.OSMAXX['OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL']
    if hasattr(settings.OSMAXX, 'RESULT_FILE_AVAILABILITY_DURATION'):
        RESULT_FILE_AVAILABILITY_DURATION = settings.OSMAXX.get['RESULT_FILE_AVAILABILITY_DURATION']

# only needed for testing
if hasattr(settings, '_OSMAXX_POLYFILE_LOCATION'):
    POLYFILE_LOCATION = settings._OSMAXX_POLYFILE_LOCATION
