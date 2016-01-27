from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from osmaxx.excerptexport.models import BBoxBoundingGeometry, OsmosisPolygonFilterBoundingGeometry
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile


class BBoxBoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ['north', 'east', 'south', 'west']
    fields = ['bounding_box']
    readonly_fields = ['bounding_box']

    def bounding_box(self, obj):
        return ', '.join([str(getattr(obj, attr)) for attr in self.list_display])
    bounding_box.short_description = 'Bounding Box'
admin.site.register(BBoxBoundingGeometry, BBoxBoundingGeometryAdmin)


class ExcerptAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public', 'is_active', 'owner', 'bbox']
    fields = ('name', 'show_bbox_link')
    readonly_fields = ('show_bbox_link',)

    def bbox(self, excerpt):
        return str(excerpt.bounding_geometry.subclass_instance)
    bbox.short_description = 'Bounding Box'

    def show_bbox_link(self, excerpt):
        admin_link = reverse(
            'admin:excerptexport_bboxboundinggeometry_change',
            args=(excerpt.bounding_geometry.subclass_instance.id,)
        )
        return mark_safe('<a href="{}">{}</a>'.format(admin_link, str(excerpt.bounding_geometry.subclass_instance)))
    show_bbox_link.short_description = 'Bounding Box'
admin.site.register(Excerpt, ExcerptAdmin)


class ExtractionOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('process_id', '_extraction_configuration', 'progress_url')
admin.site.register(ExtractionOrder, ExtractionOrderAdmin)

admin.site.register(OutputFile)
admin.site.register(OsmosisPolygonFilterBoundingGeometry)
