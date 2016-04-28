# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0012_outputfile_file_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outputfile',
            name='file_status',
        ),
        migrations.AddField(
            model_name='extractionorder',
            name='download_status',
            field=models.IntegerField(verbose_name='file status', choices=[(0, 'unknown'), (1, 'downloading'), (2, 'received')], default=0),
        ),
    ]
