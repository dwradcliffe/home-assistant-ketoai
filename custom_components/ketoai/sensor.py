"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    TEMP_FAHRENHEIT,
)
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, UPDATE_RECEIVED


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
):

    entities = [
        PoolSensorEntity(entry, "ph"),
        PoolSensorEntity(entry, "sanitizer"),
        PoolSensorEntity(entry, "water_level"),
        PoolSensorEntity(entry, "water_temp"),
        PoolSensorEntity(entry, "battery_level", True),
        PoolSensorEntity(entry, "rssi", True),
        PoolSensorEntity(entry, "solar_status", True),
        PoolSensorEntity(entry, "last_updated", True),
        PoolSensorEntity(entry, "pool_status"),
        PoolSensorEntity(entry, "outdoor_temp"),
        PoolSensorEntity(entry, "firmware_version", True),
    ]

    async_add_entities(entities)

class PoolSensorEntity(SensorEntity):
    """Representation of a Keto-AI Sensor."""

    def __init__(
        self,
        entry: ConfigEntry,
        attr_name: str,
        diagnostic: bool = False,
        **kwargs,
    ):
        """Initialize."""
        self.__attr_name = attr_name

        # We don't know anything about the actual device before the
        # first webhook so we just use the config entry id
        self._entry_id = entry.entry_id
        self._attr_unique_id = entry.entry_id + "-" + attr_name

        self._attr_name = {
            "ph": "pH",
            "sanitizer": "Sanitizer",
            "water_temp": "Water Temperature",
            "water_level": "Water Level",
            "battery_level": "Battery Level",
            "rssi": "Wifi Signal Strength",
            "solar_status": "Solar Status",
            "last_updated": "Last Updated",
            "pool_status": "Pool Status",
            "outdoor_temp": "Outdoor Temperature",
            "firmware_version": "Firmware Version",
        }.get(attr_name, attr_name)

        self._attr_icon = {
            "ph": "mdi:ph",
            "sanitizer": "mdi:test-tube",
            "water_level": "mdi:waves",
            "water_temp": "mdi:coolant-temperature",
            "battery_level": "mdi:battery",
            "rssi": "mdi:wifi",
            "solar_status": "mdi:solar-power",
            "last_updated": "mdi:update",
            "pool_status": "mdi:list-status",
            "outdoor_temp": "mdi:thermometer",
            "firmware_version": "mdi:chip",
        }.get(attr_name)

        self._attr_device_class = {
            "sanitizer": SensorDeviceClass.VOLTAGE,
            "water_temp": SensorDeviceClass.TEMPERATURE,
            "battery_level": SensorDeviceClass.BATTERY,
            "rssi": SensorDeviceClass.SIGNAL_STRENGTH,
            "outdoor_temp": SensorDeviceClass.TEMPERATURE,
        }.get(attr_name)

        self._attr_native_unit_of_measurement = {
            "ph": CONCENTRATION_PARTS_PER_MILLION,
            "water_temp": TEMP_FAHRENHEIT,
            "battery_level": "%",
            "rssi": "dBm",
            "outdoor_temp": TEMP_FAHRENHEIT,
        }.get(attr_name)

        if diagnostic:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._entry_id)
            },
            "name": "Keto AI Smart Skimmer",
            "manufacturer": "Keto AI",
            "model": "Smart Skimmer",
            "suggested_area": "Pool",
            # "sw_version": ,
        }

    async def async_added_to_hass(self):
        """Register state update callback."""
        await super().async_added_to_hass()
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass, UPDATE_RECEIVED, self._async_receive_data
        )

    async def async_will_remove_from_hass(self):
        """Clean up after entity before removal."""
        await super().async_will_remove_from_hass()
        self._unsub_dispatcher()

    @callback
    def _async_receive_data(self, data):
        """Receive new state data for the entity."""
        if data.get(self.__attr_name) is not None:
            self._attr_native_value = data[self.__attr_name]
            self.async_write_ha_state()
