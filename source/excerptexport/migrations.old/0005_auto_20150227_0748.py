# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptExport', '0004_boundinggeometry_geometry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='east',
        ),
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='north',
        ),
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='south',
        ),
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='west',
        ),
    ]
