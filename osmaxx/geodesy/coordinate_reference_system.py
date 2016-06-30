class UniversalTransverseMercatorZone:
    HEMISPHERE_PREFIXES = dict(
        north=326,
        south=327,
    )
    NUMBER_OF_ZONES_PER_HEMISPHERE = 60
    ZONE_WIDTH_DEGREES = 360 / NUMBER_OF_ZONES_PER_HEMISPHERE

    def __init__(self, hemisphere, utm_zone_number):
        assert hemisphere in self.HEMISPHERE_PREFIXES.keys()
        assert utm_zone_number - 1 in range(60)
        self.hemisphere = hemisphere
        self.utm_zone_number = utm_zone_number

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return -180 + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES
