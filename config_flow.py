"""Config flow for Keto AI."""
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Keto AI Webhook",
    {
        "keto_ai_url": "https://keto-ai.com/docs/webhooks",
        "docs_url": "https://www.home-assistant.io/integrations/keto-ai/",
    },
)
