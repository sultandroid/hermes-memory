# Telegram Delivery Setup for Daily Todo

## Current Configuration (May 2026)

| Setting | Value | Location |
|---------|-------|----------|
| Telegram Bot Token | Set via `hermes config set telegram.bot_token <TOKEN>` | `~/.hermes/config.yaml` or env |
| Home Channel ID | `-5832026231` | `gateway.telegram.home_channel` in config.yaml |

## How the Bot Sends Messages

The `hermes-telegram` platform tool handles delivery. When configured:
- The cron job's stdout is delivered to the configured home channel
- No explicit Telegram API call needed — Hermes handles it via the platform toolset

## Verification Commands

```bash
# Check if bot token is set
echo $TELEGRAM_BOT_TOKEN

# Check telegram config
grep -A5 'telegram' ~/.hermes/config.yaml

# Test hermes-telegram platform tool
hermes tools | grep telegram
```

## If Telegram Delivery Fails

If `TELEGRAM_BOT_TOKEN` is not set, the cron run will print the TODO list to stdout but not send to Telegram. To fix:

1. Obtain a bot token from [@BotFather](https://t.me/BotFather) on Telegram
2. Run: `hermes config set telegram.bot_token 123456:ABC-DEF...`
3. Restart the Hermes gateway or cron service

## Channel ID Note

The channel ID `-5832026231` is a private channel. The bot must be added as an admin/poster to that channel first before messages can be delivered.
