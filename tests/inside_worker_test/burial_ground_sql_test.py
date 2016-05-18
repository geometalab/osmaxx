from contextlib import contextmanager, closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.conftest import area_polyfile_string
from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@pytest.fixture
def graveyard_polygon_with_religion(graveyard_osm_tags_with_religion):
    return {
        osm_models.t_osm_polygon: graveyard_osm_tags_with_religion,
    }


@pytest.fixture
def graveyard_polygon_without_religion(graveyard_osm_tags_without_religion):
    return {
        osm_models.t_osm_polygon: graveyard_osm_tags_without_religion,
    }


@pytest.fixture
def graveyard_point_with_religion(graveyard_osm_tags_with_religion):
    return {
        osm_models.t_osm_point: graveyard_osm_tags_with_religion,
    }


@pytest.fixture
def graveyard_point_without_religion(graveyard_osm_tags_without_religion):
    return {
        osm_models.t_osm_point: graveyard_osm_tags_without_religion,
    }


@pytest.fixture
def graveyard_osm_tags_with_religion():
    return dict(
        amenity='grave_yard',
        religion='any value will do, as long as one is present',
    )


@pytest.fixture
def graveyard_osm_tags_without_religion():
    return dict(
        amenity='grave_yard',
    )


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(
        graveyard_polygon_with_religion, data_import):
    data = graveyard_polygon_with_religion
    with data_import(data) as engine:
        t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_a]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_does_not_put_amenity_grave_yard_without_religion_into_table_pow_a(
        graveyard_polygon_without_religion, data_import):
    data = graveyard_polygon_without_religion
    with data_import(data) as engine:
        t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_a]))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_poi_a(
        graveyard_polygon_with_religion, data_import):
    data = graveyard_polygon_with_religion
    with data_import(data) as engine:
        t_poi_a = DbTable('poi_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_a]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_without_religion_into_table_poi_a(
        graveyard_polygon_without_religion, data_import):
    data = graveyard_polygon_without_religion
    with data_import(data) as engine:
        t_poi_a = DbTable('poi_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_a]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_does_not_put_amenity_grave_yard_with_religion_into_table_landuse_a(
        graveyard_polygon_with_religion, data_import):
    data = graveyard_polygon_with_religion
    with data_import(data) as engine:
        t_landuse_a = DbTable('landuse_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_landuse_a]))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_does_not_put_amenity_grave_yard_without_religion_into_table_landuse_a(
        graveyard_polygon_without_religion, data_import):
    data = graveyard_polygon_without_religion
    with data_import(data) as engine:
        t_landuse_a = DbTable('landuse_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_landuse_a]))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_p(
        graveyard_polygon_with_religion, data_import):
    data = graveyard_polygon_with_religion
    with data_import(data) as engine:
        t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_p]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_does_not_put_amenity_grave_yard_without_religion_into_table_pow_p(
        graveyard_polygon_without_religion, data_import):
    data = graveyard_polygon_without_religion
    with data_import(data) as engine:
        t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_p]))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_poi_p(
        graveyard_polygon_with_religion, data_import):
    data = graveyard_polygon_with_religion
    with data_import(data) as engine:
        t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_p]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_without_religion_into_table_poi_p(
        graveyard_polygon_without_religion, data_import):
    data = graveyard_polygon_without_religion
    with data_import(data) as engine:
        t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_p]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_point_with_religion_into_table_pow_p(
        graveyard_point_with_religion, data_import):
    data = graveyard_point_with_religion
    with data_import(data) as engine:
        t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_p]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_does_not_put_amenity_grave_yard_point_without_religion_into_table_pow_p(
        graveyard_point_without_religion, data_import):
    data = graveyard_point_without_religion
    with data_import(data) as engine:
        t_pow_p = DbTable('pow_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_p]))) as result:
            assert result.rowcount == 0


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_point_with_religion_into_table_poi_p(
        graveyard_point_with_religion, data_import):
    data = graveyard_point_with_religion
    with data_import(data) as engine:
        t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_p]))) as result:
            assert result.rowcount == 1


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_point_without_religion_into_table_poi_p(
        graveyard_point_without_religion, data_import):
    data = graveyard_point_without_religion
    with data_import(data) as engine:
        t_poi_p = DbTable('poi_p', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_poi_p]))) as result:
            assert result.rowcount == 1


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
