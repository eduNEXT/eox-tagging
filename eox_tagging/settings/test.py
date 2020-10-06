"""
Test Django settings for eox_tagging project.
"""

from __future__ import unicode_literals

from .common import *  # pylint: disable=wildcard-import

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'rest_framework',
    'eox_tagging',
    EOX_AUDIT_MODEL_APP
]

# For testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

ROOT_URLCONF = 'eox_tagging.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

EOX_TAGGING_SKIP_VALIDATIONS = True
EOX_TAGGING_LOAD_PERMISSIONS = False
EOX_TAGGING_BEARER_AUTHENTICATION = 'eox_tagging.edxapp_wrappers.backends.bearer_authentication_i_v1_test'
EOX_TAGGING_GET_ENROLLMENT_OBJECT = "eox_tagging.edxapp_wrappers.backends.enrollment_i_v1"
EOX_TAGGING_GET_COURSE_OVERVIEW = "eox_tagging.edxapp_wrappers.backends.course_overview_i_v1"
DATA_API_DEF_PAGE_SIZE = 1000
DATA_API_MAX_PAGE_SIZE = 5000
TEST_SITE = 1
