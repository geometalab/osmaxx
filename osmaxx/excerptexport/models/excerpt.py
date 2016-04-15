from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Excerpt(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    owner = models.ForeignKey(User, related_name='excerpts', verbose_name=_('owner'))
    bounding_geometry = models.OneToOneField('BoundingGeometry', verbose_name=_('bounding geometry'))

    def send_to_conversion_service(self):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        api_client = ConversionApiClient()
        return api_client.create_boundary(self.bounding_geometry.geometry, name=self.name)

    @property
    def type_of_geometry(self):
        return self.bounding_geometry.type_of_geometry

    @property
    def extent(self):
        return self.bounding_geometry.extent

    def __str__(self):
        return self.name


def _active_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
        bounding_geometry__bboxboundinggeometry__isnull=False
    )


def private_user_excerpts(user):
    return _active_excerpts().filter(is_public=False, owner=user)


def public_user_excerpts(user):
    return _active_excerpts().filter(is_public=True, owner=user)


def other_users_public_excerpts(user):
    return _active_excerpts().filter(is_public=True).exclude(owner=user)
