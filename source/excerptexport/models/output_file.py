import os
import uuid

from django.db import models

from excerptexport import settings

from .extraction_order import ExtractionOrder


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64)
    file = models.FileField(upload_to=settings.APPLICATION_SETTINGS['data_directory'], blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    deleted_on_filesystem = models.BooleanField(default=False)
    public_identifier = models.CharField(max_length=512, default=uuid.uuid4())

    extraction_order = models.ForeignKey(ExtractionOrder, related_name='output_files')

    def __str__(self):
        return \
            '[' + str(self.id) + '] ' \
            + ('file: ' + os.path.basename(self.file.name) + ', ' if (self.file and self.file.name) else '') \
            + 'identifier: ' + self.public_identifier




