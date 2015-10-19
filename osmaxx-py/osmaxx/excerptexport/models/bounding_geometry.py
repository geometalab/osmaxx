from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Polygon

from model_utils.managers import InheritanceManager

from osmaxx.excerptexport.utils.upload_to import get_private_upload_storage
from osmaxx.utilities.dict_helpers import are_all_keys_in


class BoundingGeometry(models.Model):
    @property
    def type(self):
        return type(self).__name__

    @property
    def geometry(self):
        raise NotImplementedError

    @property
    def extent(self):
        return self.subclass_instance.geometry.extent

    @property
    def type_of_geometry(self):
        return str(self.subclass_instance.__class__.__name__)

    @property
    def subclass_instance(self):
        # TODO: don't make an extra query for this
        return BoundingGeometry.objects.get_subclass(pk=self.id)

    objects = InheritanceManager()


class OsmosisPolygonFilterBoundingGeometry(BoundingGeometry):
    """
    Bounding geometry based on a 'Osmosis polygon filter file format' file.
    """
    polygon_file = models.FileField(storage=get_private_upload_storage())

    def __str__(self):
        return 'Polygon file: ' + self.polygon_file.name


class BBoxBoundingGeometry(BoundingGeometry):
    def __init__(self, *args, **kwargs):
        attribute_names = ['north', 'east', 'south', 'west']
        if are_all_keys_in(kwargs, attribute_names) \
                and not are_all_keys_in(kwargs, ['south_west', 'north_east']):
            kwargs['south_west'] = GEOSGeometry('POINT(%s %s)' % (kwargs.pop('west'), kwargs.pop('south')))
            kwargs['north_east'] = GEOSGeometry('POINT(%s %s)' % (kwargs.pop('east'), kwargs.pop('north')))
        super().__init__(*args, **kwargs)

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
        south_west = GEOSGeometry('POINT(%s %s)' % (west, south))
        north_east = GEOSGeometry('POINT(%s %s)' % (east, north))
        return BBoxBoundingGeometry.objects.create(south_west=south_west, north_east=north_east)

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        points = []
        for coordinates in self.geometry[0]:
            points.append('(' + ', '.join([str(round(coordinate, 5)) for coordinate in coordinates]) + ')')
        return 'Bounding box' + ': ' + ', '.join(points)
