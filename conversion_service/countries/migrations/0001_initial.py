# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import countries.storage
import django.contrib.gis.db.models.fields
import countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('polyfile', countries.fields.InternalCountryFileField(verbose_name='polyfile', storage=countries.storage.CountryModuleInternalStorage, upload_to='')),
                ('associated_multipolygon', django.contrib.gis.db.models.fields.MultiPolygonField(verbose_name='associated_multipolygon', srid=4326)),
            ],
        ),
    ]
