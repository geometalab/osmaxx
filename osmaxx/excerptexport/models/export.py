import logging
import os
import shutil

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse

from osmaxx.conversion import output_format, status
from osmaxx.excerptexport._settings import (
    RESULT_FILE_AVAILABILITY_DURATION,
    EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA,
)

logger = logging.getLogger(__name__)


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(
        _("created at"), default=timezone.now, blank=True, editable=False
    )
    updated_at = models.DateTimeField(
        _("updated at"), default=None, blank=True, editable=False, null=True
    )

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

    extraction_order = models.ForeignKey(
        "excerptexport.ExtractionOrder",
        related_name="exports",
        verbose_name=_("extraction order"),
        on_delete=models.CASCADE,
    )
    file_format = models.CharField(
        choices=output_format.CHOICES,
        verbose_name=_("file format / data format"),
        max_length=10,
    )
    conversion_service_job_id = models.IntegerField(
        verbose_name=_("conversion service job ID"), null=True
    )
    status = models.CharField(
        _("job status"), choices=status.CHOICES, default=None, max_length=20, null=True
    )
    finished_at = models.DateTimeField(
        _("finished at"), default=None, blank=True, editable=False, null=True
    )

    def delete(self, *args, **kwargs):
        if hasattr(self, "output_file"):
            self.output_file.delete()
        super().delete(*args, **kwargs)

    def send_to_conversion_service(self, clipping_area_json, incoming_request):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient

        api_client = ConversionApiClient()
        extraction_format = self.file_format
        out_srs = self.extraction_order.coordinate_reference_system
        detail_level = self.extraction_order.detail_level
        parametrization_json = api_client.create_parametrization(
            boundary=clipping_area_json,
            out_format=extraction_format,
            detail_level=detail_level,
            out_srs=out_srs,
        )
        job_json = api_client.create_job(
            parametrization_json,
            self.get_full_status_update_uri(incoming_request),
            user=self.extraction_order.orderer,
        )
        self.conversion_service_job_id = job_json["id"]
        self.status = job_json["status"]
        self.save()
        return job_json

    def get_full_status_update_uri(self, request):
        return request.build_absolute_uri(self.status_update_url)

    @property
    def status_update_url(self):
        return reverse("job_progress:tracker", kwargs=dict(export_id=self.id))

    def set_and_handle_new_status(self, new_status, *, incoming_request):
        assert new_status in dict(status.CHOICES) or new_status is None
        if self.status == new_status and self.update_is_overdue:
            new_status = status.FAILED

        if self.status != new_status:
            self.status = new_status
            self.save()
            self._handle_changed_status(incoming_request=incoming_request)

    @property
    def update_is_overdue(self):
        if self.is_status_final:
            return False
        return (
            self.updated_at + EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA
        ) < timezone.now()

    def _handle_changed_status(self, *, incoming_request):
        from osmaxx.utils.shortcuts import Emissary

        emissary = Emissary(recipient=self.extraction_order.orderer)
        status_changed_message = self._get_export_status_changed_message()
        if self.status == status.FAILED:
            emissary.error(status_changed_message)
        elif self.status == status.FINISHED:
            from osmaxx.api_client.conversion_api_client import (
                ResultFileNotAvailableError,
            )

            try:
                self._fetch_result_file()
                emissary.success(status_changed_message)
            except ResultFileNotAvailableError as e:
                print(e)
                logger.error(
                    self._get_job_finished_but_result_file_missing_log_message()
                )
                emissary.warn(
                    _("{} But the result file is not available.").format(
                        status_changed_message
                    )
                )
        else:
            emissary.info(status_changed_message)
        self.extraction_order.send_email_if_all_exports_done(incoming_request)

    def _get_export_status_changed_message(self):
        from django.template.loader import render_to_string

        view_context = dict(export=self)
        return render_to_string(
            "job_progress/messages/export_status_changed.unsave_text",
            context=view_context,
        ).strip()

    def _get_job_finished_but_result_file_missing_log_message(self):
        return "Export {export_id}: Job {job_id} finished_at, but file not available.".format(
            export_id=self.id,
            job_id=self.conversion_service_job_id,
        )

    def _fetch_result_file(self):
        from osmaxx.api_client import ConversionApiClient
        from . import OutputFile
        from osmaxx.excerptexport.models.output_file import uuid_directory_path

        api_client = ConversionApiClient()
        file_path = api_client.get_result_file_path(self.conversion_service_job_id)
        now = timezone.now()
        of = OutputFile.objects.create(
            export=self,
            mime_type="application/zip",
        )
        new_file_name = uuid_directory_path(of, file_path)
        new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

        of.file.name = new_file_name

        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        shutil.move(file_path, new_file_path)
        of.file_removal_at = now + RESULT_FILE_AVAILABILITY_DURATION
        of.save()

        self.finished_at = now
        self.save()

    @property
    def result_file_available_until(self):
        if hasattr(self, "output_file"):
            return self.output_file.file_removal_at
        return None

    @property
    def is_status_final(self):
        return self.status in status.FINAL_STATUSES

    @property
    def can_be_deleted(self):
        return not self.is_running

    @property
    def is_running(self):
        if self.update_is_overdue:
            now = timezone.now()
            self.status = status.FAILED
            self.finished_at = now
            self.save()
        return not self.is_status_final

    @property
    def css_status_class(self):
        """
        based on the status, returns the bootstrap 3 class

        Returns: the bootstrap css class
        """
        default_class = "default"

        status_map = {
            status.RECEIVED: "info",
            status.QUEUED: "info",
            status.FINISHED: "success",
            status.FAILED: "danger",
            status.STARTED: "info",
            status.DEFERRED: "default",
        }
        return status_map.get(self.status, default_class)
