from django.core.files.storage import FileSystemStorage

from osmaxx.countries._settings import POLYFILE_LOCATION


class CountryInternalStorage(FileSystemStorage):
    """
    country storage which doesn't expose files to the outside world.

    Shouldn't be used outside the country module.

    It saves all data to a `data` subdirectory in the country module.
    """
    def __init__(self, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        super().__init__(
            location=POLYFILE_LOCATION,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode
        )
