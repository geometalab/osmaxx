from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExcerptExportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "osmaxx.excerptexport"
    verbose_name = _("Excerpt Export")
