from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Polygon

from django_enumfield import enum

from .excerpt import Excerpt


class BoundingGeometryType(enum.Enum):
    BOUNDINGBOX = 0
    # POLYGON = 1


class BoundingGeometry(models.Model):
    @staticmethod
    def create_from_bounding_box_coordinates(north, east, south, west):
        bounding_geometry = BoundingGeometry()
        bounding_geometry.type = BoundingGeometryType.BOUNDINGBOX
        polygon = Polygon([
            GEOSGeometry('POINT(%s %s)' % (west, south)),
            GEOSGeometry('POINT(%s %s)' % (west, north)),
            GEOSGeometry('POINT(%s %s)' % (east, north)),
            GEOSGeometry('POINT(%s %s)' % (east, south)),
            GEOSGeometry('POINT(%s %s)' % (west, south))
        ])
        bounding_geometry.geometry = GEOSGeometry(polygon)
        return bounding_geometry

    type = enum.EnumField(BoundingGeometryType, default=BoundingGeometryType.BOUNDINGBOX)
    geometry = models.GeometryField(srid=4326, blank=True, null=True, spatial_index=True)

    # django admin inline mode needs relation from BoundingGeometry to Excerpt -> inverse relation does not work
    excerpt = models.OneToOneField(Excerpt, null=True)

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        geometry_type = 'Bounding box' if (self.type == BoundingGeometryType.BOUNDINGBOX) else 'Polygon'
        points = []
        for coordinates in self.geometry[0]:
            points.append('(' + ', '.join(list(str(round(coordinate, 5)) for coordinate in coordinates)) + ')')
        return geometry_type + ': ' + ', '.join(points)
