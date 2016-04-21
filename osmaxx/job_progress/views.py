from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

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
        export.status = new_status
        _handle_changed_status(export)
        export.save()


def _handle_changed_status(export):
    emissary = Emissary(recipient=export.extraction_order.orderer)
    view_context = dict(export=export)
    emissary.info(
        render_to_string(
            'job_progress/messages/export_status_changed.txt',
            context=view_context,
        ).strip()
    )
