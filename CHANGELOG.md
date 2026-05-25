## [1.7.3](https://github.com/mitabi/InAir/compare/v1.7.2...v1.7.3) (2026-05-25)


### Bug Fixes

* synchronize package and integration versioning after the `InAir` rebranding changes
* rename the Home Assistant integration package directory from `inpost_air` to `inair`
* align the integration domain, tests, CI paths, and release metadata with the new `inair` package name

## [1.7.2](https://github.com/mitabi/InAir/compare/v1.7.1...v1.7.2) (2026-05-25)


### Features

* migrate repository links and release metadata to the new `mitabi/InAir` location
* rename the integration branding from `InPost Air` to `InAir`


### Bug Fixes

* restore automatic release archive generation in the release workflow
* refresh `uv.lock` to match locked CI dependency resolution
* fix YAML indentation in `.github/workflows/release.yaml`
* update setup and documentation strings to use the new `InAir` name consistently

## [1.7.1](https://github.com/mitabi/InAir/compare/v1.7.0...v1.7.1) (2026-05-25)


### Bug Fixes

* add readable diagnostics when parcel locker id resolution fails
* fix `pm25_norm` availability check to rely on PM2.5 data
* add ShipX `air_index_level` fallback for AQI sensors when recorder history is unavailable

# [1.7.0](https://github.com/mitabi/InAir/compare/v1.6.2...v1.7.0) (2025-11-29)


### Features

* allow to add parcel which is not available on default endpoint ([#95](https://github.com/mitabi/InAir/issues/95)) ([0720bb4](https://github.com/mitabi/InAir/commit/0720bb47da37fd7944c5c5ed1d35b12ea2d65196))

## [1.6.2](https://github.com/mitabi/InAir/compare/v1.6.1...v1.6.2) (2025-11-23)


### Bug Fixes

* Add setup to Trivy workflow ([9416961](https://github.com/mitabi/InAir/commit/94169613b9e35437996d0a3f127dc43b185cfe4d))
* Change Dependabot directory for devcontainers ([17213e2](https://github.com/mitabi/InAir/commit/17213e2c578b99aca68d33fae86e8c72f1961cf2))
* improve missing air quality data handling and entry setup ([#92](https://github.com/mitabi/InAir/issues/92)) ([ad25568](https://github.com/mitabi/InAir/commit/ad25568d88218c340cc08362580cf88f0383c644)), closes [#90](https://github.com/mitabi/InAir/issues/90)
* Update dependabot configuration directories ([e08b9eb](https://github.com/mitabi/InAir/commit/e08b9ebfd54117eb08fd1bcd9f21a4d4dc079ebc))

## [1.6.1](https://github.com/mitabi/InAir/compare/v1.6.0...v1.6.1) (2025-09-14)


### Bug Fixes

* data serialization from inpost ([#70](https://github.com/mitabi/InAir/issues/70)) ([dc93094](https://github.com/mitabi/InAir/commit/dc9309438521aa5f7ab63157b809a609f8550347))

# [1.6.0](https://github.com/mitabi/InAir/compare/v1.5.0...v1.6.0) (2025-09-13)


### Bug Fixes

* greencity.pl deprecated, switch to inpost.pl ([#68](https://github.com/mitabi/InAir/issues/68)) ([46f44ef](https://github.com/mitabi/InAir/commit/46f44ef5cff7ca5bd8b6ff75561b0b4f56f8a69e))


### Features

* add `configuration_url` for each device ([#51](https://github.com/mitabi/InAir/issues/51)) ([6c8931e](https://github.com/mitabi/InAir/commit/6c8931ec23abe825fc2b3e508aaedee60dee64ee)), closes [#50](https://github.com/mitabi/InAir/issues/50)
* added SensorStateClass.MEASUREMENT to applicable entities ([#43](https://github.com/mitabi/InAir/issues/43)) ([8166695](https://github.com/mitabi/InAir/commit/816669599df59bba0dc891a5e9d2c5a0fa740e5f))

# [1.5.0](https://github.com/mitabi/InAir/compare/v1.4.0...v1.5.0) (2025-03-03)


### Bug Fixes

* fix creation of url to find parcel locker id (fix [#12](https://github.com/mitabi/InAir/issues/12)) ([#13](https://github.com/mitabi/InAir/issues/13)) ([eb3f6d1](https://github.com/mitabi/InAir/commit/eb3f6d1cd8c9841f019082e0d9ab18278ee5c13f))


### Features

* store runtime data inside the config entry, improve typings ([#10](https://github.com/mitabi/InAir/issues/10)) ([1e4db35](https://github.com/mitabi/InAir/commit/1e4db3568bbb6b2ba68967c3292afff7cd253bfb))

# [1.4.0](https://github.com/mitabi/InAir/compare/v1.3.2...v1.4.0) (2024-05-07)


### Features

* add air quality index sensors ([f16ca43](https://github.com/mitabi/InAir/commit/f16ca43f2e5001aa8ee88c4b78f03c5c61f549cf))

## [1.3.2](https://github.com/mitabi/InAir/compare/v1.3.1...v1.3.2) (2024-03-07)


### Bug Fixes

* improve parcel locker id finding ([ae2a5ac](https://github.com/mitabi/InAir/commit/ae2a5aca25fe3c9e35cecfc2873144a5161b88cf)), closes [#6](https://github.com/mitabi/InAir/issues/6)

## [1.3.1](https://github.com/mitabi/InAir/compare/v1.3.0...v1.3.1) (2024-02-08)


### Bug Fixes

* fix parcel locker validation ([139a751](https://github.com/mitabi/InAir/commit/139a7511244cce1372e000735c8077a4f20d735b))

# [1.3.0](https://github.com/mitabi/InAir/compare/v1.2.0...v1.3.0) (2024-02-08)


### Features

* sort parcel lockers by distance in config flow ([fbe5f1e](https://github.com/mitabi/InAir/commit/fbe5f1e4864384ba32012141e651d4ece5277654))

# [1.2.0](https://github.com/mitabi/InAir/compare/v1.1.1...v1.2.0) (2024-02-04)


### Bug Fixes

* improve creation of release archive ([8a13958](https://github.com/mitabi/InAir/commit/8a13958bf17b76a6e9949f9a6187dc8004ace13e))


### Features

* improve config flow user input handling ([10add37](https://github.com/mitabi/InAir/commit/10add37690184e9a3d111bfc4d543968b8434d7b))

## [1.1.1](https://github.com/mitabi/InAir/compare/v1.1.0...v1.1.1) (2024-02-03)


### Bug Fixes

* handle parcel lockers without air quality data ([#3](https://github.com/mitabi/InAir/issues/3)) ([295e214](https://github.com/mitabi/InAir/commit/295e214acdcbd7e35b9c585b729a8a8d63765836))

# [1.1.0](https://github.com/mitabi/InAir/compare/v1.0.1...v1.1.0) (2024-02-03)


### Features

* hide unavailable entities ([#2](https://github.com/mitabi/InAir/issues/2)) ([d162e7a](https://github.com/mitabi/InAir/commit/d162e7aec2d6aa88d6e401132dea409bb27626db))

## [1.0.1](https://github.com/mitabi/InAir/compare/v1.0.0...v1.0.1) (2024-02-01)


### Bug Fixes

* update release action ([0b074e9](https://github.com/mitabi/InAir/commit/0b074e99c00e666de987ec24a7a3432b42f6a512))

# 1.0.0 (2024-02-01)


### Features

* update hacs.json ([e784051](https://github.com/mitabi/InAir/commit/e7840515f1ad915fe017f3b98eec6c50a359adae))
* update manifest ([033fb90](https://github.com/mitabi/InAir/commit/033fb9075096972f20ca34b572d9171ca0412a22))
