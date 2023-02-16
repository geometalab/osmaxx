import json

import pytest

from osmaxx.excerptexport.rest_api import views as api_views
from rest_framework.test import APIRequestFactory


@pytest.fixture
def bbox_edges():
    return {
        bound: "{0}_value".format(bound) for bound in ["west", "south", "east", "north"]
    }


@pytest.fixture
def _request(bbox_edges):
    factory = APIRequestFactory()
    request = factory.get("/estimated_file_size/", bbox_edges)
    return request
