from django import template
from django.conf import settings

register = template.Library()


@register.filter
def siteabsoluteurl(relative_or_absolute_url, request):
    """
    Produce URL suitable for offsite use.

    Args:
        relative_or_absolute_url: A relative, scheme-relative or absolute URL
        request: A Django request object, from which to take the missing parts

    Returns:
        An absolute URL, incl. scheme, host, etc.
    """
    absolute_url = request.build_absolute_uri(relative_or_absolute_url)
    if settings.OSMAXX.get('SECURED_PROXY', False) and not absolute_url.startswith('https'):
        if absolute_url.startswith('http'):
            absolute_url = absolute_url[4:]
        absolute_url = 'https' + absolute_url
    return absolute_url
