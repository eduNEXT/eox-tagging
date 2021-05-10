"""
Backend for course enrollments valid for lilac release.
"""


def get_enrollment_object():
    """Backend to get course enrollment."""
    try:
        from common.djangoapps.student.models import CourseEnrollment  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
