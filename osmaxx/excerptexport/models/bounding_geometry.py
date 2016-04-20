from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

from model_utils.managers import InheritanceManager

from osmaxx.excerptexport.utils.upload_to import get_private_upload_storage
from osmaxx.utilities.dict_helpers import are_all_keys_in
from osmaxx.utilities.model_mixins import AdminUrlModelMixin


class BoundingGeometry(models.Model):
    @property
    def type(self):
        return type(self).__name__

    @property
    def geometry(self):
        subclass_instance = self.subclass_instance
        if self == subclass_instance:
            raise NotImplementedError
        return subclass_instance.geometry

    @property
    def extent(self):
        return self.geometry.extent

    @property
    def type_of_geometry(self):
        return str(self.subclass_instance.__class__.__name__)

    def __str__(self):
        subclass_instance = self.subclass_instance
        parent = '{} {id}'.format(super().__str__(), id=self.id)
        if self == subclass_instance:
            return parent
        return '{parent}: {child}'.format(parent=parent, id=self.id, child=str(subclass_instance))

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
        return 'Polygon file {id}: {filename}'.format(self.id, self.polygon_file.name)


class BBoxBoundingGeometry(AdminUrlModelMixin, BoundingGeometry):
    def __init__(self, *args, **kwargs):
        attribute_names = ['north', 'east', 'south', 'west']
        if are_all_keys_in(kwargs, keys=attribute_names) \
                and not are_all_keys_in(kwargs, keys=['south_west', 'north_east']):
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
        polygon = Polygon.from_bbox((self.west, self.south, self.east, self.north))
        return MultiPolygon(polygon)

    @staticmethod
    def create_from_bounding_box_coordinates(north, east, south, west):
        south_west = GEOSGeometry('POINT(%s %s)' % (west, south))
        north_east = GEOSGeometry('POINT(%s %s)' % (east, north))
        return BBoxBoundingGeometry.objects.create(south_west=south_west, north_east=north_east)

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        return 'Bounding box {id}: (north={n}, east={e}, south={s}, west={w})'.format(
            id=self.id,
            n=self.north,
            e=self.east,
            s=self.south,
            w=self.west,
        )
