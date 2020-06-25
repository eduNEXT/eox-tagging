"""Module that implements helper functions for other modules."""
import crum
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from eox_core.edxapp_wrapper.enrollments import get_enrollment
from eox_core.edxapp_wrapper.users import get_edxapp_user
from opaque_keys.edx.keys import CourseKey

try:
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
except ImportError:
    from eox_tagging.test_utils import CourseOverview  # pylint: disable=ungrouped-imports, useless-suppression


def get_user(**kwargs):
    """Function used to get users."""
    user_id = kwargs.get("target_id")
    if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Skip these validations while testing
        user = User.objects.get(username=user_id)
        return user

    site = crum.get_current_request().site
    user = get_edxapp_user(username=user_id, site=site)
    return user


def get_course(**kwargs):
    """Function used to get courses from the platform."""
    course_id = kwargs.get("target_id")
    opaque_key = CourseKey.from_string(course_id)
    if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Skip these validations while testing
        return object

    course = CourseOverview.get_from_id(opaque_key)
    return course


def get_site(**kwargs):
    """Function used to get sites."""
    site_id = kwargs.get("id")

    site = Site.objects.get(id=site_id)
    return site


def get_course_enrollment(**kwargs):
    """Function used to get enrollments from the platform."""
    username = kwargs.get("username")
    course_id = kwargs.get("course_id")

    if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):
        return object

    enrollment, _ = get_enrollment(username=username, course_id=course_id)
    return enrollment


def get_object(related_object_type, **kwargs):
    """Helper function to get objects using RELATED_FIELDS dictionary."""
    RELATED_OBJECTS = {
        "user": get_user,
        "courseoverview": get_course,
        "site": get_site,
        "courseenrollment": get_course_enrollment,
    }
    try:
        related_object = RELATED_OBJECTS.get(related_object_type)(**kwargs)
    except Exception:
        raise ValidationError("This field is required.")

    return related_object