import logging
from datetime import timedelta

from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.models.extraction_order import FINAL_STATES, ExtractionOrderState
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client
from osmaxx.utilities.shortcuts import get_cached_or_set

logger = logging.getLogger(__name__)


class OrderUpdaterMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "The osmaxx order update middleware requires Django authentication middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "'osmaxx.job_progress.middleware.OrderUpdaterMiddleware'."
        )
        update_orders_of_request_user(request)


def update_orders_of_request_user(request):
    current_user = request.user
    if current_user.is_anonymous():
        return
    for order in ExtractionOrder.objects.exclude(state__in=FINAL_STATES).filter(orderer=current_user):
        update_order_if_stale(order)


def update_order_if_stale(extraction_order):
    get_cached_or_set(
        'extraction_order_{}_progress'.format(extraction_order.id),
        update_order, extraction_order,
        on_cache_hit=_log_cache_hit,
        timeout=timedelta(minutes=1).total_seconds(),
    )


def update_order(extraction_order):
    _log_cache_miss(extraction_order)
    conversion_client = get_authenticated_api_client()
    conversion_client.update_order_status(extraction_order)
    if logger.isEnabledFor(logging.DEBUG):
        message = "Fetched, updated and cached ExtractionOrder {extraction_order} progress: {progress}".format(
            extraction_order=extraction_order.id,
            progress=ExtractionOrderState.label(extraction_order.state),
        )
        logger.debug(message)
    return extraction_order.state


def _log_cache_miss(extraction_order):
    if not logger.isEnabledFor(logging.INFO):
        return
    message = "Cache miss - Re-fetching progress of pending ExtractionOrder {extraction_order}.".format(
        extraction_order=extraction_order.id,
    )
    logger.info(message)


def _log_cache_hit(cached_value, extraction_order):
    if not logger.isEnabledFor(logging.INFO):
        return
    message = (
        "Cache hit - Not re-fetching progress of pending ExtractionOrder {extraction_order}, "
        "as it has already been fetched recently. Progress then was {progress}."
    ).format(
        extraction_order=extraction_order.id,
        progress=ExtractionOrderState.label(extraction_order.state),
    )
    logger.info(message)
