from .local import *  # noqa

OSMAXX['download_file_name'] = '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s'

INSTALLED_APPS += ('osmaxx.utilities.tests.test_models', )
