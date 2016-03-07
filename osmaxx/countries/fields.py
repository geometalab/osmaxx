from django.db import models

from .storage import CountryInternalStorage


class InternalCountryFileField(models.FileField):
    """
    Makes use of the internal CountryInternalStorage.
    """

    def __init__(self, verbose_name=None, name=None, upload_to='', **kwargs):
        if 'storage' in kwargs:  # remove storage from kwargs, since we override it
            kwargs.pop('storage')

        storage = CountryInternalStorage()
        super().__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=storage, **kwargs)
