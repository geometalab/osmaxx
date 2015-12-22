from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.layout import Fieldset


# TODO: fetch from API
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


class OrderOptionsMixin(forms.Form):
    formats = forms.MultipleChoiceField(
        label=_("GIS export formats:"),
        choices=available_format_choices,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def form_layout(self):
        return Fieldset(
            _('GIS export formats'),
            'formats',
        )
