from django.utils.translation import ugettext as _

from osmaxx.conversion.converters.converter_gis.layers import OUTPUT_LAYER_NAMES

DETAIL_LEVEL_ALL = 120
DETAIL_LEVEL_REDUCED = 60

DETAIL_LEVEL_CHOICES = (
    (DETAIL_LEVEL_ALL, _('Full detail')),
    (DETAIL_LEVEL_REDUCED, _('Simplified')),
)

DETAIL_LEVEL_TABLES = {
    DETAIL_LEVEL_ALL: dict(
        included_layers=OUTPUT_LAYER_NAMES,
        level_folder_name=None,
    ),
    DETAIL_LEVEL_REDUCED: dict(
        included_layers=[
            'adminarea_a', 'boundary_l', 'geoname_l', 'geoname_p', 'landuse_a', 'military_a', 'military_p', 'misc_l',
            'natural_a', 'natural_p', 'poi_p', 'pow_p', 'railway_l', 'road_l', 'route_l', 'utility_p', 'water_a',
            'water_p', 'water_l', 'transport_l', 'coastline_l', 'landmass_a', 'sea_a',
        ],
        level_folder_name='level-{}'.format(str(DETAIL_LEVEL_REDUCED)),
    ),
}

assert set(DETAIL_LEVEL_TABLES[DETAIL_LEVEL_REDUCED]).issubset(DETAIL_LEVEL_TABLES[DETAIL_LEVEL_ALL])
