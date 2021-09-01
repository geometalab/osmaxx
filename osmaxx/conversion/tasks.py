import logging
import os
import requests
from celery import shared_task
from django.contrib.messages import constants
from django.utils import timezone
from django.utils.translation import gettext as _
from osmaxx.conversion.constants import status
from osmaxx.conversion.constants.status import FAILED, FINISHED, STARTED
from osmaxx.conversion.conversion_helper import ConversionHelper
from osmaxx.excerptexport.models import ExtractionOrder
from osmaxx.excerptexport.models.export import Export
from osmaxx.utils.shortcuts import Emissary

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="start_conversion")
def start_conversion(self, extraction_order_id):
    extraction_order = ExtractionOrder.objects.get(pk=extraction_order_id)
    emissary = Emissary(recipient=extraction_order.orderer)
    emissary.inform(
        constants.INFO,
        _("Excerpt '{name}' startet").format(name=extraction_order.excerpt_name),
    )
    with ConversionHelper(extraction_order) as helper:
        self.update_state(state="PROGRESS", meta={"progress": 0})
        start_time = timezone.now()
        helper.cut_pbf()
        estimated_pbf_size = os.path.getsize(helper._pbf.name)
        cut_time = timezone.now() - start_time
        print(f"cutting time spent: {cut_time}")
        for export in extraction_order.exports.all():
            export.status = STARTED
            export.estimated_pbf_size = estimated_pbf_size
            export.save()
            try:
                helper.create_export(export=export)
                export.status = FINISHED
                export.save()
            except Exception as e:
                export.status = FAILED
                export.save()
                print(e)
                logger.exception(e)
        emissary.inform(
            constants.INFO,
            _("Excerpt '{name}' finished.").format(name=extraction_order.excerpt_name),
        )
        extraction_order.export_finished = True
        extraction_order.save()
    return f"{extraction_order.id} finished"


@shared_task
def handle_unfinished_exports():
    for export in Export.objects.exclude(status__in=status.FINAL_STATUSES):
        if export.update_is_overdue:
            export.status = status.FAILED
            export.save()


@shared_task
def call_websites_to_send_mails():
    ready_to_send = ExtractionOrder.objects.filter(
        export_finished=True,
        email_sent=False,
    )
    if len(ready_to_send):
        eo = ready_to_send[0]
        requests.get(eo.invoke_update_url)
