from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import conversion_job.views

router = DefaultRouter()
router.register(r'extents', conversion_job.views.ExtentViewSet)
router.register(r'jobs', conversion_job.views.ConversionJobViewSet)
router.register(r'conversion_status', conversion_job.views.ConversionJobStatusViewSet)
router.register(r'gis_format_status', conversion_job.views.GISFormatStatusViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
