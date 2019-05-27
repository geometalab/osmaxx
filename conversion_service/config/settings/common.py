"""
Django settings for osmaxx project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# flake8: noqa
# pylint: skip-file
import os
from datetime import timedelta

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.gis',
]
THIRD_PARTY_APPS = [
    # async execution worker
    'django_rq',
    # rest API Framework
    'rest_framework',
    'rest_framework_gis',
    'pbf_file_size_estimation',
]
# Apps specific for this project go here.
LOCAL_APPS = [
    'osmaxx.version',
    'osmaxx.clipping_area',
    'osmaxx.conversion',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {
# }

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env.str('DJANGO_EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = env.str('DJANGO_EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = env.str('DJANGO_EMAIL_HOST_USER', default='')
EMAIL_PORT = env.int('DJANGO_EMAIL_PORT', default=25)
EMAIL_SUBJECT_PREFIX = env.str('DJANGO_EMAIL_SUBJECT_PREFIX', default='[OSMaxx] ')
EMAIL_USE_TLS = env.bool('DJANGO_EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = env.bool('DJANGO_EMAIL_USE_SSL', default=False)
EMAIL_TIMEOUT = env.int('DJANGO_EMAIL_TIMEOUT', default=None)
EMAIL_SSL_CERTFILE = env.bool('DJANGO_EMAIL_SSL_CERTFILET', default=None)
EMAIL_SSL_KEYFILE = env.bool('DJANGO_EMAIL_SSL_KEYFILE', default=None)
DEFAULT_FROM_EMAIL = env.str('DJANGO_DEFAULT_FROM_EMAIL', default='webmaster@localhost')
SERVER_EMAIL = env.str('DJANGO_SERVER_EMAIL', default='root@localhost')

EMAIL_FILE_PATH = env.str('DJANGO_EMAIL_FILE_PATH', default=None)
# allow default setting (unset) if the variable isn't set in the environment
if not EMAIL_FILE_PATH:
    del EMAIL_FILE_PATH

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = ()

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db("DJANGO_DATABASE_URL", default="postgis://postgres@mediatordatabase/postgres"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Zurich'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
LOCALE_PATHS = [
    str(ROOT_DIR('locale')),
]
# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/#the-templates-settings

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = env.str('DJANGO_STATIC_ROOT', default='/data/static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = ()

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root

# data & media

MEDIA_ROOT = env.str('DJANGO_MEDIA_ROOT', default='/data/media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'conversion_service.config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'conversion_service.config.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

# login url if param 'next' is not set
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

POSTGIS_VERSION = (2, 1)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

# RQ settings
REDIS_CONNECTION = dict(
    HOST=env.str('REDIS_HOST', default='conversionserviceredis'),
    PORT=env.str('REDIS_PORT', default=6379),
    DB=0,
    PASSWORD='',
    DEFAULT_TIMEOUT=int(timedelta(days=2).total_seconds())
)
RQ_QUEUE_NAMES = ['default', 'high']
RQ_QUEUES = {name: REDIS_CONNECTION for name in RQ_QUEUE_NAMES}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

OSMAXX_CONVERSION_SERVICE = {
    'PBF_PLANET_FILE_PATH': env.str(
        'OSMAXX_CONVERSION_SERVICE_PBF_PLANET_FILE_PATH',
        default='/var/data/osm-planet/pbf/planet-latest.osm.pbf'),
    'RESULT_TTL': env.str('OSMAXX_CONVERSION_SERVICE_RESULT_TTL', default=-1),  # never expire!
}

# Security - defaults taken from Django 1.8 (not secure enough for production)
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default=None)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
X_FRAME_OPTIONS = env.str('DJANGO_X_FRAME_OPTIONS', default='SAMEORIGIN')

## General SECURE Settings
SECURE_BROWSER_XSS_FILTER = env.bool('DJANGO_SECURE_BROWSER_XSS_FILTER', default=False)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=False)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=0)
SECURE_PROXY_SSL_HEADER = env.tuple('DJANGO_SECURE_PROXY_SSL_HEADER', default=None)
SECURE_REDIRECT_EXEMPT = env.list('DJANGO_SECURE_REDIRECT_EXEMPT', default=[])
SECURE_SSL_HOST = env.str('DJANGO_SECURE_SSL_HOST', default=None)
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=False)

## CSRF
CSRF_COOKIE_SECURE = env.bool('DJANGO_CSRF_COOKIE_SECURE', default=False)
CSRF_COOKIE_HTTPONLY = env.bool('DJANGO_CSRF_COOKIE_HTTPONLY', default=False)
CSRF_COOKIE_DOMAIN = env.str('DJANGO_CSRF_COOKIE_DOMAIN', default=None)
CSRF_COOKIE_NAME = env.str('DJANGO_CSRF_COOKIE_NAME', default='csrftoken')
CSRF_COOKIE_PATH = env.str('DJANGO_CSRF_COOKIE_PATH', default='/')
CSRF_FAILURE_VIEW = env.str('DJANGO_CSRF_FAILURE_VIEW', default='django.views.csrf.csrf_failure')

## Sessions
SESSION_CACHE_ALIAS = env.str('DJANGO_SESSION_CACHE_ALIAS', default='default')
SESSION_COOKIE_AGE = env.int('DJANGO_SESSION_COOKIE_AGE', default=timedelta(weeks=2).total_seconds())
SESSION_COOKIE_DOMAIN = env.str('DJANGO_SESSION_COOKIE_DOMAIN', default=None)
SESSION_COOKIE_HTTPONLY = env.bool('DJANGO_SESSION_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_NAME = env.str('DJANGO_SESSION_COOKIE_NAME', default='sessionid')
SESSION_COOKIE_PATH = env.str('DJANGO_SESSION_COOKIE_PATH', default='/')
SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', default=False)
SESSION_ENGINE = env.str('DJANGO_SESSION_ENGINE', default='django.contrib.sessions.backends.db')
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool('DJANGO_SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False)
SESSION_FILE_PATH = env.str('DJANGO_SESSION_FILE_PATH', default=None)
SESSION_SAVE_EVERY_REQUEST = env.bool('DJANGO_SESSION_SAVE_EVERY_REQUEST', default=False)
SESSION_SERIALIZER = env.str('DJANGO_SESSION_SERIALIZER', default='django.contrib.sessions.serializers.JSONSerializer')
