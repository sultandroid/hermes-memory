# Telegram Polling Conflict — Deep Diagnostic Tree

When the gateway log shows `Telegram polling conflict (1/5) ... Conflict: terminated by other getUpdates request`, the bot token is locked because **two things are calling `getUpdates` on the same token**. Telegram allows only one long-poller per token at a time. The lock persists for ~20-50 seconds after the last call.

## Step 1 — Confirm the server is the only suspect

```bash
# All Hermes processes on this server
pgrep -af "venv/bin/hermes"
# Output: pid 12345 /opt/.../hermes --profile myprofile gateway run

# Live HTTPS connections from Hermes to Telegram anycast
ss -tnp state established | grep -E "api.telegram|2001:67c:4e8" | grep hermes
# Expect 1-3 entries; if 0 the gateway is in backoff
```

If you see exactly one process and it has 1-3 live connections, the gateway IS connected — look at the log to see if the conflict is in the past (scrolled out of view) or recent.

## Step 2 — Test the token directly

```bash
TOKEN=...your token...
# This is destructive — it WILL trigger a polling lock for ~30s.
# Do NOT use this for diagnostics unless the gateway is already in conflict.
curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?timeout=0"
```

If the response is `{"ok":true,"result":[]}` → no other poller is active. The lock was just released. Wait 20s and check the gateway log.

If the response is `{"ok":false,"error_code":409,"description":"Conflict..."}` → someone else has the session right now. Find them.

```bash
# Check if a webhook is set (webhook overrides polling)
curl -s "https://api.telegram.org/bot${TOKEN}/getWebhookInfo"
# If "url" is non-empty, that's the poller
```

## Step 3 — Find the other instance

### Same server
```bash
pgrep -af "venv/bin/hermes"
pgrep -af "hermes" | grep -v grep
```

### Other servers / the user's laptop
The user can:
- macOS: `pgrep -af hermes` in their terminal
- Check the workstation's `~/.hermes/state.db` `gateway_state.json` for last-polled timestamp
- Check `journalctl --user -u hermes-gateway` if they run the gateway as a service

### Cloud platform
The conflict could come from a deploy preview, a CI test, or a teammate's Hermes instance. The token is shared knowledge.

## Step 4 — The 20s retry deadlock

The gateway retries every 20s. Telegram's session lock holds for 20-50s after the LAST call. If the gateway retries faster than the lock clears, the lock never gets a chance to expire.

**Trigger**: this happens when a previous process died mid-poll (kill -9, OOM, network drop) — Telegram's lock is still held by the previous process's now-dead connection, and the new process's 20s retries never let the lock clear.

**Fix**: pause the gateway for 60s:

```bash
# 1. Stop the gateway
systemctl stop hermes-gw.service

# 2. Verify no live connections
sleep 3
ss -tnp state established | grep hermes  # should be empty

# 3. Wait 60s (Telegram lock timeout)
sleep 60

# 4. Start again
systemctl start hermes-gw.service

# 5. Watch the log
tail -f /var/log/hermes/gateway.err.log | grep -E "Telegram|polling|started"
```

## Step 5 — Webhook fallback

If you cannot find the other poller and the lock won't clear, switch the gateway to webhook mode:

```bash
# Set a webhook URL (must be HTTPS and reachable from Telegram)
curl -s "https://api.telegram.org/bot${TOKEN}/setWebhook?url=https://your.domain/webhook"

# Then configure the gateway to use webhook mode
hermes config set telegram.webhook_url https://your.domain/webhook
```

This bypasses the polling lock entirely. Requires an HTTPS endpoint exposed to the internet.

## Step 6 — Token rotation

If all else fails, ask the user to:
1. Message @BotFather → `/revoke` to invalidate the current token
2. Get the new token from @BotFather
3. Update the profile `.env` on the server
4. Restart the gateway

This is the nuclear option — anyone else using the old token will need to update too.

## Detection patterns summary

| Pattern in log | Meaning |
|----------------|---------|
| `Discovering Telegram API fallback IPs via DNS-over-HTTPS` then `Connecting to Telegram (attempt 1/8)` then `polling conflict (1/5)` | New poll attempt; previous lock not yet cleared |
| Same sequence repeating with `Waiting 20s` | In backoff loop; the lock isn't releasing because the gateway keeps re-claiming |
| Live HTTPS connection count = 0 | Gateway gave up polling, in long backoff |
| `connected` or `started` line | Gateway successfully connected; if you see this the conflict was transient |
