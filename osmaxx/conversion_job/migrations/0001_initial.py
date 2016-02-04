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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rq_job_id', models.CharField(max_length=250, verbose_name='rq job id')),
                ('callback_url', models.URLField(max_length=250, verbose_name='callback url')),
                ('status', models.IntegerField(default=0, verbose_name='job status', choices=[(0, 'new'), (1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')])),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('west', models.FloatField(blank=True, null=True, verbose_name='west')),
                ('south', models.FloatField(blank=True, null=True, verbose_name='south')),
                ('east', models.FloatField(blank=True, null=True, verbose_name='east')),
                ('north', models.FloatField(blank=True, null=True, verbose_name='north')),
                ('polyfile', models.FileField(blank=True, verbose_name='polyfile', upload_to='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GISFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('format', models.CharField(max_length=10, verbose_name='format', choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite')])),
                ('progress', models.IntegerField(default=0, verbose_name='progress', choices=[(0, 'new'), (1, 'received'), (2, 'started'), (3, 'successful'), (-1, 'error')])),
                ('conversion_job', models.ForeignKey(verbose_name='conversion job', related_name='gis_formats', to='conversion_job.ConversionJob')),
            ],
        ),
        migrations.CreateModel(
            name='GISOption',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('coordinate_reference_system', models.CharField(max_length=100, verbose_name='coordinate reference system', choices=[('WGS_84', 'WGS 84')])),
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
            name='gis_options',
            field=models.OneToOneField(verbose_name='conversion job', to='conversion_job.GISOption', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='gisformat',
            unique_together=set([('conversion_job', 'format')]),
        ),
    ]
