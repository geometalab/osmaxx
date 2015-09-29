from celery import shared_task

from excerptconverter.converter_helper import module_converter_configuration
from osmaxx.excerptexport import models

from . import test_result_pipe


NAME = 'Test'
EXPORT_FORMATS = {
    'jpg': {
        'name': 'JPG',
        'file_extension': 'jpg',
        'mime_type': 'image/jpg'
    },
    'png': {
        'name': 'PNG',
        'file_extension': 'png',
        'mime_type': 'image/png'
    },
    'svg': {
        'name': 'SVG',
        'file_extension': 'svg',
        'mime_type': 'image/svg'
    }
}
EXPORT_OPTIONS = {
    'image_resolution': {
        'label': 'Resolution',
        'type': 'number',
        'default': '500'
    },
    'quality': {
        'label': 'Quality',
        'type': 'number',
        'default': '10'
    }
}


def converter_configuration():
    return module_converter_configuration(NAME, EXPORT_FORMATS, EXPORT_OPTIONS)


@shared_task
def execute(extraction_order_id, converter_configuration):
    extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
    test_result_pipe.temp_result_storage = {
        'excerpt_name': extraction_order.excerpt.name,
        'supported_formats': sorted([export_format_configuration['name']
                                    for export_format_configuration
                                    in EXPORT_FORMATS.values()]),
        'conversion_formats': converter_configuration['formats'],
        'conversion_options_quality': converter_configuration['options']['quality']
    }
    extraction_order.state = models.ExtractionOrderState.FINISHED
    extraction_order.save()
