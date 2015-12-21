from django.contrib import admin
from osmaxx.excerptexport.models import BBoxBoundingGeometry, OsmosisPolygonFilterBoundingGeometry
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile


class BBoxBoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ['north', 'east', 'south', 'west']

admin.site.register(BBoxBoundingGeometry, BBoxBoundingGeometryAdmin)
admin.site.register(OsmosisPolygonFilterBoundingGeometry)
admin.site.register(Excerpt)


class ExtractionOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('process_id', '_extraction_configuration', 'progress_url')

admin.site.register(ExtractionOrder, ExtractionOrderAdmin)
admin.site.register(OutputFile)
