# Sending a Message to the User's Telegram from a CLI Session

When the user says "ابعتهالي علي تليجرام" (send it to me on Telegram) from a CLI session, you can send directly via the bot API. This is distinct from group coordination — it's a one-way send to the user's DM.

## 1. Get the bot token

```bash
TOKEN=$(grep -E "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2- | tr -d '"' | tr -d "'")
```

## 2. Find the correct chat ID

The `home_channel` in config.yaml may NOT be reachable by the bot directly (returns "chat not found"). The reliable source is the session store:

```bash
sqlite3 ~/.hermes/state.db "SELECT DISTINCT source, chat_id FROM sessions WHERE source='telegram';"
```

This returns the real chat IDs the bot has interacted with. Test each with a probe before sending the real message:

```bash
for CHAT in <id1> <id2>; do
  curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT}" --data-urlencode "text=test" \
    | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('ok'), r.get('description'))"
done
```

- A **positive** chat ID (e.g. `5832026231`) = a DM with the user.
- A **negative** ID starting `-100` = a supergroup.
- Respect the user's standing rule: **stay silent in the group; send technical items to the DM** unless told otherwise.

## 3. Send the message

Use **curl**, not Python urllib. The system Python on macOS raises `SSLCertVerificationError: certificate verify failed: self-signed certificate in certificate chain` on `urllib.request.urlopen` to api.telegram.org. curl works fine.

```bash
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT}" \
  --data-urlencode "text=${MSG}" \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print('ok:', r.get('ok'), '| msg_id:', r.get('result',{}).get('message_id'), '| err:', r.get('description'))"
```

`ok: True` + a `message_id` confirms delivery. `ok: False` with `description` tells you the failure (e.g. "chat not found" = wrong chat ID).

## Pitfalls

- **`getUpdates` returns empty** when the gateway is running — it consumes updates via long polling, so you can't discover chat IDs that way. Use the state.db query instead.
- **Python urllib SSL fails** on this Mac — always use curl for the Telegram API.
- **`home_channel` may be stale** — the config value can point to a chat the bot can't reach. Verify against state.db.
- **Multi-line messages**: use a heredoc (`MSG=$(cat <<'EOF' ... EOF)`) to preserve line breaks, then `--data-urlencode "text=${MSG}"`.
