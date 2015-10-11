from django import forms
from django.utils.translation import ugettext as _

from crispy_forms import helper as form_helper
from crispy_forms import layout as form_layout
from .temporary_form_helper import available_format_choices


class ExcerptOrderFormPartCoordinates(forms.Form):
    excerpt_name = forms.CharField(
        label=_('Excerpt name'),
        required=True
    )
    excerpt_bounding_box_north = forms.FloatField(
        label=_('North'),
        required=True,
    )
    excerpt_bounding_box_west = forms.FloatField(
        label=_('West'),
        required=True,
    )
    excerpt_bounding_box_east = forms.FloatField(
        label=_('East'),
        required=True,
    )
    excerpt_bounding_box_south = forms.FloatField(
        label=_('South'),
        required=True,
    )

    def form_layout(self):
        return form_layout.Div(
            form_layout.HTML('<h2>' + _('New excerpt') + '</h2>'),
            form_layout.Fieldset(
                _('Create new excerpt'),
                'excerpt_name',
            ),
            form_layout.Div(
                form_layout.Fieldset(
                    _('Bounding box'),
                    form_layout.Div(
                        form_layout.Field('excerpt_bounding_box_north', wrapper_class='column-stretch-4'),
                        css_class="box-column-container balanced",
                    ),
                    form_layout.Div(
                        form_layout.Field('excerpt_bounding_box_west', wrapper_class='column-stretch-4'),
                        form_layout.Field('excerpt_bounding_box_east', wrapper_class='column-stretch-4'),
                        css_class="box-column-container separated",
                    ),
                    form_layout.Div(
                        form_layout.Field('excerpt_bounding_box_south', wrapper_class='column-stretch-4'),
                        css_class="box-column-container balanced",
                    ),
                ),
                css_class='form-group',
                id='bbox-values',
            ),
            id=FormMode.MODE_NEW,
        )


class ExcerptOrderFormCommonPart(forms.Form):
    excerpt_is_public = forms.BooleanField(
        label=_('Public'),
        required=False,
        help_text=_("Others will see name and bounding box of this excerpt. "
                    "They won't see that you created it or when you did so."),
        # widget=forms.CheckboxInput,
        initial=True,
    )
    formats = forms.MultipleChoiceField(
        label=_("GIS export formats:"),
        choices=available_format_choices,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def form_layout(self):
        return form_layout.Div(
            form_layout.Fieldset(
                _('Visibility'),
                'excerpt_is_public',
            ),
            form_layout.Fieldset(
                _('GIS export formats'),
                'formats',
            ),
        )


class ExcerptOrderFormPartExisting(forms.Form):
    existing_excerpts = forms.ChoiceField(
        label=_('Excerpt'),
        required=True,
    )

    def form_layout(self):
        return form_layout.Div(
            form_layout.HTML('<h2>' + _('Existing excerpt') + '</h2>'),
            form_layout.Fieldset(
                _('Existing excerpts'),
                'existing_excerpts',
            ),
            id=FormMode.MODE_EXISTING,
        )


class FormMode(forms.Form):
    MODE_EXISTING = 'existing-excerpt'
    MODE_NEW = 'new-excerpt'
    FORM_MODE_CHOICES = (
        (MODE_EXISTING, _('Use existing excerpt')),
        (MODE_NEW, _('Create new excerpt')),
    )
    form_mode = forms.ChoiceField(
        choices=FORM_MODE_CHOICES,
        label=False,
        widget=forms.Select(attrs={'size': '2'}),
        initial='existing-excerpt',
    )

    def form_layout(self):
        return form_layout.Div(form_layout.Field(
               'form_mode',
                css_class='btn btn-default',
            ))


class ExcerptOrderForm(ExcerptOrderFormPartCoordinates, ExcerptOrderFormCommonPart, FormMode, ExcerptOrderFormPartExisting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = form_helper.FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = form_layout.Layout(
            FormMode(self).form_layout(),
            ExcerptOrderFormPartExisting(self).form_layout(),
            ExcerptOrderFormPartCoordinates(self).form_layout(),
            ExcerptOrderFormCommonPart(self).form_layout(),
        )
        self.helper.add_input(form_layout.Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super().clean()

        if 'form_mode' not in self.cleaned_data:
            return cleaned_data

        form_mode = self.cleaned_data['form_mode']

        if form_mode == FormMode.MODE_EXISTING:
            self._remove_errors_for_non_participating_fields(fields=ExcerptOrderFormPartCoordinates().fields)

        if form_mode == FormMode.MODE_NEW:
            self._remove_errors_for_non_participating_fields(fields=ExcerptOrderFormPartExisting().fields)

        return cleaned_data

    def _remove_errors_for_non_participating_fields(self, fields):
        not_to_be_validated_fields = fields
        for key_name, _ in not_to_be_validated_fields.items():
            try:
                self._errors.pop(key_name)
            except KeyError:
                    pass

