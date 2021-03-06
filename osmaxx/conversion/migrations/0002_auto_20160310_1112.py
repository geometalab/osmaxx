# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrization',
            name='out_format',
            field=models.CharField(choices=[('fgdb', 'ESRI File Geodatabase'), ('shapefile', 'ESRI Shapefile'), ('gpkg', 'GeoPackage'), ('spatialite', 'SpatiaLite'), ('garmin', 'Garmin navigation & map data')], max_length=100, verbose_name='out format'),
        ),
    ]
