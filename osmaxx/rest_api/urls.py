import rest_framework_jwt.views
from django.conf.urls import url, include

from osmaxx.conversion import urls as conversion_urls

urlpatterns = [
    url(r'^', include(conversion_urls)),
    # login for browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # token auth
    url(r'^token-auth/$', rest_framework_jwt.views.obtain_jwt_token),
    url(r'^token-refresh/$', rest_framework_jwt.views.refresh_jwt_token),
    url(r'^token-verify/$', rest_framework_jwt.views.verify_jwt_token),
]
