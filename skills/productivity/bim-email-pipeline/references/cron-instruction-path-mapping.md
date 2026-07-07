# Cron Instruction → Actual Disk Path Mapping

Verified Jun 6, 2026. The user's cron/booking instructions reference paths
that don't always match actual disk layout. This reference maps each
instruction to what exists.

## Script Path Discrepancies

| User Instruction | Actual Disk Location | Status |
|-----------------|---------------------|--------|
| `~/Documents/04_Outlook_Connection/scripts/download_mails.py` | `~/Documents/04_Outlook_Connection/scripts/download_mails.py` (15658 bytes) | ✅ **Fixed Jun 6, 2026** — all 9 pipeline scripts synced from iCloud via `brctl download` + sequential `cp`. Fully functional. |
| `~/Documents/04_Outlook_Connection/read_outlook.py` | `~/Documents/04_Outlook_Connection/scripts/read_outlook.py` (8734 bytes) | ✅ **Fixed Jun 6, 2026** — synced from iCloud. |
| Real script path (iCloud) | `~/Documents/Documents - Mohamed'\''s MacBook Pro/04_Outlook_Connection/scripts/download_mails.py` | ✅ iCloud-origin — use as authoritative source when local copy is stale. Executable via `python3` even when cloud-locked. |

**Fix for 0-byte stubs (historical — applied Jun 6):**
```bash
# Force iCloud hydration + sequential cp to local path
for f in download_mails.py fast_organize.py project_organize.py read_outlook.py \
         generate_summary.py summarize_attachments.py outlook_local_connect.py \
         _copy_attachments.sh _copy_supplement.sh; do
  brctl download "/path/to/iCloud/scripts/$f"
  sleep 3
  cp "/path/to/iCloud/scripts/$f" "~/Documents/04_Outlook_Connection/scripts/$f"
done
```

**Prevention:** Always run iCloud-sourced scripts via `python3 <onedrive-path>` instead of copying locally. If cp is needed, use `brctl download` first to hydrate the file, wait 3s, then cp. Never cp from a dataless origin — it produces a 0-byte stub.

## BIM Target Folder Mappings

| User Instruction (from cron) | Actual Disk Path | Status | First Verified |
|-----------------------------|-----------------|--------|----------------|
| `14_MEP_Contractor/` | `Subcontractors/12_MEP_Installation/` | ✅ Exists — different number, use `12_MEP_Installation` | 2026-06-06 |
| `99_Images/` under `Docs/00_Admin/` | `Docs/00_Admin/` — no `99_Images/` subfolder | ⚠️ Must `mkdir -p` before routing. Confirmed still absent Jun 6, 2026. Only has `SAM-TO-BIM-ORG-Structure.html`. | 2026-06-05 |
| `Zamzam Museum/Docs/03_Inspection_Requests/` | Same — 435 files, heavy activity | ✅ Exists | 2026-06-06 |
| `Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md` | `_Project_Memory/PROJECT_MEMORY.md` (not root) | ✅ Last updated Jun 6, 03:07 UTC. 51KB, 12 sections. | 2026-06-06 |
| `Aseer-Museum/Scripts/PROJECT_MEMORY.md` | `Scripts/PROJECT_MEMORY.md` | ✅ Readable fallback when OneDrive locks the canonical copy. 24KB. | 2026-06-06 |

## Additional Archive Locations

| Location | Contents | Notes |
|----------|----------|-------|
| `Bim Unit/_Unsorted_Emails/Email_Archive/` | 83 items | Separate from per-project Email_Archive folders |
| `Aseer-Museum/Email_Archive/` | 0 items (verified Jun 6) | Not populated yet |

## Full Cron Instruction Step-by-Step Mapping (2026-06-06)

This maps the user's Outlook attachment pipeline cron instruction to actual disk reality.

| Cron Step | User Instruction | Actual Disk Reality | Notes |
|-----------|-----------------|---------------------|-------|
| 1 | `~/Documents/04_Outlook_Connection/download_mails.py` | `~/Documents/04_Outlook_Connection/scripts/download_mails.py` | Script is under `scripts/` subdirectory, not root. Must update path to run. |
| 2 | Check `mails/attachments/` for new files | `mails/attachments/` exists but is empty — no subfolder structure | Expected steady state. 8 categorized project subdirs removed after weeks 20-23 routing completed. |
| 4 | Check `mails/*.md` for CG responses | No `.md` files exist in `mails/` — AppleScript pipeline never writes them | Download script exits at AppleScript account enumeration before reaching the .md write code path. |
| 4 | Update `Aseer-Museum/PROJECT_MEMORY.md` | Root-level `Aseer-Museum/PROJECT_MEMORY.md` is **0 bytes** (empty stub) | Canonical project memory is at `_Project_Memory/PROJECT_MEMORY.md` (52KB) or `Scripts/PROJECT_MEMORY.md` (24KB). Update those, not the root stub. |

**Root-level PROJECT_MEMORY.md was a 0-byte stub → now a real file (updated 2026-06-09):**  
Previous sessions (Jun 5–6, 2026) confirmed `Aseer-Museum/PROJECT_MEMORY.md` was a 0-byte stub.  
On Jun 9, the **cron step 4 explicitly says to update this file** — so it was created with content (2.2KB, CG codes, sub statuses, new subs).  

**Current state (2026-06-09):** Root-level PROJECT_MEMORY.md now has content at `Aseer-Museum/PROJECT_MEMORY.md`.  
Canonical/long-form version remains at `_Project_Memory/PROJECT_MEMORY.md` (51KB, 12 sections, more detail).  
The two are **complementary**, not competing: root = cron-run compact snapshot, `_Project_Memory/` = full project memory.

**Rule for future pipeline runs:**  
- If user's cron step says "update PROJECT_MEMORY.md at Aseer-Museum/PROJECT_MEMORY.md" → create/update the root file  
- If doing a manual deep review → prefer `_Project_Memory/PROJECT_MEMORY.md`  
- Both should be updated in parallel when practical (root for cron, canonical for full context)

**download_mails.py must be run from scripts/ subdirectory:**
```bash
# WRONG (user instruction step 1):
python3 ~/Documents/04_Outlook_Connection/download_mails.py
# CORRECT:
python3 ~/Documents/04_Outlook_Connection/scripts/download_mails.py
```

## Pipeline Output Locations — Verified Jun 6, 2026

All three pipeline output locations are **empty with no recent activity**:

| Location | State | Why |
|----------|-------|-----|
| `~/Documents/04_Outlook_Connection/mails/` | Exists (dir created Jun 5) — no `.md` files ever generated | All pipeline runs fail at AppleScript account enumeration before any `.md` write occurs. The `download_mails.py` hardcodes `mails/{week_no}.md` output but never reaches that code path. |
| `~/Documents/04_Outlook_Connection/mails/attachments/` | Exists — empty, no subfolder structure | The 8 categorized project subfolders (`aseer_museum/correspondence/`, `zamzam_nwc/drawings_designs/`, etc.) were removed after routing completed. Now just a flat empty dir. |
| `Bim Unit/Aseer-Museum/Email_Archive/` | 0 items | Email_Archive under the project itself was never populated — all archive MDs went to `~/Documents/04_Outlook_Connection/mails/` on prior working pipeline runs. |

**Combined state: completely dead pipeline.** AppleScript broken (New Outlook 16.109.1 → 0 accounts), SQLite sandboxed (macOS Group Containers), No `.md` archives in pipeline's output dir.

### Hidden Archive — ~228 Email Gap Discovered (Jun 7, 2026)

The legacy archive lives at the **iCloud path**, not the local `~/Documents/04_Outlook_Connection/mails/` dir:

```
~/Documents/Documents - Mohamed's MacBook Pro/04_Outlook_Connection/mails/
  01.md through 23.md  ← actual archives (up to 1.1 MB each)
  attachments/          ← already emptied by Jun 5 routing
  PENDING_PROJECT_MEMORY_UPDATES.md  ← already APPLIED Jun 5
  EMAIL_ROUTING_WEEKS20-23_SUMMARY.md ← 238 copied, 491 skipped
```

**Gap analysis (confirmed Jun 7, 2026):**
| Source | Latest ID | Count |
|--------|-----------|-------|
| Archived in `23.md` | **34695** | Emails processed by download_mails.py |
| SQLite watermark (`.outlook_watch_state.json`) | **34923** | Highest Record_RecordID seen by read_outlook.py |
| **Unarchived gap** | **34696–34923** | **~228 emails** never downloaded |

The `read_outlook.py` launchd watcher successfully reads the SQLite DB watermark even
when it can't copy the full DB. But `download_mails.py` can't reach these IDs because
it never gets past AppleScript account enumeration. These ~228 emails (roughly 2-3 days
of mail as of Jun 7) are **lost to the pipeline** unless a direct SQLite extraction script
with elevated permissions reads them.

**This gap is a useful diagnostic signal:** If the state file's `last_id` is much higher
than the latest archived email ID in `{week}.md`, the AppleScript pipeline is falling
behind. The gap grows by ~100 emails/day on active project days.

### Even If AppleScript Worked, download_mails.py Writes to Wrong Path

The `download_mails.py` hardcodes:
```python
ROOT_DIR = os.path.dirname(SCRIPT_DIR)        # → ~/Documents/04_Outlook_Connection
base_dir = os.path.join(ROOT_DIR, "mails")     # → ~/Documents/04_Outlook_Connection/mails/
```
But the real archive lives under `Documents - Mohamed's MacBook Pro/04_Outlook_Connection/mails/`.
The two paths are **separate filesystem trees** — Apple's iCloud Drive sync creates the
`Documents - Mohamed's MacBook Pro/` folder as the real location, while `~/Documents/`
may be a symlink or iCloud synced replica.

Even if the script ran successfully (AppleScript accounts fixed), it would write to the
**empty local `mails/` dir** while the user expects to find new archives at the iCloud path.
The script's `SCRIPT_DIR` resolution (`os.path.dirname(os.path.abspath(__file__))`) drills
to `scripts/` → `ROOT_DIR = scripts/../` = the local path.

**Fix needed in download_mails.py:** Replace `ROOT_DIR` resolution with the iCloud path, or
symlink the local `~/Documents/04_Outlook_Connection/mails/` to the iCloud origin.

## Zamzam PROJECT_MEMORY.md — Empty File (Confirmed Jun 6, 2026)

The canonical PROJECT_MEMORY.md at `Zamzam Museum/Docs/00_Project_Charter/PROJECT_MEMORY.md` exists (3815 bytes) but contains **0 lines of readable content**. The file appears to be empty or contains only whitespace/BOM. Compare with Aseer's 52KB well-maintained version at `Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md`.

**Impact:** No project memory guidance available for Zamzam. All Zamzam context must be derived from email archives, watch state files, and filesystem inspection.

## Location Method

Use `find ~/Documents -path` to locate any iCloud-locked pipeline script:
```bash
find ~/Documents -path "*/04_Outlook_Connection/scripts/*.py" -type f 2>/dev/null
```
