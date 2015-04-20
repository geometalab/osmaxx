from django.db import models
from django.contrib.auth.models import User

from django_enumfield import enum

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
    process_start_date = models.DateTimeField('process start date', null=True)
    process_reference = models.CharField(max_length=128, blank=True, null=True)

    orderer = models.ForeignKey(User, related_name='extraction_orders')
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders')

    def __str__(self):
        return '[' + str(self.id) + '] orderer: ' + self.orderer.get_username() + ', excerpt: ' + self.excerpt.name + ', state: ' + self.get_state_display() \
               + ', output files: ' + str(self.output_files.count())

    @property
    def are_downloads_ready(self):
        return self.state == ExtractionOrderState.FINISHED
