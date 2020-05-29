"""
Model to store tags in the database
"""
import logging
import uuid

from django.conf import settings as base_settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

log = logging.getLogger(__name__)


class SoftDeletionQuerySet(QuerySet):
    """SoftDeletion queryset used as helper

    """

    def delete(self):
        return super(SoftDeletionQuerySet, self).update(invalidated_at=timezone.now())

    def hard_delete(self):
        """
        Hard delete using queryset
        """
        return super(SoftDeletionQuerySet, self).delete()

    def valid(self):
        """
        Returns all valid tags
        """
        return self.filter(invalidated_at=None)

    def invalid(self):
        """
        Returns all invalid tags
        """
        return self.exclude(invalidated_at=None)


class SoftDeletionManager(models.Manager):
    """SoftDelition model manager

    """

    def __init__(self, *args, **kwargs):
        """
        Softdeletion init
        """
        self.valid_only = kwargs.pop("valid_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Get queryset depending on using all objects or just valid objects
        """
        if self.valid_only:
            return SoftDeletionQuerySet(self.model).filter(invalidated_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        """
        Hard delete depending on using all objects or just valid objects
        """
        return self.get_queryset().hard_delete()

    def delete(self):
        """
        Soft delete depending on using all objects or just valid objects
        """
        return self.get_queryset().delete()


class SoftDeletionModel(models.Model):
    """Abstract Model used for soft deletion

    Attributes:
        status: status of the tag, valid or invalid
        invalidated_at: date when the tag is soft deleted
    """

    VALID = 1
    INVALID = 0

    STATUS_CHOICES = [(VALID, "Valid"), (INVALID, "Invalid")]

    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=VALID, editable=False,
    )

    invalidated_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(valid_only=False)

    class Meta:  # pylint: disable=old-style-class
        """
        Abstract class
        """
        abstract = True

    def delete(self):  # pylint: disable=arguments-differ
        self.invalidated_at = timezone.now()
        self.status = self.INVALID
        super(SoftDeletionModel, self).save()

    def hard_delete(self):
        """
        Deletes object from database
        """
        super(SoftDeletionModel, self).delete()


class TagManager(SoftDeletionManager):
    """Tag manager
    """

    pass


@python_2_unicode_compatible
class Tag(SoftDeletionModel):
    """Model class for tags

    Attributes:
        tag_value: unicode value of the tag tag
        tag_type: type of the tag
        access: access level of the tag
        activation_date: date to activate the tag
        expiration-date: date to deactivate de tag
        tagged_object: object tagged
        belongs_to: object to which the tag belongd
    """

    DEFAULT = 1

    PUBLIC_ACCESS = 1
    PROTECTED_ACCESS = 2
    PRIVATE_ACCESS = 3

    ACCESS_TAG_CHOICES = [
        (PUBLIC_ACCESS, "Public"),
        (PROTECTED_ACCESS, "Protected"),
        (PRIVATE_ACCESS, "Private"),
    ]

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
    activation_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    invalidated_at = models.DateTimeField(null=True, blank=True)

    # Generic foreign key for tagged objects
    tagged_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="%(class)s_type",
        default=DEFAULT,
    )
    tagged_object_id = models.PositiveIntegerField(default=DEFAULT)
    tagged_object = GenericForeignKey("tagged_type", "tagged_object_id")

    # Generic foreign key for `tag belonging to` USER or SITE
    belongs_to_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="belongs_to_%(class)s_type",
        default=DEFAULT,
    )
    belongs_to_object_id = models.PositiveIntegerField(default=DEFAULT)
    belongs_to = GenericForeignKey("belongs_to_type", "belongs_to_object_id")

    objects = TagManager()

    class Meta:  # pylint: disable=old-style-class
        """
        Meta class
        """
        verbose_name = "tag"
        verbose_name_plural = "tags"
        app_label = "eox_tagging"

    def __str__(self):
        return self.tag_value

    @property
    def tagged_object_name(self):
        """
        Obtain the name of the object tagged by the `Tag`
        """
        return self.tagged_object.__class__.__name__

    @property
    def belongs_to_object_name(self):
        """
        Obtain the name of the object which the tag belongs to
        """
        return self.belongs_to.__class__.__name__

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ

        if self.id:
            #  Exception raised when trying to update
            raise ValidationError(
                "EOX_TAGGING  |   Can't update tag. Tags are inmutable by definition"
            )

        # Tags validations

        if not any(
            s["tag_value"] == self.tag_value
            for s in base_settings.EOX_TAGGING_DEFINITIONS
        ):
            raise ValidationError(
                "EOX_TAGGING  |   The tag value is not in tag definitions"
            )

        if not any(
            s["tag_type"] == self.tag_type
            for s in base_settings.EOX_TAGGING_DEFINITIONS
        ):
            raise ValidationError(
                "EOX_TAGGING  |   The tag type is not in tag definitions"
            )

        if not any(
            taggeable_object == self.tagged_object_name
            for taggeable_object in base_settings.EOX_TAGGING_CAN_TAGGED
        ):
            raise ValidationError("EOX_TAGGING  |   Object is not available to tag")

        super(Tag, self).save(*args, **kwargs)
