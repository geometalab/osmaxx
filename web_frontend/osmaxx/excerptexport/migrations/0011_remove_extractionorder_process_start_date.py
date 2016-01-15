# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0010_extractionorder_progress_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extractionorder',
            name='process_start_date',
        ),
    ]
