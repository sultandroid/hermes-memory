# Hermes Telegram Gateway Setup — Samaya Delivery Channel

Used for cron job delivery (Project 121 watchdog) and general messaging.

## Prerequisites
- Bot token from @BotFather on Telegram
- macOS with Hermes installed

## Setup Steps

### 1. Add bot token to ~/.hermes/.env
```bash
# Edit the .env file and set:
TELEGRAM_BOT_TOKEN=<your_bot_token>

# Optional access control:
TELEGRAM_ALLOWED_USERS=<comma-separated-user-ids>
```

### 2. Install python-telegram-bot
```bash
python3 -m pip install python-telegram-bot
```

### 3. Verify token works
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
# Returns {"ok": true, "result": {"id": ..., "is_bot": true, "username": "..."}}
```

### 4. Start the gateway
```bash
# Foreground (test):
hermes gateway run

# Background service:
hermes gateway install
hermes gateway start
hermes gateway status
```

## Current Config (Samaya)
- **Bot:** @SultanMacBook_Bot
- **Token:** in `~/.hermes/.env` as `TELEGRAM_BOT_TOKEN`
- **Cron delivery:** Project 121 (Zamzam) watchdog delivers to Telegram
- **Gateway status:** Ready to start

## Troubleshooting
- Gateway logs: `grep -i "telegram\|error" ~/.hermes/logs/gateway.log | tail -20`
- Token issues: verify with `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"`
- Package missing: `python3 -m pip install python-telegram-bot`
- Gateway crash loop: `systemctl --user reset-failed hermes-gateway`
