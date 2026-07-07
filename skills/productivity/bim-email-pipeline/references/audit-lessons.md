# BIM Email Pipeline — Audit Lessons (May 2026)

After a professional audit by Claude Code (acting as AI Skills Professional),
5 critical, 8 major, and 10 minor issues were identified and fixed. Key lessons below.

## Critical Issues Found & Fixed

### 1. State File Corruption (atomic writes)
**Problem:** `json.dump` writes in-place. A crash mid-write truncates the file,
losing all `processed_ids` history → every email gets re-processed as "new".

**Fix:** Write to `.tmp` → `os.replace(tmp, path)` = atomic on POSIX.
Also wrap `json.load` in try/except with automatic `.bak` recovery.

### 2. AppleScript Injection (removed entirely)
**Problem:** Inline AppleScript in `r'''...'''` raw strings with string interpolation
of user-supplied values (folder names, attachment names, message IDs). A `"` in
any value breaks AppleScript syntax; a crafted value could inject commands.

**Fix:** Move AppleScript to **standalone `.applescript` files** called via
`osascript file.applescript arg1 arg2`. Arguments are passed via `on run argv`
as separate command-line args — no string interpolation, no injection vector.
**Never use `osascript -e` with interpolated values.**

### 3. No Concurrency Protection (PID lock)
**Problem:** Two cron instances can overlap if a run takes longer than the interval.
Both read the same state, both process the same emails, both write duplicates.

**Fix:** PID lock file (`~/.hermes/scripts/.email_pipeline.lock`).
Check process existence via `os.kill(pid, 0)` before overwriting.
Register `atexit` cleanup.

### 4. Unbounded processed_ids List
**Problem:** `processed_ids` grows forever. After 1 year → ~18K+ entries.
O(n) membership checks slow down over time; JSON serialization grows.

**Fix:** Convert to set for O(1) lookups. Prune to `MAX_TRACKED_IDS=5000`.

### 5. Uncaught TimeoutExpired
**Problem:** `subprocess.run(timeout=120)` raises `TimeoutExpired` if osascript
hangs. No handler = crash the entire pipeline run.

**Fix:** Wrap all subprocess calls in try/except. Add retry wrapper with
exponential backoff (2s, 4s, 8s) for transient AppleScript failures.

## Major Improvements

| Issue | Fix |
|-------|-----|
| `every message of f` fetches ALL emails into memory | Indexed access: `items startIdx thru total` (via file-based script) |
| `download_attachment` does O(n) folder scan per attachment | `message id <msgId>` direct lookup |
| Hardcoded OneDrive path | `BIM_UNIT_PATH` env var with fallback |
| Log file grows unbounded | `RotatingFileHandler` (10MB × 5) |
| Dead code (`fetch_emails_by_keyword`) | Removed |
| No exit codes for cron monitoring | 0 = success, 2 = partial failure |
| Classifier regex `\bas\b` causes false positives | Tightened to upper-case context (`\bASER-\d`, `\bOC-ASER\b`) |

## AppleScript Architecture — File-Based is the Right Pattern

```
# DO: Standalone .applescript file, called as:
result = subprocess.run(["osascript", script_path, arg1, arg2], ...)

# DON'T: Inline script in Python string:
result = subprocess.run(["osascript", "-e", script_with_interpolation, "--", arg1], ...)
```

Rationale:
- No injection vector (args are clean argv items, not string-interpolated)
- Scripts are independently testable: `osascript bim_fetch_emails.applescript "Inbox" 50`
- Syntax errors caught at file-save time, not at runtime
- No escaping needed (`applescript_escape()` function deleted)

## State File Format

```json
{
  "last_run": "2026-05-28T18:07:13.827087",
  "processed_ids": ["id1", "id2", ...]
}
```

## Minimal Run Loop

```
Python script → osascript .applescript (fetch) → parse ===EMAIL=== format
  → classify project + category
  → osascript .applescript (download) for each attachment
  → copy to project subfolder
  → archive as .md
  → log register update
  → save state atomically
```

## Cron Setup (every 2h, no_agent mode)

```bash
hermes cron create \
  --name "BIM Email Pipeline" \
  --schedule "every 2h" \
  --prompt "Run the BIM Email Pipeline..." \
  --script bim_email_pipeline.py \
  --no-agent
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Another instance running" | `rm ~/.hermes/scripts/.email_pipeline.lock` |
| State corruption | `rm ~/.hermes/scripts/.email_pipeline_state.json*` |
| Outlook not responding | Ensure Microsoft Outlook app is **running** |
| Test AppleScript separately | `osascript ~/.hermes/scripts/bim_fetch_emails.applescript "Inbox" 5` |
