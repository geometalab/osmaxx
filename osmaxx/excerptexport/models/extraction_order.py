import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
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

FINAL_STATES = {ExtractionOrderState.FINISHED, ExtractionOrderState.CANCELED, ExtractionOrderState.FAILED}


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
    excerpt = models.ForeignKey(Excerpt, related_name='extraction_orders', verbose_name=_('excerpt'), null=True)
    country_id = models.IntegerField(verbose_name=_('country ID'), null=True, blank=True)
    progress_url = models.URLField(verbose_name=_('progress URL'), null=True, blank=True)
    process_start_time = models.DateTimeField(verbose_name=_('process start time'), null=True, blank=True)
    download_status = models.IntegerField(
        _('file status'),
        choices=DOWNLOAD_STATUSES,
        default=DOWNLOAD_STATUS_NOT_DOWNLOADED
    )

    def forward_to_conversion_service(self, *, incoming_request):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        clipping_area_json = self.excerpt.send_to_conversion_service()
        gis_options = self.extraction_configuration['gis_options']
        api_client = ConversionApiClient()
        jobs_json = []
        for extraction_format in self.extraction_formats:
            parametrization_json = api_client.create_parametrization(clipping_area_json, extraction_format, gis_options)
            job_json = api_client.create_job(parametrization_json, incoming_request)
            jobs_json.append(job_json)
        return jobs_json

    def __str__(self):
        return ', '.join(
            [
                '[{order_id}] orderer: {orderer_name}'.format(
                    order_id=self.id,
                    orderer_name=self.orderer.get_username(),
                ),
                'excerpt: {}'.format(str(self.excerpt_name)),
                'state: {}'.format(self.get_state_display()),
                'output files: {}'.format(str(self.output_files.count())),
            ]
        )

    @property
    def excerpt_name(self):
        """
        Returns:
              user-given excerpt name for user-defined excerpts,
              country name for countries,
              None if order has no excerpt (neither country nor user-defined)
        """
        if self.excerpt:
            return self.excerpt.name
        elif self.country_id:
            from osmaxx.api_client import ConversionApiClient
            return ConversionApiClient().get_country_name(self.country_id)

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
        if not value:
            value = {}
        else:
            value = dict(value)
        new_formats = frozenset(value.pop('gis_formats', []))
        previous_formats = self.exports.values_list('file_format', flat=True)
        assert new_formats.issuperset(previous_formats)
        self._extraction_configuration = json.dumps(value)
        self._new_formats = new_formats  # Will be collected and cleaned up by attach_new_formats.
        if self.id is not None:
            attach_new_formats(self.__class__, instance=self)

    @property
    def extraction_formats(self):
        return list(self.exports.values_list('file_format', flat=True))  # TODO: make this lazy

    @property
    def process_due_time(self):
        from django.conf import settings  # import locally, so migrations can't depend on settings
        return self.process_start_time + settings.OSMAXX.get('EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA')

    def set_status_from_conversion_progress(self, job_overall_progress):
        if self.state not in [ExtractionOrderState.FINISHED, ExtractionOrderState.FAILED]:
            self.state = get_order_status_from_conversion_progress(job_overall_progress)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('excerptexport:status', kwargs={'extraction_order_id': self.id})


@receiver(post_save, sender=ExtractionOrder)
def attach_new_formats(sender, instance, **kwargs):
    if hasattr(instance, '_new_formats'):
        for format in instance._new_formats:
            instance.exports.get_or_create(file_format=format)
        del instance._new_formats
