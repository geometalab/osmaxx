from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.views import _update_progress as update_order


def update_orders_of_request_user(request):
    for order in ExtractionOrder.objects.all():
        update_order(order)


class OrderUpdaterMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "The osmaxx order update middleware requires Django authentication middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "'osmaxx.job_progress.middleware.OrderUpdaterMiddleware'."
        )
        update_orders_of_request_user(request)
