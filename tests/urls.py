from django.conf.urls import url, include
from osmaxx.conversion import urls as conversion_urls

urlpatterns = [
    url(r'^', include(conversion_urls)),
]
