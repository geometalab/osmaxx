from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Excerpt(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    owner = models.ForeignKey(User, related_name='excerpts', verbose_name=_('owner'))
    bounding_geometry_raw_reference = models.OneToOneField('BoundingGeometry', verbose_name=_('bounding geometry'))

    @property
    def bounding_geometry(self):
        return self.bounding_geometry_raw_reference.geometry_instance

    @bounding_geometry.setter
    def bounding_geometry(self, bounding_geometry):
        self.bounding_geometry_raw_reference = bounding_geometry

    @property
    def extent(self):
        return self.bounding_geometry_raw_reference.extent

    def __str__(self):
        return self.name
