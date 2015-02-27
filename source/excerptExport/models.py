from django.db import models
from django.contrib.gis.db import models
from django_enumfield import enum
from django.contrib.auth.models import User


class ExtractionOrderState(enum.Enum):
    UNDEFINED = 0
    INITIALIZED = 1
    WAITING = 2
    PROCESSING = 3
    FINISHED = 4
    CANCELED = 5


class BoundingGeometryType(enum.Enum):
    BOUNDINGBOX = 0
    #POLYGON = 1


class Excerpt(models.Model):
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(User, related_name='excerpts')

    def __str__(self):
        return self.name


class BoundingGeometry(models.Model):
    type = enum.EnumField(BoundingGeometryType, default=BoundingGeometryType.BOUNDINGBOX)
    geometry = models.GeometryField(srid=4326, blank=True, null=True, spatial_index=True)

    excerpt = models.OneToOneField(Excerpt, null=True)

    # overriding the default manager with a GeoManager instance.
    # required to perform spatial queries
    objects = models.GeoManager()

    def __str__(self):
        return 'Bounding box' if (self.type == BoundingGeometryType.BOUNDINGBOX) else 'Polygon'


class ExtractionOrder(models.Model):
    state = enum.EnumField(ExtractionOrderState, default=ExtractionOrderState.INITIALIZED)
    process_start_date = models.DateTimeField('process start date')
    process_reference = models.CharField(max_length=128)

    orderer = models.ForeignKey(User, related_name='extraction_orders')
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders')

    def __str__(self):
        return 'orderer: ' + self.orderer.get_username() + ', excerpt: ' + self.excerpt.name


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64)
    path = models.CharField(max_length=512)
    create_date = models.DateTimeField('create date')
    deleted_on_filesystem = models.BooleanField(default=False)

    extraction_order = models.ForeignKey(ExtractionOrder, related_name='output_files')

    def __str__(self):
        return self.path