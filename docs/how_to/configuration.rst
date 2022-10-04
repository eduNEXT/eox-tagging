CONFIGURATIONS
===============

This plugin can't be used without setting the right configuration, if this happens then the application using
the plugin won't be able to tag any object.

This configuration defines the possible tags that can be created and the validations used in the process. This
object also has validations, so to be able to tag it must be created correctly or a validation error will be raised
while creating tags.

Configuration object
--------------------

The configuration object is an array of JSON objects that looks like this:

.. code-block:: JSON

        {
            "validate_<FIELD_NAME>": "<VALIDATION>"
        }

Where <FIELD_NAME> can be any editable tag field, and <VALIDATION> any of the defined validations.

Validations
^^^^^^^^^^^

Here's how to create validated fields, first, add the key validate_<FIELD_VALUE> to the configuration dictionary, where:

* The FIELD_VALUE must be a Tag field, if not an exception will be raised.

* If this is defined in EOX_TAGGING_DEFINITIONS as one of the tag definitions ``validate_<FIELD_VALUE_1>: <VALIDATIONS>``, then:

  * The application will expect that <VALIDATIONS> is a dictionary of validations or a string.
  * This dictionary has for keys the validations you want to perform and for values, the values allowed for the field. In case it is a string, the field must be equal to that string.
  * If a key or value is not defined then an exception will be raised. In case that is a string, the field must be equal to that string.

* If this is defined ``<FIELD_VALUE>: <VALIDATIONS>``, then:

  * The application will expect just a string as a validation. This is also a way to define the required fields.
  * The settings for EOX_TAGGING_DEFINITIONS can be a combination of dictionary validations and strings.
  * If a key in the settings dictionary has as prefix `validate` it means that the <key, value> can have a dictionary of validations as value. If not, is assume that value of that tag field is equal to that string.

* force_<FIELD_VALUE> allowing to set a value to a field without running validations or directly specifying it in the tag object.

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
| ``between``   | the field must be greater than the first member of    |  ``validate_expiration_date : {"between": [DATE_1, DATE_2]}``  |
|               | the list and less than the last member. Or can be     |                                                                |
|               | equal to one of the two. The list must be sorted.     |                                                                |
+---------------+-------------------------------------------------------+----------------------------------------------------------------+

**Important note:** the validation `equals` can be replaced with: <FIELD_NAME>: <VALUE>.

Fields
^^^^^^

+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| Name(s)                 | Description                             |  Value/Format         | Possible validators                        |
+=========================+=========================================+=======================+============================================+
| tag_value               | Contains possible values for the field  | Not specified         | in, exists, equals, regex, opaque          |
|                         |                                         |                       | any validation that can validate a string. |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| access                  | Contains possible values for the field  | Public, private,      | Any validator but must have at least one   |
|                         |                                         | protected.            | of the values defined.                     |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| expiration_date         | Contains possible datetime values for   | Year-month-day H:M:S  | in, exists, equals, between. If apply, the |
|                         | the field.                              |                       | values must match the format specified.    |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| activation_date         | Contains possible datetime values for   | Year-month-day H:M:S  | in, exists, equals, between. If apply, the |
|                         | the field.                              |                       | values must match the format specified.    |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| target_object           | Contains the only possible target value | User, site,           | equals. The values must match the targets  |
|                         | of that tag.                            | CourseEnrollment,     | predefined.                                |
|                         |                                         | OpaqueKeyProxyModel*  |                                            |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| owner_object            | Contains the only possible owner value  | User, site,           | equals. The values must match the targets  |
|                         | of that tag.                            |                       | predefined.                                |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+
| tag_type                | Contains the only possible type         | Not specified         | equals. The tag_type must always exist and |
|                         | of that tag.                            |                       | needs to be unique in the config array.    |
+-------------------------+-----------------------------------------+-----------------------+--------------------------------------------+

* In the configuration, if the user wants to create a tag on a course it must use OpaqueKeyProxyModel as the target_object.

**Important note:** as mentioned above the tag fields can or not have ``validate_`` in front of the <FIELD_NAME>, if they don't have it,
the application will assume that the field must be equal to the value. For example:

.. code-block:: JSON

        {
            "FIELD_NAME": "VALUE"
        }

This means that the FIELD with FIELD_NAME must be equal to VALUE when creating a tag, otherwise, an error will be raised.

Setting values using the configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The configuration object can also be used to set TAG values. For example, if I want all the tags to have access level `PRIVATE`
then I would do the following:

In the configuration object:

.. code-block:: JSON

        {
            "force_access": "PRIVATE"
        }

This helps to set constant values across tags without doing it explicitly while creating each one.

Errors
------

If a validation is not fulfilled, then a validation error will be raised and the tag won't be created. Please, make sure that the tag configuration
is correct.

Examples
--------

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