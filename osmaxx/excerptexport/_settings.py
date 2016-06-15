import os
from datetime import timedelta

from django.conf import settings

POLYFILE_LOCATION = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'polyfiles'))
OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS = timedelta(hours=1)  # default every hour
PURGE_OLD_RESULT_FILES_AFTER = timedelta(days=14)  # default to two weeks

if hasattr(settings, 'OSMAXX'):
    if hasattr(settings.OSMAXX, 'OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS'):
        OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS = settings.OSMAXX['OLD_RESULT_FILES_REMOVAL_CHECK_INTERVAL_HOURS']
    if hasattr(settings.OSMAXX, 'OLD_RESULT_FILES_REMOVAL_DAYS'):
        PURGE_OLD_RESULT_FILES_AFTER = timedelta(settings.OSMAXX.get('OLD_RESULT_FILES_REMOVAL_DAYS'))

# only needed for testing
if hasattr(settings, '_OSMAXX_POLYFILE_LOCATION'):
    POLYFILE_LOCATION = settings._OSMAXX_POLYFILE_LOCATION
