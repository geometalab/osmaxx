import os
import time

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from osmaxx.conversion import output_format, status
from osmaxx.clipping_area.models import ClippingArea
from osmaxx.conversion.converters.converter import convert
from osmaxx.conversion.converters.converter_gis.detail_levels import DETAIL_LEVEL_CHOICES, DETAIL_LEVEL_ALL
from osmaxx.conversion import coordinate_reference_system as crs


def job_directory_path(instance, filename):
    return 'job_result_files/{0}/{1}'.format(instance.id, filename)


class Parametrization(models.Model):
    out_format = models.CharField(verbose_name=_("out format"), choices=output_format.CHOICES, max_length=100)
    out_srs = models.IntegerField(
        verbose_name=_("output SRS"), help_text=_("EPSG code of the output spatial reference system"),
        null=True, blank=True, default=4326, choices=crs.CHOICES
    )
    clipping_area = models.ForeignKey(ClippingArea, verbose_name=_('Clipping Area'), on_delete=models.CASCADE)
    detail_level = models.IntegerField(verbose_name=_('detail level'), choices=DETAIL_LEVEL_CHOICES, default=DETAIL_LEVEL_ALL)

    def __str__(self):
        return _("{}: {} as EPSG:{}").format(self.id, self.get_out_format_display(), self.out_srs)

    @property
    def epsg(self):
        return "EPSG:{}".format(self.out_srs)


class Job(models.Model):
    callback_url = models.URLField(_('callback url'), max_length=250)
    parametrization = models.ForeignKey(verbose_name=_('parametrization'), to=Parametrization, on_delete=models.CASCADE)
    rq_job_id = models.CharField(_('rq job id'), max_length=250, null=True)
    status = models.CharField(_('job status'), choices=status.CHOICES, default=status.RECEIVED, max_length=20)
    resulting_file = models.FileField(_('resulting file'), upload_to=job_directory_path, null=True, max_length=250)
    estimated_pbf_size = models.FloatField(_('estimated pbf size in bytes'), null=True)
    unzipped_result_size = models.FloatField(
        _('file size in bytes'), null=True, help_text=_("without the static files, only the conversion result")
    )
    extraction_duration = models.DurationField(
        _('extraction duration'), help_text=_('time needed to generate the extraction'), null=True
    )
    own_base_url = models.CharField(
        _('own base url'), help_text=_('the url from which this job is reachable'), max_length=250
    )
    queue_name = models.CharField(
        _('queue name'), help_text=_('queue name for processing'), default='default',
        max_length=50, choices=[(key, key) for key in settings.RQ_QUEUE_NAMES]
    )

    def start_conversion(self, *, use_worker=True):
        self.rq_job_id = convert(
            conversion_format=self.parametrization.out_format,
            area_name=self.parametrization.clipping_area.name,
            osmosis_polygon_file_string=self.parametrization.clipping_area.osmosis_polygon_file_string,
            output_zip_file_path=self._out_zip_path(),
            filename_prefix=self._filename_prefix(),
            detail_level=self.parametrization.detail_level,
            out_srs=self.parametrization.epsg,
            use_worker=use_worker,
            queue_name=self.queue_name,
        )
        self.save()

    def zip_file_relative_path(self):
        return job_directory_path(self, '{}.{}'.format(self._filename_prefix(), 'zip'))

    def get_absolute_url(self):
        base_uri = self.own_base_url
        if base_uri.endswith('/'):
            base_uri = base_uri[:-1]
        return base_uri + reverse('conversion_job-detail', kwargs={'pk': self.id})

    def _out_zip_path(self):
        # assure path exists
        complete_zip_file_path = os.path.join(
            settings.MEDIA_ROOT, self.zip_file_relative_path()
        )
        os.makedirs(os.path.dirname(complete_zip_file_path), exist_ok=True)
        return complete_zip_file_path

    @property
    def get_absolute_file_path(self):
        if self.has_file:
            return self.resulting_file.path
        return None

    def _filename_prefix(self):
        return '{basename}_{srs}_{date}_{out_format}_{detail_level}'.format(
            basename=slugify(self.parametrization.clipping_area.name),
            srs=slugify(self.parametrization.get_out_srs_display()),
            date=time.strftime("%Y-%m-%d"),
            out_format=self.parametrization.out_format,
            detail_level=slugify(self.parametrization.get_detail_level_display()),
        )

    @property
    def has_file(self):
        return bool(self.resulting_file)

    def delete(self, *args, **kwargs):
        if self.has_file:
            os.unlink(self.resulting_file.path)
        return super().delete(args, kwargs)

    def __str__(self):
        return _("job {} with rq_id {} ({})").format(self.id, self.rq_job_id, self.parametrization.clipping_area.name)
