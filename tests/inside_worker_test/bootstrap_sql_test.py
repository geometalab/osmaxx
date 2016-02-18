import os

import pytest
import sqlalchemy

from tests.inside_worker_test.conftest import sql_from_bootstrap_relative_location
from tests.inside_worker_test.declarative_schema import osm_models

worker_only_test = pytest.mark.skipif(
    not os.environ.get("TEST_INSIDE_WORKER", False),
    reason="This tests only runs in special enviroment"
)

db_name = 'osmaxx_db'

gis_db_connection_kwargs = dict(username='postgres', password='postgres', database=db_name)


international_text_strings = [
    ('ascii', 'some normal ascii', 'some normal ascii'),
    ('umlaut', 'öäüüäüö', 'öäüüäüö'),
    ('special_chars', "*+?'^'%ç#", "*+?'^'%ç#"),
    ('japanese', "大洲南部広域農道", 'dà zhōu nán bù guǎng yù nóng dào'),
    ('chinese russian', "二连浩特市 Эрээн хот", 'èr lián hào tè shì Éréén hot'),
    ('arabic', "شارع المنيرة الرئيسي", 'sẖạrʿ ạlmnyrẗ ạlrỷysy'),
    # transliteration doesn't work on eritrean characters!
    ('eritrean', 'ጋሽ-ባርካ', 'ጋሽ-ባርካ'),
]


@pytest.fixture(params=international_text_strings)
def international_text(request):
    return dict(
        variant=request.param[0],
        text=request.param[1],
        expected=request.param[2],
    )


@worker_only_test
def test_label_transliterated_correctly(osmaxx_schemas, international_text):
    no_row_operation = -1
    engine = osmaxx_schemas
    address_script_setup = 'sql/filter/address/000_setup-drop_and_recreate_table.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script_setup)).execution_options(autocommit=True))
    assert result.rowcount == no_row_operation

    default_params = {'name': international_text['text'], 'addr:street': 'somevalue', 'building': 'some', 'entrance': None, }
    engine.execute(osm_models.t_osm_point.insert().values(**default_params).execution_options(autocommit=True))

    address_script = 'sql/filter/address/010_address.sql'
    result = engine.execute(sqlalchemy.text(sql_from_bootstrap_relative_location(address_script)).execution_options(autocommit=True))
    assert result.rowcount == 1

    result = engine.execute(sqlalchemy.text("select label from osmaxx.address_p").execution_options(autocommit=True))
    assert result.rowcount == 1
    results = result.fetchall()
    assert len(results) == 1
    assert results[0]['label'] == international_text['expected']


xeno = "大洲南部広域農道"
xeno_transliterated = 'dà zhōu nán bù guǎng yù nóng dào'
latin = 'Turicum'


@pytest.fixture(params=[
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
])
def label_input(request):
    return request.param


@worker_only_test
def test_label(osmaxx_schemas, label_input):
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
