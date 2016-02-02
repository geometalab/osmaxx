from django.contrib import admin
from django.utils.safestring import mark_safe

from osmaxx.excerptexport.models import BBoxBoundingGeometry, OsmosisPolygonFilterBoundingGeometry
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile


class BBoxBoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ('north', 'east', 'south', 'west')
    fields = (list_display,)
    readonly_fields = list_display
admin.site.register(BBoxBoundingGeometry, BBoxBoundingGeometryAdmin)


class ExcerptAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public', 'is_active', 'owner', 'bounding_geometry']
    fields = ('name', ('bounding_geometry', 'bounding_geometry_subclass_instance_edit_link'))
    readonly_fields = ('bounding_geometry_subclass_instance_edit_link',)

    def bounding_geometry_subclass_instance_edit_link(self, excerpt):
        admin_link = excerpt.bounding_geometry.subclass_instance.get_admin_url()
        return mark_safe(
            '<a href="{}">'
            '<img src="/static/admin/img/icon_changelink.gif" alt="Change" height="10" width="10"></img> Edit {} {}'
            '</a>'.format(
                admin_link,
                type(excerpt.bounding_geometry.subclass_instance).__name__,
                excerpt.bounding_geometry.subclass_instance.id,
            ),
        )
    bounding_geometry_subclass_instance_edit_link.short_description = 'Boundary'
admin.site.register(Excerpt, ExcerptAdmin)


class ExtractionOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('process_id', '_extraction_configuration', 'progress_url')
admin.site.register(ExtractionOrder, ExtractionOrderAdmin)

admin.site.register(OutputFile)
admin.site.register(OsmosisPolygonFilterBoundingGeometry)
