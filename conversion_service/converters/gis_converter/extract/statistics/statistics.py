from converters.gis_converter.extract.statistics.osm_groups import *  # noqa: ignore * import
from converters.gis_converter.helper.default_postgres import get_default_postgres_wrapper


def gather_statistics(outfile):
    out_file = open(outfile, 'w')
    all_stats = Statistics().gather_all()
    for stat in all_stats:
        print(';'.join(stat), file=out_file)
    out_file.close()


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
        self._retrieve_sorted_statistic_part('adminarea_a', BOUNDARIES)

        self._retrieve_sorted_statistic_part('boundary_l', BOUNDARIES)

        self._retrieve_sorted_statistic_part('geoname_l', SETTLEMENTS)
        self._retrieve_sorted_statistic_part('geoname_p', SETTLEMENTS)

        self._retrieve_sorted_statistic_part('landuse_a', LANDUSES)

        self._retrieve_sorted_statistic_part('military_a', MILITARY_AREAS)
        self._retrieve_sorted_statistic_part('military_p', MILITARY_AREAS)

        self._retrieve_sorted_statistic_part('misc_l', MISC_LINES)

        self._retrieve_sorted_statistic_part('natural_a', NATURAL_AREAS)
        self._retrieve_sorted_statistic_part('natural_p', NATURAL_POIS)

        self._retrieve_sorted_statistic_part(
            'nonop_l',
            HIGHWAY_RAILWAY_TYPES,
            label='highway',
            where_clause_type='type_and_status',
            extra_kwargs={'type': 'highway'}
        )
        self._retrieve_sorted_statistic_part(
            'nonop_l',
            HIGHWAY_RAILWAY_TYPES,
            label='railway',
            where_clause_type='type_and_status',
            extra_kwargs={'type': 'railway'}
        )

        self._retrieve_sorted_statistic_part('pow_a', PLACES_OF_WORSHIP)
        self._retrieve_sorted_statistic_part('pow_p', PLACES_OF_WORSHIP)

        self._retrieve_sorted_statistic_part('poi_a', PUBLIC_POIS, label='public')
        self._retrieve_sorted_statistic_part('poi_a', RECYCLING_POIS, label='recycling')
        self._retrieve_sorted_statistic_part('poi_a', EDUCTATION_POIS, label='education')
        self._retrieve_sorted_statistic_part('poi_a', HEALTH_POIS, label='health')
        self._retrieve_sorted_statistic_part('poi_a', LEISURE_POIS, label='leisure')
        self._retrieve_sorted_statistic_part('poi_a', CATERING_POIS, label='catering')
        self._retrieve_sorted_statistic_part('poi_a', ACCOMODATION_IN_POIS, label='accomodation_in')
        self._retrieve_sorted_statistic_part('poi_a', ACCOMODATION_OUT_POIS, label='accomodation_out')
        self._retrieve_sorted_statistic_part(
            'poi_a',
            SHOP_POIS,
            label='shop',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'shop'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            VENDING_POIS,
            label='vending',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'vending'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            MONEY_POIS,
            label='money',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'money'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            TOURISM_POIS,
            label='tourism',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'tourism'},
        )
        self._retrieve_sorted_statistic_part('poi_a', DESTINATION_POIS, label='destination')
        self._retrieve_sorted_statistic_part('poi_a', MISC_POIS, label='miscpoi')
        self._retrieve_sorted_statistic_part(
            'poi_a',
            SPORT,
            label='sport',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'sport'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            MAN_MADE,
            label='man_made',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'man_made'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            HISTORIC,
            label='historic',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'historic'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_a',
            AMENITY,
            label='amenity',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'amenity'},
        )
        self._retrieve_sorted_statistic_part('poi_p', PUBLIC_POIS, label='public')
        self._retrieve_sorted_statistic_part('poi_p', RECYCLING_POIS, label='recycling')
        self._retrieve_sorted_statistic_part('poi_p', EDUCTATION_POIS, label='education')
        self._retrieve_sorted_statistic_part('poi_p', HEALTH_POIS, label='health')
        self._retrieve_sorted_statistic_part('poi_p', LEISURE_POIS, label='leisure')
        self._retrieve_sorted_statistic_part('poi_p', CATERING_POIS, label='catering')
        self._retrieve_sorted_statistic_part('poi_p', ACCOMODATION_IN_POIS, label='accomodation_in')
        self._retrieve_sorted_statistic_part('poi_p', ACCOMODATION_OUT_POIS, label='accomodation_out')
        self._retrieve_sorted_statistic_part(
            'poi_p',
            SHOP_POIS,
            label='shop',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'shop'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            VENDING_POIS,
            label='vending',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'vending'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            MONEY_POIS,
            label='money',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'money'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            TOURISM_POIS,
            label='tourism',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'tourism'},
        )
        self._retrieve_sorted_statistic_part('poi_p', DESTINATION_POIS, label='destination')
        self._retrieve_sorted_statistic_part('poi_p', MISC_POIS, label='miscpoi')
        self._retrieve_sorted_statistic_part(
            'poi_p',
            SPORT,
            label='sport',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'sport'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            MAN_MADE,
            label='man_made',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'man_made'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            HISTORIC,
            label='historic',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'historic'},
        )
        self._retrieve_sorted_statistic_part(
            'poi_p',
            AMENITY,
            label='amenity',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'amenity'},
        )

        self._retrieve_sorted_statistic_part('railway_l', RAILWAY_TYPES)

        self._retrieve_sorted_statistic_part(
            'road_l',
            ROAD_TYPES,
            label='road',
            where_clause_type='aggregate_unequals',
            extra_kwargs={'type': 'roundabout'},
        )

        self._retrieve_sorted_statistic_part(
            'road_l',
            ROUNDABOUT_TYPES,
            label='roundabout',
            where_clause_type='aggregate_equals',
            extra_kwargs={'type': 'roundabout'},
        )

        self._retrieve_sorted_statistic_part('route_l', ROUTE_TYPES)
        self._retrieve_sorted_statistic_part('traffic_a', TRAFFIC_AREA_TYPES)
        self._retrieve_sorted_statistic_part('traffic_p', TRAFFIC_POINTS_TYPES)
        self._retrieve_sorted_statistic_part('transport_a', TRANSPORT_AREAS_TYPES)
        self._retrieve_sorted_statistic_part('transport_p', TRANSPORT_AREAS_TYPES)
        self._retrieve_sorted_statistic_part('utility_a', UTILITY_AREA_TYPES)
        self._retrieve_sorted_statistic_part('utility_p', UTILITY_POINTS_TYPES)
        self._retrieve_sorted_statistic_part('utility_l', UTILITY_LINES_TYPES, label='power')
        self._retrieve_sorted_statistic_part('utility_l', PIPELINE, label='man_made')
        self._retrieve_sorted_statistic_part('water_a', WATER_AREA_TYPES)
        self._retrieve_sorted_statistic_part('water_p', WATER_POINT_TYPES)
        self._retrieve_sorted_statistic_part('water_l', WATER_LINE_TYPES)
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
            [item.insert(0, label) for item in query_results]  # in place label addition
        self._stats.extend(query_results)
        self._stats.append([''])  # insert an empty row

    def _retrieve_statistic(self, table_name, where_clause_type, **kwargs):
        where_clause = self._where_clauses[where_clause_type].format(**kwargs)
        query_string = "SELECT count(type) from osmaxx.{table} where {where_clause}".format(
            table=table_name,
            where_clause=where_clause,
        )
        return self._postgres.execute_raw(query_string).fetchone()[0]  # we know there is exactly one result!
