# Pipeline Execution Guide

Step-by-step procedure for running the BIM email pipeline as a cron job.

## 1. Prerequisites

- `~/Documents/04_Outlook_Connection/scripts/download_mails.py` must exist (for Step 1-2)
- Microsoft Outlook must be running **if** downloading new emails (Step 1-2) — Steps 3-6 work on files already on disk regardless of Outlook state
- OneDrive must be syncing (or files will be placeholders; metadata-only ops still work)

## 2. Execution Order
### Step 1: Check Outlook

```bash
osascript -e 'tell app "System Events" to (name of processes) contains "Microsoft Outlook"'
```
If `false`, **skip email download** but **continue** with Step 3 (check for unprocessed attachment files) and Step 6 (scan email archives / PROJECT_MEMORY updates). Attachments from previous runs may still be un-filed, and archive files may have been modified by a prior crash-recovery run. The only step that needs Outlook live is Step 1 — everything else operates on files already on disk.

### Step 2: Download emails
```bash
cd ~/Documents/04_Outlook_Connection/scripts && python3 download_mails.py
```
Exit 0 = ran successfully.  
- **No stdout** means no new emails found (everything already archived).  
- **Archiving progress output** (`Archiving Week NN`, `Downloading: ...`) means new emails were found and downloaded — read the output to know what came in.  
Exit 2 = file not found at that path (check `ls`).  

**Edge case: script itself is dataless.** If the script file shows `compressed,dataless` flags (check with `ls -laO`), Python will fail to execute it even though the file exists. Recovery: `brctl download scripts/download_mails.py` (iCloud-backed) or restore from source control. If unrecoverable, report the gap and proceed — the pipeline can still report on existing attachments and update PROJECT_MEMORY.

**⚠️ New variant (confirmed 2026-06-19): Script has size, no dataless flag, still EDEADLK.** The `file` command returns `ERROR: cannot read (Resource deadlock avoided)` even though `ls -laO` shows no `compressed,dataless` flags and `stat` reports 3KB+ of actual content on disk. This occurs when iCloud File Provider holds a POSIX-level exclusive handle on a recently-written file (e.g. downloaded by Outlook). The script cannot be executed despite appearing fully materialized. Recovery: same as `com.apple.provenance` locks — only NSFileCoordinator via Swift works (see `onedrive-edeadlk-provenance.md` § "Apparent EDEADLK on non-dataless files"). Kill OneDrive does NOT resolve this variant. Detection: run `file <script>` first — if it errors but `ls -laO` shows no `dataless`, you have this variant.

**Pitfall: script times out because 8,000+ inbox messages take 3–5 min to scan.**  
The script iterates the full Inbox metadata in chunks of 100 via AppleScript. An 8,982-message inbox requires ~90 AppleScript calls at ~2–3 seconds each = 180–270 seconds just for scanning, before any email download. A 120s or 180s foreground timeout will not be enough.

**Fix: always run in background with 600s timeout.**  
```bash
python3 ~/Documents/04_Outlook_Connection/scripts/download_mails.py &
PID=$!
wait $PID 2>/dev/null
```
Or in the Hermes cron environment:
- `terminal(background=true, notify_on_complete=true, timeout=600)` — this avoids the 180s foreground cap and lets AppleScript finish.
- After wait, check process log with `process(action='log', ...)` to see the full output.
- The script prints its progress to stdout; scan for "Found N new emails" and "Archiving Week" to know if anything new arrived.

**Caveat: no stdout for background is misleading.** A background run that prints nothing may have completed with 0 new emails — or may still be running. Wait for `notify_on_complete` before reading its output. If a prior run is still alive (e.g. leftover pid), kill it first with `kill <pid>` before re-running.

**Dataless .md archives — separate timeout risk.** Even after the inbox scan succeeds, the script reads every existing `.md` archive to deduplicate Outlook IDs. If those `.md` files are OneDrive dataless placeholders (`st_blocks=0`), the script hits EDEADLK and hangs. This is a different bottleneck from inbox scanning. A timeout at this stage means the archive scan is stuck but new emails may have already been written — check for new numbered `.md` files and attachment counts in the organizer output.

**Detection:**
```bash
ls -laO scripts/download_mails.py
# If "compressed,dataless" → need brctl recovery first
file scripts/download_mails.py
# If "ERROR: cannot read" → dataless, content purged
```

### Step 3: Scan attachments directory

**Two tiers of files to scan:**

**Tier A — Root-level files** (sit directly in `attachments/`, no subfolder). These are inline images from email bodies, standalone PDFs, and unsorted downloads. Common root-level file types discovered during pipeline runs:
- Inline images: `image001.jpg`–`image012.png`, `image001.png`–`image012.png` (email body images, numbered by Outlook)
- UUID-named JPEGs: `324b9fb2-...jpg`, `bf687b48-...jpg` (inline attachments)
- `WhatsApp Image YYYY-MM-DD at HH.MM.SS.jpeg` — phone photos sent via email
- Standalone PDFs: `certificates.pdf`, `FTSM 90 (1).pdf`, `WOOD WORKS IFC.pdf`, `Technical Manual Support.pdf.crdownload (1).pdf`
- `MOC-MUS-ASE-1E0-ZD-0056 reply.pdf` (also inside `aseer_museum/correspondence/` — already filed)
- Spreadsheets: `تكاليف متاجر جبل عمر.xlsx` (also inside `makkah_jabal_omar/`)

**Root-level file routing:**
| Pattern | Destination | Notes |
|---------|------------|-------|
| `image*.jpg`, `image*.png`, `*.jpeg` | `Aseer-Museum/Docs/00_Admin/99_Images/` | Email inline images |
| `WhatsApp Image*.jpeg` | `Aseer-Museum/Docs/00_Admin/99_Images/` | Site/phone photos |
| `*.pdf` starting with `MOC-MUS-ASE`, `MOC-ASEER` | `05_Correspondence_Archive/02_Correspondence_MOC/` | Already filed in subdirs — check first |
| `certificates.pdf` | `04_Specifications_and_BOQ/02_Product_Datasheets/` | Certificates |
| `FTSM 90 (1).pdf` | `04_Specifications_and_BOQ/` | Submittal |
| `*.xlsx` with Arabic name | Check `makkah_jabal_omar/`, `haramein_ghamamah/` duplicates first |
| `*.crdownload` files | **Skip** — Chrome partial downloads, not real files |
| UUID `*.jpg` (hex-only basename) | `Aseer-Museum/Docs/00_Admin/99_Images/` | Attachment images |

Check if each root-level file already exists in its subdirectory-organized counterpart before routing. Many root files are duplicates of what's already filed under `aseer_museum/`, `zamzam_nwc/`, etc.

**Tier B — Category subdirectories** (already organized by the download script):
- `aseer_museum/` — subdirs: correspondence, drawings_designs, others, proposals_contracts, reports, schedules, site_photos, technical_specifications
- `zamzam_nwc/` — same subdir structure
- `general/` — same subdir structure (catch-all for unclassified)
- `admin_hr/` — admin/HR related
- `makkah_jabal_omar/`, `haramein_ghamamah/`, `hoarding_signage/`

**Metadata collection on locked files:** Use `stat -f` CLI flags which work on OneDrive dataless files (reads inode metadata, not content):
```bash
# Timestamp (modification time) — works even when cat/open fails
stat -f '%Sm' "path/to/file"           # → "Jun 12 14:31:41 2026"

# Size + flags
ls -laO "path/to/file"                  # → shows 'compressed,dataless' if purged

# Blocks allocated — 0 = dataless placeholder
stat -f '%b' "path/to/file"

# All of the above in one command (works under EDEADLK)
stat -f '%N: %z bytes, %Sm, blocks=%b' "path/to/file"
```

The `-f` format flags (`%Sm`, `%b`, `%z`) access the inode metadata layer that macOS resolves even when the file's content pages are purged by OneDrive/iCloud. This is faster than `os.stat()` in Python when you only need a quick timestamp for the pipeline report.

⚠️ All files may be OneDrive placeholders (st_blocks=0). Use `os.listdir` + `os.stat` for metadata — these work even when `open()` fails with EDEADLK.

### Step 4: Compare against BIM targets

#### Bulk basename comparison with `comm -23` (fast, zero OneDrive reads)

When you need to compare a list of attachment files against all BIM project files without triggering OneDrive locks, use the `find` + `awk` + `comm` pipeline. This approach reads only directory metadata (inode entries), never opens file content, so it works under all EDEADLK states:

```bash
# Step A: Collect BIM filenames from all target project folders
BIM="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"

# Combine multiple project trees into one sorted base list
find "$BIM/Aseer-Museum" "$BIM/Zamzam Museum" -type f 2>/dev/null \
  | awk -F/ '{print $NF}' \
  | tr '[:upper:]' '[:lower:]' \
  | sort -u > /tmp/bim_basenames.txt

# Step B: Collect attachment filenames — scope to ROOT only (no subdirs)
ATTACH="/Users/mohamedessa/Documents/04_Outlook_Connection/mails/attachments"
find "$ATTACH" -maxdepth 1 -type f 2>/dev/null \
  | awk -F/ '{print $NF}' \
  | tr '[:upper:]' '[:lower:]' \
  | sort > /tmp/attach_basenames.txt

# Step C: Find files in attach_basenames but NOT in bim_basenames
comm -23 /tmp/attach_basenames.txt /tmp/bim_basenames.txt > /tmp/new_basenames.txt
echo "New files (by basename): $(wc -l < /tmp/new_basenames.txt)"
cat /tmp/new_basenames.txt
```

**Advantages:**
- Works under ALL OneDrive lock states — only directory traversal, zero file opens
- `find` at per-project scope (Aseer-Museum, Zamzam Museum) bypasses the OneDrive stall that affects broad `find` on the full tree
- Completes in seconds even when sub-agent delegation times out
- The same pattern extends to per-subfolder comparison (run `comm` per target folder)

**Limitations:**
- Basename-only comparison can miss same-name files in different subfolders (handled by per-subfolder `comm` runs if needed)
- `_1` suffix duplicates pass through (filter with the `is_download_duplicate()` check below)
- Arabic Unicode normalization not applied (use the `tr '[:upper:]' '[:lower:]'` for ASCII-only match)

**Verification loop for each flagged "new" file:** To avoid false positives from `_1` duplicates or subfolder-routed files, verify each hit with a targeted `find -iname`:
```bash
for f in $(cat /tmp/new_basenames.txt); do
  found=$(find "$BIM/Aseer-Museum" "$BIM/Zamzam Museum" -iname "$f" -type f 2>/dev/null | head -1)
  if [ -n "$found" ]; then
    echo "FALSE POSITIVE (already in BIM): $f at $found"
  fi
done
```

#### Fast-path shortcut (most runs):

This is the common case on 2-hour cycles — saves OneDrive lock risk and ~20s per run.

```bash
# Quick check — are there any new attachments since last run?
LAST_LOG=~/Documents/04_Outlook_Connection/mails/pipeline_run_2026-06-12_15-33.md
NEW_FILES=$(find ~/Documents/04_Outlook_Connection/mails/attachments -type f \
  -newer "$LAST_LOG" ! -name ".DS_Store" 2>/dev/null | wc -l)
if [ "$NEW_FILES" -eq 0 ] && [ "$HAS_NEW_EMAILS" = false ]; then
  echo "Fast-path: no new files since last run — skipping BIM comparison"
  # resume at Step 6
fi
```

**⚠️ Pitfall: `find -newer` misses stale attachments downloaded before the previous pipeline run.** Observed 2026-06-13: 5 attachment files downloaded Jun 12 04:12 but never filed to BIM (the crash of an earlier download_mails run on Week 23 prevented the organizer from processing Week 24's attachments). These files predate ALL pipeline logs from Jun 12–13, so `find -newer <last_log>` returned 0 and the fast-path skipped the comparison. The files accumulated as un-filed orphans despite being on disk for 24+ hours.

**BIM tree change detection (for richer reporting):** After the comparison, run a `find -newer` against the BIM tree itself to detect what non-attachment work has been happening in the project since the last pipeline run. This adds useful context to the pipeline report:
```bash
LAST_LOG=$(ls -t ~/Documents/04_Outlook_Connection/mails/pipeline_run_*.md 2>/dev/null | head -1)
BIM_ROOT="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"
NEW_BIM_FILES=$(find "$BIM_ROOT" -type f -newer "$LAST_LOG" ! -name ".DS_Store" 2>/dev/null | head -40)
if [ -n "$NEW_BIM_FILES" ]; then
    echo "Notable: $(echo "$NEW_BIM_FILES" | wc -l | tr -d ' ') new/changed files in BIM since last run"
    echo "Categories: $(echo "$NEW_BIM_FILES" | sed 's|.*Bim Unit/||' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -5)"
fi
```
This catches Revit RFA families, project docs, and BIM model changes that aren't email-derived. Report them in the "Notable Observations" section.

**Fix: add a second gate that checks for stale attachment files older than the mails archive modification time.** If `download_mails.py` said no new emails but the attachment directory has files from before the last successful pipeline filing run, they may be orphans:

```bash
# Check for stale (pre-last-run) attachment files
COMPARE_EST=$(stat -f "%m" ~/Documents/04_Outlook_Connection/mails/pipeline_run_2026-06-13_04-30.md 2>/dev/null || echo 0)
STALE_COUNT=0
for f in ~/Documents/04_Outlook_Connection/mails/attachments/general/others/*; do
    [ -f "$f" ] || continue
    FM=$(stat -f "%m" "$f" 2>/dev/null || echo 0)
    if [ "$FM" -lt "$COMPARE_EST" ]; then
        STALE_COUNT=$((STALE_COUNT + 1))
    fi
done
if [ "$STALE_COUNT" -gt 0 ]; then
  echo "⚠️  $STALE_COUNT stale un-filed attachments (pre-date last pipeline log) — running full comparison"
  # continue to full Step 4
fi
```

This second gate catches orphaned attachments that the fast-path would otherwise skip.

If new files DO exist, cross-reference attachment filenames against these 7 BIM subfolder trees:

| Target Folder | Project | What Goes There |
|---------------|---------|-----------------|
| `Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive` | Aseer | Correspondence, submittals, NCRs, SIs |
| `Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ` | Aseer | Approved specs, BOQs |
| `Aseer-Museum/Reports & Meeting/00_Daily Reports` | Aseer | Daily progress reports |
| `Aseer-Museum/Design Files/00_Scope_and_Proposals` | Aseer | Scope docs, proposals |
| `Aseer-Museum/Subcontractors/14_MEP_Contractor` | Aseer | MEP contractor docs |
| `Aseer-Museum/Docs/00_Admin/99_Images` | Aseer | Site photos, images |
| `Zamzam Museum/Docs/03_Inspection_Requests` | Zamzam | Inspection requests |

**⚠️ Pitfall: the 7 targets above are NOT exhaustive.** Files flagged as "new" from these 7 may already exist in other BIM subdirectories not listed above, such as:
- `09_Correspondence/` and `09_Correspondence/2026-0N/` (date-sorted correspondence)
- `Email_Archive/_attachments/` and `Email_Archive/Attachments/`
- `Docs/07_Reports/`, `Docs/08_Meeting_Minutes/`, `Docs/10_Test_and_Inspection/`
- `Design Files/_DUPLICATES_REVIEW/` and `Design Files/Package_Part 2/`
- `Contracts/02_NRS_Contract/02_Proposals_and_Quotes/`
- `Subcontractors/02_Lighting_Designer/`
- `02_Submittals/` (system-generated submittal structure)

**Confirmed 2026-06-20:** All 14 files that appeared "new" from the 7-target scan were found in these other BIM subdirectories. Without this broader scan, false positives would have triggered unnecessary copies.

**Mandatory secondary verification step (after initial 7-folder scan):**
```bash
# After identifying "new" files from the 7 targets, verify each one across the ENTIRE BIM tree
BIM_ROOT="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"
for f in $(cat /tmp/flagged_new.txt); do
  found=$(find "$BIM_ROOT/Aseer-Museum" "$BIM_ROOT/Zamzam Museum" -iname "$f" -type f 2>/dev/null | head -1)
  if [ -n "$found" ]; then
    echo "FALSE POSITIVE (already in BIM at alternate subdir): $f -> $found"
    echo "Already filed in: $(echo "$found" | sed 's|.*Bim Unit/||' | sed 's|/[^/]*$||')"
  fi
done
```

**This secondary pass MUST be a hard requirement before any `cp`/`shutil.copy2` call.** Do not skip it, even when running in fast-path mode. The 7 targets are a rough first filter; the full BIM tree is the ground truth.

**⚠️ Pitfall: `find` at scale on OneDrive silently truncates results.**

Do NOT attempt comparison via `find "Bim Unit/Aseer-Museum" -type f` with `head -3000` or even without head — OneDrive dataless files cause `find` to skip locked directories and return a tiny subset (e.g. 86 files out of 6,000+). This was observed on 2026-06-12: a broad `find` across the Aseer-Museum BIM tree returned only 95 files, while individual subfolder `find` calls (targeting specific paths like `05_Correspondence_Archive/`) returned correct counts (88 files). Narrow per-subfolder `find` calls bypass the OneDrive provider lock at scale.

Validation check: if a broad BIM scan returns suspiciously few results (<500 files for Aseer-Museum which has 6000+), discard it and use per-target-folder scans instead.

**⚠️ Pitfall: `delegate_task` sub-agents can waste context on deep archive recursion.**

When delegating folder inventory for the 7 BIM target folders, some contain massive sub-archives that are irrelevant for attachment comparison:
- `05_Correspondence_Archive/14_Previous_and_Raw_Packages/` — 9,716 files
- `05_Correspondence_Archive/15_Deliverables_to_NRS/` — 1,134 files  
- `05_Correspondence_Archive/16_Incoming_Drawings_Archive/` — 2,077 files

A full recursive `find` on any of the 7 targets returns these massive sets, bloating the sub-agent's summary (50+KB for a single folder). The vast majority are old revisions, CAD assets, and archived deliverables — not relevant for cross-referencing current attachment files.

**Fix in delegation prompt:** Explicitly tell the sub-agent to return **only flat filenames as a sorted list** — no per-subfolder breakdown, no counts per subfolder, no table formatting. The minimal format:

```
one_filename.pdf
another_file.xlsx
...
```

This keeps sub-agent summaries under 1KB for even the largest folders. Confirmed 2026-06-21: a sub-agent asked for a "simple list of filenames" for a 220-file folder returned only 6KB of output. Without that instruction, it would have returned a full file metadata dump (~30KB+).

If the sub-agent still produces a verbose breakdown despite this instruction, fall back to inline `find | awk -F/ '{print $NF}' | sort` (one-line shell command, no sub-agent needed) which completes in seconds regardless of folder size.

**Two approaches:**
```python
from hermes_tools import search_files

bim_files = set()
for target_path in BIM_TARGETS:
    result = search_files(pattern='*', target='files', path=target_path, limit=100000)
    for entry in result['files']:
        bim_files.add(entry.split('/')[-1].lower())

root_files = [f for f in os.listdir(attach_root) if os.path.isfile(os.path.join(attach_root, f))]
new_files = [f for f in root_files if f.lower() not in bim_files]
```
See `references/search-files-bim-scanning.md` for full pattern with Arabic normalization.

**B) os.walk (fallback when search_files unavailable):**
```python
import os
bim_base = '~/Library/CloudStorage/.../Bim Unit'
all_bim_files = set()
for root, dirs, files in os.walk(bim_base):
    for f in files:
        all_bim_files.add(f.lower())

attachments = ['file1.pdf', 'file2.pdf', ...]  # from os.listdir
new_files = [f for f in attachments if f.lower() not in all_bim_files]
```

### Step 5: Copy truly new files to BIM

If a file is NOT found in any target folder AND NOT in the broad BIM tree:
1. Determine project from filename prefix:
   - `MOC-MUS-ASE`, `MOC-ASEER`, `MOC-Asser` → Aseer Museum
   - `ZAM-NWC`, `ZAM-` → Zamzam Museum
   - Arabic names like `العرض الفني` → check category folder name
2. Copy to the appropriate subfolder under BIM Unit
3. Log the copy action

**Recommended: Delegate the entire comparison+copy loop to a sub-agent.** Two approaches:

**⚠️ Pitfall: delegating OneDrive path comparisons risks sub-agent 600s timeout (confirmed 2026-06-19).** When the `delegate_task` sub-agent attempts to `find` or `open` files under `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/`, the OneDrive File Provider locks can cause the sub-agent to hang, exhausting its 600s timeout and returning `status: timeout` with no results. The leader then has no comparison data and must redo the work inline.

**Prevention: Pre-compute file lists locally before delegating.** Extract basenames from both sides using shell commands that only touch directory metadata (not file content), write to `/tmp/*.txt`, and have the sub-agent only compare the text files:

```bash
# Fast pre-computation — works under all lock states
find "$BIM_ROOT/Aseer-Museum" -type f 2>/dev/null | awk -F/ '{print $NF}' | tr '[:upper:]' '[:lower:]' | sort > /tmp/bim_basenames.txt
find "$ATTACH_DIR" -maxdepth 1 -type f | awk -F/ '{print $NF}' | tr '[:upper:]' '[:lower:]' | sort > /tmp/attach_basenames.txt
```

Then in the delegation context: "Read `/tmp/attach_basenames.txt` and `/tmp/bim_basenames.txt`. Files in the first list not in the second are new. Do NOT attempt to access OneDrive paths directly."

If the sub-agent still times out (e.g. its terminal session itself contends with OneDrive), fall back to `comm -23` comparison inline (see § "Bulk basename comparison with comm" in Step 4) — it completes in seconds with zero file reads.

**A) `delegate_task` (Hermes-native — preferred when Hermes is the leader):**
Write the attachment file list and BIM file list to `/tmp/*.txt`, then spawn a subagent with toolsets `["terminal","file"]`. The subagent does the full comparison + copy + verification loop. This is more robust than CLI labors because:
- The subagent gets its own isolated terminal session and toolset
- It can retry EDEADLK copies independently without blocking the leader
- Its output is a structured summary, not open-ended stdout

```python
from hermes_tools import write_file, terminal

# Write file lists to /tmp for the subagent
terminal('find attachments_root -type f -maxdepth 1 | while read f; do basename "$f"; done | sort > /tmp/root_attachments.txt')
terminal('find bim_root -type f 2>/dev/null | sort > /tmp/bim_all_files.txt')

# Then delegate the comparison+copy
result = delegate_task(
    goal="...compare...",
    context="BIM list at /tmp/bim_all_files.txt, attachments at /tmp/root_attachments.txt",
    toolsets=["terminal","file"]
)
```

The subagent receives both file lists and the attachment-to-BIM routing map (see Step 4) as part of its context. It returns: count of copied files, destination breakdown, any files that failed copy (EDEADLK).

**B) CLI labor (when Hermes CLI transport is unavailable):**
Use `codex exec` or `claude -p` with the file list in the prompt text. See `orchestration` skill for invocation syntax.

**Sub-agent EDEADLK handling in the delegation context:**
The sub-agent should attempt files in this order:
   - Attempts `cp -n` on each file
   - If `cp` fails with EDEADLK, falls back to `shutil.copy2` with `os.path.isfile()` no-clobber check (Python)
   - If `cat src > dest` also fails, report the file as "EDEADLK blocked — manual NSFileCoordinator required"
   - Verifies each destination file exists with matching size
   - Reports results back

**⚠️ Pitfall: sub-agent over-counts new files when scoping to organized subdirectories.**
Discovered 2026-06-13: A sub-agent tasked with comparing attachments against BIM files scanned `attachments/` recursively (including organized subdirectories like `admin_hr/`, `aseer_museum/`, `general/`) and reported 57 "new" files — all of which were already filed duplicates in those subdirectories. The correct approach is to scope comparison to ONLY the `attachments/` root (flat files), not the organized subdirectory tree. The organized subdirectories are already-filed duplicates and must be excluded from the "new" set.

```python
# CORRECT: scope to root attachments only
import os
attach_root = '/path/to/attachments/'
root_files = [f for f in os.listdir(attach_root) 
              if os.path.isfile(os.path.join(attach_root, f))]

# WRONG: recursive walk picks up already-filed duplicates
all_attachments = []
for root, dirs, files in os.walk(attach_root):  # ❌ includes admin_hr/, aseer_museum/, etc.
    all_attachments.extend(files)
```

**Mandatory instruction in the delegation context:**
> "Compare ONLY flat files in the attachments/ directory root. Do NOT walk subdirectories (admin_hr/, aseer_museum/, general/, etc.) — those contain already-filed duplicates. Scope: `[f for f in os.listdir(attach_root) if os.path.isfile(...)]`."

**⚠️ Pitfall: `_1` suffix duplicates — download script creates suffixed copies of already-filed attachments.**

The download script appends `_1`, `_2`, etc. suffixes to attachment filenames when extracting identical-named files from different emails (e.g., `baseline 10 may.pdf` → `baseline 10 may_1.pdf`, `Samaya Invest, BLK360 G2.pdf` → `Samaya Invest, BLK360 G2_1.pdf`). These `_1` files are NOT new content — they are downloaded duplicates whose original (unsuffixed) version is already filed in BIM.

**Detection logic (add after root-only scoping + before BIM comparison):**
```python
def is_download_duplicate(filename: str) -> bool:
    """Check if filename is a _1 suffix duplicate of an already-filed file."""
    import re
    # Pattern: name_1.ext, name_2.ext, name_3.ext, name (1).ext
    m = re.match(r'^(.+?)[ _]\(?\d+\)?(?=\.)', filename)
    if not m:
        return False
    base_candidate = m.group(1) + '.' + filename.rsplit('.', 1)[-1]
    return base_candidate.lower() in bim_basenames

# Use: every file matching `_1` suffix pattern whose base exists in BIM is AUTOMATICALLY filed
new_files = [f for f in root_files
             if f.lower() not in bim_basenames
             and not is_download_duplicate(f)]
```

**Confirmed 2026-06-12:** all 10 files with `_1` suffixes matched originals already in BIM (`find -iname` with partial basename). Skip these — they consume filing effort and add zero value.

**⚠️ Pitfall: Arabic normalization mismatch — sub-agent reports false "new file" positives.**
Even when scoping correctly to root-only files, a sub-agent may report a file as "new" when it actually exists in the BIM target with slightly different Arabic Unicode normalization (Alef variants أإآٱ → ا, Yeh variants ىئ → ي, Teh Marbuta ة → ه). This was confirmed 2026-06-12: a sub-agent flagged `35- العرض الفني والمالي ...` as new, but the BIM target already had the exact basename — only the Unicode normalization differed.

**Mandatory instruction in delegation context (add this alongside the scope instruction):**
> "Before comparing against BIM target filenames, normalize BOTH sides with full Arabic Unicode normalization: NFC + Alef-mapping + Yeh-mapping + Teh-Marbuta-mapping + diacritic stripping. See the `normalize_name()` function in `search-files-bim-scanning.md`. Do not trust sub-agent claims of 'thorough comparison' — they will miss byte-level normalization differences."

**C) `find -iname` targeted lookup (fast single-file check, confirmed 2026-06-12):**

For checking whether a specific attachment file already exists anywhere in BIM (not just the 7 target folders), use `find -iname` on the full BIM tree. This is faster than `os.walk` and more robust against OneDrive stalls because it queries a single basename per call:

```python
from hermes_tools import terminal

def file_exists_in_bim(basename: str, bim_base: str) -> bool:
    """Check if a file exists anywhere in BIM using case-insensitive find."""
    # Escape single quotes for shell
    safe = basename.replace("'", "'\\''")
    result = terminal(f'find "{bim_base}" -iname "{safe}" -type f 2>/dev/null | head -1')
    return bool(result['output'].strip())
```

This works even when `find` at full tree scale fails (OneDrive File Provider stalls on large-scale traversal). The targeted per-basename query avoids the systemic lock trigger. Confirmed on 2026-06-12: found 13 files in deep BIM subfolders (e.g., Contracts/07_Qotob, Docs/03_Submittals) that a flat 7-folder comparison missed.

**Verification check after sub-agent returns new-file list:** For each flagged "new" file, search the BIM target by normalized basename only. If the normalize-name comparison says "already exists", trust the normalization result over the sub-agent's raw comparison.

### Step 6: Check email archives for CG/project updates

**⚠️ "No new emails" from download script does NOT mean archives are unchanged.**
The download script reports "No new emails in 2026" for the Inbox only. Emails can arrive via other mailboxes/folders that still get appended to the weekly archive file. **Always check the newest archive's mtime** (`stat -f "%Sm" mails/24.md`) — if it changed since the last pipeline run, there's new content, even if the download script said nothing new.

Scan these locations for new files dated today:
- `~/Documents/04_Outlook_Connection/mails/*.md` — pipeline_run files, numbered archives (23.md, etc.)
- `~/Library/CloudStorage/.../Aseer-Museum/Email_Archive/` — structured email summaries

**If the newest numbered archive (e.g. 24.md) is dataless:** first try `os.open()` with basic `O_RDONLY` in Python (see `onedrive-edeadlk-provenance.md` § "Reading locked .md files"). If that fails, recover via `brctl download <path>` (iCloud-backed paths only), then read. New archives created by the download script often get offloaded immediately by OneDrive File Provider.

**Scanning strategy for large .md archives:**
1. First pass: search for project keywords (aseer, zamzam, CG, MOC-MUS, RFI, submittal, NCR)
2. Read context around matches (surrounding 5-10 lines)
3. Extract CG codes, document revisions, and action items

Look for:
- **New CG codes** — e.g. `MOC-MUS-CG-ASE-1KN-1E0-017`
- **New document prefixes** — e.g. `MI` (Mobilization Items), previously unregistered
- **New RFI / IR numbers**
- **Critical HSE/security events** — e.g. FACP power disconnection, security breach
- **New submittal revisions**

Document findings in PROJECT_MEMORY.md directly. If locked (OneDrive EDEADLK), write `PROJECT_MEMORY_UPDATE_<date>.md` to the BIM root.

**Email thread table extraction (Zamzam/NWC pattern):** NWC and CG supervisor long email threads often contain inline submission-status tables (Arabic headers, 5+ columns: document name, submission date, number, status, notes). When found:
1. Extract the table rows preserving the Arabic-English mix
2. Translate status columns (حالة الاعتماد values: معتمد = Approved, معتمد مع ملاحظات = Approved with Comments, يعاد التقديم = Resubmit, لا مانع = No Objection, لا مانع من التوصية = No Objection to Recommend, مرفوض = Rejected)
3. Add to PROJECT_MEMORY as a Markdown table grouped by project
4. Include submission reference numbers (e.g. ZAM-NWC-MUM-DOC-CONT-064) for cross-referencing
5. File the full email chain context in the parent email for audit trail

These tables are gold for tracking approval progress — single-source status snapshots from the supervisor's side.

### Step 7: Write pipeline run log

Save to `mails/pipeline_run_<date>_<time>_<pid>.md` with:
- Run timestamp
- download_mails.py exit code and result
- New attachment count (0 if steady-state)
- Filing locations for any new files
- CG/project findings from email archive scan
- OneDrive sync status (locked / synced)
- Any issues encountered

**⚠️ Pitfall: cron overlap — two pipeline runs at the same timestamp collide on the filename.**

Observed 2026-06-12 18:00: a `write_file` to `pipeline_run_2026-06-12_18-00.md` returned a warning that a sibling subagent had already written that exact file. This happens when:
- A prior cron job is still running when the next 2-hour cycle fires (overlap).
- Multiple sub-agents from the same parent each attempt Step 7 independently.
- The cron schedule fires early before the previous run releases the file.

**Fix: always include a uniqueness token in the filename.** The pattern `pipeline_run_<date>_<time>_<pid>.md` (where `<pid>` = the cron job's PID or Hermes session ID) ensures collision-free writes:

```bash
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M")
PID=$$
LOG_FILE="$MAILS_DIR/pipeline_run_${TIMESTAMP}_${PID}.md"
```

Or in Python:
```python
import os, time
ts = time.strftime('%Y-%m-%d_%H-%M')
pid = os.getpid()
log_path = f'mails/pipeline_run_{ts}_{pid}.md'
```

**Pitfall: newly-written pipeline logs can be locked by iCloud before any reader can access them.**
Observed 2026-06-17: a pipeline run log written by `download_mails.py` to `~/Documents/04_Outlook_Connection/mails/` (iCloud-synced) was immediately locked with `com.apple.provenance` + `dataless` by iCloud FileProvider before the next command could read it. `brctl download` exit 0 failed to materialize it. The file was permanently unreadable for the entire session.

**Recommendation:** Write pipeline run logs to a location OUTSIDE iCloud/OneDrive sync:
```python
LOG_DIR = '/tmp/pipeline_logs'  # local-only, no sync lock contention
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, f'pipeline_run_{timestamp}_{pid}.md')
```
Then, if needed, copy to `~/Documents/04_Outlook_Connection/mails/` as a secondary artifact only after verifying the copy succeeds. Do not make the iCloud path the primary write target.

**Alternatively**, write the report as your final response only (no file) when running as a cron job — the system delivers it directly, and no local file is needed. Only write a local log file when the pipeline captured actionable artifacts (new files, memory updates) that need an audit trail.

```python
existing = [f for f in os.listdir('mails/') 
            if f.startswith(f'pipeline_run_{ts}') and f.endswith('.md')]
if existing:
    print(f'WARNING: {len(existing)} logs already exist for timestamp {ts} — possible cron overlap')
```

## 3. OneDrive Lock Handling

All files under `~/Documents/04_Outlook_Connection/` and `~/Library/CloudStorage/` may be OneDrive placeholders (st_blocks=0).

**Detection:** `os.stat(path).st_blocks == 0`

**Diagnostic: High CPU = systemic lock**
If OneDrive File Provider (`OneDrive File Provider.appex`) is using >50% CPU, ALL files under both paths are likely locked systemically — not just a subset. Directory traversal (`ls`, `find`, `os.listdir`) still works but any file read (`cat`, `open()`, `cp`) fails with EDEADLK. Check with:
```bash
ps aux | grep -i "OneDrive File Provider" | grep -v grep
# If CPU% > 50, systemic lock is in effect
```

**Workarounds:**
| Path type | Workaround |
|-----------|-----------|
| Non-CloudStorage (e.g. `~/Documents/04_Outlook_Connection/`) | `brctl download <path>` then wait 2s |
| CloudStorage (`~/Library/CloudStorage/...`) | **Primary: NSFileCoordinator via Swift** (see `onedrive-edeadlk-provenance.md`). `cat <source> > <dest>` and `rm + cp` work for **dataless placeholders** (st_blocks=0) but **FAIL for `com.apple.provenance` kernel-locked files** (confirmed 2026-06-13). Only NSFileCoordinator handles provenance locks. |
| Both source AND dest OneDrive-backed | NSFileCoordinator via Swift — the only reliable method for provenance-locked files. `cat` and `rm+cp` both fail. |
| Source in iCloud-synced `~/Documents/` (xattr `com.apple.fileprovider.detached#B` on dir), dest in OneDrive CloudStorage | **Cross-cloud deadlock** — all POSIX methods fail (`cp`, `cat`, `shutil.copy2`, `dd`, Python `os.open()`). `os.unlink()` succeeds on dest stubs but subsequent writes (rename, cp) still hit EDEADLK because the kernel blocks cross-provenance file creation in the OneDrive tree while iCloud holds the source lock. **Only NSFileCoordinator via Swift** works for provenance-locked source files. For OneDrive stubs that were unlinked but unreplaceable: the file is logged as "Exists as stub — may auto-sync from prior copy." |
| All paths | `os.listdir()` + `os.stat()` work for metadata even when locked |

**Diagnostic tools:**
```bash
# Check if file is a dataless placeholder
ls -laO <file>
# "compressed,dataless" flags mean content is purged

# Check real file metadata (works even on dataless files)
stat -x <file>
# Returns size, mtime, ctime, birth time — real metadata from the inode

# Check if file has any blocks allocated
python3 -c "import os; s=os.stat('<file>'); print('blocks:', s.st_blocks, '(dataless)' if s.st_blocks==0 else '(on disk)')"
```

### Systemic lock escape hatch: /tmp file lists + delegation
When ALL paths are locked (both mails dir and BIM CloudStorage), use this pattern:
1. Write file lists (basenames only) to `/tmp/*.txt` using `find ... | while read f; do basename "$f"; done | sort > /tmp/list.txt` — only directory traversal needed, no file reads
2. Optionally capture file sizes/mtimes with `stat` (also works under lock)
3. Delegate comparison to a sub-agent (delegate_task or codex/claude) that reads the `/tmp/*.txt` lists
4. Sub-agent compares normalized basenames using `unicodedata.normalize('NFC', name).lower()` for Arabic filenames

Confirmed 2026-06-12: this worked when OneDrive File Provider at 78.7% CPU locked all files on both paths. The sub-agent completed the comparison of 109 attachments vs 14,305 BIM files from `/tmp/` lists alone.

**Prefer compare_and_file.py first**  
If the lock is partial (some files readable, or just the mails path is locked), use the existing script at `scripts/compare_and_file.py` which walks directories and compares by normalized basename. It handles st_blocks=0 files gracefully (only needs stat, not open).

**Never retry the same locked file in the same run.** Document and move on.

## 4. Project-to-Category Mapping

| Attachment Category | Project | BIM Target |
|--------------------|---------|-----------|
| `aseer_museum/` | Aseer Museum | Aseer-Museum/ |
| `zamzam_nwc/` | Zamzam Museum | Zamzam Museum/ |
| `general/` | Mixed/unclassified — see per-subdir routing below | Individual routing per subdir |
| `admin_hr/` | Admin/HR | Aseer-Museum/HR/ and Aseer-Museum/Docs/00_Admin/ |
| `makkah_jabal_omar/` | Makkah/Jabal Omar | Jabal Omar - Samaya Scope/ |
| `haramein_ghamamah/` | El-Haramain Museum | El-Haramain Museum/ |
| `hoarding_signage/` | Hoarding/Signage | Check project context |

#### `general/` subdirectory routing (detailed)

This category accumulates ~100+ files across runs. Files here are not auto-classified by the download script. Route per subdirectory:

| Subdir | Content type (observed 2026-06-20) | Routing |
|--------|-----------------------------------|---------|
| `correspondence/` | NCRs, scope comments, internal letters (3 files) | Check doc code prefix: `MOC-MUS-ASE*` → Aseer-05_Correspondence_Archive; `ZAM*` → Zamzam Docs |
| `drawings_designs/` | Lidar/scanning docs, BIM user lists, design management plans, 3D model files (16 files) | Aseer-Museum/Design Files/ or Aseer-Museum/10_Plans/ |
| `proposals_contracts/` | Technical/financial proposals, quotations, staffing (9 files) | Aseer-Museum/Design Files/00_Scope_and_Proposals/ or Contracts/ |
| `reports/` | Core test reports, weekly coordination reports, CG replies (6 files) | Aseer-Museum/08_Weekly_Reports/ or Docs/10_Test_and_Inspection/ |
| `schedules/` | Leica software datasheets (4 files — dual copies) | Aseer-Museum/10_Plans/ or Design Files/00_Scope_and_Proposals/ |
| `site_photos/` | Site photography, progress photos (56 files) | Aseer-Museum/Docs/00_Admin/99_Images/. Check email context for multi-project routing. |
| `technical_specifications/` | Leica/BLK spec sheets, datasheets (19 files) | Aseer-Museum/04_Specifications_and_BOQ/ or Contracts/ |
| `others/` | Daily updates, invoices, product compliance, various (55 files) | Inspect each — many are Aseer project update files. Check filename for project code prefix. Also skip known non-project commercial docs (متجر, مقهي in Arabic filename = shop/cafe costings, not BIM files). |

**Cross-project routing for `general/`:** If the `general/site_photos/` or `general/others/` files document an issue (thermal stress on pipes, bending, structural defect) and the email context mentions a specific project, copy to that project's folder AND to Aseer-Museum/Docs/00_Admin/99_Images/ as a reference copy.

## 5a. Post-Crash Verification (script crashed mid-run)

When `download_mails.py` crashes (e.g. EDEADLK reading old archive files), the current week's archive (e.g. `24.md`) may still be complete if the crash happened on an older week. Verify:

```bash
# Check if current week archive was modified (size increased)
ls -la ~/Documents/04_Outlook_Connection/mails/24.md
# Compare against its pre-run baseline

# Count new attachments downloaded during the partial run
# Compare pre-run vs post-run file count (excluding subdirs)
find ~/Documents/04_Outlook_Connection/mails/attachments/ -maxdepth 1 -type f | wc -l

# Re-run the organizer manually if the script's auto-organizer didn't fire
python3 ~/Documents/04_Outlook_Connection/scripts/fast_organize.py 2>&1
```

**Key principle:** A crash on Week N-1 does not invalidate Week N's data. The script writes each email to the archive file immediately after downloading — if Week 24 was fully listed as `[+] Completed Archiving Week 24`, assume it's intact even if the script then crashed on Week 23.

**⚠️ The script processes weeks in REVERSE order** — newest week (e.g. Week 24) first, then older weeks (Week 23, ... Week 01). This means a crash on an older week NEVER affects the current week's archive. Confirmed 2026-06-13: Week 24 (9 emails) completed successfully, then the script crashed on Week 01 during `append_to_weekly_file`. The 24.md archive was intact and fully readable.

**Distinct crash mode: write-phase EDEADLK in `append_to_weekly_file`.** Unlike the documented read-phase dataless hang (where the script freezes during inbox-dedup scanning), this crash happens mid-way through the second week's archiving. The script outputs `[+] Completed Archiving Week <N>` for the newest week, then crashes on the next. The crash is an unhandled `OSError: [Errno 11] Resource deadlock avoided` at line ~205 in `append_to_weekly_file()` (the `f.read()` call when opening an existing .md archive for append). The script's `[!] Error reading` handlers catch read-phase EDEADLK on older archives during inbox dedup, but the write-phase EDEADLK in `append_to_weekly_file` has no try/except and kills the process.

**Recovery from write-phase crash:**
1. Verify the newest week's archive is complete (`tail -3 24.md` — should end cleanly)
2. Check count of new attachments (compare pre/post-run count in attachments/ root, excluding subdirs)
3. Proceed with Steps 3–7 normally for the attachments already downloaded — the pipeline does not need the script to fully succeed for all weeks
4. No need to re-run the script; the missed older week will be picked up on the next 2-hour cycle

## 5b. Arabic Subject Scanning (Operational & Critical Detection)

During Step 6 (email archive scan), search for these Arabic subject keywords in the `.md` archives — they signal events the pipeline should surface:

| Arabic Keyword | Meaning | Priority | Action |
|---------------|---------|----------|--------|
| `انحناء` | Bending/warping (structural issue) | 🔴 IMMEDIATE | Flag as critical technical defect. File to project Docs with photos. Update PROJECT_MEMORY with 🔴 marker. |
| `إجهادات حرارية` | Thermal stress | 🔴 IMMEDIATE | Same as above — often paired with انحناء. |
| `استقالة` | Resignation | 🟡 HR Alert | Note in admin/HR section of PROJECT_MEMORY. |
| `عهدة` | Inventory/custody | 🟡 Operational | File to project admin folder. |
| `طلب سيارة` | Vehicle request | ⚪ Low | Operational — skip unless unusual context. |
| `تصديق` | Attestation/legalization | 🟡 Admin | File to project admin. |
| `إنذار` / `Final Notice` | Warning/ultimatum | 🔴 HIGH | Flag as contractual risk. Update PROJECT_MEMORY. |
| شحنة` | Shipment/delivery | 🟡 Operational | Note in project log. |
| `مكتب العمل` / `وزارة` | Government/Labor office | 🟡 Admin | File to project admin. |
| `اجتماع` / `Meeting` | Meeting | 🟢 INFO | Check for MOM/minutes attachment. |

**Implementation in the scan step:**
```python
import re
critical_patterns = {
    'انحناء': 'CRITICAL',
    'إجهادات حرارية': 'CRITICAL',
    'Final Notice': 'HIGH',
    'إنذار': 'HIGH',
    'استقالة': 'MEDIUM',
}
with open('24.md', 'r') as f:
    for line in f:
        for kw, priority in critical_patterns.items():
            if kw in line:
                print(f'[{priority}] {line.strip()[:120]}')
```

## 5c. Multi-Project Attachment Routing

A single attachment email may serve multiple projects. Example from 2026-06-12: WhatsApp site photos and a screenshot documented a **Zamzam pipe thermal stress issue** but were filed automatically to **Aseer/99_Images** by the organizer.

**Rule:** If an attachment's context (email subject, body text) references a different project than the category folder suggests, COPY the file to the correct project's folder as well:

```python
# multi-project routing example
copies = {
    'WhatsApp Image 2026-06-08 at 5.56.19 PM (3).jpeg': [
        'Aseer-Museum/Docs/00_Admin/99_Images',  # auto-routed
        'Zamzam Museum/Docs',                      # manual copy for pipe issue
    ],
    'Screenshot 2026-06-08 181232.png': [
        'Aseer-Museum/Docs/00_Admin/99_Images',
        'Zamzam Museum/Docs',
    ],
}
```

**Detection heuristic:** When a consultant/supervision email (sender domain like `@egec.com.sa`, `@cg.com.sa`) contains technical issue photos, copy them to ALL project folders the email references — not just the auto-categorized target.

## 5d. PROJECT_MEMORY Update — Path Discovery & Sync

The root `Aseer-Museum/PROJECT_MEMORY.md` under OneDrive CloudStorage is commonly a `com.apple.provenance` placeholder (zero-byte, st_blocks=0). The `_Project_Memory/PROJECT_MEMORY.md` copy is usually more accessible. **However, both files can be individually writable on different runs** — and either can fall out of sync with the other.

**⚠️ Pitfall: 3 copies, not 2 (observed 2026-06-16).**
Beyond the main and `_Project_Memory` copies, there is also:
- `Aseer-Museum/Scripts/PROJECT_MEMORY.md` — a third copy that may hold a different revision.
Always check all 3 during the sync phase. Any one can be ahead or behind.

**⚠️ Pitfall: header vs footer version drift within the same file (observed 2026-06-16).**
The main `PROJECT_MEMORY.md` showed **Rev 14** in the header metadata (`آخر تحديث: 16 يونيو 2026 | Rev 14`) but **Rev 12** in the footer (`End of PROJECT MEMORY — Rev 12 (2026-06-13)`). This happens when the header metadata line is manually bumped without also updating the corresponding end-of-file marker. The sync check must detect this:

```python
# Check intra-file header vs footer revision mismatch
m_header = re.search(r'Rev\s+(\d+)', content.split('\n')[1])  # line 2, header
m_footer = re.search(r'Rev\s+(\d+)', content)                  # last match is footer
h_rev = int(m_header.group(1)) if m_header else 0
f_rev = int(m_footer.group(1)) if m_footer else 0
if h_rev != f_rev:
    print(f'WARNING: header Rev {h_rev} ≠ footer Rev {f_rev} — file has drifted')
```

When detected, update the footer marker to match the header during the next edit.

**⚠️ Pitfall: main vs _Project_Memory divergence (observed 2026-06-13):**
The main `PROJECT_MEMORY.md` was writable (78579 bytes on disk) at Rev 08, while `_Project_Memory/PROJECT_MEMORY.md` was also writable (85602 bytes) at Rev 10. The previous pipeline run had updated only the `_Project_Memory` copy. The main file missed 5 critical entries (Zamzam pipe thermal stress, Al Maghrabi response, EinScan LIBRE quote, Lumotion declined, updated action items).

**Procedure: always check all 3 copies. After updating one, sync the others if behind.**

### Sync check pattern
```python
import os, re

paths = {
    'main': '.../Bim Unit/Aseer-Museum/PROJECT_MEMORY.md',
    'memory': '.../Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md',
    'scripts': '.../Bim Unit/Aseer-Museum/Scripts/PROJECT_MEMORY.md',
}

revs = {}
for name, path in paths.items():
    if os.path.exists(path) and os.stat(path).st_blocks > 0:
        with open(path) as f:
            content = f.read()
        # Get the LAST Rev mention (footer marker, more reliable than header)
        m = re.findall(r'Rev\s+(\d+)', content)
        revs[name] = int(m[-1]) if m else 0
    else:
        revs[name] = 0

max_rev = max(revs.values()) if revs else 0
behind = {name: rev for name, rev in revs.items() if rev < max_rev}
if behind:
    print(f'WARNING: copies behind Rev {max_rev}: {behind} — sync needed')
elif set(revs.values()) == {max_rev} and max_rev > 0:
    print(f'All {len(revs)} copies at Rev {max_rev} — in sync')
```

Also check header vs footer within each readable copy (see drift check above).

### Update priority
1. **All writable copies** — update all 3 in the same run to prevent drift
2. **If only one writable** — update the writable one, log the sync gap in pipeline run log. List the writable paths and which are locked.
3. **If all locked** — write `PROJECT_MEMORY_UPDATE_<date>.md` to BIM root + log to mails dir

### Detecting prior PROJECT_MEMORY_UPDATE files (next-run consumption)
When the main `PROJECT_MEMORY.md` is EDEADLK-locked and a prior run created `PROJECT_MEMORY_UPDATE_<date>.md` (per rule 3 above), the current pipeline can still extract CG updates without reading the locked main file.

**Detection:** Use `find -newer` with the main file as reference — the locked file's mtime is stagnant, so any update file written after it is newer:
```bash
BIM_ROOT="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum"
find "$BIM_ROOT" -name "PROJECT_MEMORY_UPDATE_*.md" -newer "$BIM_ROOT/PROJECT_MEMORY.md" -type f 2>/dev/null
```
This catches update files in `_Project_Memory/`, `Scripts/`, or the root — anywhere in the BIM tree. Use `find` on the full `Aseer-Museum` tree, not just specific subfolders, because prior runs may have written to different locations (confirmed 2026-06-19: found `PROJECT_MEMORY_UPDATE_2026-06-19.md` in `_Project_Memory/` via this method while main file was locked).

**Reading:** If the update file itself is also EDEADLK-locked, use NSFileCoordinator via Swift (see `references/onedrive-edeadlk-provenance.md`). Update files in `_Project_Memory/` on OneDrive are often more materialized than the main file — try `os.open(O_RDONLY)` first.

**Merge status determination:** Check the update file's content for a "Rev" number or date in its filename. Compare against the last known Rev from the main PROJECT_MEMORY.md (from a prior pipeline log). If the update file contains a higher Rev, content is not yet merged — include findings in the current report under a "📥 Pending merge from prior run" section.

**Pitfall: stale update file still on disk.** If a later run successfully wrote to the main file, the update file is now redundant. Cross-check: if the main file is readable this run, compare Revs. If also locked, report "Update file found — merge status indeterminate."

### Paths
```
OneDrive SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md
OneDrive SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/PROJECT_MEMORY.md
```

The `_Project_Memory` path resolves to:
```
~/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md
```
The actual OneDrive sync cache under `~/Library/Group Containers/` keeps files materialized even when the CloudStorage symlink shows placeholders.

**Update content format:** Each entry should include:
- Date and project
- Document code and revision
- CG result (Code A/B/C/D if applicable)
- Brief English description
- Filing location

```markdown
## 🆕 Jun 12: Zamzam Museum — Pipes Bending from Thermal Stress
| **EGEC Supervision Report** | Mohamed Abdelwahab (EGEC, Sr. ME) reports horizontal bending of Zamzam pipes from thermal stress due to excavation. Contractor: install certified U-Bolts immediately. Full liability on contractor. Photos filed. |
```

**⚠️ Pitfall: content below the end marker gets orphaned after append-to-beginning patches.**
When updating PROJECT_MEMORY.md via find-and-replace (e.g. replacing the old *End of PROJECT MEMORY — Rev N* marker), any content that was previously below the marker gets orphaned — it's not part of the matched string and survives after the new marker. **Always verify the file ends cleanly after every update:**

```bash
tail -5 "PROJECT_MEMORY.md"
# Should show the end marker as the last substantive line
# If there's section content (| table rows, ## headings) below the marker, delete them
```

To clean orphaned content, match from the end marker through all orphaned text to the actual end of file and replace with just the end marker.

**Multi-pass update pattern for PROJECT_MEMORY.md (discovered 2026-06-12):**
When adding several findings at once (schedule updates, subcontractor changes, action items), batch into a single patch rather than sequential edits. Sequential patches risk: (a) orphaned content below end marker, (b) duplicate headings if old_str matches imprecisely, (c) file inconsistency if OneDrive File Provider locks mid-edit. Workflow:
1. Read the tail to understand current end section
2. Compose ALL new entries + new end marker as one replacement string
3. Apply one patch replacing the old end marker with the full new block
4. Verify the file ends cleanly at the new marker
5. If old content below the old marker survived (common with fuzzy matching), do one targeted removal patch

**QC verification (per user's fixed assignments: Kimi = QC):**
After PROJECT_MEMORY.md is updated, run:
```bash
kimi -p "QC check: verify PROJECT_MEMORY.md header shows correct Rev N and timestamp, verify no orphaned content below end marker, verify 3 new files exist at BIM destination paths."
```
Cross-check results before delivering final report.

**PRIMARY pointer:** See also `references/crash-arabic-multi-pitfalls.md` for the three key pitfalls discovered 2026-06-12 (archive crash recovery, Arabic subject scanning, multi-project routing) and `references/search-files-bim-scanning.md` for faster BIM-tree scanning with `search_files` (ripgrep) instead of `os.walk`.

**Notable Observations — adding context beyond pipeline output:** After completing Steps 1–7, compile a "Notable Observations" section in the pipeline report. Two always-relevant checks:

1. **BIM tree changes since last run** (run `find -newer` — see Step 4 fast-path section above). This catches Revit model updates, new project docs, and non-email-derived activity.
2. **Provenance lock status** — note if `com.apple.provenance` blocked any reads this run. This tracks whether the lock is persistent or intermittent.
3. **Mails dir archive modification times** — check `stat -f '%Sm'` on numbered .md archives (01.md–24.md) to see if any were touched since last pipeline run (indicating new email content even if download script said nothing new).

Example observations format:
```
### Notable Observations
- BIM tree: 25 new files since last run (Zamzam Revit RFA families, Aseer LiDAR docs, Resource Mgmt Plan 02.14)
- Provenance lock: Files in mails/ dir still locked — CG content extraction blocked
- Last archive mtime: 24.md = Jun 17 09:06 (unchanged since last run)
```

## 5. Output Artifacts

| Artifact | Location | Format |
|----------|----------|--------|
| Pipeline run log | `mails/pipeline_run_<date>_<time>_<pid>.md` | Markdown summary |
| PROJECT_MEMORY update | `Aseer-Museum/PROJECT_MEMORY_UPDATE_<date>.md` | Structured findings |
| Steady-state report | Final response | One-liner or `[SILENT]` |
