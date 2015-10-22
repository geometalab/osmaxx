import random
import string

from .common import *  # noqa

# we don't use user sessions, so it doesn't matter if we recreate the secret key on each startup
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))

# disable databases for the worker
DATABASES = {}
