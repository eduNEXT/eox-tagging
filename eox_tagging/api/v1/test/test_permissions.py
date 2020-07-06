""" Test classes for API Permissions. """
from django.contrib.auth.models import Permission, User
from django.test import TestCase, override_settings
from mock import Mock

from eox_tagging.api.v1.permissions import EoxTaggingAPIPermissionOrReadOnly, load_permissions


@override_settings(EOX_TAGGING_LOAD_PERMISSIONS=True)
class TestAPIPermissions(TestCase):
    """Test class for tags viewset."""

    def setUp(self):
        """ Permissions setup."""
        load_permissions()

        # User with permission to acccess the API
        user_permission = Permission.objects.get(codename="can_call_eox_tagging")
        self.user_authorized = User.objects.create(username="user_with_permission")
        self.user_authorized.user_permissions.add(user_permission)

        # Common user without permission
        self.common_user = User.objects.create(username="user_without_permission")

        self.has_permission = EoxTaggingAPIPermissionOrReadOnly().has_permission

    def test_API_access_success(self):
        """Used to test that an authorized user can access to the Tag API."""
        mock_request = Mock()
        mock_request.get_host.return_value = "test.com"
        mock_request.user = self.user_authorized
        mock_request.auth.client.url = "test.com"
        view = Mock()

        has_permission = self.has_permission(mock_request, view)

        self.assertTrue(has_permission)

    def test_API_access_denied(self):
        """Used to test that an unauthorized user can't access to the Tag API."""
        mock_request = Mock()
        mock_request.get_host.return_value = "test.com"
        mock_request.user = self.common_user
        mock_request.auth.client.url = "test.com"
        view = Mock()

        has_permission = self.has_permission(mock_request, view)

        self.assertFalse(has_permission)
