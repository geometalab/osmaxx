from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.layout import Fieldset, Div

from osmaxx.conversion_api import formats, coordinate_reference_systems as crs


class OrderOptionsMixin(forms.Form):
    formats = forms.MultipleChoiceField(
        label=_("GIS export formats"),
        choices=formats.FORMAT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    coordinate_reference_system = forms.ChoiceField(
        label=_('Coordinate system'),
        choices=crs.CRS_CHOICES,
        required=True,
    )

    def clean(self):
        # only needed so check is actually run by inherited class
        data = super().clean()
        return data

    def form_layout(self):
        return Div(
            Div(
                Fieldset(
                    _('Export options'),
                    'formats',

                ),
                css_class="col-md-6",
            ),
            Div(
                Fieldset(
                    _('GIS Options (ignored for garmin)'),
                    'coordinate_reference_system',
                ),
                css_class="col-md-6",
            ),
            css_class="row",
        )
