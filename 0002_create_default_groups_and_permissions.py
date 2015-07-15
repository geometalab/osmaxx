# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    """Create default groups amd permissions."""

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for group_name, attributes in settings.OSMAXX_AUTHORIZATION['groups']:
        group = Group.objects.create(
            name=group_name
        )
        if 'permissions' in attributes:
            permissions = attributes['permissions']
            for permission_code_name in permissions:
                permission = Permission.objects.get(codename=permission_code_name)
                group.permissions.add(permission)


def update_site_backward(apps, schema_editor):
    """Revert creation of default groups and permissions.."""

    Group = apps.get_model("auth", "Group")

    for group_name, attributes in settings.OSMAXX_AUTHORIZATION['groups']:
        Group.objects.delete(
            name=group_name
        )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('excerptexport', '0001_initial')
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
