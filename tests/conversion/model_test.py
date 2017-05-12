import os

import pytest

from osmaxx.conversion.constants import status


@pytest.mark.django_db()
def test_job_statuses_for_jobs(started_conversion_job, failed_conversion_job, finished_conversion_job):
    assert started_conversion_job.status == status.STARTED
    assert failed_conversion_job.status == status.FAILED
    assert finished_conversion_job.status == status.FINISHED


@pytest.mark.django_db()
def test_job_removes_file_when_deleted(finished_conversion_job):
    assert finished_conversion_job.status == status.FINISHED
    file_path = finished_conversion_job.resulting_file.path
    assert file_path is not None
    assert os.path.exists(file_path)
    finished_conversion_job.delete()
    assert not os.path.exists(file_path)


@pytest.mark.django_db()
def test_job_get_absolute_file_path_is_available_when_file_is_available(finished_conversion_job):
    assert finished_conversion_job.get_absolute_file_path.startswith('/')
    assert finished_conversion_job.resulting_file.path == finished_conversion_job.get_absolute_file_path


@pytest.mark.django_db()
def test_job_get_absolute_file_path_is_none_when_file_missing(conversion_job, started_conversion_job, failed_conversion_job):
    assert started_conversion_job.get_absolute_file_path is None
    assert failed_conversion_job.get_absolute_file_path is None
    assert conversion_job.get_absolute_file_path is None
