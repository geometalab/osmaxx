from excerptconverter.converter_helper import module_converter_configuration, run_model_execute
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


def execute(extraction_order, execution_configuration, run_as_celery_tasks):
    return run_model_execute(
        execute_task,
        EXPORT_FORMATS,
        extraction_order,
        execution_configuration,
        run_as_celery_tasks
    )


def execute_task(extraction_order_id, supported_export_formats, converter_configuration):
    extraction_order = models.ExtractionOrder.objects.get(pk=extraction_order_id)
    test_result_pipe.temp_result_storage = {
        'excerpt_name': extraction_order.excerpt.name,
        'supported_formats': sorted([export_format_configuration['name']
                                    for export_format_configuration
                                    in supported_export_formats.values()]),
        'conversion_formats': converter_configuration['formats'],
        'conversion_options_quality': converter_configuration['options']['quality']
    }
    extraction_order.state = models.ExtractionOrderState.FINISHED
    extraction_order.save()
