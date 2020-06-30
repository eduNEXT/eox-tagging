
"""
Backend CourseEnrollments file, here is the method to access enrollments
objects.
"""


def get_enrollment_object():
    """Backend to get enrollment object."""
    try:
        from student.models import CourseEnrollment
    except ImportError:
        CourseEnrollment = object
    return CourseEnrollment


def get_enrollment_dictionary():
    """Backend to get enrollment information dictionary."""
    try:
        from eox_core.edxapp_wrapper.enrollments import get_enrollment
    except ImportError:
        get_enrollment = object
    return get_enrollment
