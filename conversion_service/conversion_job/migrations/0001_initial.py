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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rq_job_id', models.CharField(verbose_name='rq job id', max_length=250)),
                ('callback_url', models.URLField(verbose_name='callback url', max_length=250)),
                ('status', models.IntegerField(choices=[(0, 'new'), (1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')], default=0, verbose_name='job status')),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('west', models.FloatField(blank=True, null=True, verbose_name='west')),
                ('south', models.FloatField(blank=True, null=True, verbose_name='south')),
                ('east', models.FloatField(blank=True, null=True, verbose_name='east')),
                ('north', models.FloatField(blank=True, null=True, verbose_name='north')),
                ('polyfile', models.FileField(verbose_name='polyfile', null=True, blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='GISFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(verbose_name='format', choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite')], max_length=10)),
                ('progress', models.IntegerField(choices=[(0, 'new'), (1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')], default=0, verbose_name='progress')),
                ('conversion_job', models.ForeignKey(to='conversion_job.ConversionJob', related_name='gis_formats', verbose_name='conversion job')),
            ],
        ),
        migrations.CreateModel(
            name='GISOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crs', models.CharField(verbose_name='coordinate reference system', choices=[('WGS_84', 'WGS 84')], max_length=100)),
                ('detail_level', models.IntegerField(choices=[(1, 'verbatim'), (2, 'simplified'), (3, 'combined')], verbose_name='detail level')),
            ],
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='extent',
            field=models.OneToOneField(to='conversion_job.Extent', verbose_name='Extent'),
        ),
        migrations.AddField(
            model_name='conversionjob',
            name='gis_option',
            field=models.OneToOneField(to='conversion_job.GISOption', null=True, verbose_name='conversion job'),
        ),
        migrations.AlterUniqueTogether(
            name='gisformat',
            unique_together=set([('conversion_job', 'format')]),
        ),
    ]
