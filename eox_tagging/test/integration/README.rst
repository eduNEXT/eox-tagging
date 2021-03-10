Integration tests
=================

.. contents::

TAG API
+++++++++++++++

Running
-------

The integration test are skipped by default due to them requiring specific
users, courses and enrollments to be registered on the data base. Once
properly configured the test can be run by setting an environment variable
``TEST_INTEGRATION````

.. code-block:: console

    $ TEST_INTEGRATION=true make python-test

Configuration
--------------

The site where the test are going to be run must have the following configuration:

.. code-block:: json
  "EOX_TAGGING_DEFINITIONS": [
        {
            "owner_object": "Site",
            "tag_type": "test_enrollment_tag",
            "validate_target_object": "courseenrollment"
        },
        {
            "owner_object": "Site",
            "tag_type": "test_course_tag",
            "validate_target_object": "OpaqueKeyProxyModel"
        },
        {
            "owner_object": "Site",
            "tag_type": "test_user_tag",
            "validate_access": {
                "equals": "PUBLIC"
            },
            "validate_target_object": "user"
        }
  ]

The file `test_data.json` must be modified to include the following data

.. code-block:: json
    {
        "base_url": "http://localhost:18000",
        "access_token": "xxjVz7oUUbfVxrHJ7HdfnpUlEhsmyW",
        "username": "user",
        "course_id": "course-v1:edX+DemoX+Demo_Course"
    }

Where username and course_id identify a user and a course that exist on the site
and the user is enrolled on said course. Access token is an authentication token
with the corresponding permissions.
