# Changelog

All notable changes to this project will be documented in this file.

The format is based on ## [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to ## [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v4.2.0 - 2022-10-09

### [4.2.0](https://github.com/eduNEXT/eox-tagging/compare/v4.1.0...v4.2.0) (2022-10-09)

#### Features

- add compatibility with nutmeg release ([#94](https://github.com/eduNEXT/eox-tagging/issues/94)) ([95e94ef](https://github.com/eduNEXT/eox-tagging/commit/95e94ef23501692c10ae45ca090d6b2f84c57b39))

#### Documentation

- change deactivation_date to expiration_date ([#87](https://github.com/eduNEXT/eox-tagging/issues/87)) ([e74b942](https://github.com/eduNEXT/eox-tagging/commit/e74b9428fc7fe279c78deac87429aeb0a62fa332))
- **bumpversion:** v4.1.0 → 4.2.0 ([3df2ebc](https://github.com/eduNEXT/eox-tagging/commit/3df2ebcdf5a50f4ecd47b7014cfba0d3bc9ad702))
- **bumpversion:** v4.1.0 → 5.0.0 ([297c81e](https://github.com/eduNEXT/eox-tagging/commit/297c81ee0ade4f1095cc3bf96b32c3e599a5d4a2))

## v5.0.0 - 2022-10-09

### [4.2.0](https://github.com/eduNEXT/eox-tagging/compare/v4.1.0...v5.0.0) (2022-10-09)

#### Features

- add compatibility with nutmeg release ([#94](https://github.com/eduNEXT/eox-tagging/issues/94)) ([95e94ef](https://github.com/eduNEXT/eox-tagging/commit/95e94ef23501692c10ae45ca090d6b2f84c57b39))

#### Documentation

- change deactivation_date to expiration_date ([#87](https://github.com/eduNEXT/eox-tagging/issues/87)) ([e74b942](https://github.com/eduNEXT/eox-tagging/commit/e74b9428fc7fe279c78deac87429aeb0a62fa332))

## v4.1.0 - 2022-09-05

### [4.1.0](https://github.com/eduNEXT/eox-tagging/compare/v4.0.0...v4.1.0) (2022-09-05)

#### Features

- added installation docs with tutor ([ffa023c](https://github.com/eduNEXT/eox-tagging/commit/ffa023cc4ea5277e4ce6433f68601b8e877e6537))

#### Bug Fixes

- get_site arg ([ee27ff1](https://github.com/eduNEXT/eox-tagging/commit/ee27ff145b0f266124c1fa63a214b7d3703dc29d))
- update API url in documentation ([eb5e0ce](https://github.com/eduNEXT/eox-tagging/commit/eb5e0ce93412c096ffb8c6cd89842da6d6c95a37))

#### Continuous Integration

- add ci pipelines ([c0f904d](https://github.com/eduNEXT/eox-tagging/commit/c0f904d64e44025b19fe58cc109c50b38bffedfd))

#### Code Refactoring

- rearrange documentation to be less overwhelming ([9ec7920](https://github.com/eduNEXT/eox-tagging/commit/9ec79204b0381f471efe8687c6e668adf2989cfe))

## [3.0.0] - 2021-11-17

### Added

- **BREAKING CHANGE**: change backends defaults from Juniper to Lilac.

## [2.3.0] - 2021-10-11

### Added

- Support for tagging Certificate objects.

## [2.2.0] - 2021-05-13

### Added

- Lilac compatibility.

### Fix

- Removed headers in audited destroy method.

## [2.1.0] - 2021-04-29

### Fix

- Removed headers in audited method.

## [2.0.1] - 2021-02-11

### Fix

- Fix eox-audit-model dependency in the settings

## [2.0.0] - 2021-02-10

### Added


---

- Swagger support alongside REST API documentation

## [1.2.0] - 2021-02-03

### Added

- Added expiration_date, tag_value and tag_type filters.

Changed

- Fixed courseenrollments filters and refactor the rest.
- Removed `required` from access field in serializer.

## [1.1.0] - 2020-12-16

### Added

- Permissions compatibility with DOT.

## [1.0.0] - 2020-11-13

### Added

- Migration compatibility with PY35.

## [0.10.1] - 2020-11-12

Changed

- Fixed not loading correct settings when testing.

## [0.10.0] - 2020-10-13

### Added

- Added support for filters in django2.2

## [0.9.0] - 2020-10-05

### Added

- Added support for Django 2.2.

## [0.8.0] - 2020-09-30

### Added

- Adding bearer_authentication to support django-oauth2-provider and django-oauth-toolkit

## [0.7.0] - 2020-08-05

Changed

- Fixed case sensitive issue in the tag serializer with the fields `target_type` and `owner_type`.

## [0.6.0] - 2020-08-03

### Added

- The user can force a value in a field using the configuration.

Changed

- Fixed datetime filters for activation_date and creation_date.

## [0.5.0] - 2020-07-14

Changed

- Using - instead of _ for the urls namespace.

## [0.4.0] - 2020-07-14

### Added

- Added eox-tagging plugin documentation.
- Now invalid tags can be return using the `key` filter.
- Added info-view for the plugin.

Changed

- The Technical information for the tag now is returned in a meta field.

## [0.3.0] - 2020-07-08

### Added

- Added validations only for DateTime fields.
- Added custom permissions to access the tag API.

Changed

- Changed Date fields like expiration date and activation date to DateTime fields.
- Changed STATUS from valid/invalid to active/inactive.

## [0.2.0] - 2020-06-26

- REST API to create, get, filter and delete tags.
- 
- New filters in Tag queryset.
- 
- First PyPI release.
- 

## [0.1.0] - 2020-06-23

### Added

- First Github Release.
