"""
eox_tagging URL Configuration
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'api/', include('eox_tagging.api.urls')),
]
