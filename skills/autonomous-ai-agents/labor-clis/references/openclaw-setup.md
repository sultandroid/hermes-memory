# OpenClaw Setup & Hermes Migration Guide

## Installation

```bash
brew install openclaw-cli
# Binary: /opt/homebrew/bin/openclaw (not `claw`)
```

## Setup Flow

```bash
openclaw setup                                  # baseline config + workspace + sessions
openclaw setup --wizard                         # interactive onboarding (models, gateway, channels)
# OR
openclaw onboard                                # guided walkthrough
openclaw gateway run --force                    # start gateway
openclaw status                                 # verify reachability
openclaw doctor --fix                           # repair common issues
```

## Known Pitfalls

### 1. Telegram Bot Token Capture Bug

The `setup --wizard` (and `onboard`) prompts for a Telegram bot token. If you paste the full message from BotFather (welcome text + token), **the whole message gets stored as the token** instead of just the token string.

**Fix:**
```bash
openclaw config set channels.telegram.botToken <actual_token>
# Restart gateway to apply
```

### 2. Pairing Approval Auto-Sets Command Owner

When you approve a pairing code:
```bash
openclaw pairing approve telegram <CODE>
```
This **also sets** `commands.ownerAllowFrom` to the sender's ID — no separate config step needed.

### 3. Hermes → OpenClaw Migration

```bash
openclaw migrate list                 # shows available providers
openclaw migrate hermes --dry-run     # preview
openclaw migrate hermes --yes         # apply (may encounter errors)
```

**Known error:** Config validation failure on `models.providers.opencode-go.baseUrl` being empty causes a **cascading failure** — the migration skips ALL file operations (skills, memory, secrets, SOUL.md) even though they have nothing to do with the config error.

**Workaround when migration fails:**
```bash
# 1. Fix the config validation error
openclaw config set models.providers.opencode-go.baseUrl "https://api.opencode-go.com/v1"

# 2. Manually copy skills and memory
mkdir -p ~/.openclaw/workspace/skills
cp ~/.hermes/memories/MEMORY.md ~/.openclaw/workspace/MEMORY.md
cp ~/.hermes/memories/USER.md ~/.openclaw/workspace/USER.md
cp ~/.hermes/SOUL.md ~/.openclaw/workspace/SOUL.md
cp -r ~/.hermes/skills/<skill-name> ~/.openclaw/workspace/skills/

# 3. Restart gateway to pick up changes
openclaw gateway run --force
```

**Alternatively**, fix the baseUrl first, then re-run the migration:
```bash
openclaw config set models.providers.opencode-go.baseUrl "https://api.opencode-go.com/v1"
openclaw migrate hermes --yes --include-secrets --overwrite
```

### 4. Gateway Lifecycle

```bash
# Start (background — runs as daemon, never exits)
openclaw gateway run --force

# Kill (when replacing or restarting)
pkill -f "openclaw.*gateway"

# Install as LaunchAgent (background service)
openclaw gateway install

# Check health
openclaw health
openclaw status
```

## Key Paths

| Item | Path |
|------|------|
| Config | `~/.openclaw/openclaw.json` |
| Workspace | `~/.openclaw/workspace/` |
| Skills | `~/.openclaw/workspace/skills/` |
| Sessions | `~/.openclaw/agents/main/sessions/` |
| Gateway log | `openclaw logs --follow` |
| Dashboard | `http://127.0.0.1:18789/` |
