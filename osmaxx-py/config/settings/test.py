from .local import *  # noqa

DEBUG = False

OSMAXX_TEST_SETTINGS = {
    'download_file_name': '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s',
    'CONVERSION_SERVICE_URL': 'http://localhost:8901/api/',
    'CONVERSION_SERVICE_USERNAME': 'osmaxxi',
    'CONVERSION_SERVICE_PASSWORD': '12345678',
}

OSMAXX.update(OSMAXX_TEST_SETTINGS)

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
            'level': 'ERROR',
        },
    },
}
