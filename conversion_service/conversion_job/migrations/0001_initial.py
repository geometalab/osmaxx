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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rq_job_id', models.CharField(max_length=250, verbose_name='rq job id')),
                ('callback_url', models.URLField(max_length=250, verbose_name='callback url')),
                ('status', models.IntegerField(choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')], verbose_name='job status')),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('west', models.FloatField(verbose_name='west', null=True, blank=True)),
                ('south', models.FloatField(verbose_name='south', null=True, blank=True)),
                ('east', models.FloatField(verbose_name='east', null=True, blank=True)),
                ('north', models.FloatField(verbose_name='north', null=True, blank=True)),
                ('polyfile', models.FileField(verbose_name='polyfile', null=True, blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('progress', models.IntegerField(choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')], verbose_name='progress')),
                ('conversion_job', models.ForeignKey(related_name='formats', verbose_name='conversion job', to='conversion_job.ConversionJob')),
            ],
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='extent',
            field=models.OneToOneField(verbose_name='Extent', to='conversion_job.Extent'),
        ),
    ]
