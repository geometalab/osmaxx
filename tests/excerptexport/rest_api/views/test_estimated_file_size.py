import json

import pytest

from osmaxx.api_client import ConversionHelper
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


def test_estimated_file_size_view_calls_api_client_with_boundaries(
    _request, bbox_edges
):
    api_views.estimated_file_size(_request)
    ConversionHelper.estimated_file_size.assert_called_with(**bbox_edges)


def test_estimated_file_size_view_returns_response_with_size_returned_by_api_client(
    _request,
):
    response = api_views.estimated_file_size(_request)
    assert response.status_code == 200
    assert json.dumps(ConversionHelper.estimated_file_size.return_value) in str(
        response.content
    )


@pytest.fixture(autouse=True)
def mock_conversion_api_client_estimated_file_size(mocker):
    mocker.patch.object(
        ConversionHelper, "estimated_file_size", return_value="estimated_size_value"
    )
