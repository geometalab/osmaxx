from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit

from .order_options_mixin import OrderOptionsMixin, get_export_options
from .bbox_bounding_geometry_mixin import BBoxBoundingGeometryMixin
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, BBoxBoundingGeometry
from osmaxx.utilities.dict_helpers import select_keys


class ExcerptForm(BBoxBoundingGeometryMixin, OrderOptionsMixin, forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'}),
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
                Field('name'), 'is_public',
            ),
            BBoxBoundingGeometryMixin(self).form_layout(),
            OrderOptionsMixin(self).form_layout(),
            Submit('submit', 'Submit'),
        )

    class Meta:
        model = Excerpt
        fields = ['name', 'is_public']

    def save(self, user):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.extraction_configuration = get_export_options()
        extraction_order.extraction_formats = self.cleaned_data['formats']

        bbox_kwargs = select_keys(self.cleaned_data, ['north', 'east', 'south', 'west'])
        bounding_geometry = BBoxBoundingGeometry(**bbox_kwargs)
        bounding_geometry.save()

        excerpt_dict = select_keys(self.cleaned_data, ['name', 'is_public'])
        excerpt = Excerpt(
            is_active=True,
            bounding_geometry_old=bounding_geometry,
            owner=user,
            **excerpt_dict
        )
        excerpt.save()
        extraction_order.excerpt = excerpt
        extraction_order.save()
        return extraction_order
