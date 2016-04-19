from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from osmaxx.excerptexport.models import Export


def tracker(request, export_id):
    export = get_object_or_404(Export, pk=export_id)
    export.status = request.GET['status']
    export.save()

    # emissary = Emissary(recipient=export.extraction_order.orderer)
    response = HttpResponse('')
    response.status_code = 200
    return response
