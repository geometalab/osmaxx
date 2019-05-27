# -*- coding: utf-8 -*-
'''
Production Configuration
'''
from .common import *  # noqa

MIDDLEWARE = [
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # before all other middlewares, with the exception of SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# get an exception when starting, if they are not defined
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS += [
    'gunicorn',
]

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# SENTRY
SENTRY_DSN = env.str('SENTRY_DSN', default=None)

if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

OSMAXX['CONVERSION_SERVICE_USERNAME'] = env.str('DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME')
OSMAXX['CONVERSION_SERVICE_PASSWORD'] = env.str('DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD')
