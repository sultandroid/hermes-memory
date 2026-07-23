#!/bin/bash
# Check Adel Darwish's OneDrive folder for new/changed files since last sync
# Called by cron — outputs a report of what's new

ADEL_DIR="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Adel  Darwish's files - 01- Execution Documents"
SNAPSHOT_DIR="/Users/mohamedessa/aseer-museum-pm/99_Archive/adel_snapshots"
SNAPSHOT_FILE="$SNAPSHOT_DIR/file_list.txt"
TODAY=$(date '+%Y-%m-%d %H:%M')

mkdir -p "$SNAPSHOT_DIR"

# Build current file inventory (relative paths, sizes, mtimes)
find "$ADEL_DIR" -type f ! -name '.DS_Store' ! -path '*/.DS_Store' -exec stat -f '%N|%z|%Sm' {} \; 2>/dev/null | sed "s|$ADEL_DIR/||" | sort > /tmp/adel_current.txt

NEW_FILES=""

if [ -f "$SNAPSHOT_FILE" ]; then
    # Compare full lines (name|size|mtime) — catches both new AND modified files
    NEW_FILES=$(comm -23 /tmp/adel_current.txt <(sort "$SNAPSHOT_FILE") 2>/dev/null)
else
    NEW_FILES=$(cat /tmp/adel_current.txt)
fi

# Update snapshot BEFORE reporting (so next run compares against this state)
cp /tmp/adel_current.txt "$SNAPSHOT_FILE"

# Report — new/changed files only
if [ -z "$NEW_FILES" ]; then
    echo "[$TODAY] No new or changed files in Adel's folder."
    exit 0
fi

COUNT=$(echo "$NEW_FILES" | wc -l | tr -d ' ')
echo "[$TODAY] $COUNT new/changed file(s) in Adel's folder:"
echo "$NEW_FILES" | while IFS='|' read -r name size mtime; do
    echo "  + $name  ($mtime)"
done
echo ""
echo "Run: hermes -z 'Adel Darwish folder has new files — scan and update repo registers'"
