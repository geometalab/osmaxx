import time
import os

from celery import shared_task

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from excerptconverter.baseexcerptconverter import BaseExcerptConverter

from osmaxx.excerptexport import models


private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


class DummyExcerptConverter(BaseExcerptConverter):
    name = 'Dummy'
    export_formats = {
        'txt': {
            'name': 'Text (.txt)',
            'file_extension': 'txt',
            'mime_type': 'text/plain'
        },
        'markdown': {
            'name': 'Markdown (.md)',
            'file_extension': 'md',
            'mime_type': 'text/markdown'
        }
    }
    export_options = {
        'detail_level': {
            'label': 'Detail level',
            'type': 'choice',
            'default': 'verbatim',
            'values': [
                {'name': 'verbatim', 'label': 'Verbatim'},
                {'name': 'simplified', 'label': 'Simplified'}
            ]
        }
    }
    steps_total = 2

    @staticmethod
    def create_output_files(execution_configuration, extraction_order, supported_export_formats):
        for format_key in execution_configuration['formats']:
            output_file = models.OutputFile.objects.create(
                mime_type=supported_export_formats[format_key]['mime_type'],
                extraction_order=extraction_order
            )

            if not os.path.exists(private_storage.location):
                os.makedirs(private_storage.location)

            file_name = str(output_file.public_identifier) + '.' + \
                supported_export_formats[format_key]['file_extension']
            file_content = ContentFile(str('detail level: ' + execution_configuration['options']['detail_level']))
            fs_file = private_storage.save(file_name, file_content)

            # file must be committed, so reopen to attach to model
            output_file.file = fs_file
            output_file.save()

            if private_storage.exists(file_name):
                message_text = _('"%s" created successful' % file_name)
                BaseExcerptConverter.inform_user(extraction_order.orderer, messages.SUCCESS, message_text, False)
            else:
                message_text = _('Creation of "%s" failed!' % file_name)
                BaseExcerptConverter.inform_user(extraction_order.orderer, messages.ERROR, message_text, False)

    @staticmethod
    @shared_task
    def execute_task(extraction_order_id, supported_export_formats, execution_configuration):
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

        fake_work_waiting_time_in_seconds = 5

        # now set the new state
        extraction_order.state = models.ExtractionOrderState.WAITING
        extraction_order.save()

        time.sleep(fake_work_waiting_time_in_seconds)

        # now set the new state
        extraction_order.state = models.ExtractionOrderState.PROCESSING
        extraction_order.save()

        message_text = _('Your extraction order "%s" has been started' % extraction_order)
        BaseExcerptConverter.inform_user(extraction_order.orderer, messages.INFO, message_text, False)

        DummyExcerptConverter.create_output_files(execution_configuration, extraction_order, supported_export_formats)

        time.sleep(fake_work_waiting_time_in_seconds)

        # now set the new state
        extraction_order.state = models.ExtractionOrderState.FINISHED
        extraction_order.save()

        # inform the user of the status change.
        message_text = _('Your extraction order %s has been processed' % extraction_order)
        BaseExcerptConverter.inform_user(extraction_order.orderer, messages.SUCCESS, message_text)
