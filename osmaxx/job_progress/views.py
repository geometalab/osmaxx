from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from osmaxx.excerptexport.models import Export
from osmaxx.utilities.shortcuts import Emissary


def tracker(request, export_id):
    export = get_object_or_404(Export, pk=export_id)
    _handle_new_status(export, request.GET['status'])

    response = HttpResponse('')
    response.status_code = 200
    return response


def _handle_new_status(export, new_status):
    if export.status != new_status:
        _handle_changed_status(export, new_status)
        export.save()


def _handle_changed_status(export, new_status):
    export.status = new_status
    emissary = Emissary(recipient=export.extraction_order.orderer)
    emissary.info(
        'Export #{export_id} "{name}" to {format} is now started.'.format(
            export_id=export.id,
            name=export.extraction_order.excerpt_name,
            format=export.get_file_format_display(),
        )
    )
