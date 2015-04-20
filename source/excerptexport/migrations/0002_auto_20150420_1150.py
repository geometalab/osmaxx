# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.geos import GEOSGeometry

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boundinggeometry',
            name='north_east',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, default=GEOSGeometry('POINT(0.0 0.0)')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='boundinggeometry',
            name='south_west',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, default=GEOSGeometry('POINT(0.0 0.0)')),
            preserve_default=True,
        ),
    ]
