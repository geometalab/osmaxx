import requests
import json
import logging

from osmaxx.excerptexport.models import ExtractionOrderState

logger = logging.getLogger(__name__)


class RestClient():
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

    def create_url(self, path):
            return self.protocol + '://' + self.host + ':' + (self.port if self.port else '') + path

    def login(self):
        request_url = self.create_url(self.api_paths['login'])
        request_data = self.credentials

        response = requests.post(request_url, data=json.dumps(request_data), headers=self.headers)

        if response.status_code == 200 and response.json() and \
           'token' in response.json() and len(response.json()['token']) > 0:
            self.headers['Authorization'] = 'JWT ' + response.json()['token']
            self.is_logged_in = True
            return True
        else:
            logging.error('API login failed.', response)
            return False

    def create_job(self, extraction_order):
        if not self.is_logged_in:
            raise Exception('Not logged in for request')

        request_url = self.create_url(self.api_paths['job']['create'])
        request_data = {
            "callback_url": "http://example.com",
            "gis_formats": extraction_order.extraction_configuration['gis']['formats'],
            "gis_options": extraction_order.extraction_configuration['gis']['options'],
            "extent": {
                "west": extraction_order.excerpt.bounding_geometry.west,
                "south": extraction_order.excerpt.bounding_geometry.south,
                "east": extraction_order.excerpt.bounding_geometry.east,
                "north": extraction_order.excerpt.bounding_geometry.north,
                "polyfile": None
            }
        }

        response = requests.post(request_url, data=json.dumps(request_data), headers=self.headers)

        if response.status_code == 200 and response.json() and 'rq_job_id' in response.json():
            response_content = response.json()
            extraction_order.process_id = response_content['rq_job_id']
            extraction_order.state = ExtractionOrderState.PROCESSING
            return True
        else:
            logging.error('API job creation failed.', response)
            return False
