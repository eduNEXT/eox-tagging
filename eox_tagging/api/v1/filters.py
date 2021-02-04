"""Filter module for tags."""
from django_filters import rest_framework as filters

from eox_tagging.constants import AccessLevel
from eox_tagging.models import Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagFilter(filters.FilterSet):
    """Filter class for tags."""

    course_id = filters.CharFilter(method="filter_by_target_object")
    username = filters.CharFilter(method="filter_by_target_object")
    target_type = filters.CharFilter(method="filter_target_types")
    created_at = filters.DateTimeFromToRangeFilter()
    activation_date = filters.DateTimeFromToRangeFilter()
    expiration_date = filters.DateTimeFromToRangeFilter()
    access = filters.CharFilter(method="filter_access_type")

    class Meta:  # pylint: disable=old-style-class, useless-suppression
        """Meta class."""
        model = Tag
        fields = ["key", "status", "tag_type", "tag_value"]

    def filter_by_target_object(self, queryset, name, value):
        """Filter that returns the tags associated with target."""
        TARGET_TYPES = {
            "course_id": "courseoverview",
            "username": "user",
        }
        if value:
            DEFAULT = {
                name: value,
            }
            try:
                filter_params = {
                    "target_type": TARGET_TYPES.get(name),
                    "target_id": DEFAULT,
                }
                queryset = queryset.find_all_tags_for(**filter_params)
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_target_types(self, queryset, name, value):  # pylint: disable=unused-argument
        """
        Filter that returns targets using their type.

        **SPECIAL CASE**: course enrollments.

        If the user wants to filter by target_type courseenrollment and wants to add filters on
        user or course, it must pass the following:

            - target_type: if the other arguments are passed this is used to differentiate between
            course_id from courseoverview and username from user object.
            - enrollment_course_id (optional)
            - enrollment_username (optional)
        """
        target_id = {}

        if value == "courseenrollment":
            course_id = self.request.query_params.get("enrollment_course_id")
            username = self.request.query_params.get("enrollment_username")
            target_id.update({"username": username, "course_id": course_id})

        try:
            if any(object_id for object_id in target_id.values()):
                queryset = queryset.find_all_tags_for(target_type=value, target_id=target_id)
            elif value:
                queryset = queryset.find_all_tags_by_type(value)
        except Exception:  # pylint: disable=broad-except
            return queryset.none()

        return queryset

    def filter_access_type(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filters targets by their access type."""
        if value:
            value_map = {v.lower(): k for k, v in AccessLevel.choices()}
            access = value_map.get(value.lower())
            queryset = queryset.filter(access=access) if access else queryset.none()

        return queryset
