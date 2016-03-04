# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClippingArea',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
                ('clipping_multi_polygon', django.contrib.gis.db.models.fields.MultiPolygonField(verbose_name='clipping MultiPolygon', srid=4326)),
            ],
        ),
    ]
