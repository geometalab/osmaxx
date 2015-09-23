from .local import *  # noqa

OSMAXX['download_file_name'] = '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s'

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append(
    'osmaxx.utilities.tests.test_models',
)
