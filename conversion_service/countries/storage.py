import os

from django.core.files.storage import FileSystemStorage

polyfile_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'polyfiles')


class CountryModuleInternalStorage(FileSystemStorage):
    """
    CountryField storage which doesn't expose files to the outside world.

    It saves all data to a `data` subdirectory in the country module.
    """
    def __init__(self, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        location = polyfile_location
        super().__init__(
            location=location,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode
        )
