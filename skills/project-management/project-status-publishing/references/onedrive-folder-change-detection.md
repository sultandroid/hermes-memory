# OneDrive Folder Change Detection (Adel Darwish Pattern)

## When to Use

When you need to monitor a OneDrive folder for new/changed files and update repo registers. This is a **file-level change detection** pattern, distinct from the status-extraction pattern in the main skill.

## Architecture

```
OneDrive folder → snapshot comparison script → change report → agent updates registers → cron (2× daily)
```

## Snapshot Script Pattern

Create a bash script that:
1. Walks the target folder with `find` + `stat` to build a file inventory (relative path | size | mtime)
2. Compares against a stored snapshot file
3. Reports new/changed files
4. Updates the snapshot

```bash
#!/bin/bash
TARGET_DIR="/path/to/OneDrive/folder"
SNAPSHOT_DIR="/path/to/repo/99_Archive/snapshots"
SNAPSHOT_FILE="$SNAPSHOT_DIR/file_list.txt"

mkdir -p "$SNAPSHOT_DIR"

find "$TARGET_DIR" -type f ! -name '.DS_Store' -exec stat -f '%N|%z|%Sm' {} \; \
  | sed "s|$TARGET_DIR/||" | sort > /tmp/current.txt

if [ -f "$SNAPSHOT_FILE" ]; then
    NEW=$(comm -23 /tmp/current.txt <(cut -d'|' -f1 "$SNAPSHOT_FILE" | sort))
    # Also detect changed files (same name, different size/mtime)
fi

cp /tmp/current.txt "$SNAPSHOT_FILE"
```

## Cron Job Setup

| Parameter | Value |
|-----------|-------|
| `schedule` | `0 9,17 * * *` (9AM/5PM KSA) |
| `workdir` | Repo root |
| `deliver` | `telegram` (or platform of choice) |
| `prompt` | Self-contained instruction to scan folder, detect changes, update registers |

## Pitfalls

- **OneDrive lock conflicts** — `find` + `stat` is read-only and safe. Don't `mv`/`rm` OneDrive files.
- **`.DS_Store` noise** — Always exclude with `! -name '.DS_Store'`
- **First run** — No snapshot exists, so all files appear "new". The script should handle this gracefully (just create the snapshot, no report).
- **Snapshot location** — Store in `99_Archive/snapshots/` (not in git-tracked area) to avoid polluting the repo with ephemeral data.
- **Agent prompt must be self-contained** — The cron job runs in a fresh session with no context. Include the full folder path, register paths, and update instructions in the prompt.
