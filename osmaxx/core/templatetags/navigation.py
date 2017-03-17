# Adopted from https://djangosnippets.org/snippets/2783/
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def siteabsoluteurl(absoluteurl, request):
    """
    receives an argument in the form of an absolute url <absoluteurl>
    Returns the same url with all the necessary path information to be used offsite
    """
    absolute_url = request.build_absolute_uri(absoluteurl)
    if settings.OSMAXX.get('SECURED_PROXY', False) and not absolute_url.startswith('https'):
        if absolute_url.startswith('http'):
            absolute_url = absolute_url[4:]
        absolute_url = 'https' + absolute_url
    return absolute_url
