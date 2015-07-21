from celery import shared_task
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
import time
import stored_messages

from osmaxx.excerptexport import models
from .services.data_conversion_service import trigger_data_conversion


def inform_user(extraction_order):
    message_text = _('Your extraction order %s has been processed' % extraction_order)
    stored_messages.api.add_message_for(
        users=[extraction_order.orderer],
        level=messages.INFO,
        message_text=message_text
    )

    if hasattr(extraction_order.orderer, 'email'):
        send_mail(
            '[OSMAXX] Process finished',
            message_text,
            'no-reply@osmaxx.hsr.ch',
            [extraction_order.orderer.email]
        )


@shared_task
def create_export(extraction_order_id, export_options):
    wait_time = 0
    # wait for the db to be updated!
    extraction_order = None
    while extraction_order is None:
        try:
            extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
        except models.ExtractionOrder.DoesNotExist:
            time.sleep(5)
            wait_time += 5
            if wait_time > 30:
                raise

    trigger_data_conversion(extraction_order, export_options)
    message_text = _('Your extraction order "%s" has been started' % extraction_order)

    stored_messages.api.add_message_for(
        users=[extraction_order.orderer],
        level=messages.INFO,
        message_text=message_text
    )

    wait_time_in_seconds = 5
    # fake some work
    time.sleep(wait_time_in_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.PROCESSING
    extraction_order.save()

    time.sleep(wait_time_in_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.WAITING
    extraction_order.save()

    time.sleep(wait_time_in_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.FINISHED
    extraction_order.save()

    # inform the user of the status change.
    inform_user(extraction_order)
