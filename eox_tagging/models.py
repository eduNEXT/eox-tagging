"""
Model to store tags in the database
"""
import logging
import uuid

from django.conf import settings as base_settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from eox_tagging.constants import AccessLevel, GenericType, Status
from eox_tagging.validators import Validators

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
            belongs_to_type=ctype,
            belongs_to_object_id=owner.id,
        )

    def find_all_tags_for(self, tagged_object):
        """Returns all valid on an object."""
        model = tagged_object.__class__
        ctype = ContentType.objects.get_for_model(model)

        return self.valid().filter(
            tagged_type=ctype,
            tagged_object_id=tagged_object.id,
        )


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
        tagged_object: object tagged
        belongs_to: object to which the tag belongs
        status: status of the tag, valid or invalid
        invalidated_at: date when the tag is soft deleted
    """
    id = models.AutoField(primary_key=True,)
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
    tagged_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="%(class)s_type",
        default=GenericType.DEFAULT,
        null=True,
        blank=True,
    )
    tagged_object_id = models.PositiveIntegerField(
        default=GenericType.DEFAULT,
        null=True,
        blank=True,
    )
    tagged_object = GenericForeignKey("tagged_type", "tagged_object_id")

    # Generic foreign key for `tag belonging to` USER or SITE
    belongs_to_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="belongs_to_%(class)s_type",
        default=GenericType.DEFAULT,
        null=True,
        blank=True,
    )
    belongs_to_object_id = models.PositiveIntegerField(
        default=GenericType.DEFAULT,
        null=True,
        blank=True,
    )
    belongs_to = GenericForeignKey("belongs_to_type", "belongs_to_object_id")

    resource_locator = models.CharField(max_length=150, null=True, blank=True)

    objects = TagQuerySet().as_manager()

    class Meta:  # pylint: disable=old-style-class
        """Meta class. """
        verbose_name = "tag"
        verbose_name_plural = "tags"
        app_label = "eox_tagging"
        unique_together = (("resource_locator", "tagged_object_id"),)

    def __str__(self):
        return self.tag_value

    @property
    def tagged_object_name(self):
        """Obtain the name of the object tagged by the `Tag`."""
        return self.tagged_object.__class__.__name__ if self.tagged_object else None

    @property
    def belongs_to_object_name(self):
        """Obtain the name of the object which the tag belongs to."""
        return self.belongs_to.__class__.__name__ if self.belongs_to else None

    def clean(self):
        Validators(self).run_validators()
        Validators(self).validate_unique_together()

    def clean_fields(self):  # pylint: disable=arguments-differ
        if getattr(base_settings, "EOX_TAGGING_SKIP_VALIDATIONS", False):  # Skip these validations while testing
            return
        Validators(self).validate_owner()
        Validators(self).validate_tagged_object()

    def full_clean(self, exclude=None, validate_unique=False):
        """
        Call clean_fields(), clean(), and validate_unique() -not implemented- on the model.
        Raise a ValidationError for any errors that occur.
        """
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
