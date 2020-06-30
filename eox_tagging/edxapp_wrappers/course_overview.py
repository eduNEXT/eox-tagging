""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_course_overview(*args, **kwargs):
    """ Get course overview object. """
    backend_function = settings.GET_COURSE_OVERVIEW
    backend = import_module(backend_function)
    return backend.get_course_overview(*args, **kwargs)
