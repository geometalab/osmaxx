# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0008_remove_boundinggeometry_excerpt_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(default=None, to='excerptexport.BoundingGeometry'),
            preserve_default=False,
        ),
    ]
