import os
import shutil

import pytest
from django.core.management import call_command
from django.utils import timezone
from django.utils.six import StringIO


@pytest.fixture
def output_file_with_file_too_old(db, output_file_with_file, mocker):
    from osmaxx.excerptexport._settings import RESULT_FILE_AVAILABILITY_DURATION
    just_a_bit_too_old = timezone.now() - RESULT_FILE_AVAILABILITY_DURATION - timezone.timedelta(minutes=1)

    output_file_with_file.file_removal_at = just_a_bit_too_old
    output_file_with_file.save()

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.file_removal_at == just_a_bit_too_old

    return output_file_with_file


def test_purge_old_result_files_call_exists():
    out = StringIO()
    call_command('purge_old_result_files', '--run_once', stdout=out)
    assert 'Removing output files that expired before ' in out.getvalue()


def test_purge_old_result_files_with_existing_files_leaves_it_be_when_younger(db, output_file_with_file):
    assert output_file_with_file.file

    out = StringIO()
    call_command('purge_old_result_files', '--run_once', stdout=out)

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.file
    assert os.path.exists(output_file_with_file.file.path)


def test_purge_old_result_files_with_existing_files_removes_it_be_when_older(output_file_with_file_too_old):
    assert output_file_with_file_too_old.file

    file_path = output_file_with_file_too_old.file.path
    expected_output = "removed {}".format(file_path)
    out = StringIO()
    call_command('purge_old_result_files', '--run_once', stdout=out)

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert expected_output in out.getvalue()
    assert not output_file_with_file_too_old.file


def test_cleanup_old_result_files_when_existing_file_has_been_removed_by_someone_else(output_file_with_file_too_old):
    file_path = output_file_with_file_too_old.file.path
    shutil.rmtree(os.path.dirname(file_path))

    assert output_file_with_file_too_old.file

    call_command('purge_old_result_files', '--run_once')

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert not output_file_with_file_too_old.file


def test_old_result_files_directory_is_being_removed_when_existing_file_has_been_removed_by_someone_else(output_file_with_file_too_old):
    file_path = output_file_with_file_too_old.file.path
    os.remove(file_path)

    assert output_file_with_file_too_old.file

    call_command('purge_old_result_files', '--run_once')

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert not output_file_with_file_too_old.file
