from django.utils.translation import gettext_lazy as _

# most common reference systems

WGS_84 = 4326
WGS_72 = 4322
PSEUDO_MERCATOR = 3857
NAD_83 = 4269
OSGB_36 = 4277

CHOICES = (
    (WGS_84, _('WGS 84')),
    (PSEUDO_MERCATOR, _('Pseudo-Mercator')),
    (WGS_72, _('WGS 72')),
    (NAD_83, _('NAD 83')),
    (OSGB_36, _('OSGB 36')),
)
