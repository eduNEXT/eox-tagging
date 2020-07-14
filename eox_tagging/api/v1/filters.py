"""Filter module for tags."""
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters

from eox_tagging.constants import AccessLevel
from eox_tagging.models import Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagFilter(filters.FilterSet):
    """Filter class for tags."""

    course_id = filters.CharFilter(method="filter_course_id")  # Tags associated to this course
    username = filters.CharFilter(method="filter_username")  # Tags associated to this username
    enrolled = filters.CharFilter(method="filter_enrolled")  # Tags associated to this username
    enrollments = filters.CharFilter(method="filter_enrollments")  # Tags associated to this username
    target_type = filters.CharFilter(method="filter_target_types")  # Tags associated to this type
    created_at = filters.DateTimeFromToRangeFilter(name="created_at")
    activated_at = filters.DateTimeFromToRangeFilter(name="activated_at")
    access = filters.CharFilter(method="filter_access_type")

    class Meta:  # pylint: disable=old-style-class
        """Meta class."""
        model = Tag
        fields = ['key', 'created_at', 'activated_at', 'status', 'course_id', 'enrolled', 'enrollments', 'username']

    def filter_course_id(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with course_id."""
        if value:
            try:
                queryset = queryset.find_all_tags_for(target_type="CourseOverview",
                                                      target_id={"course_id": str(value)})
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_username(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with username."""
        if value:
            try:
                queryset = queryset.find_all_tags_for(target_type="user",
                                                      target_id={"username": str(value)})
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_enrolled(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns tags in which the target is a course where the user is enrolled in."""
        if value:
            enrollment = {  # pylint: disable=broad-except
                "username": self.request.user.username,
                "course_id": str(value)
            }
            try:
                queryset = queryset.find_all_tags_for(target_type="courseenrollment",
                                                      target_id=enrollment)
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
            value = value_map[value.lower()]
            queryset = queryset.filter(access=value)

        return queryset
