from django.contrib import admin

from osmaxx.excerptexport.models import BoundingGeometry, Excerpt, ExtractionOrder, OutputFile


admin.site.register(BoundingGeometry)
admin.site.register(Excerpt)
admin.site.register(ExtractionOrder)
admin.site.register(OutputFile)
