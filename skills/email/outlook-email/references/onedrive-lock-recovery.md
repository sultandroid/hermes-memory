# Outlook SQLite + OneDrive Lock Recovery

> Reference for `outlook-email`. Captures the OneDrive-side failure modes that can look like SQLite lock failures, plus the recovery path. The patterns here also apply to `risk-register-management` and any other skill that reads macOS files behind OneDrive.

## When the SQLite lock isn't a SQLite lock

The skill's main file (`outlook-email/SKILL.md`) treats long WAL checkpoints and Outlook's open DB handle as the canonical lock source. Both are real. But a second class of failure looks identical from the agent's side:

**Symptom:** `sqlite3` times out, `PRAGMA wal_checkpoint` times out, even `.backup` fails. By every metric in the skill's lock-detection section, it looks like Outlook is holding the DB.

**But:** if `lsof ~/Library/.../Outlook.sqlite` does NOT show a Microsoft Outlook PID, and the WAL file is small (<500 KB), the lock is **not** SQLite-side. It's coming from elsewhere — usually OneDrive file contention or another process that opened the file briefly.

## OneDrive-triggered "phantom" locks

When the OneDrive client is in `SYNC DISABLED` state for the parent folder (check with `brctl status`), it can hold advisory locks on files in sibling folders as part of a sync re-scan. These locks look like real file locks to other processes but appear as I/O timeouts to the agent.

**Diagnostic shortcut:**

```bash
# 1. Confirm it's NOT Outlook's lock
lsof ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite

# 2. Check OneDrive state
brctl status | grep -A1 "SYNC DISABLED"

# 3. If OneDrive shows SYNC DISABLED, the user must re-hydrate
# (right-click in Finder -> "Always keep on this device")
```

## Working with OneDrive-stored SQLite/Excel/DOCX

Same recovery as `risk-register-management/references/onedrive-locked-excel-recovery.md`:

1. Ask the user to drop the file in chat → extract to `~/.hermes/cache/`
2. Read with `read_only=True, data_only=True` (openpyxl) or directly (sqlite3)
3. Check `brctl status` for SYNC DISABLED
4. Wait + retry (max 3 times)
5. Fall back to PDF mirror via `pdftotext -layout`
6. Stage to a project reference folder

## Why this matters for email scanning

A 3h cron email scan will hit the OneDrive lock the first time OneDrive is unhealthy, then keep failing for the next 3h. Symptoms:

- Email pipeline cron runs but produces no output
- Logs show repeated `sqlite3.OperationalError: database is locked` retries
- The "fall back to AppleScript" branch also hangs

When this happens, the right move is to:

1. Pause the cron (don't keep retrying — it just wastes cron time)
2. Tell the user to re-hydrate OneDrive
3. Resume the cron manually after the user confirms

The skill's main "fall back to AppleScript immediately" advice is correct for SQLite-side locks, but premature for OneDrive-side locks — those have a different recovery path.
