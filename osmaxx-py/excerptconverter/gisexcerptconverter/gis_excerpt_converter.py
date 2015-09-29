import os
import shutil
import subprocess
import tempfile
import time


from celery import shared_task

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from excerptconverter.converter_helper import ConverterHelper, module_converter_configuration, run_model_execute

from osmaxx.excerptexport import models
from osmaxx.utils import private_storage


NAME = 'GIS'
EXPORT_FORMATS = {
    'spatialite': {
        'name': 'SpatiaLite (SQLite)',
        'file_extension': 'sqlite'
    },
    'gpkg': {
        'name': 'Geo package',
        'file_extension': 'gpkg'
    },
    'shp': {
        'name': 'Shape file',
        'file_extension': 'shp'
    }
}
EXPORT_OPTIONS = {
    # has to be implemented next:
    # 'coordinate_reference_system': {
    #     'label': 'Coordinate reference system',
    #     'type': 'choice',
    #     'default': 'pseudomerkator',
    #     'groups': [
    #         {
    #             'name': 'Global coordinate reference systems',
    #             'values': [
    #                 {'name': 'pseudomerkator', 'label': 'Pseudo merkator'},
    #                 {'name': 'wgs72', 'label': 'WGS 72'},
    #                 {'name': 'wgs84', 'label': 'WGS 84'}
    #             ]
    #         },
    #         {
    #             'name': 'UTM zones for your export',
    #             'values': [
    #                 {'name': 'utm32', 'label': 'UTM zone 32'},
    #                 {'name': 'utm33', 'label': 'UTM zone 33'}
    #             ]
    #         }
    #     ]
    # },
    # 'detail_level': {
    #     'label': 'Detail level',
    #     'type': 'choice',
    #     'default': 'verbatim',
    #     'values': [
    #         {'name': 'verbatim', 'label': 'Verbatim'},
    #         {'name': 'simplified', 'label': 'Simplified'}
    #     ]
    # }
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


def extract_excerpts(execution_configuration, extraction_order, bbox_args, converter_helper):
    """
    Extract excerpt for chosen formats (execution_configuration) using docker-compose
    to trigger the conversion process (defined in blackbox/docker-compose-conversion-blackbox.yml)

    :param execution_configuration: example
        {
            'formats': ['txt', 'file_gdb'],
            'options': {
                'coordinate_reference_system': 'wgs72',
                'detail_level': 'verbatim'
            }
        }
    :param extraction_order:
    :param bbox_args example: '8.775449276 47.1892350573 8.8901920319 47.2413633153'
    :return:
    """
    for export_format_key, export_format_config in EXPORT_FORMATS.items():
        index = 0
        if export_format_key in execution_configuration['formats']:
            index += 1
            extraction_command = "docker-compose run --rm excerpt python excerpt.py {bbox_args} -f {format}"\
                .format(bbox_args=bbox_args, format=export_format_key)
            subprocess.check_call(extraction_command.split(' '))

            if len(os.listdir(settings.RESULT_MEDIA_ROOT)) > 0:
                for result_file_name in os.listdir(settings.RESULT_MEDIA_ROOT):
                    # gis files are packaged in a zip file
                    if create_output_file(
                            extraction_order, result_file_name, export_format_key):
                        converter_helper.inform_user(
                            messages.SUCCESS,
                            _('Extraction of "{file_type}" of extraction order "{order_id}" was successful. '
                              '(of {number_of_files} files of {converter_name} converter)').format(
                                file_type=export_format_config['name'],
                                file_index=index,
                                number_of_files=len(execution_configuration['formats']),
                                converter_name=NAME,
                                order_id=extraction_order.id
                            ),
                            email=False
                        )
                    else:
                        converter_helper.inform_user(
                            messages.ERROR,
                            _('The extraction of "{file}" of extraction order "{order_id}" failed.').format(
                                file=result_file_name,
                                order_id=extraction_order.id
                            ),
                            email=False
                        )
            else:
                converter_helper.inform_user(
                    messages.ERROR,
                    _('The extraction of "{file_type}" of extraction order "{order_id}" failed.').format(
                        file_type=export_format_config['name'],
                        order_id=extraction_order.id
                    ),
                    email=False
                )


def create_output_file(extraction_order, result_file_name, export_format_key):
    """
    Move file to private media storage and add OutputFile to Extractionorder

    :return: True if file created successful
    """
    output_file = models.OutputFile.objects.create(
        mime_type='application/zip',
        file_extension='zip',
        content_type=export_format_key,
        extraction_order=extraction_order
    )

    if not os.path.exists(private_storage.location):
        os.makedirs(private_storage.location)

    file_name = str(output_file.public_identifier) + '.zip'
    result_file_path = os.path.abspath(os.path.join(settings.RESULT_MEDIA_ROOT, result_file_name))
    target_file_path = os.path.abspath(os.path.join(private_storage.location, file_name))

    shutil.move(result_file_path, target_file_path)
    output_file.file = private_storage.open(target_file_path)
    output_file.save()
    # remove temporary file in private_storage
    # (file.save will copy the original file and add an random hash to the name)
    private_storage.delete(target_file_path)

    return (not os.path.isfile(target_file_path)) and private_storage.exists(output_file.file)


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

    converter_helper = ConverterHelper(extraction_order)
    extraction_order.state = models.ExtractionOrderState.WAITING
    extraction_order.save()

    with tempfile.TemporaryDirectory() as tmp_dir:
        original_cwd = os.getcwd()

        try:
            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), 'blackbox', 'docker-compose-conversion-blackbox.yml'),
                os.path.join(tmp_dir, 'docker-compose.yml')
            )
            os.chdir(tmp_dir)
            # use newest images
            subprocess.check_output("docker-compose pull".split(' '))
            # database needs to be ready
            subprocess.check_output("docker-compose up -d db".split(' '))
            # wait for the db to be up
            subprocess.check_output("sleep 10".split(' '))

            converter_helper.inform_user(
                messages.INFO,
                _('The GIS extraction of the order "{order_id}" is has been started.').format(
                    order_id=extraction_order.id
                ),
                email=False
            )

            bounding_geometry = extraction_order.excerpt.bounding_geometry
            if type(bounding_geometry) == models.BBoxBoundingGeometry:
                bbox_args = ' '.join(str(coordinate) for coordinate in [
                    bounding_geometry.west,
                    bounding_geometry.south,
                    bounding_geometry.east,
                    bounding_geometry.north
                ])

                if len(execution_configuration['formats']) > 0:
                    subprocess.check_call(("docker-compose run --rm bootstrap sh main-bootstrap.sh {bbox_args}".format(
                        bbox_args=bbox_args
                    )).split(' '))
                    extraction_order.state = models.ExtractionOrderState.PROCESSING
                    extraction_order.save()
                    extract_excerpts(
                        execution_configuration,
                        extraction_order,
                        bbox_args,
                        converter_helper
                    )

            elif type(bounding_geometry) == models.OsmosisPolygonFilterBoundingGeometry:
                converter_helper.inform_user(
                    messages.ERROR,
                    _('GIS excerpt converter is not yet able to extract polygon excerpts.'),
                    email=False
                )

            else:
                converter_helper.inform_user(
                    messages.ERROR,
                    _('GIS excerpt converter is not yet able to extract excerpts of type {type}.').format(
                        type=type(bounding_geometry).__name__
                    ),
                    email=False
                )
            converter_helper.file_conversion_finished()
        except:
            extraction_order.state = models.ExtractionOrderState.FAILED
            extraction_order.save()

            converter_helper.inform_user(
                messages.ERROR,
                _('The extraction of order {order_id} failed. Please contact an administrator.').format(
                    order_id=extraction_order.id
                ),
                email=False
            )
            raise
        finally:
            try:
                subprocess.check_call("docker-compose stop --timeout 0".split(' '))
                subprocess.check_call("docker-compose rm -v -f".split(' '))
            except:
                pass
            os.chdir(original_cwd)
