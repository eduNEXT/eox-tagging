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
    status = filters.NumberFilter(name="status")
    access = filters.ChoiceFilter(choices=AccessLevel.choices())

    class Meta:  # pylint: disable=old-style-class
        """Meta class."""
        model = Tag
        fields = ['key', 'created_at', 'activated_at', 'status', 'course_id', 'enrolled', 'enrollments', 'username']

    def filter_course_id(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with course_id."""
        if value:
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="CourseOverview",
                                                         target_id=str(value))
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_username(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with username."""
        if value:
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="user",
                                                         target_id=str(value))
                return queryset
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
                queryset = Tag.objects.find_all_tags_for(target_type="courseenrollment",
                                                         target_id=enrollment)
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_enrollments(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns the tags associated with the enrollments owned by the request user."""
        if value:
            try:
                ctype = ContentType.objects.get(model="courseenrollment")
                queryset = ctype.get_object_for_this_type(course_id=str(value))
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()

        return queryset

    def filter_target_types(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter that returns targets by their type."""
        if value:
            try:
                queryset = Tag.objects.find_all_tags_by_type(str(value))
                return queryset
            except Exception:  # pylint: disable=broad-except
                return queryset.none()
        return queryset
