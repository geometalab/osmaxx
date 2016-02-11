import django_rq

from osmaxx.conversion import _settings


def rq_enqueue_with_settings(function, *args, **kwargs):
    return django_rq.enqueue(
        function,
        result_ttl=_settings.CONVERSION_SETTINGS['RESULT_TTL'],
        *args,
        **kwargs
    )
