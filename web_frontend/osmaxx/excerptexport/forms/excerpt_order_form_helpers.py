from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from osmaxx.excerptexport.models import Excerpt
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client


def _get_active_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
        bounding_geometry__bboxboundinggeometry__isnull=False
    )


def own_private(user):
    return _get_active_excerpts().filter(is_public=False, owner=user)


def own_public(user):
    return _get_active_excerpts().filter(is_public=True, owner=user)


def other_public(user):
    return _get_active_excerpts().filter(is_public=True).exclude(owner=user)


def get_prefixed_countries():
    return get_authenticated_api_client().get_prefixed_countries()


def get_country_choices():
    return tuple((country['id'], country['name']) for country in get_prefixed_countries())


def get_existing_excerpt_choices_shortcut(user):
    country_choices = get_country_choices()
    return (
        ('Personal excerpts ({username}) [{count}]'.format(username=user.username, count=own_private(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in own_private(user))
         ),
        ('Personal public excerpts ({username}) [{count}]'
         .format(username=user.username, count=own_public(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in own_public(user))
         ),
        ('Other excerpts [{count}]'.format(count=other_public(user).count()),
         tuple((excerpt.id, excerpt.name) for excerpt in other_public(user))
         ),
        ('Countries [{count}]'.format(count=len(country_choices)),
         country_choices
         ),
    )


class SelectWidgetWithDataOptions(forms.Select):
    def __init__(self, attrs=None, choices=(), data_attributes=None):
        self._data_attributes = data_attributes
        super().__init__(attrs=attrs, choices=choices)

    def render_option(self, selected_choices, option_value, option_label):
        if self._data_attributes:
            if option_value is None:
                return super().render_option(selected_choices, option_value, option_label)
            data_option_html = ''
            if option_value in self._data_attributes:
                for data_attr_name, data_attr_value in self._data_attributes[option_value].items():
                    data_option_html += mark_safe(' {data_attr_name}={data_attr_value}'.format(
                        data_attr_name=force_text(data_attr_name),
                        data_attr_value=force_text(data_attr_value),
                    ))
            option_value = force_text(option_value)

            if option_value in selected_choices:
                selected_html = mark_safe(' selected="selected"')
                if not self.allow_multiple_selected:
                    # Only allow for a single selection.
                    selected_choices.remove(option_value)
            else:
                selected_html = ''
            return format_html('<option value="{}"{}{}>{}</option>',
                               option_value,
                               selected_html,
                               data_option_html,
                               force_text(option_label))
        else:
            return super().render_option(selected_choices, option_value, option_label)
