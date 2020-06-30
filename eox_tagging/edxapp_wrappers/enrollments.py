""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_enrollment_object(*args, **kwargs):
    """ Get enrollment object. """
    backend_function = settings.GET_ENROLLMENT_OBJECT
    backend = import_module(backend_function)
    return backend.get_enrollment_object(*args, **kwargs)


def get_enrollment_dictionary(*args, **kwargs):
    """ Get enrollment information dictionary."""
    backend_function = settings.GET_ENROLLMENT
    backend = import_module(backend_function)
    return backend.get_enrollment_dictionary(*args, **kwargs)
