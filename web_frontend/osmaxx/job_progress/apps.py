from django.apps import AppConfig


class JobProgressAppConfig(AppConfig):
    name = 'osmaxx.job_progress'
    verbose_name = 'sasdasd'

    def ready(self):
        # See https://docs.djangoproject.com/en/1.8/topics/signals/#connecting-receiver-functions
        import osmaxx.job_progress.signals  # noqa
