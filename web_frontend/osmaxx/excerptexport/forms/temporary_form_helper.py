from django.utils.translation import gettext as _

# TODO: get these from the conversion_api
available_format_choices = (
    ('fgdb', _('fgdb')),
    ('shp', _('shp')),
    ('gpkg', _('gpkg')),
    ('spatialite', _('spatialite')),
    ('garmin', _('garmin')),
)


def get_export_options(selected_options):
    return {
        'gis_options': {
            "coordinate_reference_system": "WGS_84",
            "detail_level": 1,
        },
        'gis_formats': [option.split('.')[-1] for option in selected_options],
    }
