from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select, insert
# import needed for reflection to work correctly with spacial types
from geoalchemy2 import Geometry, Geography  # noqa


class OSMImporter:
    def __init__(self):
        self._osm_derived_tables = ['osm_point', 'osm_line', 'osm_polygon', 'osm_roads']
        self._osm_base_tables = ['osm_ways', 'osm_nodes']

        _world_db_connection_parameters = {
            'username': 'gis',
            'password': 'gis',
            'port': 5432,
            'database': 'gis',
            'host': 'world-database',
        }
        world_db_connection = URL('postgresql', **_world_db_connection_parameters)
        self._world_db_engine = create_engine(world_db_connection)
        self._world_db_meta_data = MetaData()

        _local_db_connection_parameters = {
            'username': 'postgres',
            'password': 'postgres',
            'port': 5432,
            'database': 'osmaxx_db',
        }
        local_db_connection = URL('postgresql', **_local_db_connection_parameters)
        self._local_db_engine = create_engine(local_db_connection)
        self._table_metas = {}

        for to_be_created_table in self._osm_derived_tables + self._osm_base_tables:
            self._table_metas[to_be_created_table] = Table(
                to_be_created_table,
                self._world_db_meta_data,
                autoload=True,
                autoload_with=self._world_db_engine,
                postgresql_with_oids=True
            )

    def load_area_specific_data(self, *, extent):
        self._create_tables_on_local_db()
        self._load_tables(extent)
        self._load_base_tables()

    def _create_tables_on_local_db(self):
        self._world_db_meta_data.create_all(self._local_db_engine)

    def _load_tables(self, extent):
        for table_name in self._osm_derived_tables:
            table_meta = self._table_metas[table_name]
            query = select([table_meta])
            query = query.where(func.ST_Intersects(table_meta.c.way, extent.ewkt))
            self._execute_and_insert_into_local_db(query, table_meta)

    def _load_base_tables(self):
        for table_name in self._osm_base_tables:
            table_meta = self._table_metas[table_name]
            query = select([table_meta])
            self._execute_and_insert_into_local_db(query, table_meta)

    def _execute_and_insert_into_local_db(self, query, table_meta):
        query_result = self._world_db_engine.execute(query)
        if query_result.rowcount > 0:
            results = query_result.fetchall()
            for result in results:
                self._local_db_engine.execute(
                    insert(table_meta, values=result)
                )

