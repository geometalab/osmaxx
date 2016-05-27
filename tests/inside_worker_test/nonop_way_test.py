from contextlib import closing
from copy import deepcopy

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models

MAJOR_KEYS = frozenset({'highway', 'railway'})


@slow
def test_osm_object_without_status_does_not_end_up_in_nonop(non_lifecycle_data_import, nonop_l):
    engine = non_lifecycle_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(nonop_l))) as result:
        assert result.rowcount == 0


@slow
def test_osm_object_with_status_ends_up_in_nonop(lifecycle_data_import, nonop_l):
    engine = lifecycle_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(nonop_l))) as result:
        assert result.rowcount == 1


@pytest.fixture
def nonop_l():
    return DbTable('nonop_l', osm_models.metadata, schema='view_osmaxx')


@pytest.yield_fixture
def lifecycle_data_import(lifecycle_data, data_import):
    with data_import(lifecycle_data) as engine:
        yield engine


@pytest.yield_fixture
def non_lifecycle_data_import(non_lifecycle_data, data_import):
    with data_import(non_lifecycle_data) as engine:
        yield engine


@pytest.fixture
def lifecycle_data(non_lifecycle_osm_tags, osm_status):
    major_keys = MAJOR_KEYS.intersection(non_lifecycle_osm_tags)
    assert len(major_keys) == 1
    major_tag_key = next(iter(major_keys))
    osm_tags = deepcopy(non_lifecycle_osm_tags)
    major_tag_value = osm_tags.pop(major_tag_key)
    osm_tags.update({major_tag_key: osm_status, osm_status: major_tag_value})
    assert len(osm_tags) == len(non_lifecycle_osm_tags) + 1
    return {osm_models.t_osm_line: osm_tags}


@pytest.fixture
def non_lifecycle_data(non_lifecycle_osm_tags):
    return {osm_models.t_osm_line: non_lifecycle_osm_tags}


@pytest.fixture
def non_lifecycle_osm_tags(non_lifecycle_osm_tags_and_expected_nonop_subtype):
    osm_tags, _ = non_lifecycle_osm_tags_and_expected_nonop_subtype
    return osm_tags


@pytest.fixture
def expected_nonop_subtype(non_lifecycle_osm_tags_and_expected_nonop_subtype):
    _, subtype = non_lifecycle_osm_tags_and_expected_nonop_subtype
    return subtype


@pytest.fixture
def osm_status(osm_status_and_expected_osmaxx_status):
    status, _ = osm_status_and_expected_osmaxx_status
    return status


@pytest.fixture
def expected_osmaxx_status(osm_status_and_expected_osmaxx_status):
    _, osmaxx_status = osm_status_and_expected_osmaxx_status
    return osmaxx_status


@pytest.fixture(
    params=[
        (dict(highway='track'), 'track'),
        (dict(highway='track', tracktype='grade3'), 'grade3'),
        (dict(highway='footway'), 'footway'),
    ],
    ids=[
        'highway=track',
        'highway=track tracktype=grade3',
        'highway=footway',
    ],
)
def non_lifecycle_osm_tags_and_expected_nonop_subtype(request):
    return request.param


@pytest.fixture(
    params=[
        ('planned', 'P'),
        ('disused', 'D'),
        ('construction', 'C'),
        ('abandoned', 'A'),
    ],
    ids=[
        'planned',
        'disused',
        'construction',
        'abandoned',
    ],
)
def osm_status_and_expected_osmaxx_status(request):
    return request.param
