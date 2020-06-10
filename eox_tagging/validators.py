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
import crum  # pylint: disable=import-error
import logging
import re

import opaque_keys.edx.keys as all_opaque_keys
from django.conf import settings
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


class TagValidators(object):
    """ Defines all validator methods.
    """

    def __init__(self, instance, definitions):
        """
        Attributes:
            instance: instance of the model to validate before saving
        """
        self.instance = instance
        self.model_validations = {
            'User': self.__validate_user_integrity,
            'Course': self.__validate_course_integrity,
            'CourseEnrollment': self.__validate_enrollment_integrity,
            'Site': self.__validate_site_integrity,
        }
        self.current_tag_definitions = definitions

        self.validations_allowed = ["in", "exist", "regex", "object"]

    # Config validations
    def validate_config(self, settings):
        """
        Function that validates EOX_TAGGING_DEFINITIONS. The validations consist in:
            - Validate available validations
            - Validate field names
        If any error occur a ValidationError will be raised.
        """
        regex = r"validate_"

        for tag_def in settings:
            for key, value in tag_def:

                # Validate value correctness if it has validations defined
                if re.match(regex, key):  # Validations must exist in self.validations_allowed
                    for key in value:
                        if key not in self.validations_allowed:
                            raise ValidationError("EOX_TAGGING  |   The {} is not in the defined validations"
                                                  .format(key))
                # Validate key existence
                clean_key = re.sub(regex,"", key)
                try:
                    getattr(self.instance, clean_key)
                except AttributeError:
                    raise ValidationError("EOX_TAGGING  |   The tag with value {} does not have attribute {}"
                                          .format(self.instance, clean_key))

    # GFK validations

    def validate_fields_integrity(self):
        self.__validate_target_object()
        self.__validate_owner()

    def __validate_target_object(self):
        """Function that validates the target object calling the integrity validators."""

        model_target_name = self.instance.target_object_name

        try:
            self.model_validations[model_target_name]("target_object") if model_target_name else None
        except KeyError:
            raise ValidationError("EOX_TAGGING  |   Could not find integrity validation for field {}"
                                  .format(model_target_name))

    def __validate_owner(self):
        """Function that validates the owner of the tag calling the integrity validators."""

        owner_model_name = self.instance.owner_object_name
        try:
            self.model_validations[owner_model_name]("owner") if owner_model_name else None
        except KeyError:
            raise ValidationError("EOX_TAGGING  |   Could not find integrity validation for field {}"
                                  .format(owner_model_name))

    # Integrity validators
    def __validate_user_integrity(self, object_name):
        """ Function that validates existence of user."""

        request = crum.get_current_request()
        data = {
            "username": getattr(self.instance, object_name).username,  # User needs to have username
            "site": request.site
        }
        try:
            get_edxapp_user(**data)
            log.info("EOX_TAGGING  |   Validated user integrity %s", data["username"])

        except Exception:
            raise ValidationError("EOX_TAGGING  |   Could not find ID: {id} for relation {name}".format(
                id=getattr(self.instance, object_name).id,
                name=object_name,
            ))

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
    def validate_not_update(self):
        """Function that validates that the save is not an update."""
        if self.instance.id:
            #  Exception raised when trying to update
            raise ValidationError("EOX_TAGGING  |   Can't update tag. Tags are inmutable by definition")

    def validate_fields(self):
        """ Function that validates all fields for the current definition."""
        regex = r"^validate_"

        for key, value in self.current_tag_definitions:

            if re.search(regex, key):
                clean_key = re.sub(regex,"", key)
                for _key, _value in value:
                    validator_method = getattr(self, "__validate_{}".format(_key))
                    validator_method(clean_key, _value)
            else:
                validator_method = getattr(self, "__validate_equals") # Required?
                #TODO: preguntar si esta bien
                validator_method(key, value)

    def __validate_OpaqueKey(self, field, value):
        """
        Function that if called validates that the resource locator is any OpaqueKey defined in
        opaque_keys.edx.keys
        """
        try:
            field_value = getattr(self.instance, field)
        except AttributeError:
            log.error("EOX_TAGGING  |   The tag with value %s does not have attribute %s", self.instance, field)
            return

        try:
            opaque_key_to_validate = getattr(all_opaque_keys, value)
            # Validation method for OpaqueKey: opaque_key_to_validate
            getattr(opaque_key_to_validate, "from_string")(field_value)
        except InvalidKeyError:
            # We don't recognize this key
            raise ValidationError("The key {} for {} is not an opaque key".format(field_value, field))

    def __validate_in(self, field, values):

        field_value = getattr(self.instance, field)

        if field_value not in values:
            # Values allowed is list of values (at least one)

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))

    def __validate_exist(self, field, value):

        field_value = getattr(self.instance, field)

        if not field_value:
            raise ValidationError("EOX_TAGGING  |   The {} must exist in the instance created.".format(field))

    def __validate_equals(self, field, value):

        field_value = getattr(self.instance, field)

        if field_value is not value:
            raise ValidationError("EOX_TAGGING  |   The {} must be equal to {}".format(field, value))


    def __validate_object(self, field, value):

        field_value = getattr(self.instance, "{}_name".format(field))

        if field_value is not value:
            raise ValidationError("EOX_TAGGING  |   The {} must be an instance of {}.".format(field, value))

    def __validate_regex(self, field, value):

        field_value = getattr(self.instance, field)

        if not re.search(value, field_value):
            # Values allowed is regex pattern

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))

    def validate_unique_together(self):
        """Function that validates that at least one of the two fields in unique together is not null."""
        for field_tuple in self.instance._meta.unique_together[:]:  # pylint: disable=protected-access
            if all(getattr(self.instance, field_name) is None for field_name in field_tuple):
                raise ValidationError("At least one of {field_one} and {field_two} must be not null"
                                      .format(field_one=field_tuple[0], field_two=field_tuple[1]))
