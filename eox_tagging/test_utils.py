"""
Utils to run tests
"""
try:
    from django_fake_model import models as fake

    class CourseOverview(fake.FakeModel):
        """Fake Model courses."""
        pass

except ImportError:
    CourseOverview = object


try:
    from django_fake_model import models as fake

    class CourseEnrollments(fake.FakeModel):
        """Fake Model enrollments."""
        pass

except ImportError:
    CourseEnrollments = object
