from contextlib import contextmanager, closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.conftest import area_polyfile_string
from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@pytest.fixture
def graveyard_polygon(osm_tags):
    return {osm_models.t_osm_polygon: osm_tags}


@pytest.fixture
def graveyard_point(osm_tags):
    return {osm_models.t_osm_point: osm_tags}


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


@slow
def test_osmaxx_data_model_processing_does_not_put_burial_ground_into_table_pow_a(
        graveyard_polygon, data_import):
    t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_polygon) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_pow_a))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_burial_ground_into_table_poi_a(
        graveyard_polygon, data_import, osm_tags):
    t_poi_a = DbTable('poi_a', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_polygon) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_poi_a))) as result:
            assert result.rowcount == 1
            row = result.fetchone()
            expected_type = osm_tags.get('amenity', None) or osm_tags['landuse']
            assert expected_type in {'grave_yard', 'cemetery'}  # just a sanity check, not the test assertion
            assert row['type'] == expected_type
            assert row['aggtype'] == 'burial_ground'


@slow
def test_osmaxx_data_model_processing_does_not_put_burial_ground_into_table_landuse_a(
        graveyard_polygon, data_import):
    t_landuse_a = DbTable('landuse_a', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_polygon) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_landuse_a))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_does_not_put_burial_ground_into_table_pow_p(
        graveyard_polygon, data_import):
    t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_polygon) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_pow_p))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_burial_ground_into_table_poi_p(
        graveyard_polygon, data_import, osm_tags):
    t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_polygon) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_poi_p))) as result:
            assert result.rowcount == 1
            row = result.fetchone()
            expected_type = osm_tags.get('amenity', None) or osm_tags['landuse']
            assert expected_type in {'grave_yard', 'cemetery'}  # just a sanity check, not the test assertion
            assert row['type'] == expected_type
            assert row['aggtype'] == 'burial_ground'


@slow
def test_osmaxx_data_model_processing_does_not_put_burial_ground_point_into_table_pow_p(
        graveyard_point, data_import):
    t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_point) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_pow_p))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_burial_ground_point_into_table_poi_p(
        graveyard_point, data_import, osm_tags):
    t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
    with data_import(graveyard_point) as engine:
        with closing(engine.execute(sqlalchemy.select('*').select_from(t_poi_p))) as result:
            assert result.rowcount == 1
            row = result.fetchone()
            expected_type = osm_tags.get('amenity', None) or osm_tags['landuse']
            assert expected_type in {'grave_yard', 'cemetery'}  # just a sanity check, not the test assertion
            assert row['type'] == expected_type
            assert row['aggtype'] == 'burial_ground'


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
