from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'osmaxx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^excerptexport/', include('excerptexport.urls', namespace='excerptexport')),
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
