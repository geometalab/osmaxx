from contextlib import closing

import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models


@slow
def test_osmaxx_data_model_processing_puts_amenity_grave_yard_with_religion_into_table_pow_a(data_import):
    data = {
        osm_models.t_osm_polygon: dict(
            amenity='grave_yard',
            religion='any value will do, as long as one is present',
        ),
    }
    with data_import(data) as engine:
        t_pow_a = DbTable('pow_a', osm_models.metadata, schema='osmaxx')
        with closing(engine.execute(sqlalchemy.select([t_pow_a]))) as result:
            assert result.rowcount == 1
