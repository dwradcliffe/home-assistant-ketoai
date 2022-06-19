"""Support for Keto AI."""
import hashlib
import hmac
import json
import logging

import voluptuous as vol

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

from .const import DOMAIN, UPDATE_RECEIVED

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Keto AI component."""
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = config[DOMAIN]
    return True


async def handle_webhook(hass, webhook_id, request):
    """Handle incoming webhook with Keto AI inbound messages."""
    body = await request.text()
    try:
        data = json.loads(body) if body else {}
    except ValueError:
        return None

    if (
        isinstance(data, dict)
    ):
        data["webhook_id"] = webhook_id
        hass.bus.async_fire(UPDATE_RECEIVED, data)
        async_dispatcher_send(hass, UPDATE_RECEIVED, data)
        return

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, SENSOR_DOMAIN)
    )

    webhook.async_register(
        hass, DOMAIN, "Keto AI", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    await hass.config_entries.async_forward_entry_unload(entry, SENSOR_DOMAIN)
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry
