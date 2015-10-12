from django import forms
from django.http import Http404
from django.utils.translation import ugettext as _

from crispy_forms import helper as form_helper
from crispy_forms import layout as form_layout
from excerptconverter import ConverterManager
from osmaxx.excerptexport.models import BBoxBoundingGeometry, Excerpt, ExtractionOrder
from osmaxx.utilities.dict_helpers import select_keys
from .temporary_form_helper import available_format_choices, get_export_options


class ExcerptOrderFormPartExcerptNameMixin(forms.Form):
    name = forms.CharField(
        label=_('Excerpt name'),
        required=True
    )


class ExcerptOrderFormPartCoordinatesMixin(ExcerptOrderFormPartExcerptNameMixin, forms.Form):
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

    def form_layout(self):
        return form_layout.Div(
            form_layout.HTML('<h2>' + _('New excerpt') + '</h2>'),
            form_layout.Fieldset(
                _('Create new excerpt'),
                'name',
            ),
            form_layout.Div(
                form_layout.Fieldset(
                    _('Bounding box'),
                    form_layout.Div(
                        form_layout.Field('north', wrapper_class='column-stretch-4'),
                        css_class="box-column-container balanced",
                    ),
                    form_layout.Div(
                        form_layout.Field('west', wrapper_class='column-stretch-4'),
                        form_layout.Field('east', wrapper_class='column-stretch-4'),
                        css_class="box-column-container separated",
                    ),
                    form_layout.Div(
                        form_layout.Field('south', wrapper_class='column-stretch-4'),
                        css_class="box-column-container balanced",
                    ),
                ),
                css_class='form-group',
                id='bbox-values',
            ),
            id=FormModeMixin.MODE_NEW,
        )


class ExcerptOrderFormCommonPartMixin(forms.Form):
    is_public = forms.BooleanField(
        label=_('Public'),
        required=False,
        help_text=_("Others will see name and bounding box of this excerpt. "
                    "They won't see that you created it or when you did so."),
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
                'is_public',
            ),
            form_layout.Fieldset(
                _('GIS export formats'),
                'formats',
            ),
        )


class ExcerptOrderFormPartExistingMixin(forms.Form):
    existing_excerpts = forms.ChoiceField(
        label=_('Excerpt'),
        required=True,
    )

    def form_layout(self):
        return form_layout.Div(
            form_layout.HTML('<h2>' + _('Existing excerpt') + '</h2>'),
            form_layout.HTML('''
                <div class="form-group has-feedback">
                    <input id="excerptListFilterField" class="form-control" type="search" placeholder="Filter excerpts …" autocomplete="off"/>
                    <span id="excerptListFilterFieldClearer" class="clearer glyphicon glyphicon-remove-circle form-control-feedback"></span>
                </div>
                '''  # noqa: line too long ignored
             ),
            form_layout.Fieldset(
                _('Existing excerpts'),
                'existing_excerpts',
            ),
            id=FormModeMixin.MODE_EXISTING,
        )


class FormModeMixin(forms.Form):
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
        return form_layout.HTML('''
            <div class="form-group select-button-group">
                <select class="btn-group" role="group" name="form_mode" id="id_form_mode" size="2" required="required" data-form-part-switcher>
                    <option class="btn btn-default" value="{existing_value}" selected="selected" data-form-part-for="existing-excerpt">{existing_excerpt_string}</option>
                    <option class="btn btn-default" value="{new_value}" data-form-part-for="new-excerpt">{new_excerpt_string}</option>
                </select>
            </div>
            '''  # noqa: line too long ignored
        .format(
            existing_excerpt_string=self.FORM_MODE_CHOICES[0][1],
            new_excerpt_string=self.FORM_MODE_CHOICES[1][1],
            new_value=self.MODE_NEW,
            existing_value=self.MODE_EXISTING,
            )
        )


class ExcerptOrderForm(ExcerptOrderFormPartCoordinatesMixin, ExcerptOrderFormCommonPartMixin, FormModeMixin,
                       ExcerptOrderFormPartExistingMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = form_helper.FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = form_layout.Layout(
            FormModeMixin(self).form_layout(),
            form_layout.Div(
                ExcerptOrderFormPartExistingMixin(self).form_layout(),
                css_class="form-part",
                data_form_part="existing-excerpt",
            ),
            form_layout.Div(
                ExcerptOrderFormPartCoordinatesMixin(self).form_layout(),
                css_class="form-part",
                data_form_part="new-excerpt",
            ),
            ExcerptOrderFormCommonPartMixin(self).form_layout(),
        )
        self.helper.add_input(form_layout.Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super().clean()

        if 'form_mode' not in self.cleaned_data:
            return cleaned_data

        form_mode = self.cleaned_data['form_mode']

        if form_mode == FormModeMixin.MODE_EXISTING:
            self._remove_errors_for_non_participating_fields(fields=ExcerptOrderFormPartCoordinatesMixin().fields)

        if form_mode == FormModeMixin.MODE_NEW:
            self._remove_errors_for_non_participating_fields(fields=ExcerptOrderFormPartExistingMixin().fields)

        return cleaned_data

    def save(self, user):
        extraction_order = ExtractionOrder(orderer=user)
        extraction_order.extraction_configuration = self._generate_extraction_options()

        if self.cleaned_data['form_mode'] == FormModeMixin.MODE_EXISTING:
            existing_excerpt = Excerpt.objects.get(pk=int(self.cleaned_data['existing_excerpts']))
            extraction_order.excerpt = existing_excerpt
        elif self.cleaned_data['form_mode'] == FormModeMixin.MODE_NEW:
            bbox_kwargs = select_keys(self.cleaned_data, ['north', 'east', 'south', 'west'])

            bounding_geometry = BBoxBoundingGeometry(**bbox_kwargs)
            bounding_geometry.save()

            excerpt_dict = select_keys(self.cleaned_data, ['name', 'is_public'])
            excerpt = Excerpt(
                is_active=True,
                bounding_geometry=bounding_geometry,
                owner=user,
                **excerpt_dict
            )
            excerpt.save()
            extraction_order.excerpt = excerpt
        else:
            raise Http404()
        extraction_order.save()
        self._execute_converters(extraction_order)
        return extraction_order

    # helper methods
    def _execute_converters(self, extraction_order):
        converter_manager = ConverterManager(extraction_order)
        converter_manager.execute_converters()

    def _generate_extraction_options(self):
        return get_export_options(self.cleaned_data['formats'])

    def _remove_errors_for_non_participating_fields(self, fields):
        not_to_be_validated_fields = fields
        for key_name, _ignored in not_to_be_validated_fields.items():
            try:
                self._errors.pop(key_name)
            except KeyError:
                pass
