"""
Model to store tags in the database
"""
import logging
import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from eox_tagging.constants import AccessLevel, Status
from eox_tagging.validators import TagValidators

log = logging.getLogger(__name__)


class TagQuerySet(QuerySet):
    """ Tag queryset used as manager."""

    def valid(self):
        """Returns all valid tags."""
        return self.filter(invalidated_at=None)

    def invalid(self):
        """Returns all invalid tags."""
        return self.exclude(invalidated_at=None)

    def find_by_owner(self, owner):
        """Returns all valid tags owned by owner_id."""
        model = owner.__class__
        ctype = ContentType.objects.get_for_model(model)

        return self.valid().filter(
            owner_type=ctype,
            owner_object_id=owner.id,
        )

    def find_all_tags_for(self, target_object):
        """Returns all valid on an object."""
        model = target_object.__class__
        ctype = ContentType.objects.get_for_model(model)

        return self.valid().filter(
            target_type=ctype,
            target_object_id=target_object.id,
        )

    def hard_delete(self):
        """ Method for deleting Tag objects"""
        return super(TagQuerySet, self).delete()


@python_2_unicode_compatible
class Tag(models.Model):
    """
    Model class for tags.

    Overrides save method to validate data entries before saving.
    Also, overrides delete so softDeletion is available.

    Attributes:
        tag_value: unicode value of the tag. Example: free or premium
        tag_type: type of the tag. Example: Subscription tiers
        access: access level of the tag
        activation_date: date to activate the tag
        expiration-date: date to deactivate de tag
        target_object: object to tag
        belongs_to: object to which the tag belongs
        status: status of the tag, valid or invalid
        invalidated_at: date when the tag is soft deleted
    """
    key = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )

    tag_value = models.CharField(max_length=150)
    tag_type = models.CharField(max_length=150)
    access = models.PositiveIntegerField(
        choices=AccessLevel.choices(), default=AccessLevel.PUBLIC,
    )
    activation_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    status = models.PositiveIntegerField(
        choices=Status.choices(), default=Status.VALID, editable=False,
    )

    invalidated_at = models.DateTimeField(blank=True, null=True)

    # Generic foreign key for tagged objects
    target_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="%(class)s_type",
        null=True,
        blank=True,
    )
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    target_object = GenericForeignKey("target_type", "target_object_id")

    # Generic foreign key for `tag belonging to` USER or SITE
    owner_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="owner_%(class)s_type",
        null=True,
        blank=True,
    )
    owner_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    owner_object = GenericForeignKey("owner_type", "owner_object_id")

    resource_locator = models.CharField(max_length=150, null=True, blank=True)

    objects = TagQuerySet().as_manager()

    class Meta:  # pylint: disable=old-style-class
        """Meta class. """
        verbose_name = "tag"
        verbose_name_plural = "tags"
        app_label = "eox_tagging"
        unique_together = (("resource_locator", "target_object_id"),)

    def __str__(self):
        return self.tag_value

    @property
    def target_object_type(self):
        """Obtain the name of the object target by the `Tag`."""
        return self.target_object.__class__.__name__ if self.target_object else None

    @property
    def owner_object_type(self):
        """Obtain the name of the object which the tag belongs to."""
        return self.owner_object.__class__.__name__ if self.owner_object else None

    def clean(self):
        """
        Validates inter-field relations
        """
        self.validator.validate_fields()
        self.validator.validate_unique_together()

    def clean_fields(self):  # pylint: disable=arguments-differ
        """
        Validates fields individually
        """
        if getattr(settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Skip these validations while testing
            return
        self.validator.validate_fields_integrity()

    def full_clean(self, exclude=None, validate_unique=False):
        """
        Call clean_fields(), clean(), and validate_unique() -not implemented- on the model.
        Raise a ValidationError for any errors that occur.
        """
        definitions = None
        for tag_def in settings.EOX_TAGGING_DEFINITIONS:
            tag_type = tag_def.get('tag_type')
            if tag_type == self.tag_type:
                definitions = tag_def
                break

        if not definitions:
            raise ValidationError("Tag_type '{}' not configured".format(self.tag_type))

        self.validator = TagValidators(self, definitions)  # pylint: disable=attribute-defined-outside-init
        self.validator.validate_configuration()
        self.validator.validate_no_updating()
        self.clean_fields()
        self.clean()

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)

    def delete(self):  # pylint: disable=arguments-differ
        self.invalidated_at = timezone.now()
        self.status = Status.INVALID
        super(Tag, self).save()

    def hard_delete(self):
        """Deletes object from database."""
        super(Tag, self).delete()
