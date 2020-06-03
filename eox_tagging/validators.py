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
"""
import logging
import re

from django.conf import settings as base_settings
from django.core.exceptions import ValidationError

log = logging.getLogger(__name__)


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
        }

    def run_validators(self):
        """Runs defined validators."""
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
