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
print(ALLOWED_HOSTS)
DATABASES['default'] = env.db("DJANGO_DATABASE_URL")

# add the gunicorn runner
INSTALLED_APPS += ("gunicorn", )

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
