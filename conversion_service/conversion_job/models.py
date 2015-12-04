import os

import django_rq
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse

from converters import CONVERTER_CHOICES, converter_settings
from converters.boundaries import BBox
from converters.converter import Options
from countries.models import Country
from shared import JobStatus, ConversionProgress, rq_job_status_mapping
from utils.directory_helper import get_file_only_path_list_in_directory


class Extent(models.Model):
    west = models.FloatField(_('west'), null=True, blank=True)
    south = models.FloatField(_('south'), null=True, blank=True)
    east = models.FloatField(_('east'), null=True, blank=True)
    north = models.FloatField(_('north'), null=True, blank=True)
    polyfile = models.FileField(_('polyfile (deprecated)'), null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=_('country'), null=True, blank=True)

    def clean(self, exclude=None, validate_unique=True):
        if self._bbox_partially_present() and not self._bbox_present():
            raise ValidationError(_('incomplete bounding box boundaries'))
        if not(self._bbox_present() ^ self._polyfile_present()):
            raise ValidationError(_('either extents or polyfile must be given'))

    def _bbox_partially_present(self):
        return any([coordinate is not None for coordinate in self._bbox_coordinates])

    def _bbox_present(self):
        return all([coordinate is not None for coordinate in self._bbox_coordinates])

    def _polyfile_present(self):
        return bool(self.polyfile)

    def _country_present(self):
        return self.country is not None

    def get_geometry(self):
        if self._polyfile_present():
            raise NotImplementedError('Polyfile is not supported (yet).')
        if self._bbox_present():
            return BBox(*self._bbox_coordinates)
        raise RuntimeError("Should never reach this point.")  # pragma: no cover

    @property
    def _bbox_coordinates(self):
        return self.west, self.south, self.east, self.north

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class GISOption(models.Model):
    WGS_84 = 'WGS_84'
    CRS_CHOICES = (
        (WGS_84, _('WGS 84')),
    )
    DETAIL_LEVEL_VERBATIM = 1
    DETAIL_LEVEL_SIMPLIFIED = 2
    DETAIL_LEVEL_COMBINED = 3
    DETAIL_LEVELS = (
        (DETAIL_LEVEL_VERBATIM, _('verbatim')),
        (DETAIL_LEVEL_SIMPLIFIED, _('simplified')),
        (DETAIL_LEVEL_COMBINED, _('combined')),
    )
    coordinate_reference_system = models.CharField(_('coordinate reference system'), max_length=100, choices=CRS_CHOICES)
    detail_level = models.IntegerField(_('detail level'), choices=DETAIL_LEVELS)


class ConversionJob(models.Model):
    rq_job_id = models.CharField(_('rq job id'), max_length=250)
    callback_url = models.URLField(_('callback url'), max_length=250)
    status = models.CharField(_('job status'), choices=JobStatus.choices(), default=JobStatus.NEW.technical_representation, max_length=20)
    extent = models.OneToOneField(Extent, verbose_name=_('Extent'))
    gis_options = models.OneToOneField(GISOption, verbose_name=_('conversion job'), null=True)

    @property
    def output_directory(self):
        """
        Only available on saved model instances.
        """
        assert self.id is not None
        # todo: ensure job is cleaned up after files have been requested -> in conversion_service
        directory = os.path.join(converter_settings.OSMAXX_CONVERSION_SERVICE['RESULT_DIR'], str(self.id))
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def get_resulting_file_path_or_none(self, format):
        """
        :param format: format of the file
        :return: path to result file
        """
        file_paths = get_file_only_path_list_in_directory(self.output_directory)
        if not file_paths:
            return None

        file_path = [path for path in file_paths if path.split('.zip')[:-1][0].endswith(format)]
        if not file_path:
            return None
        return file_path[0]

    def get_conversion_options(self):
        return Options(output_formats=self.gis_formats.values_list('format', flat=True))

    def update_status_from_rq(self):
        rq_job = django_rq.get_queue().fetch_job(job_id=self.rq_job_id)

        # only do work if the job is not yet deleted
        if rq_job:
            self.status = rq_job_status_mapping[rq_job.status].technical_representation

            progress = rq_job.meta.get('progress', None)
            if progress:
                progress_state = progress.technical_representation
                for gis_format in self.gis_formats.all():
                    gis_format.progress = progress_state
                    gis_format.save()
            self.save()

    @property
    def progress(self):
        progresses_of_formats = [
            ConversionProgress(progress) for progress in self.gis_formats.values_list('progress', flat=True)
        ]
        overall_progress = ConversionProgress.most_significant(progresses_of_formats)
        if overall_progress is not None:
            overall_progress = overall_progress.technical_representation
        return overall_progress


class GISFormat(models.Model):
    conversion_job = models.ForeignKey(ConversionJob, verbose_name=_('conversion job'), related_name='gis_formats')
    format = models.CharField(_('format'), choices=CONVERTER_CHOICES['output_formats'], max_length=10)
    progress = models.CharField(
        _('progress'),
        choices=ConversionProgress.choices(),
        default=ConversionProgress.NEW.technical_representation,
        max_length=20,
    )

    def get_result_file_path(self):
        return self.conversion_job.get_resulting_file_path_or_none(self.format)

    def get_download_url(self, request):
        return reverse('gisformat-download-result', kwargs={'pk': self.id}, request=request)

    class Meta:
        unique_together = ('conversion_job', 'format',)
