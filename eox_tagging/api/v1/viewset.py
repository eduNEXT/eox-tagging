"""
Viewset for Tags.
"""
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework_oauth.authentication import OAuth2Authentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import TagApiPagination
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.edxapp_wrappers import get_site
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
        owner_type = self.request.query_params.get("owner_type")
        include_invalid = self.request.query_params.get("include_invalid")

        if include_invalid and include_invalid.lower() in ["true", "1"]:
            queryset = Tag.objects.all()
        else:
            queryset = Tag.objects.valid()

        owner_information = self.__get_request_owner(owner_type)

        try:
            queryset_union = queryset.none()
            for owner in owner_information:
                queryset_union |= queryset.find_by_owner(**owner)

            return queryset_union
        except Exception:  # pylint: disable=broad-except
            return queryset.none()

    def __get_request_owner(self, owner_type):
        """Returns the owners of the tag to filter the queryset."""
        site = self.__get_site()
        user = self.__get_user()

        if owner_type is None:
            return [site, user]

        if owner_type.lower() == "user":
            return user
        elif owner_type.lower() == "site":
            return site

        return None

    def __get_site(self):
        """Returns the current site."""
        site = get_site()

        return {
            "owner_id": {"id": site.id},
            "owner_type": "site",
        }

    def __get_user(self):
        """Returns the current user."""
        user = self.request.user

        return {
            "owner_id": {"username": user.username},
            "owner_type": "user",
        }
