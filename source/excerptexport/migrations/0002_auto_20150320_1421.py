# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outputfile',
            name='path',
        ),
        migrations.AddField(
            model_name='outputfile',
            name='file',
            field=models.FileField(upload_to='/var/www/eda/projects/data', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='outputfile',
            name='public_identifier',
            field=models.CharField(max_length=512, default='14268612701000000'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
