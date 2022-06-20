# Keto AI Smark Skimmer Home Assistant Integration

This is a Home Assistant integration for the Keto AI Smart Skimmer product.

NOTE: There is not yet official support from Keto AI for this to work.

## Usage
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/v/release/dwradcliffe/home-assistant-ketoai)](https://github.com/dwradcliffe/home-assistant-ketoai/releases)


1. Install HACS if you haven't already (see [installation guide](https://hacs.xyz/docs/setup/prerequisites)).
2. Add custom repository `https://github.com/dwradcliffe/home-assistant-ketoai` as "Integration" in the settings tab of HACS.
3. Find and install `Keto AI` integration in HACS's "Integrations" tab.
4. Restart Home Assistant.
5. Go to your integrations page and click `Add Integration` and look for `Keto AI`.
6. Make sure you copy the webhook URL and use that to setup the webook in Keto AI.


## Development

Testing:

```
WEBHOOK=$(cat config/.storage/core.config_entries | jq -r '.data.entries[] | select(.domain | contains("ketoai")) | .data.webhook_id')
curl -iX POST http://localhost:8123/api/webhook/$WEBHOOK -H 'Content-Type: application/json' -d '{"ph":"7.5","sanitizer":"500","battery_level":98,"outdoor_temp":91,"water_temp":87,"pool_status":"Ready to swim","rssi":-70,"solar_status":"ok","firmware_version":"v0.39"}'
```
