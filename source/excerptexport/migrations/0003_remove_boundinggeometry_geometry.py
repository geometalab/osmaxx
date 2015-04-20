# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0002_auto_20150420_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='geometry',
        ),
    ]
