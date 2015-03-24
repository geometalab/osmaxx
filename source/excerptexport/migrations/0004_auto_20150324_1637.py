# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import excerptexport.models.output_file


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(null=True, max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='file',
            field=models.FileField(null=True, upload_to='/var/www/eda/projects/data', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='public_identifier',
            field=models.CharField(default=excerptexport.models.output_file.default_public_identifier, max_length=512),
            preserve_default=True,
        ),
    ]
