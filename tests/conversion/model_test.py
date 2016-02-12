import os

import pytest


@pytest.mark.django_db()
def test_job_get_download_url_returns_none_when_file_missing(conversion_job_started, conversion_job_failed):
    assert conversion_job_started.status == conversion_job_started.STARTED
    assert conversion_job_started.get_download_url() is None

    assert conversion_job_failed.status == conversion_job_started.FAILED
    assert conversion_job_failed.get_download_url() is None


@pytest.mark.django_db()
def test_job_get_download_url_returns_path_when_file_done(conversion_job_finished):
    assert conversion_job_finished.status == conversion_job_finished.FINISHED
    assert conversion_job_finished.get_download_url() is not None
    assert conversion_job_finished.get_download_url() == conversion_job_finished.get_absolute_url() + 'download-zip/'


@pytest.mark.django_db()
def test_job_removes_file_when_deleted(conversion_job_finished):
    assert conversion_job_finished.status == conversion_job_finished.FINISHED
    file_path = conversion_job_finished.resulting_file.name
    assert file_path is not None
    assert os.path.exists(file_path)
    conversion_job_finished.delete()
    assert not os.path.exists(file_path)
