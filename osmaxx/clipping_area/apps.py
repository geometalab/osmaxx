from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClippingGeometryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "osmaxx.clipping_area"
    verbose_name = _("Clipping Geometry")
