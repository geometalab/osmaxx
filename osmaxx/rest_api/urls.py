import rest_framework_jwt.views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from osmaxx.clipping_area.viewsets import ClippingAreaViewSet
from pbf_file_size_estimation.views import SizeEstimationView

router = DefaultRouter()
router.register(r'estimate_size_in_bytes', SizeEstimationView, base_name='estimate_size_in_bytes')
router.register(r'clipping_area', ClippingAreaViewSet, base_name='clipping_area')

urlpatterns = [
    url(r'^', include(router.urls)),
    # login for browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # token auth
    url(r'^token-auth/$', rest_framework_jwt.views.obtain_jwt_token),
    url(r'^token-refresh/$', rest_framework_jwt.views.refresh_jwt_token),
    url(r'^token-verify/$', rest_framework_jwt.views.verify_jwt_token),
]
