import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django_enumfield import enum

from .excerpt import Excerpt


class ExtractionOrderState(enum.Enum):
    UNDEFINED = 0
    INITIALIZED = 1
    WAITING = 2
    PROCESSING = 3
    FINISHED = 4
    CANCELED = 5
    FAILED = 6


class ExtractionOrder(models.Model):
    state = enum.EnumField(ExtractionOrderState, default=ExtractionOrderState.INITIALIZED, verbose_name=_('state'))
    process_start_date = models.DateTimeField(null=True, verbose_name=_('process start date'))
    _extraction_configuration = models.TextField(
        blank=True, null=True, default='', verbose_name=_('extraction options')
    )
    process_id = models.TextField(blank=True, null=True, default='', verbose_name=_('process link'))
    orderer = models.ForeignKey(User, related_name='extraction_orders', verbose_name=_('orderer'))
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders', verbose_name=_('excerpt'))

    def __str__(self):
        return '[' + str(self.id) + '] orderer: ' + self.orderer.get_username() + ', excerpt: ' + self.excerpt.name +\
               ', state: ' + self.get_state_display() + ', output files: ' + str(self.output_files.count())

    @property
    def are_downloads_ready(self):
        return self.state == ExtractionOrderState.FINISHED

    @property
    def extraction_configuration(self):
        if self._extraction_configuration and not self._extraction_configuration == '':
            return json.loads(self._extraction_configuration)
        else:
            return None

    @extraction_configuration.setter
    def extraction_configuration(self, value):
        """
        :return example:
            {
                'gis': {
                    'formats': ['txt', 'file_gdb'],
                    'options': {
                        'coordinate_reference_system': 'wgs72',
                        'detail_level': 'verbatim'
                    }
                },
                'routing': { ... }
            }
        """
        if not value:
            value = {}
        self._extraction_configuration = json.dumps(value)

    @property
    def extraction_formats(self):
        extraction_formats = []
        for export_format_config in self.extraction_configuration.values():
            # merge lists to flat nested structure
            extraction_formats = extraction_formats + export_format_config['formats']
        return extraction_formats
