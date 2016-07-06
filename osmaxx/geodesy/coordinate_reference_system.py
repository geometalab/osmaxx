from django.contrib.gis.geos.collections import MultiPolygon
from django.contrib.gis.geos.polygon import Polygon

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84


class UniversalTransverseMercatorZone:
    HEMISPHERE_PREFIXES = dict(
        north=326,
        south=327,
    )
    NUMBER_OF_ZONES_PER_HEMISPHERE = 60
    ZONE_WIDTH_DEGREES = 360 / NUMBER_OF_ZONES_PER_HEMISPHERE
    MAX_LONGITUDE_OFFSET = 90.0 - 9.9e-14

    def __init__(self, hemisphere, utm_zone_number):
        assert hemisphere in self.HEMISPHERE_PREFIXES.keys()
        assert utm_zone_number in range(1, 60 + 1)
        self.hemisphere = hemisphere
        self.utm_zone_number = utm_zone_number
        self._prepared_domain = None  # Will be lazily set by self.domain

    def can_represent(self, geom):
        return self.domain.covers(geom.transform(WGS_84, clone=True))

    @property
    def domain(self):
        if self._prepared_domain is None:
            self._prepared_domain = self._computed_domain.prepared
        return self._prepared_domain

    @property
    def _computed_domain(self):
        xmin, ymin, xmax, ymax = (
            wrap_longitude_degrees(self.central_meridian_longitude_degrees - self.MAX_LONGITUDE_OFFSET),
            -90,
            wrap_longitude_degrees(self.central_meridian_longitude_degrees + self.MAX_LONGITUDE_OFFSET),
            90,
        )
        if xmin <= xmax:
            domain = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            domain.srid = WGS_84
            return domain
        else:
            # cut at idealized international date line
            return MultiPolygon(
                Polygon.from_bbox((xmin, ymin, 180, ymax)),
                Polygon.from_bbox((-180, ymin, xmax, ymax)),
                srid=WGS_84,
            )

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return -180 + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES

    def __eq__(self, other):
        return self.hemisphere, self.utm_zone_number == other.hemisphere, other.utm_zone_number

    def __hash__(self):
        return hash((self.hemisphere, self.utm_zone_number))

    def __str__(self):
        return "UTM Zone {zone_number}, {hemisphere}ern hemisphere".format(
            zone_number=self.utm_zone_number,
            hemisphere=self.hemisphere,
        )

    def __repr__(self):
        return "UTMZone({hemisphere}, {zone_number})".format(
            zone_number=self.utm_zone_number,
            hemisphere=repr(self.hemisphere),
        )

UTMZone = UniversalTransverseMercatorZone
ALL_UTM_ZONES = frozenset(UTMZone(hs, nr) for hs in UTMZone.HEMISPHERE_PREFIXES for nr in range(1, 60 + 1))


def utm_zones_for_representing(geom):
    return frozenset(zone for zone in ALL_UTM_ZONES if zone.can_represent(geom))


def wrap_longitude_degrees(longitude_degrees):
    wrapped_longitude_degrees = (longitude_degrees + 180) % 360 - 180
    assert -180 <= wrapped_longitude_degrees <= 180
    return wrapped_longitude_degrees
