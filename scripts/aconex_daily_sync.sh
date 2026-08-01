#!/usr/bin/env bash
# ============================================================
# Aconex Daily Sync — Aseer Museum
# ============================================================
# Runs Playwright headless browser to log into Aconex,
# extract mail, documents, and workflow data,
# compare with last snapshot, and report new items.
# ============================================================

export LD_LIBRARY_PATH=/tmp/aconex-libs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HUB_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SNAPSHOT_DIR="$HUB_DIR/05_Comms"
SNAPSHOT_FILE="$SNAPSHOT_DIR/aconex_snapshot_latest.json"
LOG_FILE="$SNAPSHOT_DIR/aconex_daily_sync.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Aconex Daily Sync Started" >> "$LOG_FILE"

# Run the Python extraction script
python3 "$SCRIPT_DIR/aconex_extract.py" 2>> "$LOG_FILE"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') — Aconex Daily Sync Completed Successfully" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') — Aconex Daily Sync FAILED (exit code $EXIT_CODE)" >> "$LOG_FILE"
fi
