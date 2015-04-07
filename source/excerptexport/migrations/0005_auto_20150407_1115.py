# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0004_auto_20150324_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boundinggeometry',
            old_name='excerpt',
            new_name='excerpt_old',
        ),
    ]
