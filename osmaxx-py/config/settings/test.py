from .local import *  # noqa

DEBUG = False

OSMAXX_TEST_SETTINGS = {
    'download_file_name': '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s',
    'CONVERSION_SERVICE_URL': env.str('DJANGO_OSMAXX_CONVERSION_SERVICE_URL', default='http://localhost:8901/api/'),
    'CONVERSION_SERVICE_USERNAME': 'dev',
    'CONVERSION_SERVICE_PASSWORD': 'dev',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}
