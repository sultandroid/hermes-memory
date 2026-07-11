# Cron 24h Email Scan Pattern

Trigger: Scheduled cron job checking for project-critical emails in last 24 hours.

## Key Constraints

- **No TCC SQLite access** — `sqlite3` returns "authorization denied". Use AppleScript Outlook object model only.
- **iCloud EDEADLK on register files** — `~/Documents/` files (iCloud-synced) return `OSError: [Errno 11] Resource deadlock avoided` on direct read/write. Wrap all file I/O in `osascript -e 'do shell script "python3 /tmp/script.py 2>&1"' 2>&1` — the AppleScript bridge bypasses the iCloud lock. See `references/icloud-edeadlk-workaround.md`.
- **`every folder` fails** — must target `inbox` directly. Use `folder "Name" of inbox` for project sub-folders. Standalone `folder "Name"` or `mail folder "Name"` both fail with error -1728.
- **Multiple Inbox folders exist** — `mail folder "Inbox"` or `mail folder id 1` may return the wrong (empty) Inbox. Use `get id of every mail folder whose name is "Inbox"` to discover all Inbox IDs, then check `unread count` to find the active one.
- **AppleScript `.applescript` files have a ~700-byte script body limit.** Scripts longer than ~700 bytes of AppleScript code cause `Expected variable name or property but found class name (-2741)`. Break into multiple small files (one per folder) and call `osascript` separately for each.
- **No user present** — must be fully autonomous with no clarification.
- **SILENT protocol** — if nothing new, output `[SILENT]` only.
- **Large Inbox timeout trap:** Scanning ALL messages in a 9,000+ Inbox for Aconex/WTRAN patterns times out at 120s. Aconex notifications are scattered across the full Inbox, not clustered at the end — scanning only the last 200 messages will miss them entirely. **Solution:** Use the 24h time-window filter (check `now - time received <= 86400`) to limit the scan to recent messages regardless of position, or scan the full Inbox in batches of 500 using `items (n-499) thru n of msgs` with separate `osascript` calls per batch.

## AppleScript Pattern

Include emails matching ANY of:
- Sender: Aconex Notification, Mimon Allitou, Hesham Abdelhameed, Mohammad Elbaz, Abdrabo Shahin
- Subject: Transmittal, RFI, SI-, TQ-, NCR, Code A/B/C/D, Submittal, MAR, IR-, VO
- Folder: Asher Regional Museum, Zamzam Projects, RCRC Exhibition

Silently skip ops/logistics: car requests, shipments, housing, technician transport, promotions.

## Report Format

Use emoji status column:
- 🆕 NEW — not previously reported, needs attention
- ⚠️ ACTION — requires immediate action (WeTransfer links, RFI responses due, CG Code C/D)
- ℹ️ INFO — admin/backlog, no action needed

Keep one line per item unless critical action needed. Translate Arabic subjects to English.

## Key Sender Verification

After scanning, explicitly state which key senders were NOT seen (e.g., "❌ Mimon Allitou — no emails"). This proves the scan ran and the absence was detected, not missed.

## Aconex Transmittal Register Update Pattern

When the cron task is to update a submittal register from Aconex emails:

1. **Query the project folder** (not Inbox) — Aconex notifications are filed in the project sub-folder (e.g., "Asher Regional Museum"). Use `folder "Name" of inbox` to target it directly. This is faster than scanning the full Inbox and avoids the 120s timeout trap.

2. **Extract transmittal numbers** from subject lines — pattern `{Prefix}-WTRAN-{Number}`. Prefixes: `CGP-WTRAN` = CG→Samaya, `SIC.-WTRAN` = Samaya→CG.

3. **Read the existing register** — use `osascript -e 'do shell script "python3 /tmp/script.py 2>&1"'` to bypass iCloud EDEADLK on `~/Documents/` files.

4. **Compare by transmittal number** — check if each WTRAN number already appears in the register content string. Only add rows for numbers NOT found.

5. **Insert new rows** — append to the appropriate table section (CG→Samaya, Samaya→CG, or Other). Use Python string replacement to insert after the last existing row in that table.

6. **Update frontmatter** — bump `last_updated` date and append a scan note to the `source` line.

7. **Verify** — re-read the file and confirm new transmittal numbers are present, old ones unchanged.

### Pitfall: iCloud EDEADLK on verification

After writing, re-reading the same file for verification also hits EDEADLK. Use the same `osascript` bridge for verification, or rely on the write tool's success return and skip re-read verification.
