import rest_framework_jwt.views
from django.conf.urls import include

from django.urls import path

urlpatterns = [
    # login for browsable API
    path("api-auth", include("rest_framework.urls")),
    # token auth
    path("token-auth", rest_framework_jwt.views.obtain_jwt_token),
    path("token-refresh", rest_framework_jwt.views.refresh_jwt_token),
    path("token-verify", rest_framework_jwt.views.verify_jwt_token),
]
