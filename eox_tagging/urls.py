"""
eox_tagging URL Configuration
"""
from django.conf.urls import include, url

from eox_tagging import views
from eox_tagging.api_schema import docs_ui_view

urlpatterns = [
    url(r'^eox-info$', views.info_view, name='eox-info'),
    url(r'api/', include('eox_tagging.api.urls')),
    url(r'^api-docs/$', docs_ui_view, name='apidocs-ui'),
]
