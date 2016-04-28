# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0003_auto_20150729_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excerpt',
            old_name='bounding_geometry',
            new_name='_bounding_geometry',
        ),
    ]
