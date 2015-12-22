from datetime import timedelta

import django_rq

from converters import converter_settings


def rq_enqueue_with_settings(function, *args, **kwargs):
    return django_rq.enqueue(
        function,
        result_ttl=converter_settings.OSMAXX_CONVERSION_SERVICE['RESULT_TTL'],
        ttl=timedelta(days=1).seconds,  # max time in the queue, before it is considered lost
        timeout=timedelta(hours=10).seconds,  # max time the worker may spend, before the job is cancelled
        *args,
        **kwargs
    )
