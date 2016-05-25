import os
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from osmaxx.excerptexport.models.export import Export


def uuid_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/osmaxx/<public_uuid>/<filename>
    return os.path.join('osmaxx', 'outputfiles', str(instance.public_identifier), filename)


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64, verbose_name=_('mime type'))
    file_extension = models.CharField(max_length=64, verbose_name=_('file extension'), default='')
    file = models.FileField(blank=True, null=True, verbose_name=_('file'), upload_to=uuid_directory_path,
                            max_length=250)
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
    def content_type(self):
        return self.export.file_format

    def __str__(self):
        return \
            '[' + str(self.id) + '] ' \
            + ('file: ' + os.path.basename(self.file.name) + ', ' if (self.file and self.file.name) else '') \
            + 'identifier: ' + str(self.public_identifier)

    def get_filename_display(self):
        if self.file:
            return os.path.basename(self.file.name)
        return ''

    def get_file_media_url_or_status_page(self):
        if self.file:
            return self.file.url
        from django.core.urlresolvers import reverse
        return reverse('excerptexport:export_detail', kwargs={'id': self.export.extraction_order.excerpt.id})
