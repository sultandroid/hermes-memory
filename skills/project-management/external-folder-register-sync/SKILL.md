---
name: external-folder-register-sync
title: External Folder → Repo Register Sync
description: Scan external team member OneDrive folders (Adel Darwish, etc.) for new/changed files, filter historical backfill from genuinely new items, and update repo markdown registers (RFI, NCR, submittal, SI, prequalification, material submittal). Covers the detection script, subfolder-to-register mapping, date-based filtering, and register update patterns.
trigger: user asks to check a team member's OneDrive folder for new files, or a cron job fires for folder scanning
tags: [onedrive, register-sync, adel, folder-scan, cron, project-management]
---

## Workflow

### 1. Run the detection script

```bash
bash /Users/mohamedessa/aseer-museum-pm/scripts/check_adel_files.sh
```

The script outputs all files that differ from its last snapshot. **First run after a long gap will flag hundreds of historical files** — this is expected.

### 2. Filter for genuinely new items

The script output is massive (600K+ chars). Do NOT try to register everything. Instead:

- **Focus on files dated within the last 7 days** (or since the last cron run)
- Historical backfill (Dec 2025–Jun 2026) should be noted but NOT re-registered
- Use `ls -lt` on each subfolder to see actual modification dates
- Cross-reference against existing registers to avoid duplicates

### 2a. 7-Day Recency Filter (Script-Level)

The detection script (`~/.hermes/scripts/check_adel_files.sh` — note it lives in `.hermes/scripts`, NOT the repo) includes a **7-day recency filter** that silently suppresses files older than 7 days. This prevents false positives when the snapshot file is reset or re-deployed. The filter uses `date -v -7d` on macOS to compare file mtime against the cutoff.

**Do NOT remove this filter.** Without it, a snapshot reset causes ALL files (including Feb–Apr 2026 historicals) to appear as "new" in the next cron run (3089 files were reported in one run when the filter was missing).

**mtime must be ISO-8601 for the filter to sort.** The naive `stat -f '%Sm'` output is `Apr 24 13:11:16 2026` (month-name format) — NOT lexically comparable against an ISO cutoff. If you rebuild the inventory line, use ISO format or the filter silently fails to suppress anything:
```bash
find "$ADEL_DIR" -type f -exec stat -f '%N|%z|%Sm' -t '%Y-%m-%d %H:%M' {} \; | sed "s|$ADEL_DIR/||" | sort > /tmp/adel_current.txt
# then filter:
NEW_FILES=$(echo "$NEW_FILES" | awk -F'|' -v c="$(date -v -7d '+%Y-%m-%d %H:%M')" '$3 >= c')
```
Verified working 2026-08-17: cut the false-positive 3089-file report down to the 6 genuinely recent files.

### 2. Submittal Package Folder (02. DOC - Document Submittal/GN/)

The `02. DOC - Document Submittal/` folder contains 98 numbered submittal packages (01-98), each in its own subfolder. These are NOT auto-scanned by the detection script. To process them:

**Folder structure per package:**
```
NN- DOC-ID/
  ├── DOC-ID.pdf          # Transmittal cover sheet
  ├── DOC-ID.xlsx         # Submittal register
  ├── Supporting docs     # PDFs, DOCXs (the actual submittal content)
  ├── Approval/           # CG response (if reviewed)
  ├── Rev.01/ Rev.02/     # Revisions
  └── Done/               # Completion marker
```

**Mapping rule by doc type:**
| Package Type | Doc ID Pattern | Repo Destination |
|-------------|----------------|------------------|
| Plans (PL) | `MOC-ASEER-SIC-*-PL-*` or `MOC-MUS-ASE-*-PL-*` | `03_Plans/` (match plan number) |
| Shop Drawings (ZD) | `MOC-MUS-ASE-*-ZD-*` | `03_Submittals/03.7_Submittal_Packages/` |
| BOQs (QT) | `MOC-ASEER-SIC-*-QT-*` | `03_Submittals/03.3_Material_Submittals/` or `04_Financial/` |
| Test Procedures (TP) | `MOC-ASEER-SIC-*-TP-*` | `10_Test_and_Inspection/` |
| Reports (RP) | `MOC-MUS-ASE-*-RP-*` | `07_Reports/` |
| SC Requirements | `MOC-MUS-ASE-*-SC-*` | `03_Submittals/` |
| General (GN) | `ARM-DS-GN-*` | Depends on content (see known mappings below) |

**Known GN package mappings:**
| # | Doc ID | Content | Repo Destination |
|---|--------|---------|------------------|
| 01 | ARM-DS-GN-0001 | Mobilization Phase Plan | `03_Plans/07_Mobilization/` |
| 06 | ARM-DS-GN-0006 | Narrative Reports (Rev 02-05) | `00_Status/` or `07_Reports/` |
| 13 | MOC-ASEER-SIC-1K0-PL-0013 | Submission Plan Meeting Minutes | `03_Plans/01_DMP/` |
| 15 | MOC-ASEER-SIC-1K0-PL-0015 | BEP Comment Response | `02_CG_Responses/` |

**When converting DOCX to MD for repo:**
- Place the `.md` alongside the source `.docx` in the same folder
- Use `python-docx` to walk paragraphs + tables (see `references/docx-to-md-conversion.md` for batch template)
- Escape `|` in table cells (replace with `/`) or markdown tables break
- For batch runs, write a standalone `.py` script, not inline Python (folder names with leading zeros cause `SyntaxError` in `-c` mode)
- Skip TOC-style paragraphs (style name contains "TOC")

**Git push after conversion:**
- The PM repo is `sultandroid/aseer-museum-pm` (not the viz app `sultandroid/aseer-museum-viz`)
- Clone to `/Volumes/MIcro/Temp/aseer-museum-pm` (user prefers Micro volume for git operations)
- macOS `._` metadata files in pack index cause noisy but harmless errors — add `._*` to `.gitignore`
- Commit in logical batches: contracts first, then plans, then letters/RFIs/method statements
- User expects push after every batch — "did you add to repo?" means "did you push to GitHub"

### 3. Subfolder-to-Register Mapping (Adel's main folders)

| Adel Subfolder | Repo Register | Notes |
|---------------|---------------|-------|
| `05- Request For Information-RFI/` | `01_Registers/rfi_register.md` | TQ/RFI refs, status changes, CG replies |
| `12-NCR/` | `01_Registers/ncr_register.md` | NCR documents (may not exist as folder — NCRs may be in Letters attachments) |
| `07-Pre-Qualification Submittal/` | `01_Registers/prequalification_register.md` | May not exist in Adel's structure |
| `08-Material Submittal MA/` | `01_Registers/material_submittal_register.md` | May not exist |
| `09-Method Statement MWS/` | `01_Registers/submittal_register.md` | May not exist |
| `10- CG Site Instruction SI/` | `01_Registers/si_register.md` | SI documents |
| `11-IFC Drawing/` | `01_Registers/submittal_register.md` | IFC packages |
| `13-Weekly Report/` | — | Often empty — note and skip |
| `14-Inspection Request IR/` | — | Often empty — note and skip |
| `15-Start New Activity SNA/` | — | Often empty — note and skip |
| `17-SOR/` | — | Often empty — note and skip |
| `20- DDD/` | `01_Registers/submittal_register.md` | Design Development Drawings (1G-xxxx packages) |
| `01- Letters/` | Cross-ref to NCR/SI registers | Letters attachments may contain NCRs, CG replies, TQ responses |
| `06-Weekly Meeting MOM/` | `01_Registers/meeting_minutes_register.md` | Often empty in Adel's folder |

### 4. Check subfolder existence before scanning

Many expected subfolders may not exist in the team member's OneDrive. Use `ls` and check exit code before trying to scan contents:

```bash
ls -lt "/path/to/subfolder/" 2>/dev/null || echo "FOLDER NOT FOUND"
```

### 5. Update registers

For the master Aseer `RFI.xlsx` (Workshop No. 1 coordination log), see
`references/aseer-rfi-workshop-register-structure.md` for its discipline-block layout,
response-column semantics, and how to place a new coordination RFI.

For each genuinely new item:

- **RFI register**: Add new TQ rows, update status from "Open" to "CG response received" when Approval subfolder appears
- **Submittal register**: Add new DD packages (1G-xxxx), update status codes
- **NCR register**: Add new NCR rows, update source line
- **SI register**: Add new SI entries if new folders appear

### 6. Update the last_updated timestamp

Always bump the `last_updated` field in the YAML frontmatter of every register you modify.

## Pipeline-First Rule (user correction 2026-08-01)

When the user says "update repo" after an email/scan batch, the **repo's own mandate** (AGENTS.md `Integrated Document-to-Register Pipeline`) expects you to run the intake pipeline first rather than hand-patching registers ad-hoc:

```bash
cd /Users/mohamedessa/aseer-museum-pm
python3 scripts/document_intake.py --scan-dir 05_Comms     # emails/comms
python3 scripts/document_intake.py --scan-dir 01_Registers  # existing register md
```

- `document_intake.py --incremental` does NOT exist — use `--scan-dir <dir>` or `--file <path>`.
- The pipeline auto-classifies docs and updates registers, then tells you to run `full_sync_commit.py` for push/rebuild.
- **Do NOT bypass the pipeline for straight register edits** — the user corrects ("follow repo instructions") when you patch registers manually instead. Register rows still need `last_updated` bumped in the YAML frontmatter of every register you touch.
- The intake run mutates `.sync_state.json`, `06_Risk_System/webapp/src/index.html`, and compliance files — include these in your commit.

## Git Push: post-commit hook hangs rebase (pitfall 2026-08-01)

The repo has a `.git/hooks/post-commit` hook that auto-rebuilds register web apps. During `git rebase origin/main` the hook fires per commit and **hangs on an SSH deploy to samaya-factory.com** (timeout after 120s), leaving a stale `.git/rebase-merge` that blocks the next rebase. **Disable the hook for the rebase/push, then restore it:**

```bash
cd /Users/mohamedessa/aseer-museum-pm
mv .git/hooks/post-commit .git/hooks/post-commit.bak
git fetch origin && git rebase origin/main && git push origin main 2>&1
mv .git/hooks/post-commit.bak .git/hooks/post-commit
```

If a rebase was already interrupted: `git rebase --abort; rm -rf .git/rebase-merge` before retrying. Check whether the hook is still present after recovery: `ls -la .git/hooks/post-commit`.

### 7. Daily Reports (04- Daily Report subfolder)

The `04- Daily Report/` subfolder contains daily site reports in Arabic/English PDF format. These are **not registered in any repo register** — no daily report register exists.

**When new daily reports appear:**

1. **Hydrate PDFs one at a time** — OneDrive cloud-only placeholders (0 blocks on disk) must be hydrated individually. **NEVER batch-download** — opening multiple files simultaneously causes "Resource deadlock avoided" errors. One-by-one only:
   ```bash
   ADEL_DIR="/path/to/Adel/04- Daily Report/05- May 2026/"
   for f in "Daily Report 13-05-2026.pdf" "Daily Report 14-05-2026.pdf"; do
     open -a Preview "$ADEL_DIR/$f"
     sleep 20
     stat -f "%b" "$ADEL_DIR/$f"  # Verify blocks > 0 (1808 = hydrated)
   done
   ```
   **Alternative if Preview fails:** kill OneDrive (`killall OneDrive`), wait 30s, restart (`open -a OneDrive`), wait 20s, then open with Preview again.
   See `bulk-file-organization` skill → `references/onedrive-hydration-one-by-one.md`

2. **Extract text** with `pdftotext -layout`:
   ```bash
   pdftotext -layout "$ADEL_DIR/$f" "/tmp/${f%.pdf}.txt"
   ```

3. **Analyze content** — standard Arabic daily report format with:
   - Report number (101, 102, ...)
   - Date, weather, temperature
   - Manpower tables (consultant + contractor teams)
   - Work activities (HVAC assessment, BMS, Mobilization, demolition prep, floor protection, fire fighting)
   - Safety notes
   - Photos section
   - Sign-off (Adel Darwish or Mohamed Samir)

4. **Key data to extract** for project tracking:
   - Report date and number
   - Activities performed (Arabic: اعمال التقييم, اعمال الهدم, اعمال حماية, etc.)
   - Manpower counts (planned vs actual)
   - Safety issues
   - Signatory (indicates PM transition — e.g. Adel Darwish → Mohamed Samir from 20-May)

5. **No register to update** — daily reports are site records, not submittals. Advise user on content and flag any notable items (manpower gaps, safety issues, activity changes).

### 8. Detection Script is no_agent

The cron job (`check_adel_files.sh`) is `no_agent: true` — it only compares file lists (name|size|mtime) against a stored snapshot. It does NOT:
- Open or read any file
- Extract text from PDFs
- Update any register
- Make any decisions

The script outputs a list of new/changed files and a suggestion to run `hermes -z` for processing. Actual content analysis and register updates require a separate agent session.

## Supplementary: Finding Project Data When OneDrive Files Are Locked

OneDrive cloud-only files (0 blocks on disk) return "Resource deadlock avoided" on all read attempts. When this blocks an investigation, use the following cascade to find subcontractor/specialist data:

### Cascade Order

1. **Repo registers first** — always check these before OneDrive:
   - `prequalification_register.md` — company names, PQ refs, scope descriptions, CG codes
   - `submittal_register.md` — doc refs, submission dates, CG codes
   - `specialist_register.md` — appointed specialists and status
   - `risk_register.md` — cross-references to specialist risks

2. **Outlook SQLite (email previews)** — when email .md files are deadlocked:
   ```bash
   DB="/Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
   sqlite3 "$DB" -column "
   SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
          m.Message_NormalizedSubject as subject,
          m.Message_SenderAddressList as sender,
          substr(m.Message_Preview, 1, 250) as preview
   FROM Mail m
   WHERE m.Message_NormalizedSubject LIKE '%KEYWORD%'
   ORDER BY m.Message_TimeReceived DESC
   LIMIT 10;
   "
   ```
   - `Message_Preview` contains the first ~250 chars of the email body — enough to see CG response codes ("B - Approved with Comments", "C - Revise and Resubmit")
   - Filter for `@cg.com.sa` senders to see CG responses
   - See `references/outlook-sqlite-data-discovery.md` for common query patterns

3. **Adel snapshot file listings** — the `99_Archive/adel_snapshots/file_list.txt` contains a full crawl of Adel's OneDrive folder structure. Search for doc refs:
   ```bash
   grep "ZD-0088" /Volumes/MIcro/Temp/aseer-museum-pm/99_Archive/adel_snapshots/file_list.txt
   ```
   - Approval subfolder = CG responded
   - Rev.01 subfolder = resubmitted after comments
   - File dates show the timeline

4. **Cross-reference** between all three sources to get the full picture:
   - Email subject = document ref
   - File listing shows approval folder exists
   - Registers show the company name and PQ status

### Example: Finding "who does the electrical assessment"
```
1. prequalification_register.md → PQ-0084 TABCOMM (testing & assessment)
2. Outlook: MOC-MUS-ASE-1E0-ZD-0088 → CG Code B
3. Adel snapshot: ZD-0088 in Approval/ subfolder → CG responded
4. Conclusion: TABCOMM does electrical/mechanical assessment, 3 reports approved
```

## Pitfalls

- **First-run noise**: The script's first scan after a long gap flags ALL files as "new". Filter by modification date. Only items from the last 7 days are genuinely new.
- **Old files re-appearing after snapshot reset**: If the snapshot file is deleted or the script is re-deployed, ALL files appear as "new" again — including files from Feb–Apr 2026. The detection script now includes a **7-day recency filter** (`date -v -7d`) that silently suppresses files older than 7 days. This prevents false positives from snapshot resets. The filter is in `check_adel_files.sh` — if you modify the script, preserve this filter.
- **Empty subfolders**: Several subfolders (13-Weekly Report, 14-IR, 15-SNA, 17-SOR) are consistently empty in Adel's OneDrive. Don't flag them as missing — they're expected to be empty.
- **NCRs in Letters**: NCR documents may appear as attachments in the Letters folder (e.g., `01- Letters/IN/CG/01-/مرفقات الخطاب/NCR-CG-001.pdf`) rather than in a dedicated 12-NCR folder.
- **CG Reply in Approval subfolders**: Many TQ folders have an `Approval/` subfolder containing CG response PDFs. When this appears, update the TQ status from "Open" to "CG response received".
- **DDD packages span multiple subfolders**: A single 1G-xxxx package may have a main folder (PDF+XLSX) and an `Approval/` subfolder (CG-reviewed PDFs + CRS xlsx + BS rar). Both are part of the same submittal — don't double-count.
- **Script output truncation**: The script output can exceed 600K chars. Use `ls -ltR` on specific subfolders to get focused views rather than relying on the full script output.
- **OneDrive deadlock on cloud-only files**: Files with 0 blocks on disk (cloud-only placeholders) cannot be read by any tool (`pdftotext`, `cp`, `head`, `python`) — they return "Resource deadlock avoided". The fix is to open each file individually with Preview (`open -a Preview "$file"`), wait 20s for hydration, then verify blocks > 0 with `stat -f "%b"`. Kill and restart OneDrive if Preview also fails.
- **Daily report register**: When daily reports are found, create a new register at `01_Registers/daily_report_register.md` with YAML frontmatter, a table of all reports (date, report no, prepared by, key activities, manpower, issues), and a gap analysis section showing which months have reports and which are missing.
- **OneDrive File Provider blocks ALL writes (distinct from read EDEADLK)**: The `onedrive-edeadlk` reference covers *reads* of cloud-only files. Separately, macOS OneDrive File Provider **rejects every programmatic write** into a synced folder with `Operation not permitted` (exit 1) — even after `killall OneDrive`, and even Finder AppleScript `duplicate`/`move` fail with `-8004`. `cp`, `mv`, `mkdir`, `touch`, `ditto`, `os.sendfile`, `Finder duplicate` all return `Operation not permitted` on CloudStorage paths. **There is no shell workaround — the ONLY reliable path is manual drag-and-drop in Finder.** When you must stage files for the user:
  1. Build the organized folder structure in `/tmp/` or on the Micro volume (writable, same filesystem semantics).
  2. Generate a `_FILE_MAPPING.csv`/`.md` listing each staged file → its OneDrive target folder.
  3. `open` both the staging root and the OneDrive target folder in Finder, and tell the user to drag-drop each folder across.
  4. Commit the mapping `.md` to the repo (a `.csv` is gitignored — use `.md` extension) so the placement intent is durable.
  Verified 2026-08-01: 46 PQ files staged to `/tmp/filed_pq/PQ_Documents/` + `pq_attachment_mapping.md` because OneDrive rejected every write method. The Micro volume (`/Volumes/MIcro/Temp/`) is also write-enabled where the OneDrive path is not.
- **Scrub declined-specialist names from ACTIVE files**: when a specialist declines and scope is reassigned (e.g. Lumotion → folded into Rawasin), the name must be removed from all active (non-archive) files — register rows, risk JSONs (`06_Risk_System/prr_risks.json`, `ddr_risks.json`, `risks.json`, `webapp/ddr/risks_ddr.json`), plan MDs, SOWs, trackers, scripts. Use a Python replace script over the file list; neutralize with a generic label ("the interactive specialist") rather than the firm name. Preserve `99_Archive/` (historical) untouched. Verify JSON still parses after replace. The user's instruction "don't [name] again anywhere" means grep the whole active tree and confirm zero hits.

See `references/email-pq-to-register-workflow.md` for the full batch attachment → filing → register → knowledge-extraction recipe.
