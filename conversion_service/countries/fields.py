from django.db import models

from countries.storage import CountryModuleInternalStorage


class InternalCountryFileField(models.FileField):
    """
    CountryField storage which doesn't expose files to the outside world.

    It saves all data to a `data` subdirectory in the country module.
    """

    def __init__(self, verbose_name=None, name=None, upload_to='', **kwargs):
        if 'storage' in kwargs:  # remove storage from kwargs, since we override it
            kwargs.pop('storage')

        storage = CountryModuleInternalStorage()
        super().__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=storage, **kwargs)
