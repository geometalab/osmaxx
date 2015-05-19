from django.contrib import admin
from excerptexport.models import BBoxBoundingGeometry, OsmosisPolygonFilterBoundingGeometry
from excerptexport.models import Excerpt, ExtractionOrder, OutputFile


class BoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ['north', 'east', 'south', 'west']

admin.site.register(BBoxBoundingGeometry, BoundingGeometryAdmin)
admin.site.register(OsmosisPolygonFilterBoundingGeometry)
admin.site.register(Excerpt)
admin.site.register(ExtractionOrder)
admin.site.register(OutputFile)
