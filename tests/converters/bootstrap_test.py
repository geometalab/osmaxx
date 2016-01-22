from unittest import TestCase

from unittest import mock
import os
from django.conf import settings

from converters.gis_converter.bootstrap import bootstrap


class BootStrapperTest(TestCase):
    def test_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(pbf_file_path=settings.OSMAXX_CONVERSION_SERVICE['PBF_PLANET_FILE_PATH'])
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            assert bootstrapper._postgres is postgres_mock
            bootstrapper._filter_data()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/filter/drop_and_recreate/drop_and_recreate.sql',
                'sql/filter/address/000_setup-drop_and_recreate_table.sql',
                'sql/filter/address/address.sql',
                'sql/filter/adminarea_boundary/adminarea_boundary.sql',
                'sql/filter/building/building.sql',
                'sql/filter/landuse/landuse.sql',
                'sql/filter/military/military.sql',
                'sql/filter/natural/natural.sql',
                'sql/filter/nonop/nonop.sql',
                'sql/filter/geoname/000_setup-geoname_table.sql',
                'sql/filter/geoname/010_geoname_l.sql',
                'sql/filter/geoname/020_geoname_p.sql',
                'sql/filter/pow/pow.sql',
                'sql/filter/poi/poi.sql',
                'sql/filter/misc/misc.sql',
                'sql/filter/transport/transport.sql',
                'sql/filter/railway/railway.sql',
                'sql/filter/road/road.sql',
                'sql/filter/route/route.sql',
                'sql/filter/traffic/traffic.sql',
                'sql/filter/utility/utility.sql',
                'sql/filter/water/water.sql',
                'sql/filter/create_view/create_view.sql',
            ]
            postgres_mock.execute_psycopg_file.assert_has_calls(
                [
                    mock.call(
                        os.path.join(
                            base_path_to_bootstrap,
                            relative_script_path
                        ),
                        autocommit=True
                    ) for relative_script_path in expected_script_order
                ]
            )

    def test_function_scripts_are_executed_in_correct_order(self, *args, **kwargs):
        bootstrapper = bootstrap.BootStrapper(pbf_file_path=settings.OSMAXX_CONVERSION_SERVICE['PBF_PLANET_FILE_PATH'])
        with mock.patch.object(bootstrapper, '_postgres') as postgres_mock:
            assert bootstrapper._postgres is postgres_mock
            bootstrapper._setup_db_functions()

            base_path_to_bootstrap = os.path.dirname(bootstrap.__file__)
            expected_script_order = [
                'sql/functions/0010_cast_to_positive_integer.sql',
                'sql/functions/0020_building_height.sql',
                'sql/functions/0030_transliterate.sql',
                'sql/functions/0040_interpolate_addresses.sql',
                'sql/functions/0050_cast_to_int.sql',
            ]
            postgres_mock.execute_psycopg_file.assert_has_calls(
                [
                    mock.call(
                        os.path.join(
                            base_path_to_bootstrap,
                            relative_script_path
                        ),
                        autocommit=True
                    ) for relative_script_path in expected_script_order
                ]
            )
