# -*- coding: utf-8 -*-
'''
Production Configuration
'''
from .common import *  # noqa

# SECRET/SECURITY CONFIGURATION
# ------------------------------------------------------------------------------

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
) + MIDDLEWARE_CLASSES

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SSL CONFIGURATION
# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=60)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_SSL_HOST = env.str('DJANGO_SECURE_SSL_HOST', default='')
SECURE_REDIRECT_EXEMPT = env.list('DJANGO_SECURE_REDIRECT_EXEMPT', default=[])

# OTHER SECURITY SETTINGS
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = env.bool("DJANGO_SECURE_BROWSER_XSS_FILTER", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = env.bool("DJANGO_SESSION_COOKIE_HTTPONLY", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
CSRF_COOKIE_HTTPONLY = env.bool("DJANGO_CSRF_COOKIE_HTTPONLY", default=True)
X_FRAME_OPTIONS = env.str("DJANGO_X_FRAME_OPTIONS", default='DENY')

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['.osmaxx.hsr.ch.'])
# END SITE CONFIGURATION

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

# Static Assests
# ------------------------
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='noreply osmaxx <noreply@osmaxx.hsr.ch>')
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default='emailserver')
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USERNAME')
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", default=587)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default='[osmaxx] ')
EMAIL_USE_TLS = env("DJANGO_EMAIL_USE_TLS", default=True)
SERVER_EMAIL = EMAIL_HOST_USER

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DJANGO_DATABASE_URL")


# Your production stuff: Below this line define 3rd party library settings
BROKER_URL = env.str('DJANGO_CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = BROKER_URL
