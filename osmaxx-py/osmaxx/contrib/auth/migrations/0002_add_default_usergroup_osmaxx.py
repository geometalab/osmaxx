# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def update_site_forward(apps, schema_editor):
    """Add group osmaxx."""
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ExtractionOrder = apps.get_model("excerptexport", "ExtractionOrder")
    group = Group.objects.create(name=settings.OSMAXX_FRONTEND_USER_GROUP)
    content_type = ContentType.objects.get_for_model(ExtractionOrder)
    permission, created = Permission.objects.get_or_create(codename='add_extractionorder', content_type=content_type)
    group.permissions.add(permission)


def update_site_backward(apps, schema_editor):
    """Revert add group osmaxx."""
    Group = apps.get_model("auth", "Group")
    Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
