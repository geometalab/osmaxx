# Generated by Django 3.2.6 on 2021-09-01 06:33

from django.db import migrations


def add_update_worker_jobs(apps, schema_editor):
    MINUTES = "minutes"  # we can't use from IntervalSchedule.MINUTES in migrations :-(

    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")

    # add schedule to send emails, every 10 minutes
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=MINUTES,
    )
    # handle unfinished jobs
    PeriodicTask.objects.create(
        interval=schedule,
        name="handle timed out worker jobs",
        task="osmaxx.conversion.tasks.handle_unfinished_exports",
    )
    # schedule mail sending
    PeriodicTask.objects.create(
        interval=schedule,
        name="send mails for finished exports",
        task="osmaxx.conversion.tasks.call_websites_to_send_mails",
    )


def revert(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    PeriodicTask.objects.filter(name="handle timed out worker jobs").delete()
    PeriodicTask.objects.filter(name="send mails for finished exports").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("excerptexport", "0064_extractionorder_invoke_update_url"),
    ]

    operations = [
        migrations.RunPython(add_update_worker_jobs, revert),
    ]
