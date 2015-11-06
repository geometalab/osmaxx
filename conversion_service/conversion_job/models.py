from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from converters import CONVERTER_CHOICES
from converters.boundaries import BBox
from converters.converter import Options
from shared import JobStatus, ConversionProgress


class Extent(models.Model):
    west = models.FloatField(_('west'), null=True, blank=True)
    south = models.FloatField(_('south'), null=True, blank=True)
    east = models.FloatField(_('east'), null=True, blank=True)
    north = models.FloatField(_('north'), null=True, blank=True)
    polyfile = models.FileField(_('polyfile'), null=True, blank=True)

    def clean(self, exclude=None, validate_unique=True):
        if self._bbox_partially_present() and not self._bbox_present():
            raise ValidationError(_('incomplete bounding box boundaries'))
        if not(self._bbox_present() ^ self._polyfile_present()):
            raise ValidationError(_('either extents or polyfile must be given'))

    def _bbox_partially_present(self):
        return any([coordinate is not None for coordinate in [self.west, self.south, self.east, self.north]])

    def _bbox_present(self):
        return all([coordinate is not None for coordinate in [self.west, self.south, self.east, self.north]])

    def _polyfile_present(self):
        return bool(self.polyfile)

    def get_geometry(self):
        if self._polyfile_present():
            raise NotImplementedError('Polyfile is not supported (yet).')
        if self._bbox_present():
            return BBox(self.west, self.south, self.east, self.north)
        raise RuntimeError("Should never reach this point.")

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
    crs = models.CharField(_('coordinate reference system'), max_length=100, choices=CRS_CHOICES)
    detail_level = models.IntegerField(_('detail level'), choices=DETAIL_LEVELS)


class ConversionJob(models.Model):
    rq_job_id = models.CharField(_('rq job id'), max_length=250)
    callback_url = models.URLField(_('callback url'), max_length=250)
    status = models.IntegerField(_('job status'), choices=JobStatus.choices())
    extent = models.OneToOneField(Extent, verbose_name=_('Extent'))
    gis_option = models.OneToOneField(GISOption, verbose_name=_('conversion job'), null=True)

    def get_conversion_options(self):
        return Options(output_formats=self.converter_options.values_list('format'))

    @property
    def progress(self):
        return ConversionProgress(min(self.converter_options.values_list('progress')))


class GISFormat(models.Model):
    conversion_job = models.ForeignKey(ConversionJob, verbose_name=_('conversion job'), related_name='gis_formats')
    format = models.CharField(_('format'), choices=CONVERTER_CHOICES['output_formats'], max_length=10)

    class Meta:
        unique_together = ('conversion_job', 'format',)
