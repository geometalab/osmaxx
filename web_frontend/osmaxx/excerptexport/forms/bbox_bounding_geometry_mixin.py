from django.utils.translation import ugettext_lazy as _
from django import forms

from crispy_forms.layout import Fieldset, Div, Field, HTML


class BBoxBoundingGeometryMixin(forms.Form):
    north = forms.FloatField(
        label=_('North'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
    )
    west = forms.FloatField(
        label=_('West'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
    )
    east = forms.FloatField(
        label=_('East'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
    )
    south = forms.FloatField(
        label=_('South'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
    )

    def form_layout(self):
        return Fieldset(
            _('Bounding box'),
            Div(
                Field('north', wrapper_class='column-stretch-4'),
                css_class="box-column-container balanced",
            ),
            Div(
                Field('west', wrapper_class='column-stretch-4'),
                Field('east', wrapper_class='column-stretch-4'),
                css_class="box-column-container separated",
            ),
            Div(
                Field('south', wrapper_class='column-stretch-4'),
                css_class="box-column-container balanced",
            ),
            HTML(
                '<p id="bounding-box-error" class="error"></p>'
            )
        )
