from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from osmaxx.excerptexport.models import extraction_order, ExtractionOrderState
from osmaxx.excerptexport.services.shortcuts import get_authenticated_api_client
from osmaxx.utilities.shortcuts import Emissary


def tracker(request, order_id):
    order = get_object_or_404(extraction_order.ExtractionOrder, pk=order_id)
    order.progress_url = request.GET['status']
    order.save()
    client = get_authenticated_api_client()
    client.update_order_status(order)

    emissary = Emissary(recipient=order.orderer)

    if order.are_downloads_ready:
        message = _('The extraction of the order "{order_id}" has been finished.').format(order_id=order.id)

        finished_email_subject = _('Extraction Order #{order_id} "{excerpt_name}" finished').format(
            order_id=order.id,
            excerpt_name=order.excerpt_name,
        )
        finished_email_body = _(
            'The extraction order #{order_id} "{excerpt_name}" has been finished and is ready for retrieval.'
        ).format(
            order_id=order.id,
            excerpt_name=order.excerpt_name,
        )

        emissary.success(message)
        emissary.inform_mail(subject=finished_email_subject, mail_body=finished_email_body)
    elif order.state == ExtractionOrderState.FAILED:
        message = _('The extraction order "{order_id}" has failed. Please try again later.').format(
            order_id=order.id,
        )

        finished_email_subject = _('Extraction Order "{order_id} failed').format(order_id=order.id)
        finished_email_body = _(
            'The extraction order "{order_id}" could not be completed, please try again later.'
        ).format(order_id=order.id)

        emissary.error(message)
        emissary.inform_mail(subject=finished_email_subject, mail_body=finished_email_body)
    else:
        message = _("Extraction order {order} is now {order_state}.").format(
            order=order.id,
            order_state=ExtractionOrderState.label(order.state),
        )
        emissary.info(message)
    response = HttpResponse('')
    response.status_code = 200
    return response
