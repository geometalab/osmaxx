from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from osmaxx.excerptexport.models import Excerpt


def _get_active_excerpts():
    return Excerpt.objects.filter(is_active=True).filter(
        bounding_geometry_raw_reference__bboxboundinggeometry__isnull=False
    )


def own_private(user):
    return _get_active_excerpts().filter(is_public=False, owner=user)


def own_public(user):
    return _get_active_excerpts().filter(is_public=True, owner=user)


def other_public(user):
    return _get_active_excerpts().filter(is_public=True).exclude(owner=user)


def countries():
    return _get_active_excerpts().filter(
        bounding_geometry_raw_reference__osmosispolygonfilterboundinggeometry__isnull=False
    )


def get_existing_excerpt_choices_shortcut(user):
    return (
        ('Personal excerpts ({username})'.format(username=user.username),
         tuple((excerpt.id, excerpt.name) for excerpt in own_private(user))
         ),
        ('Personal public excerpts ({username})'.format(username=user.username),
         tuple((excerpt.id, excerpt.name) for excerpt in own_public(user))
         ),
        ('Other excerpts',
         tuple((excerpt.id, excerpt.name) for excerpt in other_public(user))
         ),
        ('Countries',
         tuple((excerpt.id, excerpt.name) for excerpt in countries())
         ),
    )


def get_data_attributes_for_excerpts_shortcut():
    return {
        excerpt.id: {
            'data-geometry': "boundingbox",
            'data-north': excerpt.bounding_geometry.north,
            'data-east': excerpt.bounding_geometry.east,
            'data-south': excerpt.bounding_geometry.south,
            'data-west': excerpt.bounding_geometry.west,
        } for excerpt in _get_active_excerpts()
        }


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
