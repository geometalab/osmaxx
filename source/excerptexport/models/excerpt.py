from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Excerpt(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=128)
    is_public = models.BooleanField(verbose_name=_('is public'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    owner = models.ForeignKey(User, related_name='excerpts', verbose_name=_('owner'))
    bounding_geometry = models.OneToOneField('BoundingGeometry', verbose_name=_('bounding geometry'))

    def __str__(self):
        return self.name
