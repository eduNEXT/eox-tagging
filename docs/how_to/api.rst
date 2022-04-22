REST API
=========

Authentication and permissions
--------------------------------

Token and session authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Currently, to be able to use the API, the user must be authenticated. One of the options is to provide an authentication token when making
any request to the tagging API. In the future, public -limited- access will be provided.

As mentioned above, an authorization token can be provided as an Authorization HTTP header when calling the API.
If not, then the session authentication will be use. If any of this authentications work then the user won't be able to make any
successful API call.

API permission
^^^^^^^^^^^^^^^
If a user wants to make API calls, in addition to being authenticated must have the custom eox-tagging permission so can make any write/read operations.
This permission iscalled `can_call_eox_tagging`.


Possible API calls
---------------------

The tags are `immutable` by definition, so after creating a tag the only calls allowed are to list, get details and delete tags.

+---------------------------------+---------------------------------------------------+
| Name                            | Description                                       |
+=================================+===================================================+
| list                            | Used to list all tags owned by the user making the|
|                                 | API call. If the owner does not have any tags     |
|                                 | created yet, an empty set will be returned.       |
+---------------------------------+---------------------------------------------------+
| details                         | Used to get the information of a single tag. If   |
|                                 | the tag does not exist it returns Not Found.      |
+---------------------------------+---------------------------------------------------+
| delete                          | Used to deactivate an active tag. This implements |
|                                 | a soft delete operation.                          |
+---------------------------------+---------------------------------------------------+
| create                          | Used to create a tag.                             |
+---------------------------------+---------------------------------------------------+


Serializer fields
------------------

When creating a tag, this are the fields expected:

+----------------------------------+--------------------------------------------------+------------------+
| Field Name                       | Description                                      | Required         |
+==================================+==================================================+==================+
| tag_type                         | Works as the class of the tag.                   | Yes              |
+----------------------------------+--------------------------------------------------+------------------+
| tag_value                        | It can be thought as the class instance.         | Yes              |
+----------------------------------+--------------------------------------------------+------------------+
| access                           | Access level of the tag.                         | Yes              |
+----------------------------------+--------------------------------------------------+------------------+
| activation_date                  | Datetime when the tag will be activated.         | No               |
|                                  | It can have UTC format or Year-Month-Day H:M:S   |                  |
+----------------------------------+--------------------------------------------------+------------------+
| deactivation_date                | Datetime when the tag will be deactivated.       | No               |
|                                  | It can have UTC format or Year-Month-Day H:M:S   |                  |
+----------------------------------+--------------------------------------------------+------------------+
| target_type                      | Type of the target. Must be equal to: user, site,| Yes              |
|                                  | courseoverview or courseenrollment.              |                  |
+----------------------------------+--------------------------------------------------+------------------+
| target_id                        | ID of the target with type target_type.          | Yes              |
+----------------------------------+--------------------------------------------------+------------------+
| owner_type                       | Type of the tag owner. If omitted, site will be  | No               |
|                                  | as the owner                                     |                  |
+----------------------------------+--------------------------------------------------+------------------+

When retrieving objects, the JSON object will have the following fields (the mentioned above and):

+----------------------------------+---------------------------------------------------+
| Field Name                       | Description                                       |
+==================================+===================================================+
| meta                             | Field with technical information, like dates and  |
|                                  | information about the target and the owner.       |
+----------------------------------+---------------------------------------------------+
| status                           | Status of the tag. This could be active or        |
|                                  | inactive.                                         |
+----------------------------------+---------------------------------------------------+
| key                              | UUID Public identifier.                           |
+----------------------------------+---------------------------------------------------+


Validations
-----------

During the creation process starts, it's checked that ``target_type`` exists, if not then the creation process is interrupted and an error
will be raised. This results in returning an object describing the error ocurred. After checking if the target_type exists, the model validations
will be performed and if an error occurs the error message will be returned in a response instead of valid data.


Examples
--------

Get list of tags
^^^^^^^^^^^^^^^^

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" http://BASE_URL_SITE/eox-tagging/api/v1/tags/``

**Response**

.. code-block:: JSON

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "key": "8a265b65-9555-4cd1-9d64-ee2009d80301",
                    "tag_value": "example_tag_value",
                    "tag_type": "tag_by_example",
                    "access": "PRIVATE",
                    "activation_date": null,
                    "expiration_date": null,
                    "target_id": "course-v1:edX+DemoX+Demo_Course",
                    "owner_id": "reporting",
                    "owner_type": "User",
                    "target_type": "OpaqueKeyProxyModel",
                    "status": "VALID"
                }
            ]
        }

Create tag
^^^^^^^^^^^^^^^^

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" --data TAG_DATA http://BASE_URL_SITE/eox-tagging/api/v1/tags/``

Where TAG_DATA:

.. code-block:: JSON

        {
            "tag_type": "tag_by_example",
            "tag_value": "example_tag_value",
            "target_type": "courseoverview",
            "target_id": "course-v1:edX+DemoX+Demo_Course",
            "access": "PRIVATE",
            "owner_type": "user"
        }


**Response**:

``Status 201 Created``

.. code-block:: JSON

        {
            "key": "6a41e775-cc2b-42df-b62d-d3e92e1bc484",
            "tag_value": "example_tag_value",
            "tag_type": "tag_by_example",
            "access": "PRIVATE",
            "activation_date": null,
            "expiration_date": null,
            "target_id": "course-v1:edX+DemoX+Demo_Course",
            "owner_id": "reporting",
            "owner_type": "User",
            "target_type": "OpaqueKeyProxyModel",
            "status": "VALID"
        }

Delete tag
^^^^^^^^^^^^^^^^

**Request**

``curl -X DELETE  http://BASE_URL_SITE/eox-tagging/api/v1/tags/EXISTING_KEY_TAG/``

**Response**

``Status 204 No Content``


Filters example usage
^^^^^^^^^^^^^^^^^^^^^^

**Filter with target information:**

``/eox_tagging/api/v1/tags/?target_type=MODEL_TYPE``

``/eox_tagging/api/v1/tags/?course_id=COURSE_ID``

``/eox_tagging/api/v1/tags/?username=USERNAME``

``/eox_tagging/api/v1/tags/?enrollments=COURSE_ID``

**Filter with other fields:**

``/eox_tagging/api/v1/tags/?access=ACCESS_TYPE``
