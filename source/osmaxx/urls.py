from django.conf.urls import include, url
from django.contrib import admin

from social.apps.django_app import urls as social_urls

from excerptexport import urls as excerptexport_urls


urlpatterns = [
    url(r'', include(excerptexport_urls, namespace='excerptexport')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(social_urls, namespace='social')),
]
