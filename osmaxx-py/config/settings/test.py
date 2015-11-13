from .local import *  # noqa

OSMAXX['download_file_name'] = '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s'

INSTALLED_APPS += ('osmaxx.utilities.tests.test_models', )

# only log errors for testing
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env.str('DJANGO_LOG_LEVEL', default='ERROR'),
        },
    },
}
