"""
Model to store tags in the database.
"""
import datetime
import logging
import re
import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from opaque_keys.edx.django.models import CourseKeyField
from opaque_keys.edx.keys import CourseKey

from eox_tagging.constants import AccessLevel, Status
from eox_tagging.helpers import get_model_name
from eox_tagging.validators import TagValidators

log = logging.getLogger(__name__)


class TagQuerySet(QuerySet):
    """ Tag queryset used as manager."""

    def create_tag(self, **kwargs):
        """Method used to create tags."""
        target = kwargs.pop('target_object', None)
        if target and target.__class__.__name__ == "CourseOverview":
            kwargs['target_object'] = OpaqueKeyProxyModel.objects.create(opaque_key=target.course_id)
        else:
            kwargs['target_object'] = target
        instance = self.create(**kwargs)
        return instance

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
        if get_model_name(target_object) == 'CourseOverview':
            model = OpaqueKeyProxyModel
            target_id = OpaqueKeyProxyModel.objects.get(opaque_key=target_object.course_id).id
        else:
            model = target_object.__class__
            target_id = target_object.id
        ctype = ContentType.objects.get_for_model(model)

        return self.valid().filter(
            target_type=ctype,
            target_object_id=target_id,
        )

    def hard_delete(self):
        """ Method for deleting Tag objects"""
        return super(TagQuerySet, self).delete()


@python_2_unicode_compatible
class OpaqueKeyProxyModel(models.Model):
    """Model used to tag objects with opaque keys."""
    opaque_key = CourseKeyField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        """Method that returns the opaque_key string representation."""
        return unicode(self.opaque_key)


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

    invalidated_at = models.DateTimeField(blank=True, null=True, editable=False)

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

    objects = TagQuerySet().as_manager()

    class Meta:  # pylint: disable=old-style-class
        """Meta class. """
        verbose_name = "tag"
        verbose_name_plural = "tags"
        app_label = "eox_tagging"

    def __str__(self):
        return self.tag_value

    @property
    def target_object_type(self):
        """Obtain the name of the object target by the `Tag`."""
        target_type = self.target_object.__class__.__name__ if self.target_object else None

        if target_type == 'OpaqueKeyProxyModel':
            return self.__opaque_key_target()

        return target_type

    def __opaque_key_target(self):
        if self.target_object.__class__.__name__ == 'OpaqueKeyProxyModel' and \
           isinstance(self.target_object.opaque_key, CourseKey):
            return 'CourseOverview'
        return None

    @property
    def owner_object_type(self):
        """Obtain the name of the object which the tag belongs to."""
        return self.owner_object.__class__.__name__ if self.owner_object else None

    def get_attribute(self, attr, name=False):
        """
        Function used to format attributes getting them from self object.

        Arguments:
            - name: used if attr is target or owner and want to get the class name.
        """

        if attr and re.match(r".+object$|.+object_type$", attr):
            return self.__get_model(attr, name)

        if attr in ['activation_date', 'expiration_date']:
            return self.__get_dates(attr)

        if attr == 'access':
            return self.__get_field_choice(attr)

        return getattr(self, attr)

    def __get_dates(self, attr):
        """Function that gets formatted dates for the model."""
        date = getattr(self, attr)
        date_format = "%b %d %Y"
        try:
            date_str = datetime.datetime.strftime(date, date_format)
        except TypeError:
            return None
        return date_str

    def __get_model(self, attr, name):
        """
        Function that gets the type stored by the proxy model. This function is called when we want
        the actual type of the target object.

        Arguments:
            - attr: name of the attr
            - name: in case we want the class and not the object
        """

        field_value = getattr(self, "{}_type".format(attr))
        if name:
            return field_value
        else:
            return getattr(self, attr)

    def __get_field_choice(self, attr):
        """
        Function that gets the choice of the choice field

        Arguments:
            - attr: name of the attr
            - name: in case we want the class and not the object
        """
        field_value = getattr(self, attr)

        try:
            choice = getattr(field_value, "name")
            return choice
        except AttributeError:
            choice = AccessLevel.get_choice(field_value)
            return choice

    def clean(self):
        """
        Validates inter-field relations
        """
        self.validator.validate_fields()

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
        self.validator = TagValidators(self)  # pylint: disable=attribute-defined-outside-init
        self.clean()
        self.clean_fields()

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
