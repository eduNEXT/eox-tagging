"""
URL module for Tags API.
"""
from django.urls import include, path

from eox_tagging.api.v1.routers import router

urlpatterns = [
    path('v1/', include(router.urls)),
]
