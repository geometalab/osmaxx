# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0002_auto_20150519_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osmosispolygonfilterboundinggeometry',
            name='polygon_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/osmaxx/source/private_media'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='file',
            field=models.FileField(null=True, upload_to='', storage=django.core.files.storage.FileSystemStorage(location='/home/osmaxx/source/private_media'), blank=True, verbose_name='file'),
        ),
    ]
