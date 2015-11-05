# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion_job', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConverterOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('output_format', models.CharField(max_length=100, choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite')], verbose_name='format')),
                ('progress', models.IntegerField(choices=[(1, 'received'), (2, 'started'), (10, 'successful'), (-1, 'error')], verbose_name='progress')),
                ('conversion_job', models.ForeignKey(related_name='converter_options', to='conversion_job.ConversionJob', verbose_name='conversion job')),
            ],
        ),
        migrations.RemoveField(
            model_name='formatoption',
            name='conversion_job',
        ),
        migrations.DeleteModel(
            name='FormatOption',
        ),
    ]
