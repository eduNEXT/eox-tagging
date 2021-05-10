"""
Backend CourseOverview file, here are all the methods from
openedx.core.djangoapps.content.course_overviews.
"""


def get_enrollment_object():
    """Backend to get course overview."""
    try:
        from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseOverview = object
    return CourseOverview
