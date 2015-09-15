# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0006_outputfile_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputfile',
            name='file_extension',
            field=models.CharField(default='', max_length=64, verbose_name='file extension'),
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='content_type',
            field=models.CharField(default='', max_length=64, verbose_name='content type'),
        ),
    ]
