import requests
import json
import logging
from collections import OrderedDict

from django.core.files.base import ContentFile

from osmaxx.excerptexport.models import ExtractionOrderState, OutputFile
from osmaxx.utils import private_storage

logger = logging.getLogger(__name__)


class ConversionApiClient():
    def __init__(self, protocol, host, port, api_paths, credentials):
        """
        Args:
            protocol:       e.g. 'http'
            host:           e.g. 'www.osmaxx.ch'
            port:           e.g. '8000'
            api_paths:      e.g.
                {
                    'login': '/api/token-auth/?format=json'
                    'job': {
                        'create': '/api/jobs'
                        'status': '/api/conversion_result/{rq_job_id}'
                    }
                }
            credentials:    e.g.
                {'username':'osmaxx', 'password':'osmaxx'}
        """
        self.protocol = protocol
        self.host = host
        self.port = port
        self.api_paths = api_paths
        self.credentials = credentials
        self.is_logged_in = False

        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def _create_url(self, path):
            return self.protocol + '://' + self.host + ':' + (self.port if self.port else '') + path

    def _request_successful(self, response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.error('API job creation failed.', str(e) + " response: " + str(response.__dict__))
            return False
        return True

    def _extract_key_from_json_or_none(self, response, key):
        if self._request_successful(response):
            try:
                json_response = response.json()
                return json_response.get(key, None)
            except ValueError:
                logging.error('API job creation failed because of an JSON decoding Issue.', str(response.__dict__))
                return None
        return None

    def login(self):
        """
        Logs in the api client by requesting an API token

        Returns:
            True on successful login
            False on failed login
        """
        request_url = self._create_url(self.api_paths['login'])
        request_data = self.credentials

        response = requests.post(request_url, data=json.dumps(request_data), headers=self.headers)

        token = self._extract_key_from_json_or_none(response, 'token')
        if token and len(token) > 0:
            self.headers['Authorization'] = 'JWT ' + token
            self.is_logged_in = True
            return True
        else:
            logging.error('API login failed.', response)
            return False

    def create_job(self, extraction_order):
        """
        Kickoff a conversion job

        Args:
            extraction_order: an ExtractionOrder object
                extraction_order.extraction_configuration is directly used for the api
                -> must be in a compatible format

        Returns:
            True on successful job creation
            False on error

        Raises:
            Exception if the client is not logged in
        """
        if not self.is_logged_in:
            raise Exception('Not logged in for request')

        request_url = self._create_url(self.api_paths['job']['create'])
        request_data = OrderedDict({
            "callback_url": "http://example.com",
            "gis_formats": extraction_order.extraction_configuration['gis_formats'],
            "gis_options": extraction_order.extraction_configuration['gis_options'],
            "extent": {
                "west": extraction_order.excerpt.bounding_geometry.west,
                "south": extraction_order.excerpt.bounding_geometry.south,
                "east": extraction_order.excerpt.bounding_geometry.east,
                "north": extraction_order.excerpt.bounding_geometry.north,
                "polyfile": None
            }
        })

        response = requests.post(request_url, data=json.dumps(request_data), headers=self.headers)

        rq_job_id = self._extract_key_from_json_or_none(response, 'rq_job_id')
        if rq_job_id:
            extraction_order.process_id = rq_job_id
            extraction_order.state = ExtractionOrderState.PROCESSING
            extraction_order.save()
            return True
        else:
            logging.error('API job creation failed.', response)
            return False

    def download_result_files(self, extraction_order):
        """
        Downloads the result files if the conversion was finished,
        stores the files into the private storage and attaches them as output files to the extraction order

        Args:
            extraction_order: an ExtractionOrder object to attach the output files

        Returns:
            True if the job status was fetched successful
            False if it failed
        """
        job_status = self.job_status(extraction_order)

        if job_status and job_status['status'] == 'done' and job_status['progress'] == 'successful':
            for download_file in job_status['gis_formats']:
                if download_file['progress'] == 'successful':
                    result_response = requests.get(download_file['result_url'], headers=self.headers)
                    output_file = OutputFile.objects.create(
                        mime_type='application/zip',
                        file_extension='zip',
                        content_type=download_file['format'],
                        extraction_order=extraction_order
                    )

                    file_name = str(output_file.public_identifier) + '.zip'
                    output_file.file = private_storage.save(file_name, ContentFile(result_response.content))
                    output_file.save()
            return True
        else:
            return False

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
                            "result_url": "http://localhost:8000/api/gis_format/11/download_result/"
                        },
                        {
                            "format": "spatialite",
                            "progress": "successful",
                            "result_url": "http://localhost:8000/api/gis_format/12/download_result/"
                        }
                    ]
                }
            False on error
        """
        if not self.is_logged_in:
            raise Exception('Not logged in for request')

        request_url = self._create_url(
            self.api_paths['job']['status'].replace('{rq_job_id}', extraction_order.process_id)
        )
        response = requests.get(request_url, headers=self.headers)

        if self._request_successful(response):
            return response.json()
        else:
            return None

    def update_order_status(self, extraction_order):
        """
        Update the status of the extraction order by the status of the conversion job

        Args:
            extraction_order: an ExtractionOrder object to update the state

        Returns:
            True if the job status was fetched successful
            False if it failed
        """
        job_status = self.job_status(extraction_order)

        if job_status:
            if job_status['status'] == 'done' and job_status['progress'] == 'successful':
                if not extraction_order.state == ExtractionOrderState.FINISHED and \
                   not extraction_order.state == ExtractionOrderState.FAILED:
                    self.download_result_files(extraction_order)
                    extraction_order.state = ExtractionOrderState.FINISHED
                    extraction_order.save()
            elif job_status['status'] == 'started':
                extraction_order.state = ExtractionOrderState.PROCESSING
                extraction_order.save()
            return True
        else:
            return False


def get_api_client():
    """
    Helper method to get a ConversionApiClient instance with setting defaults.

    :return:
    """
    from django.conf import settings
    protocol = settings.OSMAXX.get('CONVERSION_SERVICE_PROTOCOL', 'http')
    host = settings.OSMAXX.get('CONVERSION_SERVICE_HOST', 'localhost')
    port = settings.OSMAXX.get('CONVERSION_SERVICE_PORT', '8901')
    api_paths = settings.OSMAXX.get('CONVERSION_SERVICE_API_PATHS', {
        'login': '/api/token-auth/?format=json',
        'job': {
            'create': '/api/jobs',
            'status': '/api/conversion_result/{rq_job_id}',
        }
    })
    credentials = settings.OSMAXX.get('CONVERSION_SERVICE_CREDENTIALS', {'username': 'admin', 'password': 'admin'})

    conversion_api_client = ConversionApiClient(
        protocol=protocol, host=host, port=port, api_paths=api_paths, credentials=credentials
    )
    return conversion_api_client


def get_authenticated_api_client():
    """
    Helper method to get an authenticated ConversionApiClient instance with setting defaults.

    :return:
    """
    conversion_api_client = get_api_client()
    conversion_api_client.login()
    return conversion_api_client
