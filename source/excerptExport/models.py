from django.db import models
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


class BoundingGeometry(models.Model):
    # 'max_digits': number of total digits
    # 'decimal_places': number of digits following decimal point
    # 7 digits following decimal point -> mm
    north = models.DecimalField(max_digits=12, decimal_places=8)
    east = models.DecimalField(max_digits=12, decimal_places=8)
    south = models.DecimalField(max_digits=12, decimal_places=8)
    west = models.DecimalField(max_digits=12, decimal_places=8)

    type = enum.EnumField(BoundingGeometryType, default=BoundingGeometryType.BOUNDINGBOX)

    # TODO: replace by models.GeometryField(srid=4326)
    # geometry = models.CharField(max_length=128)

    def __str__(self):
        return 'BoundingGeometry{type: ' + self.type + ', north: ' + self.north + ', east: ' + self.east + \
               ', south: ' + self.south + ', west: ' + self.west + '}'


class Excerpt(models.Model):
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    bounding_box = models.OneToOneField(BoundingGeometry)
    owner = models.ForeignKey(User, related_name='excerpts')

    def __str__(self):
        return 'Excerpt {name: '+self.name+', bounding box: '+self.bounding_box+'}'


class ExtractionOrder(models.Model):
    state = enum.EnumField(ExtractionOrderState, default=ExtractionOrderState.INITIALIZED)
    process_start_date = models.DateTimeField('process start date')
    process_reference = models.CharField(max_length=128)

    orderer = models.ForeignKey(User, related_name='extraction_orders')
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders')

    def __str__(self):
        return 'ExtractionOrder{orderer: ' + self.orderer + ', excerpt: ' + \
               self.excerpt + ', state: ' + self.state + '}'


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64)
    path = models.FileField(max_length=512)
    create_date = models.DateTimeField('create date')
    deleted_on_filesystem = models.BooleanField(default=False)

    extraction_order = models.ForeignKey(ExtractionOrder, related_name='output_files')

    def __str__(self):
        return 'OutputFile{mime type: '+self.mime_type+', path: '+self.path+'}'