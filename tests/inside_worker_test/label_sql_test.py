import pytest
import sqlalchemy

from tests.conftest import TagCombination
from tests.inside_worker_test.conftest import sql_from_bootstrap_relative_location, slow
from tests.inside_worker_test.declarative_schema import osm_models

xeno = "大洲南部広域農道"
xeno_transliterated = 'dà zhōu nán bù guǎng yù nóng dào'
latin = 'Turicum'

NAME_TAG_COMBINATIONS = tuple(
    TagCombination(name_tags) for name_tags in
    [
        {'name': latin, 'name:en': 'latin-en', 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': latin},
        {'name': xeno, 'name:en': 'latin-en', 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-en'},
        {'name': latin, 'name:en': None, 'name:fr': None, 'name:es': None, 'name:de': None, 'expected_label': latin},

        # correct order of fallbacks
        {'name': None, 'name:en': 'latin-en', 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-en'},
        {'name': None, 'name:en': None, 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-fr'},
        {'name': None, 'name:en': None, 'name:fr': None, 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-es'},
        {'name': None, 'name:en': None, 'name:fr': None, 'name:es': None, 'name:de': 'latin-de', 'expected_label': 'latin-de'},
        {'name': None, 'name:en': None, 'name:fr': None, 'name:es': None, 'name:de': None, 'expected_label': None},

        # correct order of fallbacks with transliterate
        {'name': xeno, 'name:en': 'latin-en', 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-en'},
        {'name': xeno, 'name:en': None, 'name:fr': 'latin-fr', 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-fr'},
        {'name': xeno, 'name:en': None, 'name:fr': None, 'name:es': 'latin-es', 'name:de': 'latin-de', 'expected_label': 'latin-es'},
        {'name': xeno, 'name:en': None, 'name:fr': None, 'name:es': None, 'name:de': 'latin-de', 'expected_label': 'latin-de'},
        {'name': xeno, 'name:en': None, 'name:fr': None, 'name:es': None, 'name:de': None, 'expected_label': xeno_transliterated},
    ]
)


@pytest.fixture(params=NAME_TAG_COMBINATIONS, ids=[str(tag_combination) for tag_combination in NAME_TAG_COMBINATIONS])
def label_input(request):
    return dict(request.param)


@slow
def test_label_addresses(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'addr:street': 'somevalue', 'building': 'some', 'entrance': None})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))
    address_script = 'sql/filter/address/010_address.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.address_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_entrance(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'addr:street': 'somevalue'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/address/020_entrance.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.address_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
@pytest.mark.skipif(True, reason='would need too much input data (houses along a line) which we have not so far')
def test_label_interpolation(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'addr:place': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/address/030_interpolation.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == -1  # result from drop table

    result = engine.execute(sqlalchemy.text("select label from osmaxx.address_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_adminarea(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/adminarea_boundary/000_setup-drop_and_recreate_table_adminarea.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'boundary': 'administrative'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/adminarea_boundary/010_adminarea.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.adminarea_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_boundary(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/adminarea_boundary/020_setup-drop_and_recreate_table_boundary.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'boundary': 'national_park'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/adminarea_boundary/030_boundary.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.boundary_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_building(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/building/000_setup-drop_and_recreate_table_building.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'building': 'some'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/building/010_building.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.building_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_geoname_l(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/geoname/000_setup-geoname_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'place': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/geoname/010_geoname_l.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.geoname_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_geoname_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/geoname/000_setup-geoname_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'place': 'asdf'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/geoname/020_geoname_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.geoname_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_landuse(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/landuse/000_setup-drop_and_recreate_table_landuse.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'leisure': 'park'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/landuse/010_landuse.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.landuse_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_military_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/military/000_setup-drop_and_recreate_table_military_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'military': 'somevalue'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/military/010_military_a.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.military_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_military_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/military/020_setup-drop_and_recreate_table_military_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'military': 'somevalue'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/military/030_military_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.military_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_barrier(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/misc/000_setup_misc_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'barrier': 'somevalue'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/misc/010_barrier.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.misc_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_misc_natural(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/misc/000_setup_misc_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'natural': 'cliff'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/misc/020_natural.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.misc_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_traffic_calming(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/misc/000_setup_misc_table.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'traffic_calming': 'asdf'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/misc/030_traffic_calming.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.misc_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_air_traffic(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/transport/040_setup-drop_and_recreate_table_transport_l.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'aeroway': 'runway'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/transport/050_air_traffic.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.transport_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_natural_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/natural/000_setup-drop_and_recreate_table_natural_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'natural': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/natural/010_natural_a.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.natural_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_natural_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/natural/020_setup-drop_and_recreate_table_natural_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'natural': 'value'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/natural/030_natural_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.natural_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_nonop(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/nonop/000_setup-drop_and_recreate_table_nonop.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    additional_setup = 'sql/filter/nonop/005_lifecycle_view.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(additional_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'highway': 'planned'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/nonop/010_nonop.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.nonop_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_amenity(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'amenity': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/010_poi_amenity.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_leisure(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'leisure': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/020_poi_leisure.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_man_made(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'some'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/030_poi_man_made.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_historic(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'historic': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/040_poi_historic.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_shop(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'shop': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/050_poi_shop.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_tourism(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'tourism': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/060_poi_tourism.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_sport(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'sport': 'value'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/070_poi_sport.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_highway(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'highway': 'emergency_access_point'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/080_poi_highway.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_emergency(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'emergency': 'phone'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/090_poi_emergency.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_drinking_water(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'water_well'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/100_poi_drinking_water.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_office(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/000_setup-drop_and_recreate_table_poi_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'office': 'government'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/110_poi_office.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_amenity(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'amenity': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/130_poi_p_amenity.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_leisure(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'leisure': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/140_poi_p_leisure.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_man_made(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/150_poi_p_man_made.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_historic(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'historic': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/160_poi_p_historic.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_shop(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'shop': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/170_poi_p_shop.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_tourism(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'tourism': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/180_poi_p_tourism.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_sport(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'sport': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/190_poi_p_sport.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_highway(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'highway': 'emergency_access_point'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/200_poi_p_highway.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_emergency(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'emergency': 'phone'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/210_poi_p_emergency.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_drinking_water(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'water_well'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/220_poi_p_drinking_water.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_poi_p_office(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/poi/120_setup-drop_and_recreate_table_poi_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'office': 'government'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/poi/230_poi_p_office.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.poi_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_pow_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/pow/000_setup-drop_and_recreate_table_pow_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'religion': 'some'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/pow/010_pow_a.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.pow_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_pow_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/pow/020_setup-drop_and_recreate_table_pow_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'religion': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/pow/030_pow_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.pow_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_railway(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/railway/000_setup-drop_and_recreate_table_railway.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'railway': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/railway/010_railway.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.railway_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_aerialway(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/railway/000_setup-drop_and_recreate_table_railway.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'aerialway': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/railway/020_aerialway.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.railway_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_road(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/road/000_setup-drop_and_recreate_table_road.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'highway': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/road/010_road.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.road_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_junction(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/road/000_setup-drop_and_recreate_table_road.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'junction': 'roundabout'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/road/020_junction.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.road_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_route(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/route/000_setup-drop_and_recreate_table_route.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'route': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/route/010_route.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.route_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_traffic_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/traffic/000_setup-drop_and_recreate_table_traffic.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'amenity': 'parking'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/traffic/010_traffic_a.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.traffic_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_traffic_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/traffic/020_setup-drop_and_recreate_table_traffic_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'barrier': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/traffic/030_traffic_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.traffic_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_transport_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/transport/000_setup-drop_and_recreate_table_transport_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'railway': 'station'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/transport/010_transport_a.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.transport_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_transport_p(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/transport/020_setup-drop_and_recreate_table_transport_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'aeroway': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/transport/030_transport_p.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.transport_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_a_power(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/000_setup-drop_and_recreate_table_utility_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'power': 'some'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/010_utility_a_power.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_a_man_made(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/000_setup-drop_and_recreate_table_utility_a.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'water_works'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/020_utility_a_man_made.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_p_power(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/030_setup-drop_and_recreate_table_utility_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'power': 'some'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/040_utility_p_power.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_p_man_made(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/030_setup-drop_and_recreate_table_utility_p.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'water_works'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/050_utility_p_man_made.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_l_power(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/060_setup-drop_and_recreate_table_utility_l.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'power': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/070_utility_l_power.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_l_man_made(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/utility/060_setup-drop_and_recreate_table_utility_l.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'man_made': 'pipeline'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/utility/080_utility_l_man_made.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.utility_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_water_a(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/water/000_water_abl_create_tables.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'waterway': 'some'})

    engine.execute(osm_models.t_osm_polygon.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/water/010_water_a_insert_table.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.water_a").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_water_b(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/water/000_water_abl_create_tables.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'leisure': 'marina'})

    engine.execute(osm_models.t_osm_point.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/water/020_water_b_insert_table.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.water_p").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label


@slow
def test_label_water_l(osmaxx_schemas, label_input):
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/water/000_water_abl_create_tables.sql'
    engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))

    expected_label = label_input.pop('expected_label')
    label_input.update({'waterway': 'some'})

    engine.execute(osm_models.t_osm_line.insert().values(**label_input).execution_options(autocommit=True))

    address_script = 'sql/filter/water/030_water_l_insert_table.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.water_l").execution_options(autocommit=True))
    assert result.fetchone()['label'] == expected_label
