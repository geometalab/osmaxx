import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django_enumfield import enum

from osmaxx.excerptexport.models.output_file import OutputFile
from .excerpt import Excerpt


# TODO: remove ExtractionOrderState,
# TODO:   since this is obsolete and replaced with osmaxx.conversion_api.statuses.STATUS_CHOICES
class ExtractionOrderState(enum.Enum):
    UNDEFINED = 0
    INITIALIZED = 1
    QUEUED = 2
    PROCESSING = 3
    FINISHED = 4
    FAILED = 6

FINAL_STATES = {ExtractionOrderState.FINISHED, ExtractionOrderState.FAILED}


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
    progress_url = models.URLField(verbose_name=_('progress URL'), null=True, blank=True)
    process_start_time = models.DateTimeField(verbose_name=_('process start time'), null=True, blank=True)
    download_status = models.IntegerField(
        _('file status'),
        choices=DOWNLOAD_STATUSES,
        default=DOWNLOAD_STATUS_NOT_DOWNLOADED
    )

    def forward_to_conversion_service(self, *, incoming_request):
        clipping_area_json = self.excerpt.send_to_conversion_service()
        jobs_json = [
            export.send_to_conversion_service(clipping_area_json, incoming_request)
            for export in self.exports.all()
        ]
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

    @property
    def output_files(self):
        return OutputFile.objects.filter(export__extraction_order=self)

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
        assert 'gis_formats' not in value
        self._extraction_configuration = json.dumps(value)

    @property
    def extraction_formats(self):
        return self.exports.values_list('file_format', flat=True)

    @extraction_formats.setter
    def extraction_formats(self, value):
        new_formats = frozenset(value)
        previous_formats = self.exports.values_list('file_format', flat=True)
        assert new_formats.issuperset(previous_formats)
        self._new_formats = new_formats  # Will be collected and cleaned up by attach_new_formats.
        if self.id is not None:
            attach_new_formats(self.__class__, instance=self)

    @property
    def process_due_time(self):
        from django.conf import settings  # import locally, so migrations can't depend on settings
        return self.process_start_time + settings.OSMAXX.get('EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA')

    def set_status_from_conversion_progress(self, job_overall_progress):
        if self.state not in [ExtractionOrderState.FINISHED, ExtractionOrderState.FAILED]:
            self.state = get_order_status_from_conversion_progress(job_overall_progress)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('excerptexport:export_list')

    def send_email_if_all_exports_done(self, incoming_request):
        if all(export.is_status_final for export in self.exports.all()):
            from osmaxx.utilities.shortcuts import Emissary
            emissary = Emissary(recipient=self.orderer)
            emissary.inform_mail(
                subject=self._get_all_exports_done_email_subject(),
                mail_body=self._get_all_exports_done_mail_body(incoming_request)
            )

    def _get_all_exports_done_email_subject(self):
        view_context = dict(
            extraction_order=self,
            successful_exports_count=self.exports.filter(output_file__isnull=False).count(),
            failed_exports_count=self.exports.filter(output_file__isnull=True).count(),
        )
        return render_to_string(
            'excerptexport/email/all_exports_of_extraction_order_done_subject.txt',
            context=view_context,
        ).strip()

    def _get_all_exports_done_mail_body(self, incoming_request):
        view_context = dict(
            extraction_order=self,
            successful_exports=self.exports.filter(output_file__isnull=False),
            failed_exports=self.exports.filter(output_file__isnull=True),
            request=incoming_request,
        )
        return render_to_string(
            'excerptexport/email/all_exports_of_extraction_order_done_body.txt',
            context=view_context,
        ).strip()


@receiver(post_save, sender=ExtractionOrder)
def attach_new_formats(sender, instance, **kwargs):
    if hasattr(instance, '_new_formats'):
        for format in instance._new_formats:
            instance.exports.get_or_create(file_format=format)
        del instance._new_formats
