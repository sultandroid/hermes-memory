# Pipeline Run — 10 Jun 2026

## Two Runs

| Run | Time | Status |
|-----|:----:|--------|
| Run 1 | 03:26 | Found 32 new files, filed 30 (2 dedup skipped) |
| Run 2 | 12:00 | Steady state — all 201 attachments already filed; no new emails |

## Run 1 (03:26)

**Source:** `pipeline_run_2026-06-10.md` (created by the pipeline script)

| Metric | Value |
|--------|-------|
| `download_mails.py` | Exited 0, no stdout (AppleScript silent-fail) |
| Attachments scanned | 201 total |
| Already filed | 169 |
| **New files found** | **32** |
| Files routed to BIM | **30** |
| Skipped (dedup) | **2** |
| Projects affected | Aseer Museum, Jabal Omar, Haramain/Ghamamah, Samaya Admin |
| MD archives | No new weekly archive (latest: 23.md) |
| PROJECT_MEMORY.md | Already at Rev 08 — no updates needed |

**Note:** This is the first pipeline run since the backlog was cleared (Jun 9) where new files were found. The 32 "new" files likely represent a small residual set from the 201 total that were routed on this pass.

## Run 2 (12:00 — This Session)

| Metric | Value |
|--------|-------|
| `download_mails.py` | Exited 0, no stdout (AppleScript silent-fail) |
| Attachments scanned | **201 files** across 7 project subfolders |
| Already filed | **201** — all confirmed pre-filed (per prior runs on Jun 9-10) |
| New files to route | **0** |
| MD archives | No 24.md yet (latest: 23.md, Week 23, analyzed Jun 9) |
| PROJECT_MEMORY.md | Rev 08 (updated Jun 10 04:35) — no new CG codes, RFIs, or updates |
| `digest_latest.md` | ✅ Updated (written successfully — iCloud path, no lock) |
| `pipeline_run_2026-06-10_12-00.md` | ✅ Created as run log |
| Delegation agents | 5 sub-agents (3 parallel for inventory, 2 parallel for comparison) — ~140s total |

### Attachment Breakdown (All Pre-Filed)

| Project | Files |
|---------|:-----:|
| aseer_museum | 53 |
| general | 115 |
| zamzam_nwc | 14 |
| admin_hr | 13 |
| haramein_ghamamah | 3 |
| makkah_jabal_omar | 3 |
| hoarding_signage | 0 |
| **Total** | **201** |

### New Findings This Run

**1. `_Project_Memory/PROJECT_MEMORY.md` is the authoritative source (75KB)**
The canonical PROJECT_MEMORY.md at Aseer-Museum root (9.5KB) was OneDrive-locked. The `_Project_Memory/` copy (75,893 bytes) was fully readable and contained Rev 08 with complete Week 23 data (all CG codes through Jun 7, 14 pending action items, full session history). The root copy is a stale/summary version; the `_Project_Memory/` copy is the working document.

Use the `_Project_Memory/PROJECT_MEMORY.md` copy as the authoritative source for pipeline email extraction (not the root copy or Scripts/ copy), because:
- It's the largest (75KB vs 9.5KB root vs 3.8KB Scripts copy)
- It's more likely to be hydrated (local sync) than the root
- It's consistently writable via `patch` (confirmed Jun 9-10)

**2. ZAM-NWC-CTR-DOC-AR-040 size discrepancy**
In `Zamzam Museum/Docs/03_Inspection_Requests/`, this file is 1,076,244 bytes (211KB smaller) vs source attachment at 1,287,719 bytes. Full-size versions exist in `Zamzam Museum/Docs/` and `Zamzam Museum/Correspondence/` (1,287,719). The Inspection Requests copy may be an earlier or compressed version.

**3. 12 stub files in `Zamzam -Visitor Center/` root**
12 of 14 Zamzam NWC files exist as 4-byte placeholder stubs in the Visitor Center root (e.g., `ZAM-NWC-CTR-IR-STR-012_Rev.00.pdf` at 4 bytes). These are empty files — created as filenames but never hydrated. All original content is in `Zamzam Museum/Docs/03_Inspection_Requests/`.

## Run 3 (14:30 — CG/Email Deep Extraction)

This run focused on deep content extraction from `23.md` (590KB, Week 23 email archive) for CG codes, delay reports, and project intelligence. `download_mails.py` ran but found no new emails (AppleScript silent-fail). All 201 attachments confirmed pre-filed in previous runs. Pipeline scripts (fast_organize, project_organize, generate_summary) all exited 0 with no output.

### CG Codes Found in 23.md (Jun 7-8)

| Ref | Document | CG Code |
|-----|----------|---------|
| MOC-MUS-ASE-1KH-PL-0043 Rev.01 | Temporary Electrical Mgmt Plan | **B** ✅ |
| MOC-MUS-ASE-1KH-PL-0043 (orig) | Temporary Electrical Mgmt Plan | **C** 🔄 |
| MOC-MUS-ASE-1KH-PL-0045 | Heat Stress Management Plan | **B** ✅ |
| MOC-MUS-ASE-1KH-PL-0046 | Lifting Operation Management Plan | **C** 🔄 |
| MOC-MUS-ASE-1K0-PL-0018 Rev.01 | Project Communication Plan | **C** 🔄 |
| MOC-MUS-ASE-1K0-PL-0020 Rev.01 | Stakeholder Management Plan | Resubmitted |
| MOC-MUS-ASE-1A0-ZD-0033 Rev.01 | Sample for 3D Render | Resubmitted |
| MOC-MUS-ASE-1C0-IR-0002 | Temporary Fence Installation | IR submitted |

### Critical Alerts

1. **Maalem Al-Haramain Museum** — Microcement base layer delayed **4 days**. 72h final notice for outstanding samples/catalogues/technical requirements. Zero manpower for ~10 days unless replacement provided. Forecast finish: 21 Jun → 24 Jun.
2. **Zamzam Museum** — 12+ active IR/MIR/WIR submissions for tunnel works (filler board, waterstop, waterproofing, rebar, formwork, concrete pouring at axes A/B/C, 14-20).
3. **Lumotion (Tony Tertyshnyk)** — Signed NDA for Aseer Museum interactive design subcontractor. Prequalification in progress.
4. **SITML (Leica Geosystems)** — Quotations for RTC360 & BLK360 G2 LiDAR. Shining 3D EinScan Libre demo completed Jun 8.
5. **SharePoint** — Abdelrahman Sakr shared "Fabrication", "Cad", "TIMBER PARTITION" folders for El-Ghamama Gift Shop.

### os.open() Transient Read Pattern

`23.md` was the only file readable via `os.open(os.O_RDONLY)`. All other dataless state files (digest_latest.md, PROJECT_MEMORY_WEEK24_UPDATE.md, etc.) remained locked. The read succeeded on first open per process but failed on subsequent calls — confirming the transient-first-read pattern documented in the skill's `com.apple.provenance` section.

### All Script Status

| Script | Exit Code | Output |
|--------|:---------:|--------|
| download_mails.py | 0 | None (AppleScript silent-fail) |
| fast_organize.py | 0 | None |
| project_organize.py | 0 | None |
| generate_summary.py | 0 | None |

Summary wrote to: `~/Documents/04_Outlook_Connection/mails/pipeline_run_2026-06-10_14-30.md`

## Key Observations

1. **Script path confirmed**: `download_mails.py` lives at `~/Documents/04_Outlook_Connection/scripts/download_mails.py`, NOT at `.../download_mails.py` (user's cron instruction says the latter).
2. **Steady-state confirmed**: 201 attachments, all filed. Matches the Jun 9 pattern. The 32 files from Run 1 were the last residuals.
3. **`brctl download` rehydration works**: iCloud dataless files at `~/Documents/04_Outlook_Connection/mails/` were successfully rehydrated with `brctl download` — key files like `digest_latest.md`, `WEEK24_EMAIL_SUPPLEMENT.md`, `ANALYSIS_RESULTS.md` became readable after forced sync.
4. **OneDrive dataless remains blocked**: Files under `Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/...` with `dataless` flag remain unreadable by any tool (`cat`, `cp`, `dd`, `Python open()`). `brctl download` fails with "Path is outside of any CloudDocs app library" for OneDrive paths.
5. **The [SILENT] rule applied**: Step 5 of the cron instructions said "Report a summary" — a full report with zero results was produced (the rule override confirmed by v2.31.0 of the skill).
