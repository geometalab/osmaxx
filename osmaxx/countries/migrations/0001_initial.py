# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import osmaxx.countries.storage
import osmaxx.countries.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('polyfile', osmaxx.countries.fields.InternalCountryFileField(storage=osmaxx.countries.storage.CountryInternalStorage, verbose_name='polyfile', upload_to='')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='polygon')),
                ('simplified_polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='simplified area')),
            ],
        ),
    ]
