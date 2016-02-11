from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .to_polyfile import create_poly_file_string


class ClippingArea(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=200)
    clipping_multi_polygon = models.MultiPolygonField(verbose_name=_('clipping MultiPolygon'))

    @property
    def osmosis_polygon_file_string(self):
        return create_poly_file_string(self.clipping_multi_polygon)

    def __str__(self):
        return "{} ({})".format(self.name, self.id)
