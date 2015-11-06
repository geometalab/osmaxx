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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('rq_job_id', models.CharField(max_length=250, verbose_name='rq job id')),
                ('callback_url', models.URLField(max_length=250, verbose_name='callback url')),
                ('status', models.IntegerField(choices=[(1, 'queued'), (2, 'started'), (3, 'done'), (-1, 'error')], verbose_name='job status')),
            ],
        ),
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('west', models.FloatField(blank=True, null=True, verbose_name='west')),
                ('south', models.FloatField(blank=True, null=True, verbose_name='south')),
                ('east', models.FloatField(blank=True, null=True, verbose_name='east')),
                ('north', models.FloatField(blank=True, null=True, verbose_name='north')),
                ('polyfile', models.FileField(blank=True, upload_to='', null=True, verbose_name='polyfile')),
            ],
        ),
        migrations.CreateModel(
            name='GISFormat',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('format', models.CharField(choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('sqlite', 'sqlite')], verbose_name='format', max_length=10)),
                ('conversion_job', models.ForeignKey(to='conversion_job.ConversionJob', related_name='gis_formats', verbose_name='conversion job')),
            ],
        ),
        migrations.CreateModel(
            name='GISOption',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('crs', models.CharField(choices=[('WGS 84', 'WGS_84')], verbose_name='coordinate reference system', max_length=100)),
                ('detail_level', models.IntegerField(choices=[('verbatim', 1), ('simplified', 2), ('combined', 3)], verbose_name='detail level')),
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
            field=models.OneToOneField(null=True, to='conversion_job.GISOption', verbose_name='conversion job'),
        ),
        migrations.AlterUniqueTogether(
            name='gisformat',
            unique_together=set([('conversion_job', 'format')]),
        ),
    ]
