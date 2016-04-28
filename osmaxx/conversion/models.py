import os
import time

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from osmaxx.clipping_area.models import ClippingArea
from osmaxx.conversion.converters.converter import convert
from osmaxx.conversion_api.formats import FORMAT_CHOICES
from osmaxx.conversion_api.statuses import STATUS_CHOICES, RECEIVED


def job_directory_path(instance, filename):
    return 'job_result_files/{0}/{1}'.format(instance.id, filename)


class Parametrization(models.Model):
    out_format = models.CharField(verbose_name=_("out format"), choices=FORMAT_CHOICES, max_length=100)
    out_srs = models.IntegerField(verbose_name=_("output SRS"), help_text=_("EPSG code of the output spatial reference system"), null=True, blank=True, default=4326)  # noqa: linelength
    clipping_area = models.ForeignKey(ClippingArea, verbose_name=_('Clipping Area'))

    def __str__(self):
        return _("{}: {} as EPSG:{}").format(self.id, self.get_out_format_display(), self.out_srs)

    @property
    def epsg(self):
        return "EPSG:{}".format(self.out_srs)


class Job(models.Model):
    callback_url = models.URLField(_('callback url'), max_length=250)
    parametrization = models.ForeignKey(verbose_name=_('parametrization'), to=Parametrization)
    rq_job_id = models.CharField(_('rq job id'), max_length=250, null=True)
    status = models.CharField(_('job status'), choices=STATUS_CHOICES, default=RECEIVED, max_length=20)
    resulting_file = models.FileField(_('resulting file'), upload_to=job_directory_path, null=True)
    own_base_url = models.CharField(
        _('own base url'), help_text=_('the url from which this job is reachable'), max_length=250
    )

    def start_conversion(self, *, use_worker=True):
        self.rq_job_id = convert(
            conversion_format=self.parametrization.out_format,
            area_name=self.parametrization.clipping_area.name,
            osmosis_polygon_file_string=self.parametrization.clipping_area.osmosis_polygon_file_string,
            output_zip_file_path=self._out_zip_path(),
            filename_prefix=self._filename_prefix(),
            out_srs=self.parametrization.epsg,
            use_worker=use_worker,
        )
        self.save()

    def zip_file_relative_path(self):
        return job_directory_path(self, '{}.{}'.format(self._filename_prefix(), 'zip'))

    def get_download_url(self):
        if not self.resulting_file.name:
            return None
        base_uri = self.own_base_url
        if base_uri.endswith('/'):
            base_uri = base_uri[:-1]
        return base_uri + reverse('conversion_job-download-zip', kwargs={'pk': self.id})

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

    def _filename_prefix(self):
        return '{}-{}_{}'.format(
            time.strftime("%Y%m%d"),
            slugify(self.parametrization.clipping_area.name),
            self.parametrization.out_format
        )

    def delete(self, *args, **kwargs):
        if self.resulting_file.name:
            os.unlink(self.resulting_file.path)
        return super().delete(args, kwargs)

    def __str__(self):
        return _("job {} with rq_id {} ({})").format(self.id, self.rq_job_id, self.parametrization.clipping_area.name)
