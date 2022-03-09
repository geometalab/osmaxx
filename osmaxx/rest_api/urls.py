import rest_framework_jwt.views
from django.conf.urls import url, include

urlpatterns = [
    # login for browsable API
    url(r"^api-auth/", include("rest_framework.urls")),
    # token auth
    url(r"^token-auth/$", rest_framework_jwt.views.obtain_jwt_token),
    url(r"^token-refresh/$", rest_framework_jwt.views.refresh_jwt_token),
    url(r"^token-verify/$", rest_framework_jwt.views.verify_jwt_token),
]
