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
        assert utm_zone_number - 1 in range(60)
        self.hemisphere = hemisphere
        self.utm_zone_number = utm_zone_number

    def can_represent(self, point):
        longitude_offset = wrap_longitude_degrees(point.x - self.central_meridian_longitude_degrees)
        return -self.MAX_LONGITUDE_OFFSET <= longitude_offset <= self.MAX_LONGITUDE_OFFSET

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return -180 + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES


def wrap_longitude_degrees(longitude_degrees):
    wrapped_longitude_degrees = (longitude_degrees + 180) % 360 - 180
    assert -180 <= wrapped_longitude_degrees <= 180
    return wrapped_longitude_degrees
