from django.conf import settings

from django.core.files.storage import FileSystemStorage


class PrivateFileSystemStorage(FileSystemStorage):
    # This is a small hack to still be able to use the standard FileSystemStorage
    # without having the hardcoded PRIVATE_MEDIA_ROOT in automatic generated migrations.
    def __init__(self, *args, **kwargs):
        if 'location' not in kwargs:
            kwargs['location'] = settings.PRIVATE_MEDIA_ROOT
        super().__init__(*args, **kwargs)


def get_private_upload_storage():
    return PrivateFileSystemStorage()
