from django.utils.translation import ugettext_lazy as _

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, Submit, HTML

from osmaxx.excerptexport.models import Excerpt


class ExcerptForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        required=True,
    )
    north = forms.FloatField(
        label=_('North'),
        required=True,
    )
    west = forms.FloatField(
        label=_('West'),
        required=True,
    )
    east = forms.FloatField(
        label=_('East'),
        required=True,
    )
    south = forms.FloatField(
        label=_('South'),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ExcerptForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                _('Excerpt'),
                Field('name'), 'is_public',
            ),
            Fieldset(
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
            ),
            Submit('submit', 'Submit'),
        )

    class Meta:
        model = Excerpt
        fields = ['name', 'is_public']
