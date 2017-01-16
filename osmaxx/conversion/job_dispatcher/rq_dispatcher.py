from django_rq import get_queue

from osmaxx.conversion import _settings


def enqueue(func, *args, **kwargs):
    queue_name = kwargs.pop('queue_name')
    return get_queue(queue_name).enqueue(func, *args, **kwargs)


def rq_enqueue_with_settings(function, *args, **kwargs):
    return enqueue(
        function,
        result_ttl=_settings.CONVERSION_SETTINGS['RESULT_TTL'],
        *args,
        **kwargs
    )
