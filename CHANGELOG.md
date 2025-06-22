# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-mm-dd

### Added

- Deployed online documentation: https://flet-dev.github.io/flet-geolocator/
- `Geolocator` control new methods: `distance_between_async`
- `Geolocator` control new properties: `position`, `configuration`
- New dataclasses: 
    - `GeolocatorConfiguration`
    - `GeolocatorWebConfiguration`
    - `GeolocatorIosConfiguration`
    - `GeolocatorAndroidConfiguration`
    - `ForegroundNotificationConfiguration`

### Changed

- Refactored `Geolocator` control to use `@ft.control` dataclass-style definition and switched to `Service` control type

#### Breaking Changes

- `Geolocator` must now be added to `Page.services` instead of `Page.overlay`.
- `Geolocator` method `get_current_position_async` parameters changed: 
    - removed `accuracy`
    - `location_settings` renamed to `configuration` (type changed)
    - `wait_timeout` renamed to `timeout`
- In all `Geolocator` methods, parameter `wait_timeout` renamed to `timeout`.
- Removed sync methods from `Geolocator`: 
    - `get_current_position` → use `get_current_position_async` instead
    - `get_last_known_position` → use `get_last_known_position_async` instead
    - `get_permission_status` → use `get_permission_status_async` instead
    - `request_permission` → use `request_permission_async` instead
    - `is_location_service_enabled` → use `is_location_service_enabled_async` instead
    - `open_app_settings` → use `open_app_settings_async` instead
    - `open_location_settings` → use `open_location_settings_async` instead
- Enum `GeolocatorActivityType` renamed to `GeolocatorIosActivityType`

## [0.1.0] - 2025-01-15

Initial release.


[Unreleased]: https://github.com/flet-dev/flet-lottie/compare/0.1.0...HEAD

[0.1.0]: https://github.com/flet-dev/flet-lottie/releases/tag/0.1.0