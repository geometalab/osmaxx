from django.conf.urls import patterns, url
from excerptExport import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^create-excerpt/$', views.list, name='create_excerpt'),
)