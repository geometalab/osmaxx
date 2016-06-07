import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse

from osmaxx.conversion_api.formats import FORMAT_CHOICES

logger = logging.getLogger(__name__)


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(_('created at'), default=timezone.now, blank=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), default=None, blank=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.id is None:
            self.created_at = now
        self.updated_at = now
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Export(TimeStampModelMixin, models.Model):
    """
    Frontend-side representation of both, a export procedure in progress (or concluded) *and* the result of exporting.

    Each ``Export`` instance corresponds to a specific, individual ``job`` sent to the conversion service and thus
    encompasses

    - the spatial selection ('clipping' or 'extraction') of the input data within one perimeter
      (``extraction_order.excerpt``)
    - the transformation of the data from the data sources' schemata (e.g. ``osm2pgsql`` schema) to the OSMaxx schema
    - the actual export to one specific GIS or navigation file format with one specific set of parameters
    """
    from osmaxx.conversion_api.statuses import RECEIVED, QUEUED, FINISHED, FAILED, STARTED, DEFERRED, FINAL_STATUSES, STATUS_CHOICES  # noqa
    INITIAL = 'initial'
    INITIAL_CHOICE = (INITIAL, _('initial'))
    STATUS_CHOICES = (INITIAL_CHOICE,) + STATUS_CHOICES

    extraction_order = models.ForeignKey('excerptexport.ExtractionOrder', related_name='exports',
                                         verbose_name=_('extraction order'))
    file_format = models.CharField(choices=FORMAT_CHOICES, verbose_name=_('file format / data format'), max_length=10)
    conversion_service_job_id = models.IntegerField(verbose_name=_('conversion service job ID'), null=True)
    status = models.CharField(_('job status'), choices=STATUS_CHOICES, default=INITIAL, max_length=20)
    finished_at = models.DateTimeField(_('finished at'), default=None, blank=True, editable=False, null=True)

    def send_to_conversion_service(self, clipping_area_json, incoming_request):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        api_client = ConversionApiClient()
        extraction_format = self.file_format
        gis_options = self.extraction_order.extraction_configuration['gis_options']
        out_srs = gis_options['coordinate_reference_system']
        parametrization_json = api_client.create_parametrization(boundary=clipping_area_json, out_format=extraction_format, out_srs=out_srs)
        job_json = api_client.create_job(parametrization_json, self.get_full_status_update_uri(incoming_request))
        self.conversion_service_job_id = job_json['id']
        self.status = job_json['status']
        self.save()
        return job_json

    def get_full_status_update_uri(self, request):
        return request.build_absolute_uri(self.status_update_url)

    @property
    def status_update_url(self):
        return reverse('job_progress:tracker', kwargs=dict(export_id=self.id))

    def set_and_handle_new_status(self, new_status, *, incoming_request):
        assert new_status in dict(self.STATUS_CHOICES)
        if self.status != new_status:
            self.status = new_status
            self.save()
            self._handle_changed_status(incoming_request=incoming_request)

    def _handle_changed_status(self, *, incoming_request):
        from osmaxx.utilities.shortcuts import Emissary
        emissary = Emissary(recipient=self.extraction_order.orderer)
        status_changed_message = self._get_export_status_changed_message()
        if self.status == self.FAILED:
            emissary.error(status_changed_message)
        elif self.status == self.FINISHED:
            from osmaxx.api_client.conversion_api_client import ResultFileNotAvailableError
            try:
                self._fetch_result_file()
                emissary.success(status_changed_message)
            except ResultFileNotAvailableError:
                logger.error(self._get_job_finished_but_result_file_missing_log_message())
                emissary.warn(_("{} But the result file is not available.").format(status_changed_message))
        else:
            emissary.info(status_changed_message)
        self.extraction_order.send_email_if_all_exports_done(incoming_request)

    def _get_export_status_changed_message(self):
        from django.template.loader import render_to_string
        view_context = dict(export=self)
        return render_to_string(
            'job_progress/messages/export_status_changed.unsave_text',
            context=view_context,
        ).strip()

    def _get_job_finished_but_result_file_missing_log_message(self):
        return 'Export {export_id}: Job {job_id} finished_at, but file not available.'.format(
            export_id=self.id,
            job_id=self.conversion_service_job_id,
        )

    def _fetch_result_file(self):
        from osmaxx.api_client import ConversionApiClient
        from . import OutputFile
        api_client = ConversionApiClient()
        file_content = api_client.get_result_file(self.conversion_service_job_id)
        now = timezone.now()
        of = OutputFile.objects.create(
            export=self,
            mime_type='application/zip',
            file_extension='zip',
        )
        of.file.save(
            of.download_file_name,
            file_content,
        )
        self.finished_at = now
        self.save()

    @property
    def is_status_final(self):
        return self.status in self.FINAL_STATUSES

    @property
    def css_status_class(self):
        """
        based on the status, returns the bootstrap 3 class

        Returns: the bootstrap css class
        """
        default_class = 'default'

        status_map = {
            self.RECEIVED: 'info',
            self.QUEUED: 'info',
            self.FINISHED: 'success',
            self.FAILED: 'danger',
            self.STARTED: 'info',
            self.DEFERRED: 'default',
        }
        return status_map.get(self.status, default_class)
