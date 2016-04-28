from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.layout import Fieldset

from osmaxx.conversion_api.formats import FORMAT_CHOICES


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
        choices=FORMAT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def form_layout(self):
        return Fieldset(
            _('Extraction options'),
            'formats',
        )
