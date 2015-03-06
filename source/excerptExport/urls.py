from django.conf.urls import patterns, url
from excerptExport import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^export/$', views.export, name='export'),
)