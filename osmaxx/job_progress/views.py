from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from osmaxx.excerptexport.models import Export
from osmaxx.utilities.shortcuts import Emissary


def tracker(request, export_id):
    export = get_object_or_404(Export, pk=export_id)
    export.status = request.GET['status']
    emissary = Emissary(recipient=export.extraction_order.orderer)
    emissary.info(
        'Export #{export_id} "{name}" is now started.'.format(
            export_id=export.id,
            name=export.extraction_order.excerpt_name,
        )
    )
    export.save()

    response = HttpResponse('')
    response.status_code = 200
    return response
