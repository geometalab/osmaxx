import django_rq

from osmaxx.converters import converter_settings


def rq_enqueue_with_settings(function, *args, **kwargs):
    return django_rq.enqueue(
        function,
        result_ttl=converter_settings.OSMAXX_CONVERSION_SERVICE['RESULT_TTL'],
        *args,
        **kwargs
    )
