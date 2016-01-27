import tempfile

from .local import *  # noqa

DEBUG = False

# Some of our tests erase PRIVATE_MEDIA_ROOT dir to clean up after themselves,
# so DON'T set this to the location of anything valuable.
PRIVATE_MEDIA_ROOT = tempfile.mkdtemp()

OSMAXX_TEST_SETTINGS = {
    'download_file_name': '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s',
    'CONVERSION_SERVICE_URL': 'http://localhost:8901/api/',
    'CONVERSION_SERVICE_USERNAME': 'dev',
    'CONVERSION_SERVICE_PASSWORD': 'dev',
}

OSMAXX.update(OSMAXX_TEST_SETTINGS)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': ''
    }
}

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
