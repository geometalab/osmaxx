import json
from unittest.mock import ANY, sentinel

import pytest
from django.contrib.gis.gdal.geometries import MultiPolygon
from hamcrest import assert_that, contains_inanyorder

from osmaxx.api_client.conversion_api_client import ConversionHelper


def test_create_boundary_makes_authorized_post_with_json_payload(
    mocker, geos_multipolygon
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    c.authorized_post.assert_called_once_with(url=ANY, json_data=ANY)


def test_create_boundary_posts_to_clipping_area_resource(mocker, geos_multipolygon):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    args, kwargs = c.authorized_post.call_args
    assert kwargs["url"] == "clipping_area/"


def test_create_boundary_posts_payload_with_structure_expected_by_conversion_service_api(
    mocker, geos_multipolygon
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    args, kwargs = c.authorized_post.call_args
    assert_that(
        kwargs["json_data"].keys(),
        contains_inanyorder("name", "clipping_multi_polygon"),
    )


def test_create_boundary_posts_name(mocker, geos_multipolygon):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["name"] == sentinel.NAME


def test_create_boundary_posts_geojson(mocker, geos_multipolygon):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["clipping_multi_polygon"] == {
        "type": "MultiPolygon",
        "coordinates": nested_list(geos_multipolygon.coords),
    }


def test_create_boundary_returns_post_request_response_json_payload_as_dict(
    mocker, geos_multipolygon
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    result = c.create_boundary(geos_multipolygon, name=sentinel.NAME)
    assert result == c.authorized_post.return_value.json.return_value


def test_create_parametrization_makes_authorized_post_with_json_payload(mocker):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    c.authorized_post.assert_called_once_with(url=ANY, json_data=ANY)


def test_create_parametrization_posts_to_conversion_parametrization_resource(mocker):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["url"] == "conversion_parametrization/"


def test_create_parametrization_posts_payload_with_structure_expected_by_conversion_service_api(
    mocker,
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    args, kwargs = c.authorized_post.call_args
    assert_that(
        kwargs["json_data"].keys(),
        contains_inanyorder("out_format", "out_srs", "detail_level", "clipping_area"),
    )


def test_create_parametrization_posts_clipping_area_id(mocker):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["clipping_area"] == sentinel.CLIPPING_AREA_ID


def test_create_parametrization_posts_out_format(mocker):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["out_format"] == sentinel.OUT_FORMAT


def test_create_parametrization_posts_out_srs(mocker):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["out_srs"] == sentinel.OUT_SRS


def test_create_parametrization_returns_post_request_response_json_payload_as_dict(
    mocker,
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_boundary_reply = dict(id=sentinel.CLIPPING_AREA_ID)
    result = c.create_parametrization(
        boundary=post_boundary_reply,
        out_format=sentinel.OUT_FORMAT,
        detail_level=sentinel.DETAIL_LEVEL,
        out_srs=sentinel.OUT_SRS,
    )
    assert result == c.authorized_post.return_value.json.return_value


def test_create_job_makes_authorized_post_with_json_payload(mocker, user):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    c.authorized_post.assert_called_once_with(url=ANY, json_data=ANY)


def test_create_job_posts_to_conversion_job_resource(mocker, user):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["url"] == "conversion_job/"


def test_create_job_posts_payload_with_structure_expected_by_conversion_servic_api(
    mocker, user
):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    args, kwargs = c.authorized_post.call_args
    assert_that(
        kwargs["json_data"].keys(),
        contains_inanyorder("callback_url", "parametrization", "queue_name"),
    )


def test_create_job_posts_callback_url(mocker, user):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["callback_url"] == sentinel.CALLBACK_URL


def test_create_job_posts_parametrization_id(mocker, user):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    args, kwargs = c.authorized_post.call_args
    assert kwargs["json_data"]["parametrization"] == sentinel.PARAMETRIZATION_ID


def test_create_job_returns_post_request_response_json_payload_as_dict(mocker, user):
    c = ConversionHelper()
    mocker.patch.object(c, "authorized_post", autospec=True)
    post_parametrization_reply = dict(id=sentinel.PARAMETRIZATION_ID)
    result = c.create_job(
        parametrization=post_parametrization_reply,
        callback_url=sentinel.CALLBACK_URL,
        user=user,
    )
    assert result == c.authorized_post.return_value.json.return_value


@pytest.fixture
def geos_multipolygon():
    return MultiPolygon(
        "MULTIPOLYGON (((5 0, 5 1, 6 1, 5 0)),"
        "((1 1, 4 0, -3 -3, 0 4, 1 1),"
        "(0 0, 3 0, -2 -2, 0 3, 0 0)))"
    )


def nested_list(nested_collection):
    """
    Turn nested collection to nested list.

    Might contain copies of leaf elements instead of references to the original ones.

    Args:
        nested_collection: a nested collection

    Returns:
        nested list with the same structure and content as nested_collection
    """
    # For alternatives, see http://stackoverflow.com/questions/1014352/

    # (Ab)use the fact that json.loads always produces Python lists for JSON lists,
    # while json.dumps turns any Python collection into a JSON list:
    return json.loads(json.dumps(nested_collection))
