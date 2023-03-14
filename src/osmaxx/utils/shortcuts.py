import datetime
from osmaxx.user_messaging.interaction import add_user_message

from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.core.cache import cache
from django.utils.translation import gettext as _


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
        try:
            email_address = self.recipient.email
            mail.send_mail(
                settings.EMAIL_SUBJECT_PREFIX + subject,
                mail_body,
                settings.DEFAULT_FROM_EMAIL,
                [email_address],
            )
        except AttributeError:
            if warn_if_no_email:
                self.warn(
                    _(
                        "There is no email address assigned to your account. You won't be notified by email!"
                    )
                )

    def inform(self, message_type, message):
        add_user_message(
            msg=message,
            level=message_type,
            user=self.recipient,
        )


def get_cached_or_set(
    cache_string,
    func,
    *args,
    timeout=datetime.timedelta(minutes=15).total_seconds(),
    on_cache_hit=None,
    **kwargs
):
    """Gets requested value from cache, else produces it with specified function and caches it.

    Gets the value at key ``cache_string`` from the cache. If it can't be found in the Django cache,
    calls ``func(*args, **kwargs)`` to obtain a new value, which is returned and stored in the cache
    at key ``cache_string``.

    Args:
        cache_string: Key for looking up the cached value and for storing newly computed values in case of a cache miss
        func: Called with ``*args`` and ``**kwargs`` in case of a cache miss to provide the value
        *args: Passed to ``func`` or ``on_cache_hit``
        timeout: How long (in seconds) to cache a newly obtained value. Defaults to 15 minutes.
        on_cache_hit: Called with the cached_value, ``*args`` and ``**kwargs`` if there was a cache hit
        **kwargs: Passed to ``func`` or ``on_cache_hit``

    Returns:
        The cached value or in case of a cache miss or the newly obtained (and now cached) value.
    """
    cached_value = cache.get(cache_string)
    if cached_value is None:
        cached_value = func(*args, **kwargs)
        cache.set(cache_string, cached_value, timeout=timeout)
    elif on_cache_hit:
        on_cache_hit(cached_value, *args, **kwargs)
    return cached_value
