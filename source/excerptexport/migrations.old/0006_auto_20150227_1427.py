# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptExport', '0005_auto_20150227_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputfile',
            name='path',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
    ]
