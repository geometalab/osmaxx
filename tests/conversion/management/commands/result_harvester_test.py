from unittest.mock import Mock, MagicMock, patch


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
        assert conversion_job.unzipped_result_size == 0
        assert conversion_job.extraction_duration == 0
        assert conversion_job.estimated_pbf_size is None
