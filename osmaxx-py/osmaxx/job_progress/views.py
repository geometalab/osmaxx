from osmaxx.excerptexport.models import extraction_order
from osmaxx.excerptexport.services import conversion_api_client


def tracker(request, order_id):
    order = extraction_order.ExtractionOrder.objects.get(pk=order_id)  # TODO: consider 404ing if not found
    client = conversion_api_client.ConversionApiClient()
    client.update_order_status(order)
