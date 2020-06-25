=============
eox_tagging
=============

Features
=========

Place your plugin features list.

Installation
============


Open edX devstack
------------------

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart Lms/Studio services.


Usage
======

Important notes:
----------------

* All the comparison with string objects are case insensitive.
* validate_<FIELD_VALUE> meaning:

  * The FIELD_VALUE must be a Tag field, if not an exception will be raised.
  * If this is defined in EOX_TAGGING_DEFINITIONS as one of the tag definitions:

    ``validate_<FIELD_VALUE_1>: <VALIDATIONS>``

    * The application will expect that <VALIDATIONS> is a dictionary of validations or a string.

    * This dictionary has for keys the validations you want to perform and for values, the values allowed for the field. In case it is a string, the field must be equal to that string.

    * If a key or value is not defined then an exception will be raised. In case that is a string, the field must be equal to that string.

  * If this is defined:

    ``<FIELD_VALUE>: <VALIDATIONS>``

    * The application will expect just a string as a validation. This is also a way to define the required fields.

    * The settings for EOX_TAGGING_DEFINITIONS can be a combination of dictionary validations and strings.

  * If a key in the settings dictionary has as prefix `validate` it means that the <key, value> can have a dictionary of validations as value. If not, is assume that
      value is a string.

* The validations available are:

+---------------+-------+-----------------------------------------------+----------------------------------------------------------------+
| Name          | Description                                           | Example                                                        |
+===============+=======================================================+================================================================+
| ``in``        | the field must be equal to one of the strings defined | ``validate_tag_value : {"in": ["tag_value_1", "tag_value_2"]}``|
|               | inside the array                                      |                                                                |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
| ``exists``    | the field must be different to None                   |  ``validate_tag_value : {"exists": true}``                     |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|  ``equals``   | the field must be equal to the dictionary value       |  ``validate_tag_value : {"equals": "tag_value"}``              |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|  ``regex``    | the field must match the pattern defined              |  ``validate_tag_value : {"regex": ".+eduNEXT"}``               |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+
|``opaque_key`` | the field must be an opaque key                       |  ``validate_tag_value : {"opaque_key": "CourseKey"}``          |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+


* The available objects to tag and validate are: User, Site, CourseOverview and CourseEnrollment

* If an owner is not defined, then it is assumed to be the site.

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
                    "Dec 04 2020",
                    "Oct 19 2020"
                ]
            }
        }

This means that:

* The tag value must be equal to tag_value.
* The field access can be `private` or `public`.
* The target type must be equal to `CourseEnrollment`
* Tag type must be equal to tag_by_edunext.
* The tag activation date must exist and be in the values defined in the array

Rest API usage
==============



Filters example usage:
/eox_tagging/api/v1/tags/?created_at_after=2020-10-10
/eox_tagging/api/v1/tags/?access=1
/eox_tagging/api/v1/tags/?target_type=user


##Contributing

Add your contribution policy. (If required)