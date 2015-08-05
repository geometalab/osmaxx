from django.utils.translation import ugettext_lazy as _
import os
import uuid

from django.db import models

from .extraction_order import ExtractionOrder
from osmaxx.excerptexport.utils.upload_to import get_private_upload_storage


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64, verbose_name=_('mime type'))
    file = models.FileField(storage=get_private_upload_storage(), blank=True, null=True,
                            verbose_name=_('file'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    deleted_on_filesystem = models.BooleanField(default=False, verbose_name=_('deleted on filesystem'))
    public_identifier = models.UUIDField(primary_key=False, default=uuid.uuid4, verbose_name=_('public identifier'))

    extraction_order = models.ForeignKey(ExtractionOrder, related_name='output_files',
                                         verbose_name=_('extraction order'))

    def __str__(self):
        return \
            '[' + str(self.id) + '] ' \
            + ('file: ' + os.path.basename(self.file.name) + ', ' if (self.file and self.file.name) else '') \
            + 'identifier: ' + str(self.public_identifier)
