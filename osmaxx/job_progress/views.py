from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from osmaxx.excerptexport.models import Export


def tracker(request, export_id):
    get_object_or_404(Export, pk=export_id)

    # emissary = Emissary(recipient=export.extraction_order.orderer)
    response = HttpResponse('')
    response.status_code = 200
    return response
