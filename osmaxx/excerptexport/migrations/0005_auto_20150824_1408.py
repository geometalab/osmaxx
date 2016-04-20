# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0004_auto_20150819_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excerpt',
            old_name='_bounding_geometry',
            new_name='bounding_geometry_raw_reference',
        ),
    ]
