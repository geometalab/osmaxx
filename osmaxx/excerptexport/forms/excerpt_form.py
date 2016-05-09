import json

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit

from .order_options_mixin import OrderOptionsMixin, get_export_options
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder
from osmaxx.utilities.dict_helpers import select_keys


class ExcerptForm(OrderOptionsMixin, forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
    )
    bounding_geometry = forms.CharField(
        label=_('Bounding Geometry (GeoJSON)'),
        required=True,
        widget=forms.Textarea(attrs={'rows': '10'}),
    )

    def __init__(self, *args, **kwargs):
        super(ExcerptForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_id = 'newExcerptForm'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('excerptexport:order_new_excerpt')

        self.helper.layout = Layout(
            Fieldset(
                _('Excerpt'),
                Field('name'),
                Field('bounding_geometry'),
                'is_public',
            ),
            OrderOptionsMixin(self).form_layout(),
            Submit('submit', 'Submit'),
        )

    def clean(self):
        clean = super().clean()
        if 'bounding_geometry' in self._errors:
            # need to add the hidden field validation error to a visible dom
            self.add_error(None, _('Area Invalid or none selected.'))
        return clean

    def clean_bounding_geometry(self):
        allowed_types = ['Polygon', 'Multipolygon']
        data = self.cleaned_data['bounding_geometry']
        data_dict = json.loads(data)
        if data_dict.get('type') not in allowed_types:
            raise ValidationError(_('Only {} are allowed as input.').format(allowed_types))
        if data_dict.get('type') == 'Polygon':
            data_dict['coordinates'] = [data_dict.get('coordinates')]
            data_dict['type'] = 'Multipolygon'
        return json.dumps(data_dict)

    class Meta:
        model = Excerpt
        fields = ['name', 'is_public', 'bounding_geometry']

    def save(self, user):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.extraction_configuration = get_export_options()
        extraction_order.extraction_formats = self.cleaned_data['formats']
        excerpt_dict = select_keys(self.cleaned_data, ['name', 'is_public', 'bounding_geometry'])
        excerpt = Excerpt(
            is_active=True,
            owner=user,
            **excerpt_dict
        )
        excerpt.save()
        extraction_order.excerpt = excerpt
        extraction_order.save()
        return extraction_order
