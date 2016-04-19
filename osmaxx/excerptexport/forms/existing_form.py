from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from osmaxx.countries.models import Country
from osmaxx.excerptexport.forms.order_options_mixin import get_export_formats
from osmaxx.excerptexport.models import ExtractionOrder, Excerpt
from osmaxx.excerptexport.models.excerpt import private_user_excerpts, public_user_excerpts, \
    other_users_public_excerpts
from osmaxx.api_client import COUNTRY_ID_PREFIX
from .order_options_mixin import OrderOptionsMixin, get_export_options


def get_country_choices():
    return tuple(
        (COUNTRY_ID_PREFIX + str(country[0]), country[1])
        for country in Country.objects.all().order_by('name').values_list('id', 'name')
    )


def get_existing_excerpt_choices(user):
    country_choices = get_country_choices()
    return (
        ('Personal excerpts ({username}) [{count}]'
            .format(username=user.username, count=private_user_excerpts(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in private_user_excerpts(user))
         ),
        ('Personal public excerpts ({username}) [{count}]'
            .format(username=user.username, count=public_user_excerpts(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in public_user_excerpts(user))
         ),
        ('Other excerpts [{count}]'.format(count=other_users_public_excerpts(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in other_users_public_excerpts(user))
         ),
        ('Countries [{count}]'.format(count=len(country_choices)), country_choices),
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
                HTML('''
                    <div class="form-group has-feedback">
                        <input id="excerptListFilterField" class="form-control" type="search" placeholder="Filter excerpts …" autocomplete="off"/>
                        <span id="excerptListFilterFieldClearer" class="clearer glyphicon glyphicon-remove-circle form-control-feedback"></span>
                    </div>
                    '''  # noqa: line too long ignored
                ),
                'existing_excerpts',
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
                attrs={'size': 10, 'required': True},
            ),
        )
        return cls

    def save(self, user):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.extraction_configuration = get_export_options()
        extraction_order.extraction_formats = get_export_formats(self.cleaned_data['formats'])

        existing_key = self.cleaned_data['existing_excerpts']
        if self._is_country(existing_key):
            from osmaxx.api_client import ConversionApiClient
            country_id = int(existing_key.strip(COUNTRY_ID_PREFIX))
            extraction_order.country_id = country_id
            extraction_order.name = ConversionApiClient().get_country_name(country_id)
        else:
            existing_excerpt = Excerpt.objects.get(pk=int(existing_key))
            extraction_order.excerpt = existing_excerpt

        extraction_order.save()
        return extraction_order

    def _is_country(self, pk):
        return pk.startswith(COUNTRY_ID_PREFIX)
