import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django_enumfield import enum

from .excerpt import Excerpt


class ExtractionOrderState(enum.Enum):
    UNDEFINED = 0
    INITIALIZED = 1
    QUEUED = 2
    PROCESSING = 3
    FINISHED = 4
    CANCELED = 5
    FAILED = 6


CONVERSION_PROGRESS_TO_EXTRACTION_ORDER_STATE_MAPPING = {
    'new': ExtractionOrderState.INITIALIZED,
    'received': ExtractionOrderState.QUEUED,
    'started': ExtractionOrderState.PROCESSING,
    'successful': ExtractionOrderState.FINISHED,
    'error': ExtractionOrderState.FAILED,
}


def get_order_status_from_conversion_progress(progress):
    return CONVERSION_PROGRESS_TO_EXTRACTION_ORDER_STATE_MAPPING.get(progress, ExtractionOrderState.UNDEFINED)


class ExtractionOrder(models.Model):
    DOWNLOAD_STATUS_NOT_DOWNLOADED = 0
    DOWNLOAD_STATUS_DOWNLOADING = 1
    DOWNLOAD_STATUS_AVAILABLE = 2

    DOWNLOAD_STATUSES = (
        (DOWNLOAD_STATUS_NOT_DOWNLOADED, 'unknown'),
        (DOWNLOAD_STATUS_DOWNLOADING, 'downloading'),
        (DOWNLOAD_STATUS_AVAILABLE, 'received'),
    )

    state = enum.EnumField(ExtractionOrderState, default=ExtractionOrderState.INITIALIZED, verbose_name=_('state'))
    _extraction_configuration = models.TextField(
        blank=True, null=True, default='', verbose_name=_('extraction options')
    )
    process_id = models.TextField(blank=True, null=True, verbose_name=_('process link'))
    orderer = models.ForeignKey(User, related_name='extraction_orders', verbose_name=_('orderer'))
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders', verbose_name=_('excerpt'))
    progress_url = models.URLField(verbose_name=_('progress URL'), null=True, blank=True)
    process_start_time = models.DateTimeField(verbose_name=_('process start time'), null=True, blank=True)
    download_status = models.IntegerField(
        _('file status'),
        choices=DOWNLOAD_STATUSES,
        default=DOWNLOAD_STATUS_NOT_DOWNLOADED
    )

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
                'gis_formats': ['txt', 'file_gdb'],
                'gis_options': {
                    'coordinate_reference_system': 'wgs72',
                    'detail_level': 'verbatim'
                },
                'routing': { ... }
            }
        """
        if not value:
            value = {}
        self._extraction_configuration = json.dumps(value)

    @property
    def extraction_formats(self):
        return json.loads(self.extraction_configuration).get('gis_formats', None)

    def set_status_from_conversion_progress(self, job_overall_progress):
        if self.state not in [ExtractionOrderState.FINISHED, ExtractionOrderState.FAILED]:
            self.state = get_order_status_from_conversion_progress(job_overall_progress)
