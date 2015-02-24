# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptExport', '0002_auto_20150224_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excerpt',
            name='bounding_box',
        ),
        migrations.AddField(
            model_name='boundinggeometry',
            name='excerpt',
            field=models.OneToOneField(null=True, to='excerptExport.Excerpt'),
            preserve_default=True,
        ),
    ]
