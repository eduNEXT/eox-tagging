"""
Serializers for tags and related objects.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from eox_tagging.constants import AccessLevel
from eox_tagging.api.v1 import fields
from eox_tagging.edxapp_accessors import get_object
from eox_tagging.models import OpaqueKeyProxyModel, Tag

PROXY_MODEL_NAME = "opaquekeyproxymodel"


class RelatedObject(object):
    """Class to use with related objects."""
    def __init__(self, object_id, object_type):
        self.object_id = object_id
        self.object_type = object_type


class RelatedObjectSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Reladed objects serializer."""

    object_id = serializers.CharField(max_length=200)
    object_type = serializers.CharField(max_length=200)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""
    target = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    access = fields.EnumField(enum=AccessLevel)

    #TODO: hacer el PR del modelo y hacer rebase
    # Hacer las propuestas:
    # 1: writeonly fields con target_type, target_owner y los tipos de id que corresponden al target
    # Tambien se deberia cambiar el get_target y get_owner
    # Intentar serializer get_target a json sin el serializador

    class Meta:  # pylint: disable=old-style-class, useless-suppression
        """Meta class."""
        model = Tag
        fields = ('key', 'tag_value', 'tag_type', 'access', 'activation_date', 'expiration_date',
                  'target', 'owner')

    # Generic Foreign Key formatted values
    def get_target(self, tag):
        """Function that returns the serialized version of the identification and type of the target."""
        target_type = tag.target_object_type
        target_id = tag.target_object_id

        if target_type.lower() == PROXY_MODEL_NAME:
            target_id = str(OpaqueKeyProxyModel.objects.get(id=target_id).opaque_key)

        target_object = RelatedObject(object_id=target_id, object_type=target_type)
        serializer = RelatedObjectSerializer(target_object)
        return serializer.data

    def get_owner(self, tag):
        """Function that returns the serialized version of identification and type of the owner."""
        owner_object = RelatedObject(object_id=tag.owner_object_id, object_type=tag.owner_object_type)
        serializer = RelatedObjectSerializer(owner_object)
        return serializer.data

    # Validation and creation of tags
    def to_internal_value(self, data):
        """Function that helps with object deserialization."""
        target = get_object(data.get("target"), "target")
        owner = get_object(data.get("owner"), "owner")

        ret = super(TagSerializer, self).to_internal_value(data)

        ret["target"] = target
        ret["owner"] = owner

        return ret

    def create(self, validated_data):
        """Function that creates a Tag instance."""
        validated_data['target_object'] = validated_data.pop("target")
        validated_data['owner_object'] = validated_data.pop("owner")
        try:
            tag = Tag.objects.create_tag(**validated_data)
        except ValidationError as e:
            raise serializers.ValidationError({"Tag": _("{}".format(e.message))})
        return tag
