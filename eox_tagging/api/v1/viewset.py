"""
Viewset for Tags.
"""
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_oauth.authentication import OAuth2Authentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import TagApiPagination
from eox_tagging.api.v1.permissions import EoxTaggingAPIPermission
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.edxapp_wrappers import get_site
from eox_tagging.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for listing and creating Tags."""

    serializer_class = TagSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (EoxTaggingAPIPermission,)
    pagination_class = TagApiPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    lookup_field = "key"
    http_method_names = ["get", "post", "delete", "head"]

    def get_queryset(self):
        """Restricts the returned tags."""
        owner_type = self.request.query_params.get("owner_type")
        include_invalid = self.request.query_params.get("include_invalid")
        user = self.request.user
        site = get_site()

        if include_invalid and include_invalid.lower() in ["true", "1"]:
            queryset = Tag.objects.all()
        else:
            queryset = Tag.objects.active()

        if owner_type:
            owner_id = {"username": user.username} if owner_type == "user" else {"id": site.id}
            try:
                queryset = queryset.find_by_owner(owner_type=owner_type, owner_id=owner_id)
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        try:
            queryset = queryset.find_by_owner(owner_type="site", owner_id={"id": site.id}) \
                | queryset.find_by_owner(owner_type="user", owner_id={"username": user.username})
            return queryset
        except Exception:  # pylint: disable=broad-except
            return queryset.none()
