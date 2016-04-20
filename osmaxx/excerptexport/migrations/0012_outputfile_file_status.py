# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0011_remove_extractionorder_process_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputfile',
            name='file_status',
            field=models.IntegerField(verbose_name='file status', choices=[(1, 'downloading'), (2, 'received')], default=0),
        ),
    ]
