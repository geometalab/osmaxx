from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import InternalCountryFileField


class Country(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    polyfile = InternalCountryFileField(verbose_name=_('polyfile'))
    border = models.MultiPolygonField(verbose_name=_('border'), help_text=_('original border multipolygon'))
    simplified_border = models.MultiPolygonField(verbose_name=_('simplified border multipolygon'))

    @property
    def type_of_geometry(self):
        """
        Only needed for easier distinction on the javascript side, has no real value otherwise.

        Returns: a string ("Country")
        """
        return 'Country'

    def __str__(self):
        return self.name
