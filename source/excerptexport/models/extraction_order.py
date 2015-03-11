from django.db import models
from django_enumfield import enum

from django.contrib.auth.models import User
from .excerpt import Excerpt


class ExtractionOrderState(enum.Enum):
    UNDEFINED = 0
    INITIALIZED = 1
    WAITING = 2
    PROCESSING = 3
    FINISHED = 4
    CANCELED = 5


class ExtractionOrder(models.Model):
    state = enum.EnumField(ExtractionOrderState, default=ExtractionOrderState.INITIALIZED)
    process_start_date = models.DateTimeField('process start date')
    process_reference = models.CharField(max_length=128)

    orderer = models.ForeignKey(User, related_name='extraction_orders')
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders')

    def __str__(self):
        return 'orderer: ' + self.orderer.get_username() + ', excerpt: ' + self.excerpt.name