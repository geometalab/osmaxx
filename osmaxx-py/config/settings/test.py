from .local import *  # noqa

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append(
    'osmaxx.utilities.tests.test_models',
)
