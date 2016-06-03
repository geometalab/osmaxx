from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VersionConfig(AppConfig):
    name = 'osmaxx.version'
    verbose_name = _("Version")
