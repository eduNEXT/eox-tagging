=============
eox_tagging
=============

Eox-tagging (A.K.A. Edunext Open extensions) is an `openedx plugin`_, that adds the capability
to tag `edx-platform`_ objects. These tags can be used to categorize, include extra information, and so on.

Installation
============

Open edX devstack
------------------

- Install a supported version of the `Open edX devstack`_. See versions for more details.

- Clone the git repo:

.. code-block:: bash

  cd ~/Documents/eoxstack/src/  # Assuming that devstack is in  ~/Documents/eoxstack/devstack/
  sudo mkdir edxapp
  cd edxapp
  git clone git@github.com:eduNEXT/eox-tagging.git

- Install plugin from your server (in this case the devstack docker lms shell):

.. code-block:: bash

  cd ~/Documents/eoxstack/devstack  # Change for your devstack path (if you are using devstack)
  make lms-shell  # Enter the devstack machine (or server where lms process lives)
  cd /edx/src/edxapp/eox-tagging
  pip install -e .
  python manage.py lms migrate eox_tagging --settings=<your app settings>

Open edX with Tutor (Maple)
----------------------------
If you are using `Tutor <https://docs.tutor.overhang.io/gettingstarted.html>`_ to deploy the Open edX instance, please follow this steps:

#. Install a new fresh instance of tutor following `this steps <https://docs.tutor.overhang.io/quickstart.html#quickstart-1-click-install>`_. *If you already have a tutor instance running you can skip this step.*
#. Add to the Tutor configuration in the file ``cat "$(tutor config printroot)/config.yml"`` this lines that install eox-tagging and eox-core lib:
    .. code-block:: yaml
    
        OPENEDX_EXTRA_PIP_REQUIREMENTS:
        - eox_core
        - eox_tagging
#. Create a new tutor plugin that adds this settings to openedx common settings:
    .. code-block:: yaml
    
        EOX_TAGGING_GET_ENROLLMENT_OBJECT = "eox_tagging.edxapp_wrappers.backends.enrollment_l_v1"
        EOX_CORE_USERS_BACKEND = "eox_core.edxapp_wrapper.backends.users_m_v1"

    .. note::
        `Here <https://github.com/eduNEXT/eox-tagging/issues/83>`_ is an example of creating a tutor plugin with a yaml file. 
        But there are other ways to create tutor plugins, please go to tutor docs and see how to add settings in Open edX common settings.
#. Install the plugin doing ``tutor plugins enable eox-tagging-plugin`` and then ``tutor config save``.
#. Build the openedx image doing ``tutor images build openedx``.
#. Start the tutor instance with the new config doing ``tutor local quickstart``.
#. All set to use eox-tagging lib!

Compatibility Notes
--------------------

+-------------------+----------------+
| Open edX Release  |     Version    |
+===================+================+
|      Ironwood     |   < 0.9 < 3.0  |
+-------------------+----------------+
|       Juniper     |   >= 0.9 < 3.0 |
+-------------------+----------------+
|        Koa        |   >= 2.2 < 5.0 |
+-------------------+----------------+
|       Lilac       |   >= 2.2 < 5.0 |
+-------------------+----------------+
|       Maple       |      >= 4.0    |
+-------------------+----------------+
|       Nutmeg      |      >= 5.0    |
+-------------------+----------------+

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.

**Ironwood**

.. code-block:: yaml

    EOX_TAGGING_GET_ENROLLMENT_OBJECT: "eox_tagging.edxapp_wrappers.backends.enrollment_i_v1"
    EOX_TAGGING_GET_COURSE_OVERVIEW: "eox_tagging.edxapp_wrappers.backends.course_overview_i_v1"
    EOX_TAGGING_BEARER_AUTHENTICATION: "eox_tagging.edxapp_wrappers.backends.bearer_authentication_i_v1"

**Koa, Lilac, Maple, Nutmeg**

.. code-block:: yaml

    EOX_TAGGING_GET_ENROLLMENT_OBJECT: "eox_tagging.edxapp_wrappers.backends.enrollment_l_v1"


Those settings can be changed in ``eox_tagging/settings/common.py`` or, for example, in ansible configurations.

**NOTE**: the current ``common.py`` works with Open edX juniper version.

Usage
======

See the `How to section <https://github.com/eduNEXT/eox-tagging/tree/master/docs/how_to>`_ for a detailed guidance on: Model, configurations and API usage.

Important notes:
----------------

* All the comparison with string objects are case insensitive.
* If a tag owner is not defined, then it is assumed to be the site.

Examples
--------

**Example 1:**

.. code-block:: JSON

        {
            "validate_tag_value":{
                "in":[
                    "example_tag_value",
                    "example_tag_value_1"
                ]
            },
            "validate_access":{
                "equals":"PRIVATE"
            },
            "validate_target_object":"OpaqueKeyProxyModel",
            "owner_object":"User",
            "tag_type":"tag_by_example"
        }

This means that:

* Tag value must be in the array
* The field access must be equal to `private`
* The target type must be equal to `CourseOverview`
* The owner type must be equal to `User`
* Tag_type must be equal to `tag_by_example`

**Example 2:**

.. code-block:: JSON

        {
            "validate_tag_value":{
                "exist":true
            },
            "validate_access":"Public",
            "validate_target_object":"User",
            "tag_type":"tag_by_edunext"
        }

This means that:

* The tag value must exist, it can take any value.
* The field access must be equal to `public`.
* The target type must be equal to `User`.
* Tag type must be equal to tag_by_edunext.

**Example 3:**

.. code-block:: JSON

        {
            "validate_tag_value":"tag_value",
            "validate_access":{
                "in":[
                    "Private",
                    "Public"
                ]
            },
            "validate_target_object":"CourseEnrollment",
            "tag_type":"tag_by_edunext",
            "validate_activation_date":{
                "exist":true,
                "in":[
                    "Dec 04 2020 10:30:40",
                    "Oct 19 2020 10:30:40"
                ]
            }
        }

This means that:

* The tag value must be equal to tag_value.
* The field access can be `private` or `public`.
* The target type must be equal to `CourseEnrollment`
* Tag type must be equal to tag_by_edunext.
* The tag activation date must exist and be between the values defined in the array. This means: value_1 <= activation_date <= value_2.
  The array must be sorted or a validation error will be raised.

Tagging REST API
================

Get list of tags
----------------

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" http://BASE_URL_SITE/eox-tagging/api/v1/tags/``

**Response**

.. code-block:: JSON

        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "meta": {
                        "created_at": "2020-07-10T13:25:54.057846Z",
                        "target_id": 2,
                        "target_type": "User",
                        "inactivated_at": null,
                        "owner_type": "User",
                        "owner_id": 7
                    },
                    "key": "55a20579-ce8e-4f0b-830e-78fe79adac46",
                    "tag_value": "tag_value",
                    "tag_type": "tag_by_edunext",
                    "access": "PUBLIC",
                    "activation_date": "2020-12-04T15:20:30Z",
                    "expiration_date": null,
                    "status": "ACTIVE"
                },
                {
                    "meta": {
                        "created_at": "2020-07-10T13:33:44.277374Z",
                        "target_id": 2,
                        "target_type": "User",
                        "inactivated_at": null,
                        "owner_type": "Site",
                        "owner_id": 1
                    },
                    "key": "2bec10f5-a9e0-4e42-9c24-f9643bb13537",
                    "tag_value": "tag_value",
                    "tag_type": "tag_by_edunext",
                    "access": "PUBLIC",
                    "activation_date": "2020-12-04T15:20:30Z",
                    "expiration_date": null,
                    "status": "ACTIVE"
                },
            ]
        }

Create tag
----------

**Request**

``curl -H 'Accept: application/json' -H "Authorization: Bearer AUTHENTICATION_TOKEN" --data TAG_DATA http://BASE_URL_SITE/eox-tagging/api/v1/tags/``

Where TAG_DATA:

.. code-block:: JSON

        {
            "tag_type": "tag_by_edunext",
            "tag_value": "tag_value",
            "target_type": "user",
            "target_id": "edx",
            "access": "public",
            "owner_type": "user",
            "activation_date": "2020-12-04 10:20:30"
        }


**Response**:

``Status 201 Created``

.. code-block:: JSON

        {
            "meta": {
                "created_at": "2020-07-10T13:25:54.057846Z",
                "target_id": 2,
                "target_type": "User",
                "inactivated_at": null,
                "owner_type": "User",
                "owner_id": 7
            },
            "key": "55a20579-ce8e-4f0b-830e-78fe79adac46",
            "tag_value": "tag_value",
            "tag_type": "tag_by_edunext",
            "access": "PUBLIC",
            "activation_date": "2020-12-04T10:20:30-05:00",
            "expiration_date": null,
            "status": "ACTIVE"
        }

Delete tag
----------

**Request**

``curl -X DELETE  http://BASE_URL_SITE/eox-tagging/api/v1/tags/EXISTING_KEY_TAG/``

**Response**

``Status 204 No Content``


Filters example usage:
----------------------

``/eox_tagging/api/v1/tags/?target_type=MODEL_TYPE``

``/eox_tagging/api/v1/tags/?course_id=COURSE_ID``

``/eox_tagging/api/v1/tags/?username=USERNAME``

``/eox_tagging/api/v1/tags/?access=ACCESS_TYPE``

``/eox_tagging/api/v1/tags/?enrollments=COURSE_ID``

Auditing Django views (Optional in Maple)
=========================================

The majority of views in eox-tagging use an auditing decorator, defined in our custom library called `eox-audit-model`_,
that helps saving relevant information about non-idempotent operations. By default this functionality is turned on. To
check your auditing records go to Django sysadmin and find DJANGO EDUNEXT AUDIT MODEL.

For more information, check the eox-audit-model documentation.


.. _Open edX Devstack: https://github.com/edx/devstack/
.. _openedx plugin: https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins
.. _edx-platform: https://github.com/edx/edx-platform/
.. _eox-audit-model: https://github.com/eduNEXT/eox-audit-model/

How to Contribute
=================

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-tagging/blob/master/CONTRIBUTING.rst
