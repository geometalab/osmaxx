from collections import namedtuple

import pytest


@pytest.fixture
def queue(fake_rq_id):
    Queue = namedtuple('Queue', ['job_ids'])
    queue = Queue(job_ids=[str(fake_rq_id)])
    return queue


def test_handle_failed_jobs_calls_update_job(mocker, fake_rq_id, queue):
    from osmaxx.conversion.management.commands import result_harvester
    mocker.patch('django_rq.get_failed_queue', return_value=queue)
    cmd = result_harvester.Command()
    _update_job_mock = mocker.patch.object(cmd, '_update_job')
    cmd._handle_failed_jobs()
    assert _update_job_mock.call_count == 1
    _update_job_mock.assert_called_once_with(job_id=str(fake_rq_id), queue=queue)


@pytest.mark.django_db()
def test_handle_successfull_jobs_calls_update_job(mocker, queue, conversion_job_started):
    from osmaxx.conversion.management.commands import result_harvester
    mocker.patch('django_rq.get_queue', return_value=queue)
    cmd = result_harvester.Command()
    _update_job_mock = mocker.patch.object(cmd, '_update_job')
    cmd._handle_running_jobs()
    assert _update_job_mock.call_count == 1
    _update_job_mock.assert_called_once_with(job_id=str(conversion_job_started.rq_job_id), queue=queue)
