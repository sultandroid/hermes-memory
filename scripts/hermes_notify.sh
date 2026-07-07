#!/bin/bash
# hermes_notify.sh — send Telegram notifications from Hermes scripts
# Usage: hermes_notify.sh telegram "message text"

PLATFORM="$1"
shift
MESSAGE="$*"

if [ "$PLATFORM" = "telegram" ]; then
    # Use Hermes send_message via a Python helper
    /usr/bin/python3 - "$MESSAGE" <<'PYEOF'
import sys, json, os, subprocess

msg = sys.stdin.read().strip()
if not msg:
    sys.exit(0)

# Use Hermes curl-based notification to Telegram
# Read the bot token and chat ID from Hermes config if available
token_file = os.path.expanduser("~/.hermes/config/telegram_token")
chat_file   = os.path.expanduser("~/.hermes/config/telegram_chat_id")

token = ""
chat_id = ""

if os.path.exists(token_file):
    with open(token_file) as f:
        token = f.read().strip()
if os.path.exists(chat_file):
    with open(chat_file) as f:
        chat_id = f.read().strip()

if not token or not chat_id:
    # Fallback: write to log
    log = os.path.expanduser("~/.hermes/scripts/.notify_log.txt")
    with open(log, "a") as f:
        from datetime import datetime as dt
        f.write(f"[{dt.now()}] {msg}\n")
    print("Telegram notify: no token/chat_id, wrote to log")
    sys.exit(0)

url = f"https://api.telegram.org/bot{token}/sendMessage"
data = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}

try:
    import urllib.request
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Sent OK")
except Exception as e:
    print(f"Telegram error: {e}")
PYEOF
else
    echo "Unknown platform: $PLATFORM"
    exit 1
fi
