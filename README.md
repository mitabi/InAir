# InAir
[![landroid_cloud](https://img.shields.io/github/v/release/mitabi/InAir.svg?include_prereleases&label=Current%20release)](https://github.com/mitabi/InAir) 
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![downloads](https://img.shields.io/github/downloads/mitabi/InAir/total?label=Total%20downloads)](https://github.com/mitabi/InAir)

This component has been created to be used with Home Assistant. 

### Installation:

#### HACS

- Ensure that HACS is installed.
- Search for and install the "InAir" integration.
- Restart Home Assistant.
- Go to Integrations and add the InAir integration

#### Manual installation

- Download the latest release.
- Unpack the release and copy the custom_components/inair directory into the custom_components directory of your Home Assistant installation.
- Restart Home Assistant.
- Go to Integrations and add the InAir integration


### Entities

This integration will set up the following entities based on the retrieved data.

Platform | Entity name | Description
-- | -- | --
`sensor` | `NO2` | NO2 concentration
`sensor` | `O3` | O3 concentration
`sensor` | `PM 1` | PM1 concentration
`sensor` | `PM 10` | PM10 concentration
`sensor` | `PM 10 norm` | PM10 concentration (normalized)
`sensor` | `PM 2.5` | PM2.5 concentration
`sensor` | `PM 2.5 norm` | PM2.5 concentration (normalized)
`sensor` | `PM 4` | PM4 concentration
`sensor` | `Pressure` | Pressure
`sensor` | `Temperature` | Temperature
`sensor` | `Humidity` | Humidity

The air quality index entities are calculated from Home Assistant recorder history. The European index uses 24-hour averages for particulate matter and 1-hour averages for NO2 and O3; the Polish index uses 1-hour averages. If historical readings are unavailable, both fall back to the air quality level from the InPost ShipX API.

Platform | Entity name | Description
-- | -- | --
`sensor` | `European Air Quality Index` | [The European Air Quality Index](https://www.eea.europa.eu/themes/air/air-quality-index).
`sensor` | `Polish Air Quality Index` | [The Polish Air Quality Index](https://powietrze.gios.gov.pl/pjp/content/health_informations) (Pol. Indeks Jakości Powietrza).

### Note

This project has been developed so far by:
- @mbober1
- @ceski23
- @mikart143



