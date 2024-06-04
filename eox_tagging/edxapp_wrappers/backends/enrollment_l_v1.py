"""
Backend for course enrollments valid for lilac release.
"""
from common.djangoapps.student.models import CourseEnrollment  # pylint: disable=C0415, E0401


def get_enrollment_object():
    """Backend to get course enrollment."""
    return CourseEnrollment
