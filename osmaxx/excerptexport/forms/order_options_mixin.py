from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.layout import Fieldset


# TODO: fetch from API
available_format_choices = (
    ('fgdb', _('ESRI File Geodatabase (FileGDB)')),
    ('shp', _('ESRI Shapefile (shp)')),
    ('gpkg', _('GeoPackage (gpkg)')),
    ('spatialite', _('SQLite based SpatiaLite (spatialite)')),
    ('garmin', _('Garmin navigation & map data (img, tdb)')),
)


def get_export_options():
    return {
        'gis_options': {
            "coordinate_reference_system": "4326",
            "detail_level": 1,
        },
    }


class OrderOptionsMixin(forms.Form):
    formats = forms.MultipleChoiceField(
        label=_("GIS export formats"),
        choices=available_format_choices,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def clean(self):
        # only needed so check is actually run by inherited class
        data = super().clean()
        return data

    def form_layout(self):
        return Fieldset(
            _('Extraction options'),
            'formats',
        )
