from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from osmaxx.excerptexport.models import ExtractionOrder, Excerpt
from osmaxx.excerptexport.models.excerpt import private_user_excerpts, public_excerpts
from .order_options_mixin import OrderOptionsMixin


def get_country_choices():
    return [
        (excerpt['id'], excerpt['name'])
        for excerpt in Excerpt.objects
        .filter(excerpt_type=Excerpt.EXCERPT_TYPE_COUNTRY_BOUNDARY, is_public=True, is_active=True)
        .order_by('name')
        .values('id', 'name')
    ]


def get_existing_excerpt_choices(user):
    country_choices = get_country_choices()
    return (
        ('Personal excerpts ({username}) [{count}]'
            .format(username=user.username, count=private_user_excerpts(user).count()),
         tuple((excerpt['id'], excerpt['name']) for excerpt in private_user_excerpts(user).values('id', 'name'))
         ),
        ('Public excerpts [{count}]'.format(count=public_excerpts().count()),
         tuple((excerpt['id'], excerpt['name']) for excerpt in public_excerpts().values('id', 'name'))
         ),
        ('Countries & administrative areas [{count}]'.format(count=len(country_choices)), country_choices),
    )


class ExistingForm(OrderOptionsMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExistingForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_id = 'existingExcerptForm'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('excerptexport:order_existing_excerpt')

        self.helper.layout = Layout(
            Fieldset(
                _('Excerpt'),
                HTML(render_to_string('excerptexport/forms/partials/existing_form_filter.html')),
                'existing_excerpts',
                HTML(render_to_string('excerptexport/forms/partials/delete_personal_excerpts_link.html'))
            ),
            OrderOptionsMixin(self).form_layout(),
            Submit('submit', 'Submit'),
        )

    @classmethod
    def get_dynamic_form_class(cls, user):
        cls.declared_fields['existing_excerpts'] = forms.ChoiceField(
            label=_('Existing excerpts'),
            required=True,
            choices=get_existing_excerpt_choices(user),
            widget=forms.Select(
                attrs={'size': 10, 'required': True, 'class': 'resizable'},
            ),
        )
        return cls

    def save(self, user):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.coordinate_reference_system = self.cleaned_data['coordinate_reference_system']
        extraction_order.extraction_formats = self.cleaned_data['formats']
        extraction_order.detail_level = self.cleaned_data['detail_level']

        existing_key = self.cleaned_data['existing_excerpts']
        excerpt = Excerpt.objects.get(pk=int(existing_key))
        extraction_order.excerpt = excerpt

        extraction_order.save()
        return extraction_order
