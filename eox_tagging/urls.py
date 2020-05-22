"""
URLs for eox_tagging.
"""
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', TemplateView.as_view(template_name="eox_tagging/base.html")),
]
