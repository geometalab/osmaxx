# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConversionJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rq_job_id', models.CharField(max_length=250, verbose_name='rq job id')),
                ('callback_url', models.URLField(max_length=250, verbose_name='callback url')),
                ('status', models.IntegerField(choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')], verbose_name='job status')),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('west', models.FloatField(null=True, blank=True, verbose_name='west')),
                ('south', models.FloatField(null=True, blank=True, verbose_name='south')),
                ('east', models.FloatField(null=True, blank=True, verbose_name='east')),
                ('north', models.FloatField(null=True, blank=True, verbose_name='north')),
                ('polyfile', models.FileField(null=True, blank=True, verbose_name='polyfile', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('progress', models.IntegerField(choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')], verbose_name='progress')),
                ('conversion_job', models.ForeignKey(related_name='formats', to='conversion_job.ConversionJob', verbose_name='conversion job')),
            ],
        ),
    ]
