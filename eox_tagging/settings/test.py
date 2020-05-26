"""
Test Django settings for eox_tagging project.
"""

from __future__ import unicode_literals

from .common import *  # pylint: disable=wildcard-import
from .production import *  # pylint: disable=wildcard-import
from .aws import *  # pylint: disable=wildcard-import


class SettingsClass(object):
    """ dummy settings class """
    pass


SETTINGS = SettingsClass()

plugin_settings(SETTINGS)
