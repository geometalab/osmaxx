from django.contrib import admin
from excerptExport.models import BoundingGeometry
from excerptExport.models import Excerpt
from excerptExport.models import ExtractionOrder
from excerptExport.models import OutputFile

# Register your models here.
admin.site.register(BoundingGeometry)
admin.site.register(Excerpt)
admin.site.register(ExtractionOrder)
admin.site.register(OutputFile)