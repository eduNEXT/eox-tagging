"""
eox_tagging URL Configuration
"""
from django.urls import include, path

from eox_tagging import views
from eox_tagging.api_schema import docs_ui_view

urlpatterns = [
    path('^eox-info$', views.info_view, name='eox-info'),
    path('api/', include('eox_tagging.api.urls')),
    path('^api-docs/$', docs_ui_view, name='apidocs-ui'),
]
