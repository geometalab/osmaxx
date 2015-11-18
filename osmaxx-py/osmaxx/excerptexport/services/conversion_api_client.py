import logging
from collections import OrderedDict
from django.conf import settings
from django.core.files.base import ContentFile

from osmaxx.api_client.API_client import RESTApiJWTClient
from osmaxx.excerptexport.models import ExtractionOrderState, OutputFile
from osmaxx.utils import private_storage

logger = logging.getLogger(__name__)


class ConversionApiClient(RESTApiJWTClient):
    service_base = settings.OSMAXX.get('CONVERSION_SERVICE_URL')
    login_url = '/token-auth/'

    username = settings.OSMAXX.get('CONVERSION_SERVICE_USERNAME')
    password = settings.OSMAXX.get('CONVERSION_SERVICE_PASSWORD')

    conversion_job_url = '/jobs/'
    conversion_job_status_url = '/conversion_result/{job_uuid}/'

    def login(self):
        """
        Logs in the api client by requesting an API token

        Returns:
            the response
            errors: None if successfull, dictionary with error list on failed login
        """
        if self.token:
            # already logged in
            return True

        self.auth(self.username, self.password)

        if not self.errors:
            return True
        return False

    def create_job(self, extraction_order):
        """
        Kickoff a conversion job

        Args:
            extraction_order: an ExtractionOrder object
                extraction_order.extraction_configuration is directly used for the api
                -> must be in a compatible format

        Returns:
            response of the call
        """
        bounding_geometry = extraction_order.excerpt.bounding_geometry.subclass_instance

        request_data = OrderedDict({
            "callback_url": "http://example.com",
            "gis_formats": extraction_order.extraction_configuration['gis_formats'],
            "gis_options": extraction_order.extraction_configuration['gis_options'],
            "extent": {
                "west": bounding_geometry.west,
                "south": bounding_geometry.south,
                "east": bounding_geometry.east,
                "north": bounding_geometry.north,
                "polyfile": None
            }
        })
        self.login()
        response = self.authorized_post(self.conversion_job_url, json_data=request_data)
        if self.errors:
            logging.error('API job creation failed.', response)
        else:
            rq_job_id = response.json().get('rq_job_id', None)
            if rq_job_id:
                extraction_order.process_id = rq_job_id
                extraction_order.state = ExtractionOrderState.PROCESSING
                extraction_order.save()
            else:
                logging.error('Could not retrieve api job id from response.', response)
        return response

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
        self.login()
        job_status = self.job_status(extraction_order)
        if job_status and job_status['status'] == 'done' and job_status['progress'] == 'successful':
            for download_file in job_status['gis_formats']:
                if download_file['progress'] == 'successful':
                    result_response = self.authorized_get(download_file['result_url'])
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
        self.login()
        response = self.authorized_get(self.conversion_job_status_url.format(job_uuid=extraction_order.process_id))

        if not self.errors:
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


def get_authenticated_api_client():
    """
    Helper method to get an authenticated ConversionApiClient instance.

    :return:
    """
    conversion_api_client = ConversionApiClient()
    conversion_api_client.login()
    return conversion_api_client
