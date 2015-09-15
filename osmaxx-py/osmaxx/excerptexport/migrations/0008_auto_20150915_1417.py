# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0007_auto_20150915_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputfile',
            name='content_type',
            field=models.CharField(blank=True, verbose_name='content type', max_length=64, null=True),
        ),
    ]
