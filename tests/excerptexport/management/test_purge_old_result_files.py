import datetime
import os
import shutil

import pytest
from django.core.management import call_command
from django.utils.six import StringIO

from osmaxx.excerptexport.models.export import TimeStampModelMixin


def timestamp_model_mixin_save_side_effect(self, *args, **kwargs):
    super(TimeStampModelMixin, self).save(*args, **kwargs)


@pytest.fixture
def output_file_with_file_too_old(db, output_file_with_file, mocker):
    from osmaxx.excerptexport._settings import PURGE_OLD_RESULT_FILES_AFTER
    just_a_bit_too_old = datetime.datetime.now() - PURGE_OLD_RESULT_FILES_AFTER - datetime.timedelta(minutes=1)

    mocker.patch.object(TimeStampModelMixin, 'save', timestamp_model_mixin_save_side_effect)

    export = output_file_with_file.export
    export.updated_at = just_a_bit_too_old
    export.save()

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.export.updated_at == just_a_bit_too_old

    return output_file_with_file


def test_purge_old_result_files_call_exists():
    out = StringIO()
    call_command('purge_old_result_files', stdout=out)
    assert 'Removing old output files that are older than ' in out.getvalue()


def test_purge_old_result_files_with_existing_files_leaves_it_be_when_younger(db, output_file_with_file):
    assert output_file_with_file.file
    output_file_with_file.save()  # we use the side-effect of the date being set to now() in case of saving
    out = StringIO()
    call_command('purge_old_result_files', stdout=out)

    output_file_with_file.refresh_from_db()

    assert output_file_with_file.file
    assert os.path.exists(output_file_with_file.file.path)


def test_purge_old_result_files_with_existing_files_removes_it_be_when_older(output_file_with_file_too_old):
    assert output_file_with_file_too_old.file

    file_path = output_file_with_file_too_old.file.path
    expected_output = "removed {}".format(file_path)
    out = StringIO()
    call_command('purge_old_result_files', stdout=out)

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert expected_output in out.getvalue()
    assert not output_file_with_file_too_old.file


def test_cleanup_old_result_files_when_existing_file_has_been_removed_by_someone_else(output_file_with_file_too_old):
    file_path = output_file_with_file_too_old.file.path
    shutil.rmtree(os.path.dirname(file_path))

    assert output_file_with_file_too_old.file

    call_command('purge_old_result_files')

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert not output_file_with_file_too_old.file


def test_old_result_files_directory_is_being_removed_when_existing_file_has_been_removed_by_someone_else(output_file_with_file_too_old):
    file_path = output_file_with_file_too_old.file.path
    os.remove(file_path)

    assert output_file_with_file_too_old.file

    call_command('purge_old_result_files')

    output_file_with_file_too_old.refresh_from_db()

    assert not os.path.exists(file_path)
    assert not os.path.exists(os.path.dirname(file_path))
    assert not output_file_with_file_too_old.file
