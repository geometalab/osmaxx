# -*- coding: utf-8 -*-
'''
Production Configuration
'''
from .common import *  # noqa

MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
) + MIDDLEWARE_CLASSES

# get an exception when starting, if they are not defined
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
DATABASES['default'] = env.db("DJANGO_DATABASE_URL")

INSTALLED_APPS += (
    'gunicorn',
    # sentry
    'raven.contrib.django.raven_compat',
)

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
# we are prepared for this but aren't using it right now
INSTALLED_APPS += (
    # 'storages',
)

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': env.str('SENTRY_RELEASE'),
}
