from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VersionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "osmaxx.version"
    verbose_name = _("Version")
