import logging

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from osmaxx.conversion import output_format, status
from osmaxx.excerptexport.excerpt_settings import (
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
    status = models.CharField(
        _("job status"),
        choices=status.CHOICES,
        default=status.RECEIVED,
        max_length=20,
        null=True,
    )
    estimated_pbf_size = models.FloatField(_("estimated pbf size in bytes"), null=True)
    unzipped_result_size = models.FloatField(
        _("file size in bytes"),
        null=True,
        help_text=_("without the static files, only the conversion result"),
    )
    extraction_duration = models.DurationField(
        _("extraction duration"),
        help_text=_("time needed to generate the extraction"),
        null=True,
    )
    finished_at = models.DateTimeField(
        _("finished at"), default=None, blank=True, editable=False, null=True
    )

    def delete(self, *args, **kwargs):
        if hasattr(self, "output_file"):
            self.output_file.delete()
        super().delete(*args, **kwargs)

    @property
    def update_is_overdue(self):
        if self.is_status_final:
            return False
        return (
            self.updated_at + EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA
        ) < timezone.now()

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

    def create_filename_base(self):
        now = timezone.now()
        basename = slugify(self.extraction_order.excerpt_name)
        srs = slugify(self.extraction_order.get_coordinate_reference_system_display())
        date = now.strftime("%Y-%m-%d")
        out_format = self.file_format
        detail_level = slugify(self.extraction_order.get_detail_level_display())
        return f"{basename}_{srs}_{date}_{out_format}_{detail_level}"
