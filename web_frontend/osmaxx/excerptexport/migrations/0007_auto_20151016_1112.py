# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0006_auto_20150918_1244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excerpt',
            old_name='bounding_geometry_raw_reference',
            new_name='bounding_geometry',
        ),
    ]
