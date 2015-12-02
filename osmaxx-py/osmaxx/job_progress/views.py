from django.shortcuts import get_object_or_404
from osmaxx.excerptexport.models import extraction_order
from osmaxx.excerptexport.services import conversion_api_client


def tracker(request, order_id):
    order = get_object_or_404(extraction_order.ExtractionOrder, pk=order_id)
    order.progress_url = request.GET['status']
    order.save()
    client = conversion_api_client.ConversionApiClient()
    client.update_order_status(order)
