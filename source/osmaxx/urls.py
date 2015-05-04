from django.conf.urls import patterns, include, url
from django.contrib import admin

from social.apps.django_app import urls as social_urls

from excerptexport import urls as excerptexport_urls
urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'osmaxx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^excerptexport/', include(excerptexport_urls, namespace='excerptexport')),
    url(r'^admin/', include(admin.site.urls)),

    url('', include(social_urls, namespace='social')),
)
