# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0005_auto_20150407_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(to='excerptexport.BoundingGeometry', null=True),
            preserve_default=True,
        ),
    ]
