import django.test
from django_rq import get_connection
from rq import get_current_job
from rq.job import Job

from manager.rq_helper import rq_enqueue_with_settings
from tests.redis_test_helpers import perform_all_jobs_sync


def store_helloworld_in_job():
    job = get_current_job(connection=get_connection())
    job.meta['world'] = 'hello'
    job.save()


def return_result(result):
    return result


class RQMetaDataTests(django.test.TestCase):
    def test_stored_metadata_is_not_available_on_original_job_proxy_object(self, *args, **kwargs):
        job = rq_enqueue_with_settings(store_helloworld_in_job)
        perform_all_jobs_sync()
        self.assertDictEqual(job.meta, {})

    def test_stored_metadata_can_be_retrieved_from_freshly_fetched_job(self, *args, **kwargs):
        job = rq_enqueue_with_settings(store_helloworld_in_job)
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertDictEqual(job_fetched.meta, {'world': 'hello'})


class RQResultTest(django.test.TestCase):
    def test_result_is_not_available_before_job_has_run(self):
        job = rq_enqueue_with_settings(return_result)
        try:
            self.assertIsNone(job.result)
        finally:
            perform_all_jobs_sync()

    def test_result_is_available_after_job_has_run(self):
        job = rq_enqueue_with_settings(return_result, 'the result')
        perform_all_jobs_sync()
        self.assertEqual(job.result, 'the result')

    def test_result_can_be_an_arbitrary_pickleable_object(self):
        nontrivial_pickleable_object = {'the result': ['can', b'e', ('an arbitrary', 'pickleable'), object]}
        job = rq_enqueue_with_settings(return_result, nontrivial_pickleable_object)
        perform_all_jobs_sync()
        self.assertEqual(job.result, nontrivial_pickleable_object)
