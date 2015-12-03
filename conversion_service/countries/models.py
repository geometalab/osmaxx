from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from countries.fields import InternalCountryFileField


class Country(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    polyfile = InternalCountryFileField(verbose_name=_('polyfile'))
    associated_multipolygon = models.MultiPolygonField(verbose_name=_('associated_multipolygon'))
