from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Polygon

from django_enumfield import enum

from .excerpt import Excerpt


class BoundingGeometryType(enum.Enum):
    BOUNDINGBOX = 0
    # POLYGON = 1


class BoundingGeometry(models.Model):
    south_west = models.PointField(default=GEOSGeometry('POINT(0.0 0.0)'))
    north_east = models.PointField(default=GEOSGeometry('POINT(0.0 0.0)'))

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
        bounding_geometry = BoundingGeometry()
        bounding_geometry.south_west = GEOSGeometry('POINT(%s %s)' % (west, south))
        bounding_geometry.north_east = GEOSGeometry('POINT(%s %s)' % (east, north))
        bounding_geometry.type = BoundingGeometryType.BOUNDINGBOX
        return bounding_geometry

    type = enum.EnumField(BoundingGeometryType, default=BoundingGeometryType.BOUNDINGBOX)

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        geometry_type = 'Bounding box' if (self.type == BoundingGeometryType.BOUNDINGBOX) else 'Polygon'
        points = []
        for coordinates in self.geometry[0]:
            points.append('(' + ', '.join([str(round(coordinate, 5)) for coordinate in coordinates]) + ')')
        return geometry_type + ': ' + ', '.join(points)
