"""Filter module for tags."""
import crum
from django_filters import rest_framework as filters
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from django.contrib.contenttypes.models import ContentType

from eox_tagging.constants import Status
from eox_tagging.models import Tag, OpaqueKeyProxyModel

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagFilter(filters.FilterSet):
    """Filter class for tags."""

    course_id = filters.CharFilter(method="filter_course_id")  # Tags associated to this course
    username = filters.CharFilter(method="filter_username")  # Tags associated to this username
    enrolled = filters.CharFilter(method="filter_enrolled")  # Tags associated to this username
    enrollments = filters.CharFilter(method="filter_enrollments")  # Tags associated to this username
    created_at = filters.DateTimeFromToRangeFilter(name="created_at")
    activated_at = filters.DateTimeFromToRangeFilter(name="activated_at")

    class Meta:
        model = Tag
        fields = ['key', 'created_at', 'activated_at', 'status', 'course_id', 'enrolled', 'enrollments', 'username']

    def filter_course_id(self, queryset, name, value):
        """Filter that returns the tags associated with course_id."""
        if value:
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="CourseOverview",
                                                         target_id=str(value))
                return queryset
            except InvalidKeyError:
                return queryset.none()

        return queryset

    def filter_username(self, queryset, name, value):
        """Filter that returns the tags associated with username."""
        if value:
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="user",
                                                         target_id=str(value))
                return queryset
            except InvalidKeyError:
                return queryset.none()

        return queryset

    def filter_enrolled(self, queryset, name, value):
        """Filter that returns tags in which the target is a course where the user is enrolled in."""
        if value:
            enrollment = {
                "username": self.request.user.username,
                "course_id": str(value)
            }
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="courseenrollment",
                                                         target_id=value)
                return queryset
            except InvalidKeyError:
                return queryset.none()

        return queryset

    def filter_enrollments(self, queryset, name, value):
        """Filter that returns the tags associated with the enrollments owned by the request user."""
        if value:
            enrollment = {
                "username": self.request.user.username,
                "course_id": str(value)
            }
            try:
                queryset = Tag.objects.find_all_tags_for(target_type="courseenrollment",
                                                         target_id=value)
                return queryset
            except InvalidKeyError:
                return queryset.none()

        return queryset
