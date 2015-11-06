import django.test
from django_rq import get_connection
from rq import get_current_job
from rq.job import Job

from conversion_service.manager.rq_helper import rq_enqueue_with_settings
from tests.redis_test_helpers import perform_all_jobs_sync


def store_in_job(key, value):
    job = get_current_job(connection=get_connection())
    job.meta[key] = value
    job.save()


def return_result(result):
    return result


class RQMetaDataTests(django.test.TestCase):
    def test_stored_metadata_is_not_available_on_original_job_proxy_object(self):
        job = rq_enqueue_with_settings(store_in_job, 'world', 'hello')
        perform_all_jobs_sync()
        self.assertDictEqual(job.meta, {})

    def test_stored_metadata_can_be_retrieved_from_freshly_fetched_job(self):
        job = rq_enqueue_with_settings(store_in_job, 'world', 'hello')
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertDictEqual(job_fetched.meta, {'world': 'hello'})

    def test_stored_metadata_value_can_be_an_arbitrary_pickleable_object(self):
        nontrivial_pickleable_object = {'the value': ['can', b'e', ('an arbitrary', 'pickleable'), object]}
        job = rq_enqueue_with_settings(store_in_job, 'world', nontrivial_pickleable_object)
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertDictEqual(job_fetched.meta, {'world': nontrivial_pickleable_object})

    def test_stored_metadata_key_can_be_an_arbitrary_hashable_object(self):
        nontrivial_hashable_object = ('the key', ('can', b'e', ('an arbitrary', 'hashable'), object))
        job = rq_enqueue_with_settings(store_in_job, nontrivial_hashable_object, 'hello')
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertEqual(job_fetched.meta[nontrivial_hashable_object], 'hello')


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
