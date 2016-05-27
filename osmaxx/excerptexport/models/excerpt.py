from django.contrib.auth.models import User
from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from osmaxx.utils.geometry_buffer_helper import with_metric_buffer


class Excerpt(models.Model):
    EXCERPT_TYPE_USER_DEFINED = 'user-defined'
    EXCERPT_TYPE_COUNTRY_BOUNDARY = 'country'
    EXCERPT_TYPES = [
        (EXCERPT_TYPE_USER_DEFINED, _('user defined')),
        (EXCERPT_TYPE_COUNTRY_BOUNDARY, _('country')),
    ]
    name = models.CharField(max_length=128, verbose_name=_('name'))
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    owner = models.ForeignKey(User, related_name='excerpts', verbose_name=_('owner'), null=True)
    bounding_geometry = models.MultiPolygonField(verbose_name=_('bounding geometry'), null=True)
    excerpt_type = models.CharField(max_length=40, choices=EXCERPT_TYPES, default=EXCERPT_TYPE_USER_DEFINED)

    COUNTRY_SIMPLIFICATION_TOLERANCE = 0.01

    def send_to_conversion_service(self):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        api_client = ConversionApiClient()
        bounding_geometry = self.bounding_geometry
        if self.excerpt_type == self.EXCERPT_TYPE_COUNTRY_BOUNDARY:
            original_srid = self.bounding_geometry.srs
            bounding_geometry = with_metric_buffer(self.bounding_geometry, buffer_meters=100, map_srid=original_srid)
            if not isinstance(bounding_geometry, geos.MultiPolygon):
                bounding_geometry = geos.MultiPolygon(bounding_geometry)
        return api_client.create_boundary(bounding_geometry, name=self.name)

    @property
    def geometry(self):
        if self.excerpt_type == self.EXCERPT_TYPE_COUNTRY_BOUNDARY:
            return self.bounding_geometry.simplify(
                tolerance=self.COUNTRY_SIMPLIFICATION_TOLERANCE,
                preserve_topology=True
            )
        return self.bounding_geometry

    @property
    def color(self):
        if self.excerpt_type == self.EXCERPT_TYPE_COUNTRY_BOUNDARY:
            return 'black'
        return 'blue'

    @property
    def extent(self):
        return self.bounding_geometry.extent

    def __str__(self):
        return self.name


def _active_user_defined_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
        bounding_geometry__isnull=False,
        excerpt_type=Excerpt.EXCERPT_TYPE_USER_DEFINED,
    )


def private_user_excerpts(user):
    return _active_user_defined_excerpts().filter(is_public=False, owner=user)


def public_user_excerpts(user):
    return _active_user_defined_excerpts().filter(is_public=True, owner=user)


def other_users_public_excerpts(user):
    return _active_user_defined_excerpts().filter(is_public=True).exclude(owner=user)
