from django.db import models
from django.utils.translation import ugettext_lazy as _

from osmaxx.conversion_api.formats import FORMAT_CHOICES


class Export(models.Model):
    """
    Frontend-side representation of both, a export procedure in progress (or concluded) *and* the result of exporting.

    Each ``Export`` instance corresponds to a specific, individual ``job`` sent to the conversion service and thus
    encompasses

    - the spatial selection ('clipping' or 'extraction') of the input data within one perimeter
      (``extraction_order.excerpt`` or ``extraction_order.country_id`)
    - the transformation of the data from the data sources' schemata (e.g. ``osm2pgsql`` schema) to the OSMaxx schema
    - the actual export to one specific GIS or navigation file format with one specific set of parameters
    """
    extraction_order = models.ForeignKey('ExtractionOrder', related_name='exports',
                                         verbose_name=_('extraction order'))
    file_format = models.TextField(choices=FORMAT_CHOICES)
