from urllib.parse import urlsplit, urlunsplit

import logging
from django import template
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def siteabsoluteurl(relative_or_absolute_url: str, request: HttpRequest) -> str:
    """
    Produce URL suitable for offsite use.

    Args:
        relative_or_absolute_url: A relative, scheme-relative or absolute URL
        request: A Django request object, from which to take the missing parts

    Returns:
        An absolute URL, incl. scheme, host, etc.
    """
    absolute_url = request.build_absolute_uri(relative_or_absolute_url)
    if settings.OSMAXX.get('SECURED_PROXY', False):
        url_components = urlsplit(absolute_url)
        if url_components.scheme.startswith('http'):
            absolute_url = urlunsplit(url_components._replace(scheme='https'))
        elif logger.getEffectiveLevel() == logging.WARNING:
            logger.warning(
                "{url} has not been converted to HTTPS, because it isn't an HTTP URL.".format(url=absolute_url)
            )
    return absolute_url
