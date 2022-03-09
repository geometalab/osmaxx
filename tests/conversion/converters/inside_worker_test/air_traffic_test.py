from contextlib import closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.conversion.converters.inside_worker_test.conftest import slow
from tests.conversion.converters.inside_worker_test.declarative_schema import osm_models


@pytest.fixture(
    params=[osm_models.t_osm_line, osm_models.t_osm_polygon],
    ids=["osm_line", "osm_polygon"],
)
def aeroway_line_feature_data(request, osm_tags):
    return {request.param: osm_tags}


@pytest.fixture(params=["runway", "taxiway", "apron"])
def osm_tags(request):
    return dict(aeroway=request.param)


@pytest.fixture
def misc_l(osmaxx_output_schema):
    return DbTable("misc_l", osm_models.metadata, schema=osmaxx_output_schema)


@pytest.fixture
def transport_l(osmaxx_output_schema):
    return DbTable("transport_l", osm_models.metadata, schema=osmaxx_output_schema)


from osmaxx.conversion._settings import CONVERSION_SETTINGS


@pytest.fixture(
    params=[
        CONVERSION_SETTINGS["CONVERSION_SCHEMA_NAME_TMP"],
        CONVERSION_SETTINGS["CONVERSION_SCHEMA_NAME_TMP_VIEW"],
    ]
)
def osmaxx_output_schema(request):
    return request.param


@slow
def test_osmaxx_data_model_processing_puts_aeroway_line_features_into_misc_l(
    aeroway_line_feature_data_import, misc_l
):
    engine = aeroway_line_feature_data_import
    with closing(engine.execute(sqlalchemy.select("*").select_from(misc_l))) as result:
        assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_produces_no_layer_transport_l(
    aeroway_line_feature_data_import, transport_l, osm_tags
):
    engine = aeroway_line_feature_data_import
    with closing(
        engine.execute(sqlalchemy.select("*").select_from(transport_l))
    ) as result:
        assert result.rowcount == 1
        row = result.fetchone()
        assert row["type"] == osm_tags["aeroway"]
        assert row["aggtype"] == "air_traffic"


@pytest.yield_fixture
def aeroway_line_feature_data_import(aeroway_line_feature_data, data_import):
    with data_import(aeroway_line_feature_data) as engine:
        yield engine
