""" File to define validations for tag model fields.

A validation over a field is done if is defined in the plugin settings as follows:

EOX_TAGGING_DEFINITIONS = [
    {
        field_name (str): name of the field to be validated,
        validations (str[]): list with the names of the validations to be performed,
        allowed (str[] | str): list of strings with the allowed values for the field or a pattern
    }
]

For every field I want to validate, I would have to define an object inside of EOX_TAGGING_DEFINITIONS
with the fields defined above

Type of validations:
    definition: it means that the value of field_name must be in allowed or match the allowed pattern
    OpaqueKey: it means that the resource locator can be validated as opaque key. Here, allowed need to be
    a string with the key type. For example: CourseKey
"""
import logging
import re

import opaque_keys.edx.keys as all_opaque_keys
from django.conf import settings as base_settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eox_core.edxapp_wrapper.courseware import get_courseware_courses
from eox_core.edxapp_wrapper.enrollments import get_enrollment
from eox_core.edxapp_wrapper.users import get_edxapp_user
from opaque_keys import InvalidKeyError  # pylint: disable=ungrouped-imports

log = logging.getLogger(__name__)

try:
    # Python 2: "unicode" is built-in
    unicode
except NameError:
    unicode = str  # pylint: disable=redefined-builtin


class Validators(object):
    """ Defines all validator methods.
    """

    def __init__(self, instance):
        """
        Attributes:
            instance: instance of the model to validate before saving
        """
        self.instance = instance
        self.functions = {  # Functions defined for validation
            "definition": self.__validate_field_definition,
            "OpaqueKey": self.__validate_opaque_key,
        }
        self.model_validations = {
            'User': self.__validate_user_integrity,
            'Course': self.__validate_course_integrity,
            'CourseEnrollment': self.__validate_enrollment_integrity,
            'Site': self.__validate_site_integrity,
        }

    # GFK validations
    def validate_tagged_object(self):
        """Function that validates the tagged object calling the integrity validators."""

        model_tagged_name = self.instance.tagged_object_name

        try:
            self.model_validations[model_tagged_name]("tagged_object") if model_tagged_name else None
        except KeyError:
            raise ValidationError("EOX_TAGGING  |   Could not find integrity validation for field {}"
                                  .format(model_tagged_name))

    def validate_owner(self):
        """Function that validates the owner of the tag calling the integrity validators."""

        belongs_to_model_name = self.instance.belongs_to_object_name
        try:
            self.model_validations[belongs_to_model_name]("belongs_to") if belongs_to_model_name else None
        except KeyError:
            raise ValidationError("EOX_TAGGING  |   Could not find integrity validation for field {}"
                                  .format(belongs_to_model_name))

    # Integrity validators
    def __validate_user_integrity(self, object_name):
        """ Function that validates existence of user."""
        data = {
            "username": getattr(self.instance, object_name).username,  # User needs to have username
        }
        try:
            get_edxapp_user(**data)
            log.info("EOX_TAGGING  |   Validated user integrity %s", data["username"])

        except Exception:
            raise ValidationError("EOX_TAGGING  |   User {} does not exist".format(data["username"]))

    def __validate_course_integrity(self, object_name):
        """ Function that validates existence of the course."""
        course_id = unicode(getattr(self.instance, object_name).course_id)  # Course needs to have course_id
        try:
            get_courseware_courses().get_course_by_id(course_id)
            log.info("EOX_TAGGING  |   Validated course integrity %s", course_id)
        except Exception:
            raise ValidationError("EOX_TAGGING  |   Course {} does not exist".format(course_id))

    def __validate_enrollment_integrity(self, object_name):
        """ Function that validates existence of the enrollment."""
        data = {
            "username": getattr(self.instance, object_name).username,
            "course_id": unicode(getattr(self.instance, object_name).course_id),
        }
        try:
            enrollment, _ = get_enrollment(**data)
            if not enrollment:
                raise ValidationError("EOX_TAGGING  |  Enrollment for user {user} and courseID {course} does not exist"
                                      .format(user=data["username"], course=data["course_id"]))
        except Exception:
            raise ValidationError("EOX_TAGGING  |   Error getting enrollment for user {user} and courseID {course}"
                                  .format(user=data["username"], course=data["course_id"]))

    def __validate_site_integrity(self, object_name):
        """ Function that validates existence of the site."""
        site_id = getattr(self.instance, object_name).id

        try:
            Site.objects.get(id=site_id)
        except ObjectDoesNotExist:
            raise ValidationError("EOX_TAGGING  |   Site {} does not exist".format(site_id))

    # Other validations
    def run_validators(self):
        """Runs defined validators on the EOX_TAGGING_DEFINITIONS object."""
        self.__validate_not_update()

        definitions = base_settings.EOX_TAGGING_DEFINITIONS

        for obj in definitions:
            validations = obj.get("validations")
            for val in validations:
                try:
                    validator_function = self.functions[val]
                    validator_function(obj)
                except AttributeError:
                    raise ValidationError("EOX_TAGGING  |   Validator {} does not exist ".format(obj))

    def __validate_not_update(self):
        """Function that validates that the save is not an update."""
        if self.instance.id:
            #  Exception raised when trying to update
            raise ValidationError("EOX_TAGGING  |   Can't update tag. Tags are inmutable by definition")

    def __validate_field_definition(self, obj):
        """
        Function that validate the existence of the definition of the field. The
        definition can be a list of values or regex like ` r'definition' `.

        If the value does not match with any value in allowed values list or regex, an
        exception is raised.

        Attributes:
            obj: the object in definitions used for validations
        """
        field = obj.get("field_name")
        values_allowed = obj.get("allowed")

        try:
            field_value = getattr(self.instance, field)
        except AttributeError:
            log.error("EOX_TAGGING  |   The tag with value %s does not have attribute %s", self.instance, field)
            return

        if isinstance(values_allowed, list) and all(value != field_value for value in values_allowed):
            # Values allowed is list of values (at least one)

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))

        elif isinstance(values_allowed, str) and not re.search(values_allowed, field_value):
            # Values allowed is regex pattern

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))

    def __validate_opaque_key(self, obj):
        """
        Function that if called validates that the resource locator is any OpaqueKey defined in
        opaque_keys.edx.keys
        """
        field = obj.get("field_name")
        values_allowed = obj.get("allowed")  # OpaqueKey for validation defined in settings

        try:
            field_value = getattr(self.instance, field)
        except AttributeError:
            log.error("EOX_TAGGING  |   The tag with value %s does not have attribute %s", self.instance, field)
            return

        try:
            opaque_key_to_validate = getattr(all_opaque_keys, values_allowed)
            # Validation method for OpaqueKey opaque_key_to_validate
            getattr(opaque_key_to_validate, "from_string")(field_value)
        except InvalidKeyError:
            # We don't recognize this key
            raise ValidationError("The key {} is not an opaque key".format(field_value))

    def validate_unique_together(self):
        """Function that validates that at least one of the two fields in unique together is not null."""
        for field_tuple in self.instance._meta.unique_together[:]:  # pylint: disable=protected-access
            if all(getattr(self.instance, field_name) is None for field_name in field_tuple):
                raise ValidationError("At least one of {field_one} and {field_two} must be not null"
                                      .format(field_one=field_tuple[0], field_two=field_tuple[1]))
