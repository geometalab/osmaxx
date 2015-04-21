from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Polygon

from .excerpt import Excerpt


class BoundingGeometry(models.Model):
    pass


class BBoxBoundingGeometry(BoundingGeometry):
    south_west = models.PointField()
    north_east = models.PointField()

    @property
    def west(self):
        return self.south_west[0]

    @property
    def east(self):
        return self.north_east[0]

    @property
    def north(self):
        return self.north_east[1]

    @property
    def south(self):
        return self.south_west[1]

    @property
    def geometry(self):
        polygon = Polygon([
            self.south_west,
            GEOSGeometry('POINT(%s %s)' % (self.west, self.north)),
            self.north_east,
            GEOSGeometry('POINT(%s %s)' % (self.east, self.south)),
            self.south_west
        ])
        return GEOSGeometry(polygon)

    @staticmethod
    def create_from_bounding_box_coordinates(north, east, south, west):
        bounding_geometry = BBoxBoundingGeometry()
        bounding_geometry.south_west = GEOSGeometry('POINT(%s %s)' % (west, south))
        bounding_geometry.north_east = GEOSGeometry('POINT(%s %s)' % (east, north))
        bounding_geometry.save()
        return bounding_geometry

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        points = []
        for coordinates in self.geometry[0]:
            points.append('(' + ', '.join([str(round(coordinate, 5)) for coordinate in coordinates]) + ')')
        return 'Bounding box' + ': ' + ', '.join(points)
