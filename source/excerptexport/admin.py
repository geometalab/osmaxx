from django.contrib import admin
from excerptexport.models import BoundingGeometry, Excerpt, ExtractionOrder, OutputFile


class BoundingGeometryAdmin(admin.ModelAdmin):
    list_display = ['north', 'east', 'south', 'west']

admin.site.register(BoundingGeometry, BoundingGeometryAdmin)
admin.site.register(Excerpt)
admin.site.register(ExtractionOrder)
admin.site.register(OutputFile)
