# pylint: skip-file
'''
Production Configuration
'''
from .common import *  # noqa

MIDDLEWARE = [
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# No fallback values for the following settings, as we WANT an exception
# during start if any of the corresponding environment variables aren't set.
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS += [
    'gunicorn',
    # sentry
]

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
# we are prepared for this but aren't using it right now
INSTALLED_APPS += [
    # 'storages',
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
