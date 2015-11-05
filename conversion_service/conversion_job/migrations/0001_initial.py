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
                ('rq_job_id', models.CharField(verbose_name='rq job id', max_length=250)),
                ('callback_url', models.URLField(verbose_name='callback url', max_length=250)),
                ('status', models.IntegerField(verbose_name='job status', choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')])),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('west', models.FloatField(verbose_name='west', null=True, blank=True)),
                ('south', models.FloatField(verbose_name='south', null=True, blank=True)),
                ('east', models.FloatField(verbose_name='east', null=True, blank=True)),
                ('north', models.FloatField(verbose_name='north', null=True, blank=True)),
                ('polyfile', models.FileField(verbose_name='polyfile', null=True, blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FormatOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('output_format', models.CharField(verbose_name='format', choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite')], max_length=100)),
                ('progress', models.IntegerField(verbose_name='progress', choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')])),
                ('conversion_job', models.ForeignKey(verbose_name='conversion job', related_name='format_options', to='conversion_job.ConversionJob')),
            ],
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='extent',
            field=models.OneToOneField(verbose_name='Extent', to='conversion_job.Extent'),
        ),
    ]
