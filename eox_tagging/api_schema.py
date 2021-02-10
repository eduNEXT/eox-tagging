"""
Swagger view generator
"""
from django.conf import settings
from django.conf.urls import include, url
from django.urls import reverse
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import SwaggerDict
from drf_yasg.views import get_schema_view
from edx_api_doc_tools import get_docs_cache_timeout, internal_utils, make_api_info
from rest_framework import permissions


class APISchemaGenerator(OpenAPISchemaGenerator):
    """
    Schema generator for eox-core.

    Define specific security definition using oauth without overwritting project wide
    settings.
    """

    def get_security_definitions(self):
        security_definitions = {
            "OAuth2": {
                "flow": "application",
                "tokenUrl": "{}{}".format(settings.LMS_ROOT_URL, reverse('access_token')),
                "type": "oauth2",
            },
        }
        security_definitions = SwaggerDict.as_odict(security_definitions)
        return security_definitions


api_urls = [
    url(r"eox-tagging/api/", include("eox_tagging.api.urls"))
]

api_info = make_api_info(
    title="eox tagging",
    version="v1",
    email=" contact@edunext.co",
    description=internal_utils.dedent("""\
    eox tagging REST API

    eox Tagging provides the ability to apply a simple label to certain objects \
    (courses, enrollments and users). The label or tag includes a timestamp for \
    when the tag is should be considered active, as well as fields to include \
    the general category of the tag (tag_type) and a value belonging to that \
    category (tag_value).

    eox tagging is meant to be a lightweight plugin with emphasis on flexibility\
    most of the logic regarding the deactivation of tags at a given time must be\
    handled separately.
    """),
)

docs_ui_view = get_schema_view(
    api_info,
    generator_class=APISchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=api_urls,
).with_ui("swagger", cache_timeout=get_docs_cache_timeout())
