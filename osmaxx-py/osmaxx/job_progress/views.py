from django.shortcuts import get_object_or_404
from osmaxx.excerptexport.models import extraction_order
from osmaxx.excerptexport.services.conversion_api_client import get_authenticated_api_client


def tracker(request, order_id):
    order = get_object_or_404(extraction_order.ExtractionOrder, pk=order_id)
    order.progress_url = request.GET['status']
    order.save()
    client = get_authenticated_api_client()
    client.update_order_status(order)
