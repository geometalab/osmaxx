import os

import pytest

from osmaxx.conversion_api.statuses import STARTED, FAILED, FINISHED


@pytest.mark.django_db()
def test_job_get_download_url_returns_none_when_file_missing(started_conversion_job, failed_conversion_job):
    assert started_conversion_job.status == STARTED
    assert started_conversion_job.get_download_url() is None

    assert failed_conversion_job.status == FAILED
    assert failed_conversion_job.get_download_url() is None


@pytest.mark.django_db()
def test_job_get_download_url_returns_path_when_file_done(finished_conversion_job):
    assert finished_conversion_job.status == FINISHED
    assert finished_conversion_job.get_download_url() is not None
    assert finished_conversion_job.get_download_url() == finished_conversion_job.get_absolute_url() + 'download-zip/'


@pytest.mark.django_db()
def test_job_removes_file_when_deleted(finished_conversion_job):
    assert finished_conversion_job.status == FINISHED
    file_path = finished_conversion_job.resulting_file.path
    assert file_path is not None
    assert os.path.exists(file_path)
    finished_conversion_job.delete()
    assert not os.path.exists(file_path)


@pytest.mark.django_db()
def test_job_get_download_url_removes_trailing_slashes_from_callback_url(conversion_job, server_url):
    from rest_framework.reverse import reverse
    url = server_url + reverse('conversion_job-detail', kwargs={'pk': conversion_job.id})
    own_base_url = server_url + '/'
    conversion_job.own_base_url = own_base_url
    conversion_job.save()
    assert conversion_job.get_absolute_url() == url
