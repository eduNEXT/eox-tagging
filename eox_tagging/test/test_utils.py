"""
Utils to run tests
"""
from django.db import models
from opaque_keys.edx.django.models import CourseKeyField

try:
    from django_fake_model import models as fake

    class CourseOverview(fake.FakeModel):
        """Fake Model enrollments."""
        course_id = CourseKeyField(max_length=255)

except ImportError:
    CourseOverview = object

try:
    from django_fake_model import models as fake

    class CourseEnrollment(fake.FakeModel):
        """Fake Model enrollments."""
        username = models.CharField(max_length=255, null=True)
        course_id = models.CharField(max_length=255, null=True)

except ImportError:
    CourseEnrollment = object
