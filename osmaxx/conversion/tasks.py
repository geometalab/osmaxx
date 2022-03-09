import logging
import os
import requests
from celery import shared_task, Task
from django.contrib.messages import constants
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import connection
from osmaxx.conversion.constants import status
from osmaxx.conversion.constants.status import FAILED, FINISHED, STARTED
from osmaxx.conversion.conversion_helper import ConversionHelper
from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.models.export import Export
from osmaxx.utils.shortcuts import Emissary

logger = logging.getLogger(__name__)

def try_again(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"retrying due to {e}")
        connection.close()
        return func(*args, **kwargs)


class FaultTolerantTask(Task):
    """ Implements after return hook to close an invalid connection.
    This way, django is forced to serve a new connection for the next
    task.
    """
    abstract = True

    def after_return(self, *args, **kwargs):
        connection.close()


@shared_task(base=FaultTolerantTask, bind=True, name="start_conversion")
def start_conversion(self, extraction_order_id):
    extraction_order = try_again(ExtractionOrder.objects.get, pk=extraction_order_id)
    # since connection closes when pbf cutter takes very long we need
    # to keep the ids as close to the database connection as possible
    export_ids = [export.id for export in extraction_order.exports.all()]

    orderer = extraction_order.orderer
    geometry = extraction_order.excerpt.geometry
    emissary = Emissary(recipient=orderer)
    emissary.inform(
        constants.INFO,
        _("Excerpt '{name}' startet").format(name=extraction_order.excerpt_name),
    )

    with ConversionHelper(geometry) as helper:
        start_time = timezone.now()
        print("cutting pbf")
        helper.cut_pbf()
        estimated_pbf_size = os.path.getsize(helper._pbf.name)
        cut_time = timezone.now() - start_time
        print(f"cutting time spent: {cut_time}")
        for export_id in export_ids:
            export = try_again(Export.objects.get, pk=export_id)
            print(f"starting export {export}")
            export.status = STARTED
            export.save()
            status = FAILED
            try:
                helper.create_export(export_id=export_id)
                status = FINISHED
            except Exception as e:
                print(e)
                logger.exception(e)
            finally:
                export = try_again(Export.objects.get, pk=export_id)
                export.estimated_pbf_size = estimated_pbf_size
                export.status = status
                export.save()

        extraction_order = try_again(ExtractionOrder.objects.get, pk=extraction_order_id)
        emissary.inform(
            constants.INFO,
            _("Excerpt '{name}' finished.").format(name=extraction_order.excerpt_name),
        )
        extraction_order.export_finished = True
        extraction_order.save()
        print(f"extraction order {extraction_order} finished.")
    return f"{extraction_order.id} finished"


@shared_task
def handle_unfinished_exports():
    for export in try_again(Export.objects.exclude, status__in=status.FINAL_STATUSES):
        if export.update_is_overdue:
            export.status = status.FAILED
            export.save()


@shared_task
def call_websites_to_send_mails():
    ready_to_send = try_again(ExtractionOrder.objects.filter,
        export_finished=True,
        email_sent=False,
    )
    if len(ready_to_send):
        eo = ready_to_send[0]
        requests.get(eo.invoke_update_url)
