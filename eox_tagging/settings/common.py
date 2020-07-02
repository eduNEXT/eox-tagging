"""
Common Django settings for eox_tagging project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from __future__ import unicode_literals

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'eox_tagging',
]


ROOT_URLCONF = 'eox_tagging.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

ALLOWED_HOSTS = ['*']


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Plugin settings
    settings.EOX_TAGGING_DEFINITIONS = []
    settings.EOX_TAGGING_LOAD_PERMISSIONS = True
    settings.DATA_API_DEF_PAGE_SIZE = 1000
    settings.DATA_API_MAX_PAGE_SIZE = 5000
