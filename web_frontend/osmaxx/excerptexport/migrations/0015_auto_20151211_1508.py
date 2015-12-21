# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0014_auto_20151209_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outputfile',
            old_name='create_date',
            new_name='creation_date',
        ),
    ]
