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
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', default=''),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': env.str('SENTRY_RELEASE', default=''),
}
