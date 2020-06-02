""" File to define validations for tag model fields
"""

import re

from django.conf import settings as base_settings
from django.core.exceptions import ValidationError


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
            "definition": self.__validate_field_definition
        }

    def run_validators(self):
        """
        Runs defined validators
        """
        self.__validate_not_update()

        definitions = base_settings.EOX_TAGGING_DEFINITIONS

        for obj in definitions:
            validations = obj["validations"]
            for val in validations:
                self.functions[val](obj)

    def __validate_not_update(self):
        """
        Function that validates that the save is not an update
        """
        if self.instance.id:
            #  Exception raised when trying to update
            raise ValidationError("EOX_TAGGING  |   Can't update tag. Tags are inmutable by definition")

    def __validate_field_definition(self, obj):
        """
        Function that validate the existence of the definition of the field. The
        definition can be a list of values or regex like ` r'definition' `

        If the value does not match with any value in allowed values list or regex, an
        exception is raised

        Attributes:
            obj: the object in definitions used for validations
        """
        field = obj["field_name"]
        field_value = getattr(self.instance, field)
        values_allowed = obj["allowed"]

        if isinstance(values_allowed, list) and all(value != field_value for value in values_allowed):
            # Values allowed is list of values (at least one)

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))

        elif isinstance(values_allowed, str) and not re.search(values_allowed, field_value):
            # Values allowed is regex pattern

            raise ValidationError("EOX_TAGGING  |   The {} is not in tag definitions".format(field))
