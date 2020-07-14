Change Log
==========

..
   All enhancements and patches to eox-tagging will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.

Unreleased
----------

* Added eox-tagging plugin documentation.
* Now invalid tags can be return using the `key` filter.
* Added info-view for the plugin.

[0.3.0] - 2020-07-08
--------------------

Added
_____

* Added validations only for DateTime fields.
* Added custom permissions to access the tag API.

Changed
_______

* Changed Date fields like expiration date and activation date to DateTime fields.
* Changed STATUS from valid/invalid to active/inactive.

[0.2.0] - 2020-06-26
---------------------

* REST API to create, get, filter and delete tags.
* New filters in Tag queryset.

* First PyPI release.

[0.1.0] - 2020-06-23
---------------------

Added
~~~~~

* First Github Release.
