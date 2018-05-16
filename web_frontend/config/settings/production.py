# -*- coding: utf-8 -*-
'''
Production Configuration
'''
from .common import *  # noqa

MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
    # add whitenoise middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
) + MIDDLEWARE_CLASSES

# get an exception when starting, if they are not defined
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS += (
    'gunicorn',
    # sentry
    'raven.contrib.django.raven_compat',
)

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# SENTRY
SENTRY_DSN = env.str('SENTRY_DSN', default=None)

if SENTRY_DSN:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'release': env.str('SENTRY_RELEASE', default=''),
    }

OSMAXX['CONVERSION_SERVICE_USERNAME'] = env.str('DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME')
OSMAXX['CONVERSION_SERVICE_PASSWORD'] = env.str('DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD')
