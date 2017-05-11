"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from raven.contrib.django.middleware.wsgi import Sentry
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conversion_service.config.settings.production")

application = get_wsgi_application()
application = Sentry(DjangoWhiteNoise(application))
