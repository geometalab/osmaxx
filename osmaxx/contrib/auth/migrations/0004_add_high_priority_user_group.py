# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def create_high_priority_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")  # noqa
    Group.objects.create(name=settings.OSMAXX['EXCLUSIVE_USER_GROUP'])


def remove_high_priority_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")  # noqa
    Group.objects.get(name=settings.OSMAXX['EXCLUSIVE_USER_GROUP']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0003_auto_20160310_1102'),
    ]

    operations = [
        migrations.RunPython(create_high_priority_group, remove_high_priority_group),
    ]
