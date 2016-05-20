from contextlib import contextmanager, closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.conftest import area_polyfile_string
from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@pytest.fixture(params=[osm_models.t_osm_polygon, osm_models.t_osm_point], ids=['osm_polygon', 'osm_point'])
def graveyard_data(request, osm_tags):
    return {request.param: osm_tags}


@pytest.fixture(
    params=[
        dict(amenity='grave_yard', religion='any value will do, as long as one is present'),
        dict(amenity='grave_yard'),
        dict(landuse='cemetery', religion='any value will do, as long as one is present'),
        dict(landuse='cemetery'),
    ],
    ids=[
        'amenity=grave_yard with religion=*',
        'amenity=grave_yard without religion',
        'landuse=cemetery with religion=*',
        'landuse=cemetery without religion',
    ]
)
def osm_tags(request):
    return request.param


@pytest.fixture(params=['pow_a', 'landuse_a', 'pow_p'])
def non_burial_ground_target_layer(request):
    return DbTable(request.param, osm_models.metadata, schema='osmaxx')


@pytest.fixture(params=['poi_a', 'poi_p'])
def burial_ground_target_layer(request):
    return DbTable(request.param, osm_models.metadata, schema='osmaxx')


@slow
def test_osmaxx_data_model_processing_does_not_put_burial_ground_into_non_burial_ground_target_layer(
        burial_ground_data_import, graveyard_data, non_burial_ground_target_layer):
    if all(source_table is osm_models.t_osm_point for source_table in graveyard_data.keys()) \
            and not non_burial_ground_target_layer.name.endswith('_p'):
        pytest.skip()
    engine = burial_ground_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(non_burial_ground_target_layer))) as result:
        assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_burial_ground_into_burial_ground_target_layer(
        burial_ground_data_import, graveyard_data, osm_tags, burial_ground_target_layer):
    if all(source_table is osm_models.t_osm_point for source_table in graveyard_data.keys()) \
            and not burial_ground_target_layer.name.endswith('_p'):
        pytest.skip()
    engine = burial_ground_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(burial_ground_target_layer))) as result:
        assert result.rowcount == 1
        row = result.fetchone()
        expected_type = osm_tags.get('amenity', None) or osm_tags['landuse']
        assert expected_type in {'grave_yard', 'cemetery'}  # just a sanity check, not the test assertion
        assert row['type'] == expected_type
        assert row['aggtype'] == 'burial_ground'


@pytest.yield_fixture
def burial_ground_data_import(graveyard_data, data_import):
    with data_import(graveyard_data) as engine:
        yield engine


@pytest.fixture()
def data_import(osmaxx_schemas, clean_osm_tables, monkeypatch):
    from tests.inside_worker_test.conftest import cleanup_osmaxx_schemas
    from osmaxx.conversion.converters.converter_gis.bootstrap.bootstrap import BootStrapper

    assert osmaxx_schemas == clean_osm_tables  # same db-connection
    engine = osmaxx_schemas
    monkeypatch.setattr(
        'osmaxx.conversion.converters.converter_gis.helper.postgres_wrapper.create_engine', lambda *_, **__: engine)

    class _BootStrapperWithoutPbfFile(BootStrapper):
        def __init__(self, data):
            super().__init__(area_polyfile_string=area_polyfile_string())
            self.data = data

        def _reset_database(self):
            pass  # Already taken care of by clean_osm_tables fixture.

        def _import_from_world_db(self, with_boundaries):
            for table, values in self.data.items():
                engine.execute(table.insert().execution_options(autocommit=True), values)

        def _setup_db_functions(self):
            pass  # Already taken care of by osmaxx_functions fixture.

    @contextmanager
    def import_data(data):
        bootstrapper = _BootStrapperWithoutPbfFile(data)
        try:
            bootstrapper.bootstrap()
            yield engine
        finally:
            cleanup_osmaxx_schemas(bootstrapper._postgres._engine)

    return import_data
