"""
Viewset for Tags.
"""
import crum
from django.conf import settings
from django.contrib.sites.models import Site
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework_oauth.authentication import OAuth2Authentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import TagApiPagination
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for listing and creating Tags."""

    serializer_class = TagSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAdminUser,)
    pagination_class = TagApiPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    lookup_field = "key"
    http_method_names = ["get", "post", "delete", "head"]

    def get_queryset(self):
        """Restricts the returned tags."""
        queryset = Tag.objects.all()
        owner_type = self.request.query_params.get('owner_type', None)
        user = self.request.user

        if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Use TEST_SITE while testing
            site = Site.objects.get(id=settings.TEST_SITE)
        else:
            site = crum.get_current_request().site

        if owner_type:
            owner_id = user.username if owner_type == "user" else site.id
            try:
                queryset = queryset.find_by_owner(owner_type="user", owner_id=owner_id)
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        try:
            return queryset.find_by_owner(owner_type="site", owner_id=site.id) \
                | queryset.find_by_owner(owner_type="user", owner_id=user.username)
        except Exception:  # pylint: disable=broad-except
            return queryset.none()
