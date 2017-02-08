import pytest
import subprocess

from osmaxx.conversion.converters import utils


@pytest.fixture
def subprocess_check_call_mock(mocker):
    return mocker.patch.object(subprocess, 'check_call')


def test_logged_check_call_accepts_params(subprocess_check_call_mock):
    test_call = ['echo', '0']
    utils.logged_check_call(test_call)
    subprocess_check_call_mock.assert_called_with(test_call)

    test_call = "echo 0"
    utils.logged_check_call(test_call, shell=True)
    subprocess_check_call_mock.assert_called_with(test_call, shell=True)


def test_logged_check_call_raises():
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        test_call = ['false']
        utils.logged_check_call(test_call)
    assert excinfo.value.output is None
    assert excinfo.value.returncode == 1


def test_logged_check_call_logs_error_content(mocker, subprocess_check_call_mock):
    error_output = 'example output that is available'
    error_return_code = 17
    command = 'cmd'
    error = subprocess.CalledProcessError(cmd=command, output=error_output, returncode=error_return_code)
    subprocess_check_call_mock.side_effect = error

    logger_mock = mocker.patch.object(utils.logger, 'error')
    with pytest.raises(subprocess.CalledProcessError):
        utils.logged_check_call(command)
    logger_mock.assert_called_with('Command `{}` exited with return value {}\nOutput:\n{}'
                                   .format(command, error_return_code, error_output))
