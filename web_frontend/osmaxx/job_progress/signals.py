from django.core.handlers.wsgi import WSGIRequest
from django.core.signals import request_started
from django.dispatch import receiver


@receiver(request_started)
def _request_receiver(sender, environ, **kwargs):
    request = WSGIRequest(environ)
    update_orders_of_request_user(request)


def update_orders_of_request_user(request):
    pass
