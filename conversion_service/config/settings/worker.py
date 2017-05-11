# pylint: skip-file

import random
import string

from .common import *  # noqa

# we don't use user sessions, so it doesn't matter if we recreate the secret key on each startup
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))

# disable databases for the worker
DATABASES = {}

INSTALLED_APPS += (
    # sentry
    'raven.contrib.django.raven_compat',
)

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
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            "rq_console": {
                "level": "DEBUG",
                "class": "rq.utils.ColorizingStreamHandler",
                "formatter": "verbose",
            },
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            "rq.worker": {
                "level": "WARNING",
                "handlers": ['rq_console', "sentry"],
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
        'dsn': "sync+" + SENTRY_DSN,
        'release': env.str('SENTRY_RELEASE', default=''),
    }
