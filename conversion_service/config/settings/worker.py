# pylint: skip-file

import random
import string

from .common import *  # noqa

# we don't use user sessions, so it doesn't matter if we recreate the secret key on each startup
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))

# disable databases for the worker
DATABASES = {}

# SENTRY
SENTRY_DSN = env.str('SENTRY_DSN', default=None)

if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

