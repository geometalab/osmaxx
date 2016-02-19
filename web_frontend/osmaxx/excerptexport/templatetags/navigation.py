# Adopted from https://djangosnippets.org/snippets/2783/
from django import template

register = template.Library()


@register.filter
def siteabsoluteurl(absoluteurl, request):
    """
    receives an argument in the form of an absolute url <absoluteurl>
    Returns the same url with all the necessary path information to be used offsite
    """
    return request.build_absolute_uri(absoluteurl)
