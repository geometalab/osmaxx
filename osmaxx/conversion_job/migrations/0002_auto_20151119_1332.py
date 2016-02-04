# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion_job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversionjob',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('queued', 'queued'), ('started', 'started'), ('done', 'done'), ('error', 'error')], verbose_name='job status', default='new', max_length=20),
        ),
        migrations.AlterField(
            model_name='gisformat',
            name='progress',
            field=models.CharField(choices=[('new', 'new'), ('received', 'received'), ('started', 'started'), ('successful', 'successful'), ('error', 'error')], verbose_name='progress', default='new', max_length=20),
        ),
    ]
