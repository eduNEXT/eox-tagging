`TAG` MODEL
============

What is a tag
-------------

A tag is an object created over a specified target by an entity called owner. This tag works as an object classifier.

Attributes
-----------

+--------------------------+----------------------------------------------------------------------------+
| Name                     |  Description                                                               |
+==========================+============================================================================+
| tag_type                 | This attribute works as a category, it can be for example:                 |
|                          | `subscription_tier`.                                                       |
+--------------------------+----------------------------------------------------------------------------+
| tag_value                | Contains the value of the tag. This would be for `subscription_tier`       |
|                          | the value `free`.                                                          |
+--------------------------+----------------------------------------------------------------------------+
| access                   | The access level for the tag, it can be public, private and protected. This|
|                          | this defines the visibility of the tag to the users. The default is public.|
+--------------------------+----------------------------------------------------------------------------+
| activation_date          | Datetime when the tag will be activated.                                   |
+--------------------------+----------------------------------------------------------------------------+
| deactivation_date        | Datetime when the tag will be deactivated.                                 |
+--------------------------+----------------------------------------------------------------------------+
| created_at               | Creation date.                                                             |
+--------------------------+----------------------------------------------------------------------------+
| status                   | Current tag status, when created is ACTIVE, and when is deleted becomes    |
|                          | an inactive tag.                                                           |
+--------------------------+----------------------------------------------------------------------------+
| target_object            | Represents the tag target, this can be a user, courseenrollment, site or   |
|                          | course.                                                                    |
+--------------------------+----------------------------------------------------------------------------+
| owner_object             | Represents the tag owner. This can be a user or site.                      |
+--------------------------+----------------------------------------------------------------------------+


Validations
-----------

The validations done on a tag depends on the configuration object. Before starting with the validation process, the right configuration is selected,
that is the one that matches with the tag_type of the tag being created. Then, the validations defined are executed.

Besides these validations, integrity validations are performed, i.e. the existence of the target and owner is checked.
