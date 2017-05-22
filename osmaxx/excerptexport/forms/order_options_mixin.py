from crispy_forms.layout import Fieldset, Div
from django import forms
from django.utils.translation import ugettext_lazy as _

from osmaxx.conversion import output_format
from osmaxx.conversion.converters.converter_gis.detail_levels import DETAIL_LEVEL_CHOICES
from osmaxx.conversion import coordinate_reference_systems as crs


class OrderOptionsMixin(forms.Form):
    formats = forms.MultipleChoiceField(
        label=_("GIS export formats"),
        choices=output_format.CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    coordinate_reference_system = forms.ChoiceField(
        label=_('Coordinate system'),
        choices=crs.CHOICES,
        required=True,
    )
    detail_level = forms.ChoiceField(
        label=_('Detail level'),
        choices=DETAIL_LEVEL_CHOICES,
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
                    _('GIS options (ignored for Garmin and PBF)'),
                    'coordinate_reference_system',
                    'detail_level',
                ),
                css_class="col-md-6",
            ),
            css_class="row",
        )
