"""
Utils to run tests
"""
from django.db import models


try:
    from django_fake_model import models as fake

    class CourseFakeModel(fake.FakeModel):
        """
        Fake Model courses.
        """

        pass


except ImportError:
    CourseFakeModel = object


try:
    from django_fake_model import models as fake

    class EnrollmentsFakeModel(fake.FakeModel):
        """
        Fake Model enrollments.
        """

        pass

except ImportError:
    EnrollmentsFakeModel = object