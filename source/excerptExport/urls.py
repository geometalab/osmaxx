from django.conf.urls import patterns, url
from excerptExport import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new_excerpt_export, name='new'),
    url(r'^create/$', views.create_excerpt_export, name='create'),
)