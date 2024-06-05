"""
Test integration file.
"""
from django.test import TestCase


class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with openedx
    """

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_tagging.edxapp_wrappers.backends.course_overview_i_v1  # isort:skip
        import eox_tagging.edxapp_wrappers.backends.bearer_authentication_i_v1  # isort:skip
        import eox_tagging.edxapp_wrappers.backends.enrollment_l_v1  # isort:skip
