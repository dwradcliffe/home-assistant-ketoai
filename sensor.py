"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
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
      PoolSensorEntity(entry, "battery_level"),
    ]

    async_add_entities(entities)

class PoolSensorEntity(SensorEntity):
    """Representation of a Keto-AI Sensor."""

    def __init__(
        self,
        entry: ConfigEntry,
        attr_name: str,
        **kwargs,
    ):
        """Initialize."""
        self.__attr_name = attr_name

        # We don't know anything about the actual device before the
        # first webhook so we just use the config entry id
        self._attr_unique_id = entry.entry_id + "-" + attr_name

        self._attr_name = {
            "ph": "pH",
            "sanitizer": "Sanitizer",
            "water_temp": "Water Temperature",
            "water_level": "Water Level",
            "battery_level": "Battery Level",
        }.get(attr_name, attr_name)

        self._attr_icon = {
            "ph": "mdi:ph",
            "sanitizer": "mdi:test-tube",
            "water_level": "mdi:waves",
            "water_temp": "mdi:coolant-temperature",
            "battery_level": "mdi:battery",
        }.get(attr_name)

        self._attr_device_class = {
            "sanitizer": SensorDeviceClass.VOLTAGE,
            "water_temp": SensorDeviceClass.TEMPERATURE,
            "battery_level": SensorDeviceClass.BATTERY,
        }.get(attr_name)

        self._attr_native_unit_of_measurement = {
            "ph": CONCENTRATION_PARTS_PER_MILLION,
            # "sanitizer": ,
            # "water_level": ,
            "water_temp": TEMP_FAHRENHEIT,
            "battery_level": "%",
        }.get(attr_name)

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False

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
        # if data["id"] != self._attr_unique_id:
        #     return
        if data.get(self.__attr_name) is not None:
            self._attr_native_value = data[self.__attr_name]
            self.async_write_ha_state()
