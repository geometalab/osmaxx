from django.utils.translation import ugettext as _

from osmaxx.conversion.converters.converter_gis.sql_tables import VIEW_NAMES

DETAIL_LEVEL_ALL = 120
DETAIL_LEVEL_REDUCED = 60

DETAIL_LEVEL_CHOICES = (
    (DETAIL_LEVEL_ALL, _('Complete')),
    (DETAIL_LEVEL_REDUCED, _('Simplified')),
)

DETAIL_LEVEL_TABLES = {
    DETAIL_LEVEL_ALL: dict(
        tables=VIEW_NAMES,
        specialized_sql_file_ending=None,
    ),
    DETAIL_LEVEL_REDUCED: dict(
        tables=[
            'adminarea_a', 'boundary_l', 'geoname_l', 'geoname_p', 'landuse_a', 'military_a', 'military_p', 'misc_l',
            'natural_a', 'natural_p', 'poi_p', 'pow_p', 'railway_l', 'road_l', 'route_l', 'utility_p', 'water_a',
            'water_p', 'water_l', 'transport_l', 'coastline_l', 'landmass_a', 'ocean_a',
        ],
        specialized_sql_file_ending=str(DETAIL_LEVEL_REDUCED),
    ),
}
