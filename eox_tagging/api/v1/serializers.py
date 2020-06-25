"""
Serializers for tags and related objects.
"""
import crum
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers

from eox_tagging.api.v1 import fields
from eox_tagging.constants import AccessLevel, Status
from eox_tagging.edxapp_accessors import get_object
from eox_tagging.models import Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""
    target_id = serializers.CharField(source='target_object')
    owner_id = serializers.CharField(source='owner_object', required=False)
    owner_type = serializers.CharField(source='owner_object_type')
    target_type = serializers.CharField(source='target_object_type')
    access = fields.EnumField(enum=AccessLevel)
    status = fields.EnumField(enum=Status, required=False)

    # Write only fields used to create tags
    username = serializers.CharField(write_only=True, required=False)
    course_id = serializers.CharField(write_only=True, required=False)

    class Meta:  # pylint: disable=old-style-class, useless-suppression
        """Meta class."""
        model = Tag
        fields = ('key', 'tag_value', 'tag_type', 'access', 'activation_date', 'expiration_date',
                  'target_id', 'owner_id', 'owner_type', 'target_type', 'username', 'course_id', 'status')

    # Validation and creation of tags
    def create(self, validated_data):
        """Function that creates a Tag instance."""

        # Finding target and owner objects
        target_object = None
        owner_object = None
        target_type = validated_data.pop("target_object_type")
        owner_type = validated_data.pop("owner_object_type", None)

        data = {
            "target_id": validated_data.pop("target_object", None),
        }
        try:
            target_object = get_object(target_type, **data)
        except Exception:  # pylint: disable=broad-except
            serializers.ValidationError({"Target": _("Error getting {} object."
                                         .format(target_type))})

        if owner_type == "user":
            owner_object = self.context.get("request").user
        else:
            owner_object = crum.get_current_request().site

        # Set objects
        tag_object = {
            "target_object": target_object,
            "owner_object": owner_object,
        }
        tag_object.update(validated_data)
        try:
            tag = Tag.objects.create_tag(**tag_object)
        except ValidationError as e:
            raise serializers.ValidationError({"Tag": _("{}".format(e.message))})
        return tag
