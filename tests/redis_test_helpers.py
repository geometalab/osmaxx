import django_rq


def perform_all_jobs_sync():
    worker = django_rq.get_worker()
    worker.work(burst=True)
