import os
import shutil
import subprocess
import tempfile
import time

from celery import shared_task

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from excerptconverter.baseexcerptconverter import BaseExcerptConverter
from excerptconverter.converter_helper import inform_user, file_conversion_finished

from osmaxx.excerptexport import models
from osmaxx.utils import private_storage


class GisExcerptConverter(BaseExcerptConverter):
    @staticmethod
    def name():
        return 'GIS'

    @staticmethod
    def export_formats():
        return {
            'spatialite': {
                'name': 'SpatiaLite (SQLite)',
                'file_extension': 'sqlite',
                'mime_type': 'application/x-sqlite3'
            },
            'gpkg': {
                'name': 'Geo package',
                'file_extension': 'gpkg',
                'mime_type': 'application/octet-stream'  # Not verified!
            },
            'shp': {
                'name': 'Shape file',
                'file_extension': 'shp',
                'mime_type': 'application/octet-stream'  # Not verified!
            }
        }

    @staticmethod
    def export_options():
        return {
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

    @staticmethod
    def extract_excerpts(execution_configuration, extraction_order, bbox_args):
        """
        Extract excerpt for chosen formats (execution_configuration) using docker-compose
        to trigger the conversion process (defined in blackbox/docker-compose-conversion-blackbox.yml)

        :param execution_configuration:
        :param extraction_order:
        :param bbox_args example: '8.775449276 47.1892350573 8.8901920319 47.2413633153'
        :return:
        """
        for export_format_key, export_format_config in GisExcerptConverter.export_formats().items():
            index = 0
            if export_format_key in execution_configuration['formats']:
                index += 1
                extraction_command = "docker-compose run excerpt python excerpt.py %(bbox_args)s -f %(format)s" % {
                    'bbox_args':  bbox_args,
                    'format': export_format_key
                }
                subprocess.check_call(extraction_command.split(' '))

                if len(os.listdir(settings.RESULT_MEDIA_ROOT)) > 0:
                    for result_file_name in os.listdir(settings.RESULT_MEDIA_ROOT):
                        # gis files are packaged in a zip file
                        if GisExcerptConverter.create_output_file(extraction_order, result_file_name):
                            inform_user(
                                extraction_order.orderer,
                                messages.SUCCESS,
                                _('Extraction of "%(file_type)s" of extraction order "%(order_id)s" was successful. '
                                  '(File %(file_index)s of %(number_of_files)s of %(converter_name)s converter)') % {
                                    'file_type': export_format_config['name'],
                                    'file_index': index,
                                    'number_of_files': len(execution_configuration['formats']),
                                    'converter_name': GisExcerptConverter.name(),
                                    'order_id': extraction_order.id
                                },
                                email=False
                            )
                        else:
                            inform_user(
                                extraction_order.orderer,
                                messages.ERROR,
                                _('The extraction of "%(file)s" of extraction order "%(order_id)s" failed.') % {
                                    'file': result_file_name,
                                    'order_id': extraction_order.id
                                },
                                email=False
                            )
                else:
                    inform_user(
                        extraction_order.orderer,
                        messages.ERROR,
                        _('The extraction of "%(file_type)s" of extraction order "%(order_id)s" failed.') % {
                            'file_type': export_format_config['name'],
                            'order_id': extraction_order.id
                        },
                        email=False
                    )

    @staticmethod
    def create_output_file(extraction_order, result_file_name):
        """
        Move file to private media storage and add OutputFile to Extractionorder

        :return: True if file created successful
        """
        output_file = models.OutputFile.objects.create(
            mime_type='application/zip',
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

        return os.path.isfile(target_file_path)

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

        extraction_order.state = models.ExtractionOrderState.WAITING
        extraction_order.save()

        with tempfile.TemporaryDirectory() as tmp_dir:
            original_cwd = os.getcwd()

            try:
                print(tmp_dir)
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

                inform_user(
                    extraction_order.orderer,
                    messages.INFO,
                    _('The GIS extraction of the order "%s" is has been started.') % extraction_order.id,
                    email=False
                )

                bounding_geometry = extraction_order.excerpt.bounding_geometry
                if type(bounding_geometry) == models.BBoxBoundingGeometry:
                    bbox_args = '%(excerpt_south_border)s %(excerpt_west_border)s %(excerpt_north_border)s ' \
                        '%(excerpt_east_border)s' % {
                            'excerpt_north_border': bounding_geometry.north,
                            'excerpt_west_border': bounding_geometry.west,
                            'excerpt_south_border': bounding_geometry.south,
                            'excerpt_east_border': bounding_geometry.east
                        }

                    if len(execution_configuration['formats']) > 0:
                        subprocess.check_call(("docker-compose run bootstrap sh main-bootstrap.sh %s" %
                                               bbox_args).split(' '))
                        extraction_order.state = models.ExtractionOrderState.PROCESSING
                        extraction_order.save()
                        GisExcerptConverter.extract_excerpts(
                            execution_configuration,
                            extraction_order,
                            bbox_args
                        )

                elif type(bounding_geometry) == models.OsmosisPolygonFilterBoundingGeometry:
                    inform_user(
                        extraction_order.orderer,
                        messages.ERROR,
                        _('GIS excerpt converter is not yet able to extract polygon excerpts.'),
                        email=False
                    )

                else:
                    inform_user(
                        extraction_order.orderer,
                        messages.ERROR,
                        _('GIS excerpt converter is not yet able to extract excerpts of type %s.') %
                        type(bounding_geometry).__name__,
                        email=False
                    )

                subprocess.check_call("docker-compose stop --timeout 0".split(' '))
                subprocess.check_call("docker-compose rm -vf".split(' '))

                file_conversion_finished(extraction_order.orderer)
            except:
                extraction_order.state = models.ExtractionOrderState.FAILED
                extraction_order.save()

                inform_user(
                    extraction_order.orderer,
                    messages.ERROR,
                    _('The extraction of order %(order_id)s failed. '
                      'Please contact an administrator.') % {
                        'order_id': extraction_order.id
                    },
                    email=False
                )
                raise
            finally:
                os.chdir(original_cwd)
