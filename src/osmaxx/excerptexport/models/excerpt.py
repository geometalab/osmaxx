from django.conf import settings
from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.cache import cache
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from osmaxx.utils.geometry_buffer_helper import with_metric_buffer

EARTH_CIRCUMFERENCE_IN_METERS = 40075.017 * 1000
DEGREES_PER_CIRCLE = 360
DEGREES_PER_METERS_AT_EQUATOR = DEGREES_PER_CIRCLE / EARTH_CIRCUMFERENCE_IN_METERS
NYQIST_FACTOR = 1 / 2


class Excerpt(models.Model):
    EXCERPT_TYPE_USER_DEFINED = "user-defined"
    EXCERPT_TYPE_COUNTRY_BOUNDARY = "country"
    EXCERPT_TYPES = [
        (EXCERPT_TYPE_USER_DEFINED, _("user defined")),
        (EXCERPT_TYPE_COUNTRY_BOUNDARY, _("country")),
    ]
    name = models.CharField(max_length=128, verbose_name=_("name"))
    is_public = models.BooleanField(default=False, verbose_name=_("is public"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="excerpts",
        verbose_name=_("owner"),
        null=True,
        on_delete=models.CASCADE,
    )
    bounding_geometry = models.MultiPolygonField(verbose_name=_("bounding geometry"))
    excerpt_type = models.CharField(
        max_length=40, choices=EXCERPT_TYPES, default=EXCERPT_TYPE_USER_DEFINED
    )

    COUNTRY_SIMPLIFICATION_TOLERANCE_ANGULAR_DEGREES = 0.001
    BUFFER_METERS = 200

    CACHE_TIMEOUT_IN_SECONDS = None  # cache forever

    def simplified_buffered(self):
        """
        First simplifies, then buffers a copy of the self.bounding_geometry.

        The resulting area completely includes the area enclosed by the bounding_geometry.

        Returns: the resulting area
        """
        cache_key = "excerpt-buffered-{}".format(self.pk)

        geometry = cache.get(cache_key)
        if geometry:
            return geometry

        simplification_tolerance = (
            DEGREES_PER_METERS_AT_EQUATOR * NYQIST_FACTOR * self.BUFFER_METERS
        )
        original_srid = self.bounding_geometry.srs
        bounding_geometry = self.bounding_geometry.simplify(
            tolerance=simplification_tolerance, preserve_topology=True
        )
        bounding_geometry = with_metric_buffer(
            bounding_geometry, buffer_meters=self.BUFFER_METERS, map_srid=original_srid
        )
        if not isinstance(bounding_geometry, geos.MultiPolygon):
            bounding_geometry = geos.MultiPolygon(bounding_geometry)
        cache.set(cache_key, bounding_geometry, self.CACHE_TIMEOUT_IN_SECONDS)
        return bounding_geometry

    @property
    def geometry(self):
        if self.excerpt_type == self.EXCERPT_TYPE_COUNTRY_BOUNDARY:
            return self.simplified_buffered().simplify(
                tolerance=self.COUNTRY_SIMPLIFICATION_TOLERANCE_ANGULAR_DEGREES,
                preserve_topology=True,
            )
        return self.bounding_geometry

    @property
    def color(self):
        if self.excerpt_type == self.EXCERPT_TYPE_COUNTRY_BOUNDARY:
            return "black"
        return "blue"

    @property
    def extent(self):
        return self.bounding_geometry.extent

    @property
    def has_running_exports(self):
        return any(
            export.is_running
            for extraction_order in self.extraction_orders.all()
            for export in extraction_order.exports.all()
        )

    def attached_export_count(self, user):
        return self.extraction_orders.filter(orderer=user).aggregate(Count("exports"))[
            "exports__count"
        ]

    def __str__(self):
        return self.name


def private_user_excerpts(user):
    return _active_user_defined_excerpts().filter(is_public=False, owner=user)


def public_excerpts():
    return _active_user_defined_excerpts().filter(is_public=True)


def countries_and_administrative_areas():
    # We don't care about publicness or ownership with these and always return all (active ones) of them.
    return _active_excerpts().filter(excerpt_type=Excerpt.EXCERPT_TYPE_COUNTRY_BOUNDARY)


def _active_user_defined_excerpts():
    return _active_excerpts().filter(excerpt_type=Excerpt.EXCERPT_TYPE_USER_DEFINED)


def _active_excerpts():
    return Excerpt.objects.filter(is_active=True)
