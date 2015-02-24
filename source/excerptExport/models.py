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


class BoundingBox(models.Model):
    # 'max_digits' must be greater or equal to 'decimal_places'
    north = models.DecimalField(max_digits=16, decimal_places=16)
    east = models.DecimalField(max_digits=16, decimal_places=16)
    south = models.DecimalField(max_digits=16, decimal_places=16)
    west = models.DecimalField(max_digits=16, decimal_places=16)

    def __str__(self):
        return 'BoundingBox{north: ' + self.north + ', east: ' + self.east + \
               ', south: ' + self.south + ', west: ' + self.west + '}'


class Excerpt(models.Model):
    name = models.CharField(max_length=128)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    bounding_box = models.OneToOneField(BoundingBox)
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