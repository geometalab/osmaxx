from django.utils.translation import gettext_lazy as _

GEOMETRY_BBOX = 'bbox'
GEOMETRY_POLYGON_FILE = 'polyfile'


GEOMETRY_TYPES = (
    (GEOMETRY_BBOX, _('Bounding Box')),
    (GEOMETRY_POLYGON_FILE, _('Polygon File')),
)