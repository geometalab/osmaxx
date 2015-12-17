from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from osmaxx.excerptexport.views import (
    list_downloads,
    download_file,
    extraction_order_status,
    list_orders,
    access_denied,
    order_form_view,
    request_access,
    order_new_excerpt,
)


excerpt_export_urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="excerptexport/templates/index.html"), name='index'),
    url(r'^access_denied/$', access_denied, name='access_denied'),

    url(r'^downloads/$', list_downloads, name='downloads'),
    url(r'^downloads/(?P<uuid>[A-Za-z0-9_-]+)/$', download_file, name='download'),

    url(r'^orders/$', list_orders, name='orders'),
    url(r'^orders/new/$', order_form_view, name='new'),
    url(r'^orders/new/new_excerpt/$', order_new_excerpt, name='new_excerpt'),
    url(r'^orders/(?P<extraction_order_id>[0-9]+)$', extraction_order_status, name='status'),

    url(r'^request_access/$', request_access, name='request_access'),
]

login_logout_patterns = [
    url(r'^login/$', login,
        {'template_name': 'excerptexport/templates/login.html'}, name='login'),
    url(r'^logout/$', logout,
        {'template_name': 'excerptexport/templates/logout.html'}, name='logout'),
]

urlpatterns = excerpt_export_urlpatterns + login_logout_patterns
