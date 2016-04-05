from itertools import chain
from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select, insert
# import needed for reflection to work correctly with spatial types
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
        self._world_db_engine = create_engine(world_db_connection, use_native_hstore=True)
        self._world_db_meta_data = MetaData()

        _local_db_connection_parameters = {
            'username': 'postgres',
            'password': 'postgres',
            'port': 5432,
            'database': 'osmaxx_db',
        }
        local_db_connection = URL('postgresql', **_local_db_connection_parameters)
        self._local_db_engine = create_engine(local_db_connection, use_native_hstore=True)
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
        osm_line = self._table_metas['osm_line']
        osm_ways = self._table_metas['osm_ways']
        osm_nodes = self._table_metas['osm_nodes']

        local_line_osm_ids_query = self._local_db_engine.execute(
            select([osm_line.c.osm_id])
        )
        if local_line_osm_ids_query.rowcount > 0:
            line_osm_ids = [q.osm_id for q in local_line_osm_ids_query.fetchall()]
            osm_ways_query = select([osm_ways]).where(
                osm_ways.c.id.in_(line_osm_ids)
            )
            rows_altered = self._execute_and_insert_into_local_db(osm_ways_query, osm_ways)
            if rows_altered > 0:
                local_osm_ways_query = self._local_db_engine.execute(
                    select([osm_ways.c.nodes])
                )
                if local_osm_ways_query.rowcount > 0:
                    array_rows = chain.from_iterable(local_osm_ways_query.fetchall())
                    node_ids = chain.from_iterable(array_rows)
                    osm_nodes_query = select([osm_nodes]).where(
                        osm_nodes.c.id.in_(node_ids)
                    )
                    self._execute_and_insert_into_local_db(osm_nodes_query, osm_nodes)

    def _execute_and_insert_into_local_db(self, query, table_meta):
        query_result = self._world_db_engine.execute(query)
        row_count = query_result.rowcount
        if row_count > 0:
            results = query_result.fetchall()
            for result in results:
                self._local_db_engine.execute(
                    insert(table_meta, values=result)
                )
        return row_count
