# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0007_auto_20150407_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='excerpt_old',
        ),
    ]
