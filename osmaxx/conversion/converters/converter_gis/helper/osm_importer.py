from itertools import chain
from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select, insert, expression
from geoalchemy2 import Geometry, Geography


class OSMImporter:
    def __init__(self):
        self._osm_derived_tables = ['osm_point', 'osm_line', 'osm_polygon', 'osm_roads']
        self._osm_base_tables = ['osm_ways', 'osm_nodes']
        self._osm_boundaries_tables = ['coastlines', 'land_polygons', 'water_polygons']

        _world_db_connection_parameters = dict(
            username='gis',
            password='gis',
            port=5432,
            database='gis',
            host='world-database',
        )
        world_db_connection = URL('postgresql', **_world_db_connection_parameters)
        self._world_db_engine = create_engine(world_db_connection)

        _osm_boundaries_db_connection_parameters = dict(
            username='osmboundaries',
            password='osmboundaries',
            port=5432,
            database='osmboundaries',
            host='osmboundaries-database',
        )
        osm_boundaries_db_connection = URL('postgresql', **_osm_boundaries_db_connection_parameters)
        self._osm_boundaries_db_engine = create_engine(osm_boundaries_db_connection)

        _local_db_connection_parameters = dict(
            username='postgres',
            password='postgres',
            port=5432,
            database='osmaxx_db',
        )
        local_db_connection = URL('postgresql', **_local_db_connection_parameters)
        self._local_db_engine = create_engine(local_db_connection)

        assert Geometry, Geography  # assert classes needed for GIS-reflection are available
        self._db_meta_data = MetaData()
        self._table_metas = self._get_meta_tables()

    def _autoinspect_tables(self, tables, autoloader):
        return {
            table: Table(table, self._db_meta_data, autoload=True, autoload_with=autoloader)
            for table in tables
        }

    def _get_meta_tables(self):
        meta_boundaries = self._autoinspect_tables(
            tables=self._osm_boundaries_tables, autoloader=self._osm_boundaries_db_engine
        )
        meta_boundaries.update(
            self._autoinspect_tables(
                tables=self._osm_derived_tables + self._osm_base_tables, autoloader=self._world_db_engine
            )
        )
        return meta_boundaries

    def load_area_specific_data(self, *, extent):
        self._create_tables_on_local_db()
        self._load_tables(extent)
        self._load_base_tables()
        self._load_boundaries_tables(extent)

    def _create_tables_on_local_db(self):
        self._db_meta_data.create_all(self._local_db_engine)

    def _load_tables(self, extent):
        for table_name in self._osm_derived_tables:
            table_meta = self._table_metas[table_name]
            query = select([table_meta])
            query = query.where(func.ST_Intersects(table_meta.c.way, extent.ewkt))
            self._execute_and_insert_into_local_db(query, table_meta)

    def _load_base_tables(self):
        line_osm_ids = self._get_local_osm_ids()
        if len(line_osm_ids) == 0:
            return
        local_ways = self._insert_corresponding_ways(line_osm_ids)
        if local_ways.rowcount == 0:
            return
        self._insert_corresponding_osm_nodes(local_ways)

    def _load_boundaries_tables(self, extent):
        multipolygon_cast = Geometry(geometry_type='MULTIPOLYGON', srid=4326)
        multilinestring_cast = Geometry(geometry_type='MULTILINESTRING', srid=4326)
        table_casts = {
            'land_polygons': multipolygon_cast,
            'water_polygons': multipolygon_cast,
            'coastlines': multilinestring_cast,
        }
        for table_name in self._osm_boundaries_tables:
            source_table_meta = self._table_metas[table_name]
            query = select([
                source_table_meta.c.ogc_fid,
                source_table_meta.c.fid,
                source_table_meta.c.wkb_geometry
            ])
            query = query.where(func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt))
            self._execute_and_insert_into_local_db(query, source_table_meta, source_engine=self._osm_boundaries_db_engine)
            from sqlalchemy_views import CreateView
            view_definition_query = select([
                source_table_meta.c.ogc_fid,
                source_table_meta.c.fid,
                expression.cast(
                    func.ST_Multi(func.ST_Intersection(source_table_meta.c.wkb_geometry, extent.ewkt)),
                    table_casts[table_name]
                ).label('geom')
            ]).where(func.ST_Intersects(source_table_meta.c.wkb_geometry, extent.ewkt))
            view_meta = MetaData()
            view = Table(table_name, view_meta, schema='view_osmaxx')

            from sqlalchemy.dialects import postgresql
            from sqlalchemy.sql import text
            query_defintion_string = str(
                view_definition_query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
            )
            query_defintion_string = query_defintion_string.replace('ST_AsEWKB(CAST', 'CAST')
            query_defintion_string = query_defintion_string.replace('))) AS geom', ')) AS geom')
            query_defintion_text = text(query_defintion_string)
            create_view = CreateView(view, query_defintion_text, or_replace=True)
            self._local_db_engine.execute(create_view)

    def _get_local_osm_ids(self):
        osm_line = self._table_metas['osm_line']
        local_line_osm_ids_results = self._local_db_engine.execute(
            select([osm_line.c.osm_id])
        )
        return [q.osm_id for q in local_line_osm_ids_results.fetchall()]

    def _insert_corresponding_ways(self, line_osm_ids):
        osm_ways = self._table_metas['osm_ways']
        osm_ways_query = select([osm_ways]).where(
            osm_ways.c.id.in_(line_osm_ids)
        )
        self._execute_and_insert_into_local_db(osm_ways_query, osm_ways)
        return self._local_db_engine.execute(select([osm_ways.c.nodes]))

    def _insert_corresponding_osm_nodes(self, ways):
        osm_nodes = self._table_metas['osm_nodes']
        array_rows = chain.from_iterable(ways.fetchall())
        node_ids = chain.from_iterable(array_rows)
        osm_nodes_query = select([osm_nodes]).where(
            osm_nodes.c.id.in_(node_ids)
        )
        self._execute_and_insert_into_local_db(osm_nodes_query, osm_nodes)

    def _execute_and_insert_into_local_db(self, query, table_meta, source_engine=None):
        if source_engine is None:
            source_engine = self._world_db_engine
        query_result = source_engine.execute(query)
        if query_result.rowcount > 0:
            results = query_result.fetchall()
            for result in results:
                self._local_db_engine.execute(
                    insert(table_meta, values=result)
                )
