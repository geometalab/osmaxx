import os
import shutil

import pytest
from django.core.management import call_command
from django.utils import timezone
from django.utils.six import StringIO

from osmaxx.excerptexport.models import OutputFile


@pytest.fixture
def expired_output_file_with_file(db, output_file_with_file, mocker):
    just_a_bit_too_old = timezone.now() - timezone.timedelta(minutes=1)

    output_file_with_file.file_removal_at = just_a_bit_too_old
    output_file_with_file.save()

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.file_removal_at == just_a_bit_too_old

    return output_file_with_file


@pytest.fixture
def expired_output_file(db, output_file, mocker):
    just_a_bit_too_old = timezone.now() - timezone.timedelta(minutes=1)

    output_file.file_removal_at = just_a_bit_too_old
    output_file.save()

    output_file.refresh_from_db()

    assert output_file.file_removal_at == just_a_bit_too_old

    return output_file


def test_purge_expired_result_files_call_exists(db):
    out = StringIO()
    call_command('purge_expired_result_files', '--run_once', stdout=out)
    assert 'Removing output files that expired before ' in out.getvalue()


def test_purge_expired_result_files_with_existing_files_leaves_it_be_when_younger(db, output_file_with_file):
    assert output_file_with_file.file

    out = StringIO()
    call_command('purge_expired_result_files', '--run_once', stdout=out)

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.file
    assert os.path.exists(output_file_with_file.file.path)


def test_purge_expired_result_files_with_existing_files_removes_it_when_older(expired_output_file_with_file):
    assert expired_output_file_with_file.file
    old_id = expired_output_file_with_file.id

    file_path = expired_output_file_with_file.file.path
    pk = expired_output_file_with_file.id
    expected_output = "Output File #{}: {} removed".format(pk, file_path)
    out = StringIO()
    call_command('purge_expired_result_files', '--run_once', stdout=out)

    assert not os.path.exists(file_path)
    assert expected_output in out.getvalue()
    assert OutputFile.objects.filter(pk=old_id).count() == 0


def test_cleanup_old_result_files_when_existing_file_directory_has_been_removed_by_someone_else(expired_output_file_with_file):
    file_path = expired_output_file_with_file.file.path
    shutil.rmtree(os.path.dirname(file_path))

    assert expired_output_file_with_file.file
    old_id = expired_output_file_with_file.id

    call_command('purge_expired_result_files', '--run_once')

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert OutputFile.objects.filter(pk=old_id).count() == 0


def test_old_result_files_directory_is_being_removed_when_existing_file_has_been_removed_by_someone_else(expired_output_file_with_file):
    file_path = expired_output_file_with_file.file.path
    os.remove(file_path)

    assert expired_output_file_with_file.file
    old_id = expired_output_file_with_file.id

    call_command('purge_expired_result_files', '--run_once')

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert OutputFile.objects.filter(pk=old_id).count() == 0


def test_old_result_file_without_associated_file_doesnt_raise(expired_output_file):
    call_command('purge_expired_result_files', '--run_once')
    old_id = expired_output_file.id
    assert OutputFile.objects.filter(pk=old_id).count() == 0
