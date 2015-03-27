import os

from django import template


register = template.Library()


@register.filter
def filter_filename(file_object):
    return os.path.basename(file_object.name) if file_object and file_object.name else file_object
