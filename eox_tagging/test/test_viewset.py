""" Test classes for Tags viewset. """
import datetime

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from eox_tagging.constants import AccessLevel
from eox_tagging.models import Tag
from eox_tagging.test.test_utils import CourseOverview


@override_settings(
    EOX_TAGGING_DEFINITIONS=[
        {
            "tag_type": "example_tag_1",
            "validate_owner_object": "User",  # default = Site
            "validate_access": {"equals": "PRIVATE"},
            "validate_tag_value": {"in": ["example_tag_value", "example_tag_value_1"]},
            "validate_target_object": "User",
            "validate_expiration_date": {"exist": True},
        },
        {
            "tag_type": "example_tag_2",
            "validate_owner_object": "Site",
            "validate_access": {"equals": "PRIVATE"},
            "validate_tag_value": {"in": ["example_tag_value", "example_tag_value_1"]},
            "validate_target_object": "User",
            "validate_expiration_date": {"exist": True},
        },
    ])
@CourseOverview.fake_me
class TestTagViewSet(TestCase):
    """Test class for tags viewset."""

    def setUp(self):
        """ Model setup used to create objects used in tests."""
        self.target_object = User.objects.create(username="user_test")

        # Admin authentication
        password = 'mypassword'
        self.admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

        self.example_tag = Tag.objects.create(
            tag_value="example_tag_value",
            tag_type="example_tag_1",
            target_object=self.target_object,
            owner_object=self.admin,
            access=AccessLevel.PRIVATE,
            expiration_date=datetime.date(2020, 10, 19),
        )

        # Test URLs
        self.URL = reverse("tag-list")

    def test_get_all_tags(self):
        """Used to test getting all tags."""
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)

    def test_retreive_tag(self):
        """Used to test getting a tag given its key."""
        response = self.client.get("{URL}{key}/".format(URL=self.URL, key=self.example_tag.key.hex))

        self.assertEqual(response.status_code, 200)

    def test_create_tag(self):
        """"Used to test creating a tag."""
        data = {
            "tag_type": "example_tag_1",
            "tag_value": "example_tag_value",
            "target_type": "user",
            "target_id": "user_test",
            "owner_type": "user",
            "access": "PRIVATE",
            "expiration_date": "2020-12-04 10:20:30",
        }

        response = self.client.post(self.URL, data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_create_tag_without_owner(self):
        """"
        Used to test creating a tag without an owner. The owner should be set as a default
        to be the site.
        """
        data = {
            "tag_type": "example_tag_2",
            "tag_value": "example_tag_value",
            "target_type": "user",
            "target_id": "user_test",
            "access": "PRIVATE",
            "expiration_date": "2020-12-04 10:20:30",
        }

        response = self.client.post(self.URL, data, format='json')

        self.assertEqual(response.data.get("owner_type").lower(), "site")

    def test_create_tag_with_iso_datetime_format(self):
        """"Used to test creating a tag using ISO format in datetime fields."""
        data = {
            "tag_type": "example_tag_1",
            "tag_value": "example_tag_value",
            "target_type": "user",
            "target_id": "user_test",
            "owner_type": "user",
            "access": "PRIVATE",
            "expiration_date": "2020-12-04T10:20:30.15785",
        }

        response = self.client.post(self.URL, data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_create_tag_with_wrong_datetime_format(self):
        """"
        Used to test creating a tag using wrong format in datetime fields. This results in a
        bad request.
        """
        data = {
            "tag_type": "example_tag_1",
            "tag_value": "example_tag_value",
            "target_type": "user",
            "target_id": "user_test",
            "owner_type": "user",
            "access": "PRIVATE",
            "expiration_date": "12-04-2020 10:20:30",
        }

        response = self.client.post(self.URL, data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_patch_tag(self):
        """Used to test that a tag can't be updated."""
        response = self.client.patch("{URL}{key}/".format(URL=self.URL, key=self.example_tag.key.hex))

        self.assertEqual(response.status_code, 405)

    def test_put_tag(self):
        """Used to test that a tag can't be updated."""
        response = self.client.put("{URL}{key}/".format(URL=self.URL, key=self.example_tag.key.hex))

        self.assertEqual(response.status_code, 405)

    def test_filter_by_tag_key(self):
        """Used to test getting a tag given its key."""
        url = "{URL}?key={key}".format(URL=self.URL, key=self.example_tag.key.hex)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_filter_by_username(self):
        """Used to test getting a tag given its target."""
        URL = "{URL}?username={user}".format(URL=self.URL, user="user_test")

        response = self.client.get(URL)

        self.assertEqual(response.status_code, 200)

    def test_filter_by_type(self):
        """Used to test getting a tag given its target."""
        URL = "{URL}?target_type={type}".format(URL=self.URL, type="user")

        response = self.client.get(URL)

        self.assertEqual(response.status_code, 200)

    def test_soft_delete(self):
        """Used to test a tag soft deletion."""
        URL = "{URL}{key}/".format(URL=self.URL, key=self.example_tag.key.hex)

        response = self.client.delete(URL)

        self.assertEqual(response.status_code, 204)
