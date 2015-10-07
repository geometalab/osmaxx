from celery import shared_task

from excerptconverter.converter_helper import module_converter_configuration


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


@shared_task
def execute_task(extraction_order_id, converter_configuration):
    pass
