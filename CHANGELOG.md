# Changelog

All notable changes to this project will be documented in this file.

The format is based on ## [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to ## [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v9.1.0](https://github.com/eduNEXT/eox-tagging/compare/v9.0.0...v9.1.0) - (2025-06-09)

### Changed

- **Teak Support**: Upgrade requirements base on edx-platform Teak

## [v9.0.0](https://github.com/eduNEXT/eox-tagging/compare/v8.0.0...v9.0.0) - (2024-12-19)

### Changed

- **Sumac Support**: Removed support for Python 3.8. Upgrade requirements base on edx-platform Sumac
  release update GitHub workflows and actions version, and update integration test to use new Sumac release with Tutor.

## [v8.0.0](https://github.com/eduNEXT/eox-tagging/compare/v7.3.0...v8.0.0) - (2024-10-22)

#### ⚠ BREAKING CHANGES

- **Dropped Support for Django 3.2**: Removed support for Django 3.2 in this plugin. As a result, we have also dropped support for Open edX releases from Maple up to and including Palm, which rely on Django 3.2. Future versions of this plugin may not be compatible with these Open edX releases.

## [v7.3.0](https://github.com/eduNEXT/eox-tagging/compare/v7.2.0...v7.3.0) - (2024-10-01)

### Added

- **JWT Support**: API for `Tags` now supports JWT (JSON Web Tokens) authentication
  aiming to mitigate the deprecation of Bearer and keep available the token-based authorization

## [v7.2.0](https://github.com/eduNEXT/eox-tagging/compare/v7.1.0...v7.2.0) - (2024-08-06)

### Added

- **Integration Tests**: A new GitHub workflow has been added to run
  integration tests. These tests validate backend imports and ensure the
  `/eox-info` endpoint functions correctly.

### Fixed

- **Redwood Compatibility**: Corrected a build-time error, ensuring full
  compatibility with the Redwood release. For this, a new `ImproperlyConfigured`
  exception is handled when loading the API permissions.

### Changed

- **Redwood Support**: Updated requirements based on the edx-platform Redwood release. Revised integration tests to use the new Redwood release with Tutor.
  release update GitHub workflows with new Python (3.10 and 3.11) and actions
  version, and update integration test to use new redwood release with Tutor.

## v7.1.0 - 2024-03-19

### [7.1.0](https://github.com/eduNEXT/eox-tagging/compare/v7.0.0...v7.1.0) (2024-03-19)

#### Features

* add workflow to add items to the Dedalo project DS-831 ([#103](https://github.com/eduNEXT/eox-tagging/issues/103)) ([0c93d84](https://github.com/eduNEXT/eox-tagging/commit/0c93d845dd3c1f29c8e5ac517c167094bb61e2ba))

## v7.0.0 - 2024-02-13

### [7.0.0](https://github.com/eduNEXT/eox-tagging/compare/v6.0.0...v7.0.0) (2024-02-13)

#### ⚠ BREAKING CHANGES

* add compatibility with Quince release
  
* chore: update main requirements & add django 4.2 support
  
* chore: support django 42 & solve issues in testing
  
* fix: delete deprecated pylint rules
  
* fix: use pylint messages control
  
* fix: ignore migrations from quality tests
  
* fix: solve deprecated methods & apply linter corrections
  
* chore: update github-actions requirements
  
* docs: update compatibility notes
  
* fix: add required blank line after table
  

#### Performance Improvements

* add compatibility with Quince release ([#102](https://github.com/eduNEXT/eox-tagging/issues/102)) ([cff9359](https://github.com/eduNEXT/eox-tagging/commit/cff93597d26b93d5a403f2bc89f821f4bff77caa))

#### Documentation

* improve changelog ([ba004ef](https://github.com/eduNEXT/eox-tagging/commit/ba004efbc96f8d44f0c1f59b9853e790054882ac))

## v6.0.0 - 2024-01-02

### [6.0.0](https://github.com/eduNEXT/eox-tagging/compare/v5.1.0...v6.0.0) (2024-01-02)

#### ⚠ BREAKING CHANGES

* add compatibility with palm release
  
* perf: add support for palm release
  
* fix: remove 3.10 version test
  
* fix: pylint issues
  
* docs: update readme
  

#### Performance Improvements

* add compatibility with Open edX Palm release DS-708 ([#100](https://github.com/eduNEXT/eox-tagging/issues/100)) ([9540f2a](https://github.com/eduNEXT/eox-tagging/commit/9540f2a02774d3278b44b0548afed6ac81b94615))

## v5.1.0 - 2023-02-10

### [5.1.0](https://github.com/eduNEXT/eox-tagging/compare/v5.0.0...v5.1.0) (2023-02-10)

#### Features

- add compatibility with Open edX olive release ([4b985c0](https://github.com/eduNEXT/eox-tagging/commit/4b985c04a2810bdaac78b37f0af05b6ed8622d4c))

#### Documentation

- adds issue template ([0758024](https://github.com/eduNEXT/eox-tagging/commit/0758024f6287991c085af98d433b14ef8d4c598a))
- update readme with olive version ([8eec015](https://github.com/eduNEXT/eox-tagging/commit/8eec0157f5e7bfcc915a66b3440d441066d0488e))

#### Continuous Integration

- adds mantainer group ([bd105de](https://github.com/eduNEXT/eox-tagging/commit/bd105deab7d4a9fc7b0d0a5f4de484ae0686e24d))
- update the changelog updater step in bumpversion ([#95](https://github.com/eduNEXT/eox-tagging/issues/95)) ([35cb9e1](https://github.com/eduNEXT/eox-tagging/commit/35cb9e1538c491a4d99f79f8e06b6663c3492bdd))
- update workflows to github actions ([7d7ac61](https://github.com/eduNEXT/eox-tagging/commit/7d7ac6119cdc955439d4fea41e77caea1c772356))

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
