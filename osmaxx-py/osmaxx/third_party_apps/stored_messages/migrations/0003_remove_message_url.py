# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stored_messages', '0002_message_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='url',
        ),
    ]
