from django.db import models

from .extraction_order import ExtractionOrder


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64)
    path = models.CharField(max_length=512)
    create_date = models.DateTimeField('create date')
    deleted_on_filesystem = models.BooleanField(default=False)

    extraction_order = models.ForeignKey(ExtractionOrder, related_name='output_files')

    def __str__(self):
        return self.path