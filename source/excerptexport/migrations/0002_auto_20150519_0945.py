# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OsmosisPolygonFilterBoundingGeometry',
            fields=[
                ('boundinggeometry_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='excerptexport.BoundingGeometry')),
                ('polygon_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/var/www/eda/projects/data/private/'), upload_to='')),
            ],
            bases=('excerptexport.boundinggeometry',),
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/var/www/eda/projects/data/private/'), blank=True, upload_to='', null=True, verbose_name='file'),
        ),
    ]
