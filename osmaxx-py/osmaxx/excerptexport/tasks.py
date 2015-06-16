from celery import shared_task
from django.core.mail import send_mail
import time
from osmaxx.excerptexport import models


@shared_task
def send_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def create_export(extraction_order_id):
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

    print('pk %s' % extraction_order_id)
    extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)

    twenty_seconds = 20
    # fake some work
    time.sleep(twenty_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.PROCESSING
    extraction_order.save()

    time.sleep(twenty_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.WAITING
    extraction_order.save()

    time.sleep(twenty_seconds)
    # now set the new state
    extraction_order.state = models.ExtractionOrderState.FINISHED
    extraction_order.save()
