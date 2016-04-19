import csv

from osmaxx.conversion.converters.converter_gis.extract.statistics import osm_groups
from osmaxx.conversion.converters.converter_gis.helper.default_postgres import get_default_postgres_wrapper


def gather_statistics(outfile):
    with open(outfile, 'w') as out_file:
        csv_writer = csv.writer(out_file, delimiter=';')
        all_stats = Statistics().gather_all()
        csv_writer.writerows(all_stats)


class Statistics:
    def __init__(self, postgres=None):
        self._postgres = postgres
        if not self._postgres:
            self._postgres = get_default_postgres_wrapper()
        self._where_clauses = {
            'default': "type='{element}'",
            'type_and_status': "type='{type}' and status='{element}'",
            'aggregate_equals': "aggtype='{type}' and type='{element}'",
            'aggregate_unequals': "aggtype<>'{type}' and type='{element}'",
        }
        self._stats = []

    def gather_all(self):
        self._retrieve_sorted_statistic_part('adminarea_a', osm_groups.BOUNDARIES)

        self._retrieve_sorted_statistic_part('boundary_l', osm_groups.BOUNDARIES)

        self._retrieve_sorted_statistic_part('geoname_l', osm_groups.SETTLEMENTS)
        self._retrieve_sorted_statistic_part('geoname_p', osm_groups.SETTLEMENTS)

        self._retrieve_sorted_statistic_part('landuse_a', osm_groups.LANDUSES)

        self._retrieve_sorted_statistic_part('military_a', osm_groups.MILITARY_AREAS)
        self._retrieve_sorted_statistic_part('military_p', osm_groups.MILITARY_AREAS)

        self._retrieve_sorted_statistic_part('misc_l', osm_groups.MISC_LINES)

        self._retrieve_sorted_statistic_part('natural_a', osm_groups.NATURAL_AREAS)
        self._retrieve_sorted_statistic_part('natural_p', osm_groups.NATURAL_POIS)

        self._retrieve_sorted_statistic_part(
            'nonop_l',
            osm_groups.HIGHWAY_RAILWAY_TYPES,
            label='highway',
            where_clause_type='type_and_status',
            extra_kwargs={'type': 'highway'}
        )
        self._retrieve_sorted_statistic_part(
            'nonop_l',
            osm_groups.HIGHWAY_RAILWAY_TYPES,
            label='railway',
            where_clause_type='type_and_status',
            extra_kwargs={'type': 'railway'}
        )

        self._retrieve_sorted_statistic_part('pow_a', osm_groups.PLACES_OF_WORSHIP)
        self._retrieve_sorted_statistic_part('pow_p', osm_groups.PLACES_OF_WORSHIP)

        self._retrieve_sorted_statistic_part('poi_a', osm_groups.PUBLIC_POIS, label='public')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.RECYCLING_POIS, label='recycling')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.EDUCTATION_POIS, label='education')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.HEALTH_POIS, label='health')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.LEISURE_POIS, label='leisure')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.CATERING_POIS, label='catering')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.ACCOMODATION_IN_POIS, label='accomodation_in')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.ACCOMODATION_OUT_POIS, label='accomodation_out')
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.SHOP_POIS,
            label='shop',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'shop'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.VENDING_POIS,
            label='vending',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'vending'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.MONEY_POIS,
            label='money',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'money'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.TOURISM_POIS,
            label='tourism',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'tourism'},
        )
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.DESTINATION_POIS, label='destination')
        self._retrieve_sorted_statistic_part('poi_a', osm_groups.MISC_POIS, label='miscpoi')
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.SPORT,
            label='sport',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'sport'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.MAN_MADE,
            label='man_made',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'man_made'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.HISTORIC,
            label='historic',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'historic'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            osm_groups.AMENITY,
            label='amenity',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'amenity'},
        )
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.PUBLIC_POIS, label='public')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.RECYCLING_POIS, label='recycling')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.EDUCTATION_POIS, label='education')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.HEALTH_POIS, label='health')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.LEISURE_POIS, label='leisure')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.CATERING_POIS, label='catering')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.ACCOMODATION_IN_POIS, label='accomodation_in')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.ACCOMODATION_OUT_POIS, label='accomodation_out')
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.SHOP_POIS,
            label='shop',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'shop'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.VENDING_POIS,
            label='vending',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'vending'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.MONEY_POIS,
            label='money',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'money'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.TOURISM_POIS,
            label='tourism',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'tourism'},
        )
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.DESTINATION_POIS, label='destination')
        self._retrieve_sorted_statistic_part('poi_p', osm_groups.MISC_POIS, label='miscpoi')
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.SPORT,
            label='sport',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'sport'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.MAN_MADE,
            label='man_made',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'man_made'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.HISTORIC,
            label='historic',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'historic'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            osm_groups.AMENITY,
            label='amenity',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'amenity'},
        )

        self._retrieve_sorted_statistic_part('railway_l', osm_groups.RAILWAY_TYPES)

        self._retrieve_sorted_statistic_part(
            'road_l',
            osm_groups.ROAD_TYPES,
            label='road',
            where_clause_type='aggregate_unequals',
            extra_kwargs={'type': 'roundabout'},
        )

        self._retrieve_sorted_statistic_part(
            'road_l',
            osm_groups.ROUNDABOUT_TYPES,
            label='roundabout',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'roundabout'},
        )

        self._retrieve_sorted_statistic_part('route_l', osm_groups.ROUTE_TYPES)
        self._retrieve_sorted_statistic_part('traffic_a', osm_groups.TRAFFIC_AREA_TYPES)
        self._retrieve_sorted_statistic_part('traffic_p', osm_groups.TRAFFIC_POINTS_TYPES)
        self._retrieve_sorted_statistic_part('transport_a', osm_groups.TRANSPORT_AREAS_TYPES)
        self._retrieve_sorted_statistic_part('transport_p', osm_groups.TRANSPORT_AREAS_TYPES)
        self._retrieve_sorted_statistic_part('utility_a', osm_groups.UTILITY_AREA_TYPES)
        self._retrieve_sorted_statistic_part('utility_p', osm_groups.UTILITY_POINTS_TYPES)
        self._retrieve_sorted_statistic_part('utility_l', osm_groups.UTILITY_LINES_TYPES, label='power')
        self._retrieve_sorted_statistic_part('utility_l', osm_groups.PIPELINE, label='man_made')
        self._retrieve_sorted_statistic_part('water_a', osm_groups.WATER_AREA_TYPES)
        self._retrieve_sorted_statistic_part('water_p', osm_groups.WATER_POINT_TYPES)
        self._retrieve_sorted_statistic_part('water_l', osm_groups.WATER_LINE_TYPES)
        return self._stats.copy()

    def _retrieve_sorted_statistic_part(
            self, table_name, element_list, where_clause_type='default', label=None, extra_kwargs=None):
        self._stats.append([table_name])
        query_results = []
        for element in element_list:
            clause_kwargs = {'element': element}
            if extra_kwargs is not None:
                clause_kwargs.update(extra_kwargs)
            query_results.append(
                [
                    element,
                    '{}'.format(
                        self._retrieve_statistic(table_name, where_clause_type=where_clause_type, **clause_kwargs)
                    )
                ]
            )
        query_results = sorted(query_results, key=lambda t: t[1], reverse=True)
        if label:
            for item in query_results:
                item.insert(0, label)
        self._stats.extend(query_results)
        self._stats.append([''])  # insert an empty row

    def _retrieve_statistic(self, table_name, where_clause_type, **kwargs):
        where_clause = self._where_clauses[where_clause_type].format(**kwargs)
        query_string = "SELECT count(type) from osmaxx.{table} where {where_clause}".format(
            table=table_name,
            where_clause=where_clause,
        )
        return self._postgres.execute_sql_command(query_string).fetchone()[0]  # we know there is exactly one result!
