# Keto AI Smark Skimmer Home Assistant Integration

This is a Home Assistant integration for the Keto AI Smart Skimmer product.

## Usage

## Development

Testing:

```
WEBHOOK=$(cat config/.storage/core.config_entries | jq '.data.entries[] | select(.domain | contains("ketoai")) | .data.webhook_id')
curl -iX POST http://localhost:8123/api/webhook/$WEBHOOK -H 'Content-Type: application/json' -d '{"ph":"7.5","sanitizer":"500"}'
