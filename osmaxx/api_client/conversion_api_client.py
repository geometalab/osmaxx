import json
import logging
from collections import OrderedDict

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from requests import HTTPError
from rest_framework.reverse import reverse

from osmaxx.api_client.API_client import JWTClient, reasons_for
from osmaxx.excerptexport.models import ExtractionOrderState, OutputFile
from osmaxx.utils import get_default_private_storage

logger = logging.getLogger(__name__)

COUNTRY_ID_PREFIX = 'country-'
SERVICE_BASE_URL = settings.OSMAXX.get('CONVERSION_SERVICE_URL')
LOGIN_URL = '/token-auth/'

USERNAME = settings.OSMAXX.get('CONVERSION_SERVICE_USERNAME')
PASSWORD = settings.OSMAXX.get('CONVERSION_SERVICE_PASSWORD')

CONVERSION_JOB_URL = '/jobs/'
ESTIMATED_FILE_SIZE_URL = '/estimate_size_in_bytes/'


class ConversionApiClient(JWTClient):
    def __init__(self):
        super().__init__(
            service_base=SERVICE_BASE_URL,
            login_url=LOGIN_URL,
            username=USERNAME,
            password=PASSWORD,
        )

    def create_boundary(self, multipolygon, *, name):
        geo_json = json.loads(multipolygon.json)
        json_payload = dict(name=name, clipping_multi_polygon=geo_json)
        response = self.authorized_post(url='clipping_area/', json_data=json_payload)
        return response.json()

    def create_parametrization(self, *, boundary, out_format, out_srs):
        """

        Args:
            boundary: A dictionary as returned by create_boundary
            out_format: A string identifying the output format
            out_srs: A string identifying the spatial reference system of the output

        Returns:
            A dictionary representing the payload of the service's response
        """
        json_payload = dict(clipping_area=boundary['id'], out_format=out_format, out_srs=out_srs)
        response = self.authorized_post(url='conversion_parametrization/', json_data=json_payload)
        return response.json()

    def create_job(self, parametrization, callback_url):
        """

        Args:
            parametrization: A dictionary as returned by create_parametrization
            incoming_request: The request towards the front-end triggering this job creation

        Returns:
            A dictionary representing the payload of the service's response
        """
        json_payload = dict(parametrization=parametrization['id'], callback_url=callback_url)
        response = self.authorized_post(url='conversion_job/', json_data=json_payload)
        return response.json()

    @staticmethod
    def _extraction_processing_overdue(progress, extraction_order):
        if extraction_order.process_start_time is None:
            return None
        process_unfinished = progress in ['new', 'received', 'started']
        timeout_reached = timezone.now() > extraction_order.process_due_time
        return process_unfinished and timeout_reached

    # TODO: replace this by a call to extraction_order.forward_to_conversion_service(request)
    def _create_job_TODO_replace_me(self, extraction_order, request):  # noqa
        """
        Kickoff a conversion job

        Args:
            extraction_order: an ExtractionOrder object
                extraction_order.extraction_configuration is directly used for the api
                -> must be in a compatible format

        Returns:
            response of the call
        """
        if hasattr(extraction_order.excerpt, 'bounding_geometry'):
            bounding_geometry = extraction_order.excerpt.bounding_geometry.subclass_instance
        else:
            bounding_geometry = None

        request_data = OrderedDict({
            "callback_url": request.build_absolute_uri(
                reverse('job_progress:tracker', kwargs=dict(order_id=extraction_order.id))
            ),
            "gis_formats": extraction_order.extraction_formats,
            "gis_options": extraction_order.extraction_configuration['gis_options'],
            "extent": {
                "west": bounding_geometry.west if bounding_geometry else None,
                "south": bounding_geometry.south if bounding_geometry else None,
                "east": bounding_geometry.east if bounding_geometry else None,
                "north": bounding_geometry.north if bounding_geometry else None,
                "country": extraction_order.country_id,
            }
        })
        try:
            response = self.authorized_post(CONVERSION_JOB_URL, json_data=request_data)
        except HTTPError as e:
            logging.error('API job creation failed.', e.response)
            return e.response
        rq_job_id = response.json().get('rq_job_id', None)
        if rq_job_id:
            extraction_order.process_id = rq_job_id
            extraction_order.process_start_time = timezone.now()
            extraction_order.progress_url = response.json()['status']
            extraction_order.state = ExtractionOrderState.QUEUED
            extraction_order.save()
        else:
            logging.error('Could not retrieve api job id from response.', response)
        return response

    def _download_result_files(self, extraction_order, job_status):
        """
        Downloads the result files if the conversion was finished,
        stores the files into the private storage and attaches them as output files to the extraction order

        Args:
            extraction_order: an ExtractionOrder object to attach the output files
            job_status: the job status from the conversion api
        """
        with transaction.atomic():
            extraction_order.refresh_from_db()
            if extraction_order.download_status == extraction_order.DOWNLOAD_STATUS_NOT_DOWNLOADED:
                extraction_order.download_status = extraction_order.DOWNLOAD_STATUS_DOWNLOADING
                extraction_order.save()
                for download_file in job_status['gis_formats']:
                    assert download_file['progress'] == 'successful'
                    self._download_file(download_file, extraction_order)
                extraction_order.download_status = extraction_order.DOWNLOAD_STATUS_AVAILABLE
                extraction_order.save()

    def _download_file(self, download_file_dict, extraction_order):
        result_response = self.authorized_get(download_file_dict['result_url'])
        output_file = OutputFile.objects.create(
            mime_type='application/zip',
            file_extension='zip',
            content_type=download_file_dict['format'],
            extraction_order=extraction_order,
        )
        file_name = str(output_file.public_identifier) + '.zip'
        output_file.file = get_default_private_storage().save(file_name, ContentFile(result_response.content))
        output_file.save()

    def job_status(self, extraction_order):
        """
        Get the status of the conversion job

        Args:
            extraction_order: an ExtractionOrder object containing a process id

        Returns:
            A status dict on success like:
                {
                    "rq_job_id": "4b529c79-559c-4730-9cd2-03ea91c9a5ef",
                    "status": "done",
                    "progress": "successful",
                    "gis_formats": [
                        {
                            "format": "fgdb",
                            "progress": "successful",
                            "result_url": "http://<conversion service host>:8901/api/gis_format/11/download_result/"
                        },
                        {
                            "format": "spatialite",
                            "progress": "successful",
                            "result_url": "http://<conversion service host>:8901/api/gis_format/12/download_result/"
                        }
                    ]
                }
            False on error
        """
        if not extraction_order.progress_url:  # None or empty
            return None
        try:
            response = self.authorized_get(url=extraction_order.progress_url)
        except HTTPError:
            return None
        return response.json()

    def update_order_status(self, extraction_order):
        """
        Update the status of the extraction order by the status of the conversion job

        Args:
            extraction_order: an ExtractionOrder object to update the state
        """
        job_status = self.job_status(extraction_order)

        if job_status:
            progress = job_status['progress']
            extraction_order.set_status_from_conversion_progress(progress)
            extraction_order.save()
            if progress == 'successful':
                self._download_result_files(extraction_order, job_status)
            elif self._extraction_processing_overdue(progress, extraction_order):
                logger.warning(
                    'Extraction order %s processing timeout overdue. Set status to FAILED.',
                    extraction_order.id,
                )
                extraction_order.state = ExtractionOrderState.FAILED
                extraction_order.save()

    def estimated_file_size(self, north, west, south, east):
        request_data = {
            "west": west,
            "south": south,
            "east": east,
            "north": north
        }
        try:
            response = self.authorized_post(ESTIMATED_FILE_SIZE_URL, json_data=request_data)
        except HTTPError as e:
            return reasons_for(e)
        return response.json()
