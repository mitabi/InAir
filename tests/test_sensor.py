"""Sensor tests."""

from unittest.mock import AsyncMock

import pytest

from custom_components.inpost_air.const import Entities
from custom_components.inpost_air.coordinator import ValueWithNorm
from custom_components.inpost_air.models import ParcelLocker
from custom_components.inpost_air.sensor import PARCEL_LOCKER_SENSORS
from custom_components.inpost_air.sensors.aqi.european import (
    EuropeanAirQualityIndexSensor,
)
from custom_components.inpost_air.sensors.aqi.polish import PolishAirQualityIndexSensor


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
