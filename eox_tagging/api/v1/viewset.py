"""
Viewset for Tags.
"""
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_oauth.authentication import OAuth2Authentication

from eox_tagging.api.v1.filters import TagFilter
from eox_tagging.api.v1.pagination import TagApiPagination
from eox_tagging.api.v1.permissions import EoxTaggingAPIPermissionOrReadOnly
from eox_tagging.api.v1.serializers import TagSerializer
from eox_tagging.constants import AccessLevel
from eox_tagging.edxapp_wrappers import get_site
from eox_tagging.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for listing and creating Tags."""

    serializer_class = TagSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (EoxTaggingAPIPermissionOrReadOnly,)
    pagination_class = TagApiPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    lookup_field = "key"
    http_method_names = ["get", "post", "delete", "head"]

    def get_queryset(self):
        """Restricts the returned tags."""
        queryset = Tag.objects.all()

        queryset = self.__get_objects_by_status(queryset)

        queryset = self.__get_objects_by_permission(queryset)

        return queryset

    def __get_objects_by_status(self, queryset):
        """Method that returns queryset filtered by tag status."""
        include_invalid = self.request.query_params.get("include_invalid")

        if not include_invalid or include_invalid.lower() not in ["true", "1"]:
            queryset = queryset.valid()

        return queryset

    def __get_objects_by_permission(self, queryset):
        """Method that returns queryset filtered by user permissions."""
        if self.request.user.has_perm("auth.can_call_eox_tagging"):
            return self.__get_objects_by_owner(queryset)
        else:
            return self.__get_objects_by_target(queryset)

    def __get_objects_by_owner(self, queryset):
        """Method that returns queryset filtered by tag owner"""
        owner_type = self.request.query_params.get("owner_type")
        owner_information = self.__get_request_owner(owner_type)

        try:
            queryset_union = queryset.none()
            for owner in owner_information:
                queryset_union |= queryset.find_by_owner(**owner)

            return queryset_union
        except Exception:  # pylint: disable=broad-except
            return queryset.none()

    def __get_objects_by_target(self, queryset):
        """Method that returns queryset filtered by tag owner"""
        queryset = queryset.find_all_tags_for(**self.__get_user("target")) \
                           .filter(access__in=[AccessLevel.PRIVATE, AccessLevel.PUBLIC])
        return queryset

    def __get_request_owner(self, object_type):
        """Returns the owners of the tag to filter the queryset."""
        site = self.__get_site("owner")
        user = self.__get_user("owner")

        if not object_type:
            return [site, user]

        if object_type.lower() == "user":
            return [user]

        if object_type.lower() == "site":
            return [site]

        return []

    def __get_site(self, role):
        """Returns the current site."""
        site = get_site()

        return {
            "%s_id" % role: {"id": site.id},
            "%s_type" % role: "site",
        }

    def __get_user(self, role):
        """Returns the current user."""
        user = self.request.user

        return {
            "%s_id" % role: {"username": user.username},
            "%s_type" % role: "user",
        }
