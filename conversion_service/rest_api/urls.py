from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import conversion_job.views

router = DefaultRouter()
router.register(r'extents', conversion_job.views.ExtentViewSet)
router.register(r'jobs', conversion_job.views.ConversionJobViewSet)
router.register(r'conversion_status', conversion_job.views.ConversionJobStatusViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # login for browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # token auth
    url(r'^api/token-auth/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/token-refresh/$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^api/token-verify/$', 'rest_framework_jwt.views.verify_jwt_token'),
]
