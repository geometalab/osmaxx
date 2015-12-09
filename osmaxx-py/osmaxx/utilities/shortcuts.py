import datetime

from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.core.cache import cache
from django.shortcuts import _get_queryset
from django.utils.translation import gettext as _

import stored_messages


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object, or None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_list_or_none(klass, *args, **kwargs):
    """
    Uses filter() to return a list of objects, or return None if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    object_list = list(queryset.filter(*args, **kwargs))
    if not object_list:
        return None
    return object_list


class Emissary:
    def __init__(self, recipient):
        self.recipient = recipient

    def info(self, message):
        self.inform(messages.INFO, message)

    def success(self, message):
        self.inform(messages.SUCCESS, message)

    def warn(self, message):
        self.inform(messages.WARNING, message)

    def error(self, message):
        self.inform(messages.ERROR, message)

    def debug(self, message):
        self.inform(messages.DEBUG, message)

    def inform_mail(self, subject, mail_body, warn_if_no_email=True):
        email = getattr(self.recipient, 'email', None)
        if email:
            mail.send_mail(
                '[OSMAXX] ' + subject,
                mail_body,
                settings.DEFAULT_FROM_EMAIL,
                [self.recipient.email]
            )
        if warn_if_no_email and not email:
            self.warn(
                _("There is no email address assigned to your account. You won't be notified by email!")
            )

    def inform(self, message_type, message):
        stored_messages.api.add_message_for(
            users=[self.recipient],
            level=message_type,
            message_text=message
        )


def get_cached_or_set(cache_string, func, timeout=datetime.timedelta(minutes=15).seconds):
    cached_value = cache.get(cache_string)
    if cached_value is None:
        cached_value = func()
        cache.set(cache_string, cached_value, timeout=timeout)
    return cached_value
