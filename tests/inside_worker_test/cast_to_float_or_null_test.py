import pytest
import sqlalchemy

from tests.inside_worker_test.conftest import slow


@pytest.fixture(params=[2, 2.2, 3.898986, "3.898986", "6", "0.2", 0.6])
def valid_float_representation(request):
    return request.param


@pytest.fixture(params=["a2", "10b", "3.898986k", "3k.898986", "l6.9"])
def invalid_floats(request):
    return request.param


@slow
def test_cast_to_float_null_if_failed_returns_floats_with_valid_floats(osmaxx_functions, valid_float_representation):
    engine = osmaxx_functions
    result = engine.execute(
        sqlalchemy.text(
            "select cast_to_float_null_if_failed($${}$$) as float_value;".format(valid_float_representation)
        ).execution_options(autocommit=True)
    )
    assert result.rowcount == 1
    results = result.fetchall()
    assert len(results) == 1
    assert results[0]['float_value'] == float(valid_float_representation)


@slow
def test_cast_to_float_null_if_failed_returns_null_with_invalid_floats(osmaxx_functions, invalid_floats):
    engine = osmaxx_functions
    result = engine.execute(
        sqlalchemy.text(
            "select cast_to_float_null_if_failed($${}$$) as float_value;".format(invalid_floats)
        ).execution_options(autocommit=True)
    )
    assert result.rowcount == 1
    results = result.fetchall()
    assert len(results) == 1
    assert results[0]['float_value'] is None
