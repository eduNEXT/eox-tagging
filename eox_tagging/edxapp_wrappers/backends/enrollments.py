
"""Backend abstraction."""


def get_enrollment_object():
    """Backend to get enrollment object."""
    try:
        from student.models import CourseEnrollment
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment
