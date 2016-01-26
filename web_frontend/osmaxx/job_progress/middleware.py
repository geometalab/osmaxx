from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.models.extraction_order import FINAL_STATES
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client


def update_orders_of_request_user(request):
    current_user = request.user
    if current_user.is_anonymous():
        return
    for order in ExtractionOrder.objects.exclude(state__in=FINAL_STATES).filter(orderer=current_user):
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


def update_order(extraction_order):
    conversion_client = get_authenticated_api_client()
    conversion_client.update_order_status(extraction_order)
