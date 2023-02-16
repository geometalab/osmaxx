import pytest
import subprocess

from osmaxx.conversion.converters import utils


@pytest.fixture
def subprocess_check_call_mock(mocker):
    return mocker.patch.object(subprocess, 'run')


def test_logged_check_call_forwards_args(subprocess_check_call_mock):
    test_call = ['echo', '0']
    utils.logged_check_call(test_call)
    subprocess_check_call_mock.assert_called_with(test_call, check=True, capture_output=True)


def test_logged_check_call_forwards_kwargs(subprocess_check_call_mock):
    test_call = "echo 0"
    utils.logged_check_call(test_call, shell=True)
    subprocess_check_call_mock.assert_called_with(test_call, shell=True, check=True, capture_output=True)


def test_logged_check_call_raises():
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        utils.logged_check_call('false')
    # the result should be an CalledProcessError, maybe check on that when done
    assert excinfo.value.output is not None
    assert excinfo.value.returncode == 1


def test_logged_check_call_logs_error_content(mocker, subprocess_check_call_mock):
    error_output = 'example output'
    error_return_code = 17
    command = 'cmd'

    error = subprocess.CalledProcessError(cmd=command, output=error_output, returncode=error_return_code)
    subprocess_check_call_mock.side_effect = error
    logger_mock = mocker.patch.object(utils.logger, 'error')

    with pytest.raises(subprocess.CalledProcessError):
        utils.logged_check_call(command)

    expected_output = 'Command `cmd` exited with return value 17\nOutput:\nexample output'
    logger_mock.assert_called_with(expected_output)
