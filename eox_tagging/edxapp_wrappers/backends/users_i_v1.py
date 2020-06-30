"""
Backend get edxapp users.
"""


def get_platform_user():
    """Backend to get edxapp users."""
    try:
        from eox_core.edxapp_wrapper.users import get_edxapp_user
    except ImportError:
        get_edxapp_user = object
    return get_edxapp_user
