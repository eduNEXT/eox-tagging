"""
Test integration file.
"""
from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=['local.edly.io', 'testserver'], SITE_ID=2)
class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with openedx
    """

    def setUp(self):
        """
        Set up the base URL for the tests
        """
        self.base_url = 'http://local.edly.io'

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_tagging.edxapp_wrappers.backends.course_overview_i_v1  # isort:skip
        import eox_tagging.edxapp_wrappers.backends.bearer_authentication_i_v1  # isort:skip
        import eox_tagging.edxapp_wrappers.backends.enrollment_l_v1  # isort:skip

    def test_info_view(self):
        """
        Tests the info view endpoint in Tutor
        """
        info_view_url = f'{self.base_url}/eox-tagging/eox-info'

        # Simulate a GET request to the info endpoint using the full URL
        response = self.client.get(info_view_url)

        # Verify the response status code
        self.assertEqual(response.status_code, 200)

        # Verify the response format
        response_data = response.json()
        self.assertIn('version', response_data)
        self.assertIn('name', response_data)
        self.assertIn('git', response_data)
