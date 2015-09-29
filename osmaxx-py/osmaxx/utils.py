import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class PrivateSystemStorage(FileSystemStorage):
    """
    Exended Standard filesystem storage
    """
    def __init__(self, location=None, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        super().__init__(location, base_url, file_permissions_mode, directory_permissions_mode)

        # create the base dir, if it doesn't exist, fails with an exception when missing the rights to do so
        if not os.path.exists(self.location):
            os.makedirs(self.location)


private_storage = PrivateSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)
