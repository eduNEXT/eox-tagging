"""
Test classes for Tags model
"""


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from eox_tagging.models import Tag


class TestTag(TestCase):
    """Class for testing the Tag model
    """

    def setUp(self):
        """ Model setup used to create objects used in tests
        """
        self.tagged_object = User.objects.create(username="Tag")
        self.belongs_to_object = User.objects.create(username="User")

        Tag.objects.create(
            tag_value="testValue",
            tag_type="testType",
            tagged_object=self.tagged_object,
            belongs_to=self.belongs_to_object,
        )

    def test_valid_tag(self):
        """ Used to confirm that the tags created are valid
        """
        test_tag = Tag.objects.get(id=1)
        tag_status = getattr(test_tag, "status")

        self.assertEqual(tag_status, 1)

    def test_tag_value(self):
        """ Used to confirm that the tag_value is correct
        """

        test_tag = Tag.objects.get(id=1)
        tag_value = getattr(test_tag, "tag_value")

        self.assertEqual(tag_value, "testValue")

    def test_tag_type(self):
        """ Used to confirm that the tag_type is correct
        """

        test_tag = Tag.objects.get(id=1)
        tag_value = getattr(test_tag, "tag_type")

        self.assertEqual(tag_value, "testType")

    def test_tag_value_not_in_settings(self):
        """ Used to confirm validation error when the value is not defined
        """
        with self.assertRaises(ValidationError):
            Tag.objects.create(
                tag_value="testValues",
                tag_type="testType",
                tagged_object=self.tagged_object,
                belongs_to=self.belongs_to_object,
            )

    def test_tag_type_not_in_settings(self):
        """ Used to confirm validation error when the type is not defined
        """
        with self.assertRaises(ValidationError):
            Tag.objects.create(
                tag_value="testValue",
                tag_type="testTypes",
                tagged_object=self.tagged_object,
                belongs_to=self.belongs_to_object,
            )

    def test_tag_different_generic_objects(self):
        """ Used to confirm the tags can be use with any object defined in settings
        """
        pass

    def test_tag_different_generic_objects_fail(self):
        """ Used to confirm the tags can't be use with objects not defined in settings
        """
        pass

    def test_tag_inmutable(self):
        """ Used to confirm that the tags can't be updated
        """
        test_tag = Tag.objects.get(id=1)
        setattr(test_tag, "tag_value", "value")
        with self.assertRaises(ValidationError):
            test_tag.save()

    def test_tag_soft_delete(self):
        """ Used to confirm that the tags can be invalidated soft deleting them
        """

        test_tag = Tag.objects.get(id=1)
        test_tag.delete()
        tag_status = getattr(test_tag, "status")

        self.assertEqual(tag_status, 0)
