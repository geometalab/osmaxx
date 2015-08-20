import os
import shutil
import subprocess
import tempfile
import time

from celery import shared_task

from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from excerptconverter.baseexcerptconverter import BaseExcerptConverter

from osmaxx.excerptexport import models


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
        for export_format_key, export_format_config in GisExcerptConverter.export_formats():
            if export_format_key in execution_configuration['formats']:
                extraction_command = "docker-compose run excerpt python excerpt.py %(bbox_args)s -f %(format)s" % {
                    'bbox_args':  bbox_args,
                    'format': export_format_key
                }
                subprocess.check_call(extraction_command.split(' '))

                BaseExcerptConverter.inform_user(
                    extraction_order.orderer,
                    messages.SUCCESS,
                    _('The extraction of "%(file_type)s" of order "%(extraction_order)s") was successful.') % {
                        'file_type': export_format_config['name'],
                        'extraction_order': extraction_order
                    },
                    False
                )

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

        with tempfile.TemporaryDirectory() as tmp_dir:
            original_cwd = os.getcwd()

            try:
                print(tmp_dir)
                shutil.copyfile(
                    os.path.join(os.path.dirname(__file__), 'blackbox', 'docker-compose-conversion-blackbox.yml'),
                    os.path.join(tmp_dir, 'docker-compose.yml')
                )
                os.chdir(tmp_dir)
                subprocess.check_call("docker-compose build".split(' '))
                # database needs time to be ready
                subprocess.check_output("docker-compose run bootstrap sleep 10".split(' '))

                BaseExcerptConverter.inform_user(
                    extraction_order.orderer,
                    messages.INFO,
                    _('The extraction of the order "%s" is ready to start.') % extraction_order,
                    False
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

                    subprocess.check_call(("docker-compose run bootstrap sh main-bootstrap.sh %s" %
                                           bbox_args).split(' '))
                    GisExcerptConverter.extract_excerpts(execution_configuration, extraction_order, bbox_args)

                elif type(bounding_geometry) == models.OsmosisPolygonFilterBoundingGeometry:
                    BaseExcerptConverter.inform_user(
                        extraction_order.orderer,
                        messages.ERROR,
                        _('GIS excerpt converter is not yet able to extract polygon excerpts.'),
                        False
                    )

                else:
                    BaseExcerptConverter.inform_user(
                        extraction_order.orderer,
                        messages.ERROR,
                        _('GIS excerpt converter is not yet able to extract excerpts of type %s.') %
                        type(bounding_geometry).__name__,
                        False
                    )

                subprocess.check_call("docker-compose stop --timeout 0".split(' '))
                subprocess.check_call("docker-compose rm -f".split(' '))

                BaseExcerptConverter.inform_user(
                    extraction_order.orderer,
                    messages.INFO,
                    _('The extraction of the order "%s" has been finished.') % extraction_order,
                    False
                )
            except:
                BaseExcerptConverter.inform_user(
                    extraction_order.orderer,
                    messages.ERROR,
                    _('The extraction of order %s failed. Please contact an administrator.') % extraction_order,
                    False
                )
                raise
            finally:
                os.chdir(original_cwd)
