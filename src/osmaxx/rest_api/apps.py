from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestAPIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "osmaxx.rest_api"
    verbose_name = _("Rest API")
