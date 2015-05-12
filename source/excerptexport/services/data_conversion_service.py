import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from excerptexport import settings as excerptexport_settings
from excerptexport.models import OutputFile


private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


def trigger_data_conversion(extraction_order, export_options):
    """
    Run data conversion script

    :param export_options: dictionary
    """
    export_formats_configuration = {}
    for export_configuration_group_key, export_configuration_group in excerptexport_settings.EXPORT_OPTIONS.items():
        export_formats_configuration.update(export_configuration_group['formats'])
    """
    'gis': {
        'formats': {
            'file_gdb': {
                'name': 'FileGDB',
                'file_extension': 'gdb'
            },
            'geo_package': {
                'name': 'GeoPackage',
                'file_extension': 'geo'
            }
        }
    },
    'routing': {
        'name': 'Routing',
        'formats': {
            'img': {
                'name': 'IMG',
                'file_extension': 'img'
            }
        }
    }
    """
    for export_type_key, export_type in export_options.items():
        for format_key in export_type['formats']:
            output_file = OutputFile.objects.create(
                mime_type=export_formats_configuration[format_key]['mime_type'],
                extraction_order=extraction_order
            )

            if not os.path.exists(private_storage.path):
                os.makedirs(private_storage.path)

            file_name = str(output_file.public_identifier) + '.' + \
                export_formats_configuration[format_key]['file_extension']
            file_content = ContentFile(str(output_file.public_identifier))
            file = private_storage.save(file_name, file_content)

            # file must be committed, so reopen to attach to model
            output_file.file = file
            output_file.save()
