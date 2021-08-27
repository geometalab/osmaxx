from fnmatch import fnmatch

from .common import *  # noqa


class glob_list(list):  # noqa
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False


DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="CHANGEME!!!")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# django-debug-toolbar
# ------------------------------------------------------------------------------
INTERNAL_IPS = glob_list(env.tuple("DJANGO_INTERNAL_IPS", default=("127.0.0.1",)))

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"
