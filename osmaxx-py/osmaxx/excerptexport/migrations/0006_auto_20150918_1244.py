# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0005_auto_20150824_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputfile',
            name='content_type',
            field=models.CharField(max_length=64, default='', verbose_name='content type'),
        ),
        migrations.AddField(
            model_name='outputfile',
            name='file_extension',
            field=models.CharField(max_length=64, default='', verbose_name='file extension'),
        ),
    ]
