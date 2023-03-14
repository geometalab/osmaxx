from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def remove_all_whitespace(value):
    return ''.join(value.split())


@register.filter
@stringfilter
def strip(value, *args, **kwargs):
    return value.strip(*args, **kwargs)
