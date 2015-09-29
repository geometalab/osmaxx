from excerptconverter.converter_helper import module_converter_configuration, run_model_execute


NAME = 'Dummy'
EXPORT_FORMATS = {
    'jpg': {
        'name': 'JPG',
        'file_extension': 'jpg',
        'mime_type': 'image/jpg'
    }
}
EXPORT_OPTIONS = {
    'resolution': {
        'label': 'Resolution',
        'type': 'text',
        'default': '200'
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
    pass
