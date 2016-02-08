from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CountryConfig(AppConfig):
    name = 'osmaxx.countries'
    verbose_name = _("Countries")
