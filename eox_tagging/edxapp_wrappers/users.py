""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_platform_user(*args, **kwargs):
    """ Get edxapp user information."""
    backend_function = settings.GET_EDXAPP_USERS
    backend = import_module(backend_function)
    return backend.get_edxapp_user(*args, **kwargs)
