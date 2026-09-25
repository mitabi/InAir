"""Sensor tests."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.inair.const import DOMAIN

from custom_components.inair.const import Entities
from custom_components.inair.coordinator import ValueWithNorm
from custom_components.inair.models import ParcelLocker
from custom_components.inair.sensor import PARCEL_LOCKER_SENSORS
from custom_components.inair.sensors.aqi.european import (
    EuropeanAirQualityIndexSensor,
)
from custom_components.inair.sensors.aqi.polish import PolishAirQualityIndexSensor


def test_pm25_norm_exists_fn_uses_pm25_data():
    """PM25_NORM entity should depend on PM25, not PM10."""
    description = next(
        sensor for sensor in PARCEL_LOCKER_SENSORS if sensor.key == Entities.PM2_5_Norm
    )

    data_with_pm25 = {
        Entities.PM2_5: ValueWithNorm(Entities.PM2_5, value=12.0, norm=24.0),
    }
    data_without_pm25 = {
        Entities.PM10: ValueWithNorm(Entities.PM10, value=20.0, norm=40.0),
    }

    assert description.exists_fn(data_with_pm25) is True
    assert description.exists_fn(data_without_pm25) is False


def test_pm_sensors_use_density_unit():
    """PM sensors should keep reporting in micrograms per cubic meter.

    The unit may be backed by either the legacy homeassistant.const constant
    (homeassistant < 2023.11) or the UnitOfDensity enum, depending on the
    version of Home Assistant it is imported under, so only the unit value is
    asserted rather than the exact symbol.
    """
    pm_sensor_keys = {
        Entities.PM2_5,
        Entities.PM1,
        Entities.PM10,
        Entities.PM4,
        Entities.NO2,
        Entities.O3,
    }

    units = {
        sensor.native_unit_of_measurement
        for sensor in PARCEL_LOCKER_SENSORS
        if sensor.key in pm_sensor_keys
    }

    assert units == {"μg/m³"}


@pytest.mark.parametrize(
    "sensor_cls, expected",
    [
        (EuropeanAirQualityIndexSensor, "VERY_GOOD"),
        (PolishAirQualityIndexSensor, "VERY_GOOD"),
    ],
)
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_aqi_fallback_to_shipx_air_index_level(sensor_cls, expected):
    """AQI sensors should fall back to ShipX air_index_level when no history exists."""
    api_client = AsyncMock()
    api_client.get_shipx_air_index_level = AsyncMock(return_value=expected)

    sensor = sensor_cls(ParcelLocker("AJE01BAPP", "56311"), api_client)
    sensor.get_sensors_data = AsyncMock(return_value=[])

    await sensor.async_update()

    assert sensor.native_value == expected
    api_client.get_shipx_air_index_level.assert_awaited_once_with("AJE01BAPP")


async def test_get_sensors_data_queries_device_registry():
    """Device query should use the registry's async_get_device.

    The identifiers+connections signature of async_get_device has been the
    canonical API on every Home Assistant version (2023.x through latest),
    so no version-specific branching is needed.
    """
    sensor = EuropeanAirQualityIndexSensor(ParcelLocker("AJE01BAPP", "56311"), None)
    sensor.device_info = {
        "identifiers": {(DOMAIN, "AJE01BAPP")},
        "connections": None,
    }

    registry = MagicMock()
    registry.async_get_device.return_value = None

    with patch(
        "custom_components.inair.sensors.air_quality_index.device_registry.async_get",
        return_value=registry,
    ):
        await sensor.get_sensors_data([])

    registry.async_get_device.assert_called_once_with(
        identifiers={(DOMAIN, "AJE01BAPP")}, connections=None
    )
