"""
Test classes for Tags router
"""
from django.conf.urls import include, url
from django.test import TestCase
from django.urls import reverse
from rest_framework.routers import DefaultRouter
from rest_framework.test import URLPatternsTestCase

from eox_tagging.api.v1.viewset import TagViewSet


class TestRouters(URLPatternsTestCase, TestCase):
    """Test class for API router."""

    router = DefaultRouter()
    router.register(r"tags", TagViewSet, basename='tag')

    urlpatterns = [
        url(r"api/v1/", include(router.urls)),
    ]

    def setUp(self):
        """Router setup."""
        self.router = DefaultRouter()

    def test_get_route_for_list_tags(self):
        """Used to test correctness of list route."""
        list_route = reverse("tag-list")

        self.assertEqual(list_route, "/api/v1/tags/")

    def test_get_route_for_tag_details(self):
        """Used to test correctness of details route."""
        detail_route = reverse("tag-detail", args=[1])

        self.assertEqual(detail_route, "/api/v1/tags/1/")
