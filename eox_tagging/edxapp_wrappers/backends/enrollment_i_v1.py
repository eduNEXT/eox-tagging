"""
Backend CourseEnrollments file, here is the method to access enrollments
objects.
"""


def get_enrollment_object():
    """Backend to get enrollment object."""
    try:
        from student.models import CourseEnrollment  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
