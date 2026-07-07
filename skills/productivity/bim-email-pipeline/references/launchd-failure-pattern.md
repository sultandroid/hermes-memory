# launchd Failure Pattern — read_outlook.py

The local `~/Documents/04_Outlook_Connection/scripts/launchd_err.log` records repeated
failures of a separate launchd job attempting to run `read_outlook.py`. This error
log has **two distinct phases** as the file availability changed:

## Phase 1: File Not Found (Jun 5 → early Jun 6)

```
/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/mohamedessa/Documents/04_Outlook_Connection/scripts/read_outlook.py': [Errno 2] No such file or directory
```

~25 consecutive failures. The script `read_outlook.py` only existed in the OneDrive-backed `Documents - Mohamed's MacBook Pro/` folder, not at the local `~/Documents/04_Outlook_Connection/scripts/` path.

## Phase 2: File Exists, Runtime Crash (late Jun 6 → current)

### Specific Error: SQLite PermissionError

The crash is NOT an AppleScript call — it is a **macOS TCC sandboxing denial** on the Outlook SQLite database:

```
Traceback (most recent call last):
  File ".../read_outlook.py", line 104, in main
    snap = snapshot_db()
  File ".../read_outlook.py", line 60, in snapshot_db
    shutil.copy2(src, dst + suffix)
PermissionError: [Errno 1] Operation not permitted:
'/Users/.../Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite'
```

The `launchd_out.log` shows `[]` because `snapshot_db()` wraps the error and
the empty list is the `except` fallback in `main()`.

**Root cause:** The `launchd` context and this Hermes terminal session lack **Full Disk Access**
(aka `kTCCServiceSystemPolicyAllFiles` entitlement). The Outlook Group Container
(`UBF8T346G9.Office`) is sandboxed and only applications granted Full Disk Access
in **System Settings → Privacy & Security → Files & Folders** can read it.

**As of Jun 7, 2026:** 57 total error lines (25x Phase 1 file-not-found + 32x Phase 2
PermissionError). Launchd accumulates ~12 failures/day. The `.outlook_watch_state.json`
still shows `last_id: 34923` from a prior successful run — this value is now **stale**.

## What This Means for the Pipeline

This is a **separate launchd job** from the Hermes cron pipeline. It does not affect
the email attachment watchdog or the bim-email-pipeline cron job. The error is benign
but indicates there's an orphaned launchd plist pointing to the wrong path, and even
after fixing the path the script has a runtime bug.

## Finding the Launchd Plist

If needed, search for the offending plist:
```bash
launchctl list | grep -i outlook
find ~/Library/LaunchAgents -name "*outlook*" -o -name "*read_outlook*"
```

## Resolution

Either:
1. Fix `read_outlook.py` line 104 (`main()`) — likely an AppleScript call that fails silently or a data access path that returns incomplete results, then crashes when processing the partial output.
2. Disable the launchd job if `read_outlook.py` is superseded by `download_mails.py`.
3. Copy from the OneDrive path if the local copy is stale again:
```bash
brctl download "/path/to/iCloud/04_Outlook_Connection/scripts/read_outlook.py"
cp ".../read_outlook.py" ~/Documents/04_Outlook_Connection/scripts/read_outlook.py
```
