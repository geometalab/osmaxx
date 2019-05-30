from unittest.mock import Mock, MagicMock, patch
import pytest

from osmaxx.conversion import status


@pytest.fixture
def queue(fake_rq_id):
    job = Mock(**{'get_status.return_value': status.STARTED, 'id': fake_rq_id})
    queue = Mock(**{'fetch_job.return_value': job})
    return queue


@pytest.fixture
def failed_queue(fake_rq_id):
    queue = Mock(**{'failed_job_registry.get_job_ids.return_value': [fake_rq_id]})
    return queue


def test_handle_failed_jobs_calls_set_failed_unless_final(mocker, fake_rq_id, failed_queue):
    mocker.patch('django_rq.get_queue', return_value=failed_queue)

    from osmaxx.conversion.management.commands import result_harvester
    from osmaxx.conversion.models import Job

    conversion_job_mock = Mock()
    mocker.patch.object(Job.objects, 'get', return_value=conversion_job_mock)
    cmd = result_harvester.Command()
    _set_failed_unless_final = mocker.patch.object(cmd, '_set_failed_unless_final')
    _update_job_mock = mocker.patch.object(cmd, '_notify')
    cmd._handle_failed_jobs()
    _set_failed_unless_final.assert_called_once_with(conversion_job_mock, rq_job_id=fake_rq_id)
    _update_job_mock.assert_called_once_with(conversion_job_mock)


@pytest.mark.django_db()
def test_handle_successfull_jobs_calls_update_job(mocker, queue, started_conversion_job):
    mocker.patch('django_rq.get_queue', return_value=queue)
    from osmaxx.conversion.management.commands import result_harvester
    cmd = result_harvester.Command()
    _update_job_mock = mocker.patch.object(cmd, '_update_job')
    cmd._handle_running_jobs()
    assert _update_job_mock.call_count == 1
    _update_job_mock.assert_called_once_with(rq_job_id=str(started_conversion_job.rq_job_id))


@pytest.mark.django_db()
def test_handle_update_job_informs(mocker, queue, fake_rq_id, started_conversion_job):
    mocker.patch('django_rq.get_queue', return_value=queue)
    from osmaxx.conversion.management.commands import result_harvester
    cmd = result_harvester.Command()
    _update_job_mock = mocker.patch.object(cmd, '_notify')
    cmd._update_job(rq_job_id=fake_rq_id)
    assert _update_job_mock.call_count == 1
    _update_job_mock.assert_called_once_with(started_conversion_job)


def test_add_meta_data_to_job_with_out_of_bounds_exception():
    from osmaxx.conversion.management.commands.result_harvester import add_meta_data_to_job
    conversion_job = MagicMock()
    conversion_job.unzipped_result_size = None
    conversion_job.extraction_duration = None
    conversion_job.estimated_pbf_size = None
    conversion_job.parametrization.clipping_area.clipping_multi_polygon.extent = -70, 70, 80, -10
    rq_job = Mock()
    rq_job.meta = {
        'unzipped_result_size': 0,
        'duration': 0,
    }

    with patch('osmaxx.conversion.management.commands.result_harvester.logger') as logger_mock:
        add_meta_data_to_job(
            conversion_job=conversion_job,
            rq_job=rq_job
        )
        logger_mock.exception.assert_called_once_with("pbf estimation failed")
        assert conversion_job.estimated_pbf_size is None


def multiple_queue_test_parameters():
    queue_with_all_jobs = Mock()
    queue_with_no_jobs = Mock()
    queue_with_no_jobs.fetch_job.return_value = None
    return [
        ([queue_with_all_jobs, queue_with_no_jobs], queue_with_all_jobs.fetch_job.return_value),
        ([queue_with_no_jobs, queue_with_all_jobs], queue_with_all_jobs.fetch_job.return_value),
        ([queue_with_no_jobs, queue_with_no_jobs], None),
    ]


@pytest.mark.parametrize("queues,expected", multiple_queue_test_parameters())
def test_multiple_queue_fetch_job(mocker, fake_rq_id, queues, expected):
    from osmaxx.conversion.management.commands.result_harvester import fetch_job

    mocker.patch('django_rq.get_queue', side_effect=queues)
    job = fetch_job(fake_rq_id, ['queue_one', 'queue_two'])
    assert job is expected
