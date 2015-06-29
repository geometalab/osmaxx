# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import osmaxx.excerptexport.utils.upload_to


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0003_auto_20150602_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osmosispolygonfilterboundinggeometry',
            name='polygon_file',
            field=models.FileField(upload_to='', storage=osmaxx.excerptexport.utils.upload_to.PrivateFileSystemStorage()),
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='file',
            field=models.FileField(blank=True, storage=osmaxx.excerptexport.utils.upload_to.PrivateFileSystemStorage(), upload_to='', null=True, verbose_name='file'),
        ),
    ]
