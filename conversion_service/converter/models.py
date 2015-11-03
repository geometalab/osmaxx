from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from conversion_service.converters.boundaries import BBox
from conversion_service.shared import JobStatus, ConversionProgress


class Extent(models.Model):
    west = models.FloatField(_('west'), null=True, blank=True)
    south = models.FloatField(_('south'), null=True, blank=True)
    east = models.FloatField(_('east'), null=True, blank=True)
    north = models.FloatField(_('north'), null=True, blank=True)
    polyfile = models.FileField(_('polyfile'), null=True, blank=True)

    def clean(self, exclude=None, validate_unique=True):
        if (self.polyfile is not None) ^ all([self.west, self.south, self.east, self.north]):
            raise ValidationError(_('either extents ot polyfile must be given'))

    def get_geometry(self):
        if self.polyfile:
            raise NotImplementedError
        if all([self.west, self.south, self.east, self.north]):
            return BBox(self.west, self.south, self.east, self.north)
        else:
            raise RuntimeError("this really shouldn't be happening! Sorry, we f**ked up.")


class ConversionJob(models.Model):
    rq_job_id = models.CharField(_('rq job id'), max_length=250)
    callback_url = models.URLField(_('callback url'), max_length=250)
    status = models.IntegerField(_('job status'), choices=JobStatus.choices())

    @property
    def progress(self):
        return ConversionProgress(min(self.formats.values_list('progress')))


class Format(models.Model):
    progress = models.IntegerField(_('progress'), choices=ConversionProgress.choices())
    conversion_job = models.ForeignKey(ConversionJob, verbose_name=_('conversion job'), related_name='formats')
