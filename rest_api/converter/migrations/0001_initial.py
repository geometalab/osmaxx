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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rq_job_id', models.CharField(verbose_name='rq job id', max_length=250)),
                ('callback_url', models.URLField(verbose_name='callback url', max_length=250)),
                ('status', models.IntegerField(verbose_name='job status', choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')])),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('west', models.FloatField(blank=True, verbose_name='west', null=True)),
                ('south', models.FloatField(blank=True, verbose_name='south', null=True)),
                ('east', models.FloatField(blank=True, verbose_name='east', null=True)),
                ('north', models.FloatField(blank=True, verbose_name='north', null=True)),
                ('polyfile', models.FileField(blank=True, verbose_name='polyfile', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('progress', models.IntegerField(verbose_name='progress', choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')])),
                ('conversion_job', models.ForeignKey(verbose_name='conversion job', related_name='formats', to='conversion_job.ConversionJob')),
            ],
        ),
    ]
