from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Excerpt(models.Model):
    EXCERPT_TYPE_USER_DEFINED = 'user-defined'
    EXCERPT_TYPE_COUNTRY_BOUNDARY = 'country'
    EXCERPT_TYPES = [
        (
            EXCERPT_TYPE_USER_DEFINED, _('user defined')
        ),
        (
            EXCERPT_TYPE_COUNTRY_BOUNDARY, _('country'),
        ),
    ]
    name = models.CharField(max_length=128, verbose_name=_('name'))
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    owner = models.ForeignKey(User, related_name='excerpts', verbose_name=_('owner'))
    bounding_geometry = models.MultiPolygonField(verbose_name=_('bounding geometry'), null=True)
    country = models.ForeignKey('countries.Country', verbose_name=_('Country'), null=True)
    excerpt_type = models.CharField(max_length=40, choices=EXCERPT_TYPES, default=EXCERPT_TYPE_USER_DEFINED)

    def send_to_conversion_service(self):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        api_client = ConversionApiClient()
        geometry = self.bounding_geometry
        if not geometry:
            geometry = self.country.border
        return api_client.create_boundary(geometry, name=self.name)

    @property
    def geometry(self):
        if self.bounding_geometry:
            return self.bounding_geometry
        if self.country:
            return self.country.border

    @property
    def type_of_geometry(self):
        return str(self.__class__.__name__)

    @property
    def extent(self):
        return self.bounding_geometry.extent

    def __str__(self):
        return self.name


def _active_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
        bounding_geometry__isnull=False
    )


def private_user_excerpts(user):
    return _active_excerpts().filter(is_public=False, owner=user)


def public_user_excerpts(user):
    return _active_excerpts().filter(is_public=True, owner=user)


def other_users_public_excerpts(user):
    return _active_excerpts().filter(is_public=True).exclude(owner=user)
