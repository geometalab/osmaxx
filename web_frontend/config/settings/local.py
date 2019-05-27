from fnmatch import fnmatch

from .common import *  # noqa


class glob_list(list):  # noqa
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default='CHANGEME!!!')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
INSTALLED_APPS += ['debug_toolbar', ]
DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = glob_list(env.tuple('DJANGO_INTERNAL_IPS', default=('127.0.0.1',)))

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'JQUERY_URL': '/static/osmaxx/libraries/jquery/jquery.min.js',
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
