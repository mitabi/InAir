from abc import abstractmethod
from datetime import timedelta
import logging
from typing import TYPE_CHECKING

from homeassistant.components import recorder
from homeassistant.components.recorder import history
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers import device_registry, entity_registry
from homeassistant.util import dt as dt_util

from custom_components.inair import utils
from custom_components.inair.coordinator import AIR_INDEX_LEVEL_KEY
from custom_components.inair.models import ParcelLocker
from custom_components.inair.const import DOMAIN, Entities

if TYPE_CHECKING:
    from custom_components.inair.api import InPostApi

_LOGGER = logging.getLogger(__name__)


class AirQualityIndexSensor(SensorEntity):
    """
    Represents a sensor for measuring air quality index.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        parcel_locker: ParcelLocker,
        coordinator=None,
    ) -> None:
        self._attr_device_info = utils.get_device_info(parcel_locker)
        self._attr_icon = "mdi:air-filter"
        self._coordinator = coordinator
        self._locker_code = parcel_locker.locker_code

    @property
    def _api_client(self) -> "InPostApi | None":
        return getattr(self._coordinator, "api_client", None)

    @abstractmethod
    async def async_update(self) -> None:
        """
        Update sensor's state
        """

    def get_last_n_hours_data(self, entity_id, n: int):
        """
        Retrieve the last n hours of data for a given entity.
        """
        raw_states = history.state_changes_during_period(
            hass=self.hass,
            start_time=dt_util.utcnow() - timedelta(hours=n),
            end_time=dt_util.utcnow(),
            entity_id=entity_id,
        ).get(entity_id, [])

        return [
            float(item.state) for item in raw_states if utils.can_be_float(item.state)
        ]

    async def get_sensors_data(
        self, sensors: list[tuple[Entities, int]]
    ) -> list[tuple[Entities, list[float]]]:
        """
        Retrieves data from sensors for the specified time period.
        """
        identifiers = (
            self.device_info.get("identifiers") if self.device_info is not None else None
        )
        connections = (
            self.device_info.get("connections") if self.device_info is not None else None
        )
        registry = device_registry.async_get(self.hass)
        identifier = next(iter(identifiers), None) if identifiers else None
        get_device_by_identifier = getattr(
            registry, "async_get_device_by_identifier", None
        )
        get_device_by_connection = getattr(
            registry, "async_get_device_by_connection", None
        )
        get_devices = getattr(registry, "async_get_devices", None)
        device = None
        if any(
            method is not None
            for method in (
                get_device_by_identifier,
                get_device_by_connection,
                get_devices,
            )
        ):
            # New registry lookups are scoped to a config entry.
            for entry in self.hass.config_entries.async_entries(DOMAIN):
                if identifier is not None and get_device_by_identifier is not None:
                    device = get_device_by_identifier(identifier, entry.entry_id)
                if device is None and get_device_by_connection is not None:
                    for connection in connections or ():
                        if (
                            device := get_device_by_connection(
                                connection, entry.entry_id
                            )
                        ) is not None:
                            break
                if device is None and get_devices is not None and (
                    identifiers or connections
                ):
                    devices = get_devices(
                        identifiers=identifiers or None,
                        connections=connections or None,
                        config_entry_id=entry.entry_id,
                    )
                    device = devices[0] if devices else None
                if device is not None:
                    break
        else:
            # Older Home Assistant versions only have the unscoped lookup.
            device = registry.async_get_device(
                identifiers=identifiers, connections=connections
            )

        if device is None:
            return []

        entities = dict(
            map(
                lambda entity: (
                    ""
                    if entity.translation_key is None
                    else entity.translation_key.upper(),
                    entity,
                ),
                entity_registry.async_entries_for_device(
                    registry=entity_registry.async_get(self.hass), device_id=device.id
                ),
            )
        )
        available_entities = [
            (entities[entity_key], hours)
            for (entity_key, hours) in sensors
            if entity_key in entities
        ]
        values = await recorder.get_instance(self.hass).async_add_executor_job(  # type: ignore
            lambda: [
                (
                    Entities(entity.translation_key.upper()),  # type: ignore
                    self.get_last_n_hours_data(entity.entity_id, hours),
                )
                for (entity, hours) in available_entities
            ]
        )

        return values

    async def get_current_air_index_level(self) -> str | None:
        """Get air quality index level from the point data endpoint response."""
        data = getattr(self._coordinator, "data", None)
        level = data.get(AIR_INDEX_LEVEL_KEY) if isinstance(data, dict) else None
        if isinstance(level, str) and level:
            return level.upper()

        return await self.get_shipx_air_index_level()

    async def get_shipx_air_index_level(self) -> str | None:
        """Retrieve fallback air quality index level from ShipX API."""
        if self._api_client is None:
            return None

        try:
            return await self._api_client.get_shipx_air_index_level(self._locker_code)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.debug("Failed to fetch ShipX air_index_level fallback: %s", err)
            return None
