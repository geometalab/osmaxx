from django.contrib.gis.geos.collections import MultiPolygon
from django.contrib.gis.geos.polygon import Polygon

from osmaxx.conversion_api.coordinate_reference_systems import WGS_84

MIN_LONGITUDE_DEGREES = -180
MAX_LONGITUDE_DEGREES = +180


class UniversalTransverseMercatorZone:
    HEMISPHERE_PREFIXES = dict(north=326, south=327)
    NUMBER_OF_ZONES_PER_HEMISPHERE = 60
    VALID_ZONE_NUMBERS = range(1, NUMBER_OF_ZONES_PER_HEMISPHERE + 1)
    ZONE_WIDTH_DEGREES = 360 / NUMBER_OF_ZONES_PER_HEMISPHERE
    MAX_LONGITUDE_OFFSET = 90.0 - 9.9e-14

    def __init__(self, hemisphere, utm_zone_number):
        assert hemisphere in self.HEMISPHERE_PREFIXES.keys()
        assert utm_zone_number in self.VALID_ZONE_NUMBERS
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
                Polygon.from_bbox((xmin, ymin, MAX_LONGITUDE_DEGREES, ymax)),
                Polygon.from_bbox((MIN_LONGITUDE_DEGREES, ymin, xmax, ymax)),
                srid=WGS_84,
            )

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return MIN_LONGITUDE_DEGREES + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES

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
UTM_ZONE_NUMBERS = UTMZone.VALID_ZONE_NUMBERS
ALL_UTM_ZONES = frozenset(UTMZone(hs, nr) for hs in UTMZone.HEMISPHERE_PREFIXES for nr in UTM_ZONE_NUMBERS)


def utm_zones_for_representing(geom):
    return frozenset(zone for zone in ALL_UTM_ZONES if zone.can_represent(geom))


def wrap_longitude_degrees(longitude_degrees):
    return confine(longitude_degrees, MIN_LONGITUDE_DEGREES, MAX_LONGITUDE_DEGREES)


def confine(value, lower_bound, upper_bound):
    modulus = upper_bound - lower_bound
    result = (value - lower_bound) % modulus + lower_bound
    assert lower_bound <= result <= upper_bound
    return result
