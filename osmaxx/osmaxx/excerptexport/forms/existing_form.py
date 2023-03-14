from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from django import forms
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from osmaxx.excerptexport.models import ExtractionOrder, Excerpt
from osmaxx.excerptexport.models.excerpt import (
    private_user_excerpts,
    public_excerpts,
    countries_and_administrative_areas,
)
from .order_options_mixin import OrderOptionsMixin


def get_existing_excerpt_choices(user):
    private_choices = _choicify(private_user_excerpts(user))
    public_choices = _choicify(public_excerpts())
    country_choices = _choicify(countries_and_administrative_areas().order_by("name"))
    return (
        (
            "Personal excerpts ({usr}) [{count}]".format(
                usr=user.username, count=len(private_choices)
            ),
            private_choices,
        ),
        ("Public excerpts [{count}]".format(count=len(public_choices)), public_choices),
        (
            "Countries & administrative areas [{count}]".format(
                count=len(country_choices)
            ),
            country_choices,
        ),
    )


def _choicify(excerpts_query_set):
    return tuple(excerpts_query_set.values_list("id", "name"))


class ExistingForm(OrderOptionsMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_id = "existingExcerptForm"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("excerptexport:order_existing_excerpt")

        self.helper.layout = Layout(
            Fieldset(
                _("Excerpt"),
                HTML(
                    render_to_string(
                        "excerptexport/forms/partials/existing_form_filter.html"
                    )
                ),
                "existing_excerpts",
                HTML(
                    render_to_string(
                        "excerptexport/forms/partials/delete_personal_excerpts_link.html"
                    )
                ),
            ),
            OrderOptionsMixin(self).form_layout(),
            Submit("submit", "Export (will take more than 30 minutes)"),
        )

    @classmethod
    def get_dynamic_form_class(cls, user):
        cls.declared_fields["existing_excerpts"] = forms.ChoiceField(
            label=_("Existing excerpts"),
            required=True,
            choices=get_existing_excerpt_choices(user),
            widget=forms.Select(
                attrs={"size": 10, "required": True, "class": "resizable"},
            ),
        )
        return cls

    def save(self, user, request):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.coordinate_reference_system = self.cleaned_data[
            "coordinate_reference_system"
        ]
        extraction_order.extraction_formats = self.cleaned_data["formats"]
        extraction_order.detail_level = self.cleaned_data["detail_level"]

        existing_key = self.cleaned_data["existing_excerpts"]
        excerpt = Excerpt.objects.get(pk=int(existing_key))
        extraction_order.excerpt = excerpt

        # cheap way to later on call the website from the worker to
        # invoke the middleware that sends emails, in order not to have to rely
        # on people using the site
        callback_uri = request.build_absolute_uri("/")
        extraction_order.invoke_update_url = callback_uri
        extraction_order.save()
        return extraction_order
