# pylint: skip-file
"""
Production Configuration
"""
from .common import *  # noqa

# No fallback values for the following settings, as we WANT an exception
# during start if any of the corresponding environment variables aren't set.
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# SENTRY
SENTRY_DSN = env.str("SENTRY_DSN", default=None)

if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])
