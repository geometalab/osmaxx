from django.conf.urls import patterns, url
from excerptexport import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new_excerpt_export, name='new'),
    url(r'^downloads/$', views.show_downloads, name='downloads'),
    url(r'^download/$', views.download_file, name='download'),
    url(r'^create/$', views.create_excerpt_export, name='create'),
)
