import json
import logging

from django.conf import settings
from requests import HTTPError

from osmaxx.api_client.API_client import JWTClient, reasons_for, LazyChunkedRemoteFile

logger = logging.getLogger(__name__)

SERVICE_BASE_URL = settings.OSMAXX.get('CONVERSION_SERVICE_URL')
LOGIN_URL = '/token-auth/'

USERNAME = settings.OSMAXX.get('CONVERSION_SERVICE_USERNAME')
PASSWORD = settings.OSMAXX.get('CONVERSION_SERVICE_PASSWORD')

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
