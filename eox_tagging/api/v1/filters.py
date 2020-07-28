"""Filter module for tags."""
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters

from eox_tagging.constants import AccessLevel
from eox_tagging.models import Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagFilter(filters.FilterSet):
    """Filter class for tags."""

    course_id = filters.CharFilter(name="course_id", method="filter_by_target_object")
    username = filters.CharFilter(name="username", method="filter_by_target_object")
    enrolled = filters.CharFilter(name="enrollment", method="filter_by_target_object")
    enrollments = filters.CharFilter(method="filter_enrollments")
    target_type = filters.CharFilter(method="filter_target_types")
    created_at = filters.DateTimeFromToRangeFilter(name="created_at")
    activation_date = filters.DateTimeFromToRangeFilter(name="activation_date")
    access = filters.CharFilter(method="filter_access_type")

    class Meta:  # pylint: disable=old-style-class
        """Meta class."""
        model = Tag
        fields = ['key', 'created_at', 'activation_date', 'status', 'course_id', 'enrolled', 'enrollments', 'username']

    def filter_by_target_object(self, queryset, name, value):
        """Filter that returns the tags associated with target."""
        TARGET_TYPES = {
            "course_id": "courseoverview",
            "username": "user",
            "enrollment": "courseenrollment",
        }
        if value:
            TARGET_IDENTIFICATION = {
                "enrollment": {
                    "username": self.request.user.username,
                    "course_id": str(value),
                },
            }
            DEFAULT = {
                name: str(value),
            }
            try:
                filter_params = {
                    "target_type": TARGET_TYPES.get(name),
                    "target_id": TARGET_IDENTIFICATION.get(name, DEFAULT),
                }
                queryset = queryset.find_all_tags_for(**filter_params)
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_enrollments(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with the enrollments owned by the request user."""
        if value:
            try:
                ctype = ContentType.objects.get(model="courseenrollment")
                enrollments_queryset = queryset.find_all_tags_by_type("courseenrollment")

                query_enrollments = []
                for tag_enrollment in enrollments_queryset:
                    target_id = tag_enrollment.target_object_id
                    enrollment = ctype.get_object_for_this_type(id=target_id)
                    if str(enrollment.course_id) == str(value):
                        query_enrollments.append(tag_enrollment)

                return query_enrollments
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_target_types(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns targets by their type."""
        if value:
            try:
                queryset = queryset.find_all_tags_by_type(str(value))
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
