# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0003_remove_boundinggeometry_geometry'),
    ]

    operations = [
        migrations.RenameModel('BoundingGeometry', 'BBoxBoundingGeometry'),
    ]
