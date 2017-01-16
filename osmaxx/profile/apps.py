from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExcerptExportConfig(AppConfig):
    name = 'osmaxx.profile'
    verbose_name = _("Profile")
