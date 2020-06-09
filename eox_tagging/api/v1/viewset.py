"""
Viewset for Tags.
"""
import crum

from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import DataApiResultsSetPagination
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for listing and creating Tags."""

    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    pagination_class = DataApiResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    lookup_field = "key"
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        """Restricts the returned tags."""
        queryset = Tag.objects.all()
        user = self.request.user
        try:
            site = crum.get_current_request().site
            return queryset.find_by_owner(owner_type="site", owner_id=site.id) \
                   | queryset.find_by_owner(owner_type="user", owner_id=user.username)
        except AttributeError:
            return queryset.find_by_owner(owner_type="user", owner_id=user.username)
