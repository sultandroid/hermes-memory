# Connecting a Hermes Agent Instance to a Telegram Group

> Instructions for getting another Hermes Agent (or any agent) into a shared Telegram group.
> Last updated: 2026-07-23

## Prerequisites

- A Telegram bot token (create via [@BotFather](https://t.me/botfather))
- The agent must support Telegram as a platform connector

## Steps

### 1. Create a Bot

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Choose a name and username (must end in `_bot`)
4. Save the token — you'll need it for config

### 2. Configure Hermes Agent

In `~/.hermes/config.yaml` under `platforms.telegram`:

```yaml
platforms:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN"
    allowed_chat_ids:
      - "-1001234567890"  # Group chat ID
```

### 3. Get the Group Chat ID

1. Add the bot to the group
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. The chat ID appears in the response (negative number for groups, e.g. `-1001234567890`)

### 4. Restart Hermes

The bot will join and start reading messages.

### 5. Reply Rule Configuration

To only reply when @mentioned (silent observer mode):

```yaml
telegram:
  reply_on_mention_only: true
```

Omit this setting (or set to `false`) to reply to all messages.

## For Non-Hermes Agents (Claude Code, etc.)

If you're using Claude Code CLI or another agent, you can run it via a Telegram bot wrapper that:
1. Pipes group messages to the agent's stdin
2. Returns the agent's stdout to the group

This requires a custom wrapper script — Hermes has this built in natively.
