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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('rq_job_id', models.CharField(verbose_name='rq job id', max_length=250)),
                ('callback_url', models.URLField(verbose_name='callback url', max_length=250)),
                ('status', models.IntegerField(verbose_name='job status', choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')])),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('west', models.FloatField(verbose_name='west', null=True, blank=True)),
                ('south', models.FloatField(verbose_name='south', null=True, blank=True)),
                ('east', models.FloatField(verbose_name='east', null=True, blank=True)),
                ('north', models.FloatField(verbose_name='north', null=True, blank=True)),
                ('polyfile', models.FileField(verbose_name='polyfile', null=True, blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='GISFormat',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('format', models.CharField(verbose_name='format', max_length=10, choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite')])),
                ('progress', models.IntegerField(verbose_name='progress', null=True, blank=True, choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')])),
                ('conversion_job', models.ForeignKey(verbose_name='conversion job', related_name='gis_formats', to='conversion_job.ConversionJob')),
            ],
        ),
        migrations.CreateModel(
            name='GISOption',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('crs', models.CharField(verbose_name='coordinate reference system', max_length=100, choices=[('WGS_84', 'WGS 84')])),
                ('detail_level', models.IntegerField(verbose_name='detail level', choices=[(1, 'verbatim'), (2, 'simplified'), (3, 'combined')])),
            ],
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='extent',
            field=models.OneToOneField(verbose_name='Extent', to='conversion_job.Extent'),
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='gis_option',
            field=models.OneToOneField(verbose_name='conversion job', to='conversion_job.GISOption', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='gisformat',
            unique_together=set([('conversion_job', 'format')]),
        ),
    ]
