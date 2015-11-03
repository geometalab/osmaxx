import django.test
from django_rq import get_connection
from rq import get_current_job
from rq.job import Job

from conversion_service.manager.rq_helper import rq_enqueue_with_settings
from tests.redis_test_helpers import perform_all_jobs_sync


def hello():
    job = get_current_job(connection=get_connection())
    job.meta['world'] = 'hello'
    job.save()


class RQConnectionTests(django.test.TestCase):
    def test_meta_not_available_without_fetch(self, *args, **kwargs):
        job = rq_enqueue_with_settings(hello)
        perform_all_jobs_sync()
        self.assertDictEqual(job.meta, {})

    def test_meta_retrieval_with_fetch_succeeds(self, *args, **kwargs):
        job = rq_enqueue_with_settings(hello)
        perform_all_jobs_sync()
        job_fetched = Job.fetch(job.id, connection=get_connection())
        self.assertDictEqual(job_fetched.meta, {'world': 'hello'})
