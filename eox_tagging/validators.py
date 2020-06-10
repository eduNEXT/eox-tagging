""" File to define validations for tag model fields.
"""
try:
    import crum
except ImportError:
    crum = object

import logging
import re

import opaque_keys.edx.keys as all_opaque_keys
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
            definitions: configuration matching fields to validate
        """
        self.instance = instance
        self.model_validations = {
            'User': self.__validate_user_integrity,
            'Course': self.__validate_course_integrity,
            'CourseEnrollment': self.__validate_enrollment_integrity,
            'Site': self.__validate_site_integrity,
        }
        self.current_tag_definitions = definitions

    # Config validations
    def validate_configuration(self):
        """
        Function that validates EOX_TAGGING_DEFINITIONS. The validations consist in:
            - Validate available validations
            - Validate field names
        If any error occur a ValidationError will be raised.
        """
        regex = r"validate_"

        for key, value in self.current_tag_definitions.items():

            # Validate value correctness if it has validations defined
            if re.match(regex, key):
                for _key in value:  # Validations must exist as a class method
                    try:
                        getattr(self, "validate_{}".format(_key))
                    except AttributeError:
                        raise ValidationError(u"EOX_TAGGING  |   The {} defined in configurations is not"
                                              u"in the defined validations."
                                              .format(key))
            # Validate key existence
            clean_key = re.sub(regex, "", key)
            try:
                getattr(self.instance, clean_key)
            except AttributeError:
                raise ValidationError(u"EOX_TAGGING  |   The field defined in configurations {}"
                                      u" is not part of the model."
                                      .format(clean_key))

    # GFK validations

    def validate_fields_integrity(self):
        """Helper function that calls for every object that needs integrity validation."""
        fields_to_validate = ["owner_object", "target_object"]
        map(self.__validate_model, fields_to_validate)

    def __validate_model(self, field_name):
        """Function that validates the instances in GFK fields calling the integrity validators."""
        try:
            model_name = getattr(self.instance, "{}_type".format(field_name))
        except AttributeError:
            raise ValidationError("EOX_TAGGING  |   The field {} is not defined for the Tag instance"
                                  .format(field_name))
        try:
            if model_name:
                self.model_validations[model_name](field_name)
        except KeyError:
            raise ValidationError("EOX_TAGGING  |   Could not find integrity validation for field {}"
                                  .format(field_name))

    # Integrity validators
    def __validate_user_integrity(self, object_name):
        """
        Function that validates existence of user.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        request = crum.get_current_request()
        data = {
            "username": getattr(self.instance, object_name).username,  # User needs to have username
            "site": request.site
        }
        try:
            get_edxapp_user(**data)

        except Exception:
            raise ValidationError("EOX_TAGGING  |   Could not find ID: {id} for relation {name}".format(
                id=getattr(self.instance, object_name).id,
                name=object_name,
            ))

    def __validate_course_integrity(self, object_name):
        """
        Function that validates existence of the course.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        course_id = unicode(getattr(self.instance, object_name).course_id)  # Course needs to have course_id
        try:
            get_courseware_courses().get_course_by_id(course_id)
            log.info("EOX_TAGGING  |   Validated course integrity %s", course_id)
        except Exception:
            raise ValidationError("EOX_TAGGING  |   Course {} does not exist".format(course_id))

    def __validate_enrollment_integrity(self, object_name):
        """
        Function that validates existence of the enrollment.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
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
        """
        Function that validates existence of the site.

        Arguments:
            - object_name: name of the object to validate. It can be: target_object or owner_object
        """
        site_id = getattr(self.instance, object_name).id

        try:
            Site.objects.get(id=site_id)
        except ObjectDoesNotExist:
            raise ValidationError("EOX_TAGGING  |   Site {} does not exist".format(site_id))

    # Other validations
    def validate_no_updating(self):
        """Function that validates that the save is not an update."""
        if self.instance.id:
            #  Exception raised when trying to update
            raise ValidationError("EOX_TAGGING  |   Can't update tag. Tags are inmutable by definition")

    def validate_fields(self):
        """ Function that validates all fields for the current definition."""
        regex = r"^validate_"

        for key, value in self.current_tag_definitions.items():

            if re.search(regex, key):
                clean_key = re.sub(regex, "", key)
                for _key, _value in value.items():
                    validator_method = getattr(self, "validate_{}".format(_key))
                    validator_method(clean_key, _value)
            else:
                validator_method = getattr(self, "validate_equals")
                validator_method(key, value)

    def validate_OpaqueKey(self, field, value):
        """
        Function that if called validates that that field is value OpaqueKey defined in
        opaque_keys.edx.keys.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, field)
        try:
            opaque_key_to_validate = getattr(all_opaque_keys, value)
            # Validation method for OpaqueKey: opaque_key_to_validate
            getattr(opaque_key_to_validate, "from_string")(field_value)
        except InvalidKeyError:
            # We don't recognize this key
            raise ValidationError("The key {} for {} is not an opaque key".format(field_value, field))

    def validate_in(self, field, values):
        """
        Function that validates that the field is exists in values.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, field)

        if field_value not in values:
            # Values allowed is list of values (at least one)

            raise ValidationError("EOX_TAGGING  |   The field {} is not in tag definitions".format(field))

    def validate_exist(self, field, value):  # pylint: disable=unused-argument
        """
        Function that validates that the field exists, this means, is not None.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, field)

        if not field_value:
            raise ValidationError("EOX_TAGGING  |   The field {} must exist in the instance created.".format(field))

    def validate_equals(self, field, value):
        """
        Function that validates that the field_value is equal to value.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, field)

        field_value = getattr(field_value, "name", field_value)  # In case is choicefield

        if field_value != value:
            raise ValidationError("EOX_TAGGING  |   The field {} must be equal to {}".format(field, value))

    def validate_object(self, field, value):
        """
        Function that validates that the field is instance of value.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, "{}_type".format(field))

        if field_value != value:
            raise ValidationError("EOX_TAGGING  |   The field {} must be an instance of {}.".format(field, value))

    def validate_regex(self, field, value):
        """
        Function that validates that the field matches value.

        Arguments:
            - field: field to validate
            - value: validations defined for the field
        """
        field_value = getattr(self.instance, field)

        if not re.search(value, field_value):
            # Values allowed is regex pattern

            raise ValidationError("EOX_TAGGING  |   The field {} is not in tag definitions".format(field))

    def validate_unique_together(self):
        """Function that validates that at least one of the two fields in unique together is not null."""
        for field_tuple in self.instance._meta.unique_together[:]:  # pylint: disable=protected-access
            if all(getattr(self.instance, field_name) is None for field_name in field_tuple):
                raise ValidationError("At least one of {field_one} and {field_two} must be not null"
                                      .format(field_one=field_tuple[0], field_two=field_tuple[1]))

    # Helper functions
    def __set_defaults(self):
        """ Function that at the end of validations set defaults if needed. """
        pass
