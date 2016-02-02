from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import conversion_job.views
from clipping_geometry.viewsets import ClippingAreaViewSet
from countries.views import CountryViewSet
from file_size_estimation.views import SizeEstimationView

router = DefaultRouter()
router.register(r'extents', conversion_job.views.ExtentViewSet)
router.register(r'jobs', conversion_job.views.ConversionJobViewSet)
router.register(r'conversion_result', conversion_job.views.ConversionJobStatusViewSet, base_name='conversion_job_result')
router.register(r'gis_format', conversion_job.views.GISFormatStatusViewSet)
router.register(r'estimate_size_in_bytes', SizeEstimationView, base_name='estimate_size_in_bytes')
router.register(r'country', CountryViewSet)
router.register(r'clipping_area', ClippingAreaViewSet, base_name='clipping_area')

urlpatterns = [
    url(r'^', include(router.urls)),
]
