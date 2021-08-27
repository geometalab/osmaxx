# pylint: skip-file
from .common import *  # noqa

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="CHANGEME!!!")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

INTERNAL_IPS = env.tuple("DJANGO_INTERNAL_IPS", default=("127.0.0.1",))


# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"
