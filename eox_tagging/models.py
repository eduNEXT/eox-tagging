"""
Models to store tags in the database
"""
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Tag(models.Model):
    """Model class for tags

    Attributes:
        tag_value:
        tag_type:
        access:
        activation_date:
        expiration-date:
    """

    PUBLIC_ACCESS = 1
    PROTECTED_ACCESS = 2
    PRIVATE_ACCESS = 3

    ACCESS_TAG_CHOICES = [
        (PUBLIC_ACCESS, "Public"),
        (PROTECTED_ACCESS, "Protected"),
        (PRIVATE_ACCESS, "Private"),
    ]

    VALID_TAG = 1
    INVALID_TAG = 0

    STATUS_TAG_CHOICES = [(VALID_TAG, "Valid"), (INVALID_TAG, "Invalid")]

    id = models.AutoField(primary_key=True,)
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )

    tag_value = models.CharField(max_length=150)
    tag_type = models.CharField(max_length=150)
    access = models.PositiveIntegerField(
        choices=ACCESS_TAG_CHOICES, default=PUBLIC_ACCESS,
    )
    status = models.PositiveIntegerField(
        choices=STATUS_TAG_CHOICES, default=VALID_TAG, editable=False,
    )
    activation_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    invalidated_at = models.DateTimeField(null=True)

    # Generic foreign key for tagged objects
    tagged_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="tagged_%(class)s_type")
    tagged_object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey("tagged_type", "tagged_object_id")

    # Generic foreign key for `tag belonging to` USER or SITE
    belongs_to_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="belongs_to_%(class)s_type")
    belongs_to_object_id = models.PositiveIntegerField()
    belongs_to = GenericForeignKey("belongs_to_type", "belongs_to_object_id")

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.tag_value
