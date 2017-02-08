import pytest


def test_logged_check_call_accepts_params(mocker):
    from osmaxx.conversion.converters.utils import logged_check_call
    subprocess_check_call_mock = mocker.patch('osmaxx.conversion.converters.utils.subprocess.check_call')
    test_call = ['echo', '0']
    logged_check_call(test_call)
    subprocess_check_call_mock.assert_called_with(test_call)

    test_call = "echo 0"
    logged_check_call(test_call, shell=True)
    subprocess_check_call_mock.assert_called_with(test_call, shell=True)


def test_logged_check_call_raises(mocker):
    import subprocess
    from osmaxx.conversion.converters.utils import logged_check_call
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        test_call = ['false']
        logged_check_call(test_call)
    assert excinfo.value.output is None
    assert excinfo.value.returncode == 1


def test_logged_check_call_logs_error_content(mocker):
    import subprocess
    from osmaxx.conversion.converters.utils import logged_check_call
    error_output = 'example output that is available'
    error_return_code = 17
    command = 'cmd'
    error = subprocess.CalledProcessError(cmd=command, output=error_output, returncode=error_return_code)
    mocker.patch('osmaxx.conversion.converters.utils.subprocess.check_call', side_effect=error)
    logger_mock = mocker.patch('osmaxx.conversion.converters.utils.logger.error')
    with pytest.raises(subprocess.CalledProcessError):
        logged_check_call(command)
    logger_mock.assert_called_with('Command `{}` exited with return value {}\nOutput:\n{}'
                                   .format(command, error_return_code, error_output))
