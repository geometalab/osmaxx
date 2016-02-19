import os

import pytest


@pytest.mark.django_db()
def test_job_get_download_url_returns_none_when_file_missing(started_conversion_job, conversion_job_failed):
    assert started_conversion_job.status == started_conversion_job.STARTED
    assert started_conversion_job.get_download_url() is None

    assert conversion_job_failed.status == started_conversion_job.FAILED
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


@pytest.mark.django_db()
def test_job_get_download_url_removes_trailing_slashes_from_callback_url(conversion_job, server_url):
    from rest_framework.reverse import reverse
    url = server_url + reverse('conversion_job-detail', kwargs={'pk': conversion_job.id})
    own_base_url = server_url + '/'
    conversion_job.own_base_url = own_base_url
    conversion_job.save()
    assert conversion_job.get_absolute_url() == url
