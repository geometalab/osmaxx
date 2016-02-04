# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion_job', '0004_extent_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisformat',
            name='format',
            field=models.CharField(max_length=10, choices=[('fgdb', 'fgdb'), ('shp', 'shp'), ('gpkg', 'gpkg'), ('spatialite', 'spatialite'), ('garmin', 'garmin')], verbose_name='format'),
        ),
    ]
