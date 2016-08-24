from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from osmaxx.excerptexport.views import (
    access_denied,
    delete_excerpt,
    export_list,
    export_detail,
    manage_own_excerpts,
    order_new_excerpt,
    order_existing_excerpt,
    request_access,
)


excerpt_export_urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="excerptexport/templates/index.html"), name='index'),
    url(r'^access_denied/$', access_denied, name='access_denied'),

    url(r'^exports/$', export_list, name='export_list'),
    url(r'^exports/(?P<id>[A-Za-z0-9_-]+)/$', export_detail, name='export_detail'),
    url(r'^orders/new/new_excerpt/$', order_new_excerpt, name='order_new_excerpt'),
    url(r'^orders/new/existing_excerpt/$', order_existing_excerpt, name='order_existing_excerpt'),

    url(r'^excerpts/(?P<pk>[A-Za-z0-9_-]+)/delete/$', delete_excerpt, name='delete_excerpt'),
    url(r'^excerpts/$', manage_own_excerpts, name='manage_own_excerpts'),

    url(r'^request_access/$', request_access, name='request_access'),
]

login_logout_patterns = [
    url(r'^login/$', login,
        {'template_name': 'osmaxx/login.html'}, name='login'),
    url(r'^logout/$', logout,
        {'template_name': 'osmaxx/logout.html'}, name='logout'),
]

urlpatterns = excerpt_export_urlpatterns + login_logout_patterns
