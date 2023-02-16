import os
import shutil
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from osmaxx.excerptexport.models.export import Export


def uuid_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/osmaxx/<public_uuid>/<filename>
    return os.path.join(
        "osmaxx",
        "outputfiles",
        str(instance.public_identifier),
        os.path.basename(filename),
    )


class OutputFile(models.Model):
    mime_type = models.CharField(max_length=64, verbose_name=_("mime type"))
    file = models.FileField(
        blank=True,
        null=True,
        verbose_name=_("file"),
        upload_to=uuid_directory_path,
        max_length=250,
    )
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("create date")
    )
    deleted_on_filesystem = models.BooleanField(
        default=False, verbose_name=_("deleted on filesystem")
    )
    public_identifier = models.UUIDField(
        primary_key=False, default=uuid.uuid4, verbose_name=_("public identifier")
    )
    export = models.OneToOneField(
        Export,
        related_name="output_file",
        verbose_name=_("export"),
        on_delete=models.CASCADE,
    )
    file_removal_at = models.DateTimeField(
        _("file removal date"), default=None, blank=True, editable=False, null=True
    )

    def __str__(self):
        fname = (
            os.path.basename(self.file.name) if (self.file and self.file.name) else ""
        )
        return (
            f"[{str(self.id)}] file: {fname}, identifier: {str(self.public_identifier)}"
        )

    def delete(self, *args, **kwargs):
        self._remove_file()
        super().delete(*args, **kwargs)

    @property
    def content_type(self):
        return self.export.file_format

    @property
    def file_extension(self):
        if self.has_file:
            _discarded, file_extension = os.path.splitext(self.file)
            return file_extension
        return "zip"

    @property
    def has_file(self):
        return bool(self.file)

    def _remove_file(self, save=False):
        if self.file:
            file_path = self.file.path
            file_directory = os.path.dirname(file_path)
            if os.path.exists(file_directory):
                assert len(os.listdir(file_directory)) <= 1
                shutil.rmtree(file_directory)
            self.file = None
        if save:
            self.save()

    def get_filename_display(self):
        if self.file:
            return os.path.basename(self.file.name)
        return ""

    def get_file_media_url_or_status_page(self):
        if self.file:
            return self.file.url
        from django.urls import reverse

        return reverse(
            "excerptexport:export_detail",
            kwargs={"id": self.export.extraction_order.excerpt.id},
        )
