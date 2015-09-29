from excerptconverter.converter_helper import module_converter_configuration, run_model_execute


name = 'Dummy'
export_formats = {
    'jpg': {
        'name': 'JPG',
        'file_extension': 'jpg',
        'mime_type': 'image/jpg'
    }
}
export_options = {
    'resolution': {
        'label': 'Resolution',
        'type': 'text',
        'default': '200'
    }
}


def converter_configuration():
    return module_converter_configuration(name, export_formats, export_options)


def execute(extraction_order, execution_configuration, run_as_celery_tasks):
    return run_model_execute(
        execute_task,
        export_formats,
        extraction_order,
        execution_configuration,
        run_as_celery_tasks
    )


def execute_task(extraction_order_id, supported_export_formats, converter_configuration):
    pass
