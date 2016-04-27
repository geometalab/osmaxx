import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from osmaxx.excerptexport.models.export import Export
from osmaxx.excerptexport.utils.upload_to import get_private_upload_storage


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64, verbose_name=_('mime type'))
    content_type = models.CharField(max_length=64, verbose_name=_('content type'), default='')
    file = models.FileField(storage=get_private_upload_storage(), blank=True, null=True,
                            verbose_name=_('file'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    deleted_on_filesystem = models.BooleanField(default=False, verbose_name=_('deleted on filesystem'))
    public_identifier = models.UUIDField(primary_key=False, default=uuid.uuid4, verbose_name=_('public identifier'))
    export = models.OneToOneField(Export, related_name='output_file', verbose_name=_('export'))

    @property
    def download_file_name(self):
        return settings.OSMAXX['download_file_name'] % {
            'id': str(self.public_identifier),
            'name': os.path.basename(self.file.name) if self.file else None,
            'date': self.creation_date.strftime("%F"),
            'excerpt_name': self.export.extraction_order.excerpt_name.replace(" ", ""),
            'content_type': self.content_type if self.content_type else 'file',
            'file_extension': self.file_extension
        }

    @property
    def file_extension(self):
        return self.export.file_format

    def __str__(self):
        return \
            '[' + str(self.id) + '] ' \
            + ('file: ' + os.path.basename(self.file.name) + ', ' if (self.file and self.file.name) else '') \
            + 'identifier: ' + str(self.public_identifier)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('excerptexport:download', kwargs=dict(uuid=self.public_identifier))
