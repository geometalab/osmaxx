import json
import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from requests import HTTPError

from osmaxx.api_client.API_client import JWTClient, reasons_for, LazyChunkedRemoteFile
from osmaxx.excerptexport.models import OutputFile
from osmaxx.utils import get_default_private_storage

logger = logging.getLogger(__name__)

SERVICE_BASE_URL = settings.OSMAXX.get('CONVERSION_SERVICE_URL')
LOGIN_URL = '/token-auth/'

USERNAME = settings.OSMAXX.get('CONVERSION_SERVICE_USERNAME')
PASSWORD = settings.OSMAXX.get('CONVERSION_SERVICE_PASSWORD')

OLD_CONVERSION_JOB_URL = '/jobs/'  # TODO: remove
CONVERSION_JOB_URL = '/conversion_job/'
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

    def get_result_file(self, job_id):
        download_url = self._get_result_file_url(job_id)
        if download_url:
            return LazyChunkedRemoteFile(download_url, download_function=self.authorized_get)
        else:
            raise ResultFileNotAvailableError

    def _get_result_file_url(self, job_id):
        job_detail_url = CONVERSION_JOB_URL + '{}/'.format(job_id)
        return self.authorized_get(job_detail_url).json()['resulting_file']

    @staticmethod
    def _extraction_processing_overdue(progress, extraction_order):
        if extraction_order.process_start_time is None:
            return None
        process_unfinished = progress in ['new', 'received', 'started']
        timeout_reached = timezone.now() > extraction_order.process_due_time
        return process_unfinished and timeout_reached

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

    def job_status(self, export):
        """
        Get the status of the conversion job

        Args:
            export: an Export object

        Returns:
            The status of the associated job

        Raises:
            AssertionError: If `export` has no associated job
        """
        assert isinstance(export.conversion_service_job_id, int)
        response = self.authorized_get(url='conversion_job/{}'.format(export.conversion_service_job_id))
        return response.json()['status']

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


class ResultFileNotAvailableError(RuntimeError):
    pass
