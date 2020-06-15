"""Tag model helper."""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from opaque_keys.edx.django.models import CourseKeyField

try:
    # Python 2: "unicode" is built-in
    unicode
except NameError:
    unicode = str  # pylint: disable=redefined-builtin


@python_2_unicode_compatible
class ProxyModel(models.Model):
    """Model used to tag objects with opaque keys."""
    opaque_key = CourseKeyField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        """Method that returns the opaque_key string representation."""
        return unicode(self.opaque_key)
