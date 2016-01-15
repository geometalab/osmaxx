from django.contrib import admin
from osmaxx.excerptexport.models import BBoxBoundingGeometry, OsmosisPolygonFilterBoundingGeometry
from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile


class BBoxBoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ['north', 'east', 'south', 'west']

admin.site.register(BBoxBoundingGeometry, BBoxBoundingGeometryAdmin)
admin.site.register(OsmosisPolygonFilterBoundingGeometry)
admin.site.register(Excerpt)
admin.site.register(ExtractionOrder)
admin.site.register(OutputFile)
