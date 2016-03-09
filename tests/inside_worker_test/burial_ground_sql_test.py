import sqlalchemy

from osmaxx.converters.gis_converter.bootstrap.bootstrap import BootStrapper
from tests.inside_worker_test.conftest import slow, cleanup_osmaxx_schemas
from tests.inside_worker_test.declarative_schema import osm_models


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(
        osmaxx_functions, clean_osm_tables, monkeypatch):
    assert osmaxx_functions == clean_osm_tables  # same db-connection
    engine = osmaxx_functions

    def create_osm_data():
        engine.execute(
            osm_models.t_osm_polygon.insert().values(
                amenity='grave_yard',
                religion='any value will do, as long as one is present',
            ).execution_options(autocommit=True)
        )
    monkeypatch.setattr(
        'osmaxx.converters.gis_converter.helper.postgres_wrapper.create_engine', lambda *_, **__: engine)
    monkeypatch.setattr(BootStrapper, '_reset_database', lambda _self: None)  # Already taken care of by fixtures.
    monkeypatch.setattr(BootStrapper, '_convert_osm_pbf_to_postgres', lambda _self: create_osm_data())
    monkeypatch.setattr(BootStrapper, '_setup_db_functions', lambda _self: None)  # Already taken care of by fixtures.
    bootstrapper = BootStrapper(pbf_file_path=None)
    try:
        bootstrapper.bootstrap()
        t_pow_a = sqlalchemy.sql.schema.Table('pow_a', osm_models.metadata, schema='osmaxx')
        result = engine.execute(sqlalchemy.select([t_pow_a]))
        assert result.rowcount == 1
    finally:
        try:
            result.close()  # Release row and table locks.
        except NameError:
            pass
        cleanup_osmaxx_schemas(engine)
