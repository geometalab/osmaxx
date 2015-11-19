from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import conversion_job.views
from file_size_estimation.views import SizeEstimationView

router = DefaultRouter()
router.register(r'extents', conversion_job.views.ExtentViewSet)
router.register(r'jobs', conversion_job.views.ConversionJobViewSet)
router.register(r'conversion_result', conversion_job.views.ConversionJobStatusViewSet, base_name='conversion_job_result')
router.register(r'gis_format', conversion_job.views.GISFormatStatusViewSet)
router.register(r'estimate_size_in_bytes', SizeEstimationView, base_name='estimate_size_in_bytes')

urlpatterns = [
    url(r'^', include(router.urls)),
    # login for browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # token auth
    url(r'^token-auth/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^token-refresh/$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^token-verify/$', 'rest_framework_jwt.views.verify_jwt_token'),
]
