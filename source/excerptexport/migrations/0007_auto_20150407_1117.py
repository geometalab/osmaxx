# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def revert_one_to_one_bounding_geo_to_excerpt(apps, schema_editor):
    Excerpt = apps.get_model('excerptexport', 'Excerpt')
    for excerpt in Excerpt.objects.all():
        excerpt.bounding_geometry = excerpt.boundinggeometry
        excerpt.save()

def revert_one_to_one_excerpt_to_bounding_geo(apps, schema_editor):
    BoundingGeometry = apps.get_model('excerptexport', 'BoundingGeometry')
    for bounding_geometry in BoundingGeometry.objects.all():
        bounding_geometry.excerpt_old = bounding_geometry.excerpt
        bounding_geometry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0006_excerpt_bounding_geometry'),
    ]

    operations = [
        migrations.RunPython(revert_one_to_one_bounding_geo_to_excerpt, revert_one_to_one_excerpt_to_bounding_geo)
    ]
