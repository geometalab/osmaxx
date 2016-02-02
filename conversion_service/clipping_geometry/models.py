from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class ClippingArea(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=200)
    clipping_multi_polygon = models.MultiPolygonField(verbose_name=_('clipping MultiPolygon'))
