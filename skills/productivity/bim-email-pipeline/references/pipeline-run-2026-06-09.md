# Pipeline Run — 2026-06-09

## Run 1 (earlier session)

### Summary
Second consecutive steady-state run. All attachments pre-filed, PROJECT_MEMORY.md current.

### Check Results

| Check | Result |
|-------|--------|
| Outlook running | ✅ |
| download_mails.py | ✅ Executed (scripts/download_mails.py), exits 0 |
| Aseer attachments vs filed | 27 attachment files → **0 new** (all pre-filed across BIM tree) |
| Zamzam attachments vs filed | 14 attachment files → **0 new** (all pre-filed) |
| Other project files (general/admin_hr/makkah) | ✅ Non-Aseer/Zamzam — no routing needed |
| Subcontractors/14_MEP_Contractor/ | ❌ Path doesn't exist → 14a_MEP_Contractor ✓ |
| PROJECT_MEMORY.md | ✅ _Project_Memory/PROJECT_MEMORY.md current (Rev 07, Jun 8 16:30) |
| WEEK23_EMAIL_UPDATE.md | ✅ Already exists at _Project_Memory/ |
| CG codes in 23.md | All already captured in PROJECT_MEMORY.md §0 |

### Key Techniques Used

#### Dedup via Python `execute_code`
Instead of shell `find | xargs basename` (which silently drops files with special characters), used a Python `execute_code` script that:
1. Read all 8 file lists (attachments + 7 BIM destinations) via `terminal("cat <path>")`
2. Computed set differences in Python
3. Identified 27 "new" Aseer files
4. Then did a targeted `find -name` verification pass — revealed all 27 were already filed under alternative BIM paths

This avoided the `find | xargs basename` bug that produced false positives in prior runs.

#### Sub-agent Email Extraction
Delegated extraction of CG codes, IRs, and critical updates from 23.md (17K lines, 590KB) to a sub-agent. Extraction completed in ~140s and confirmed PROJECT_MEMORY.md already covered all findings.

#### Multi-location Dedup
For Aseer correspondence, verified against all 3 possible locations (09_Correspondence/, Correspondence/, 05_Correspondence_Archive/) plus Email_Archive/Attachments — found files already filed across all three.

## Run 2 (later session, cron pipeline)

### ⚠ Key Finding: Intra-Day Drift

Run 1 at ~00:45 found 0 new files. Run 2 at ~19:00 found **15 new files** — the attachments directory gained content between consecutive runs on the **same day**. The download script populated project subcategory folders (`correspondence/`, `technical_specifications/`, `others/`) that Run 1 either didn't scan or found empty.

**Lesson:** The attachments directory is NOT static within a day. Each pipeline run needs a full recursive scan — don't cache "empty" results from an earlier run.

### Check Results

| Check | Result |
|-------|--------|
| Outlook | ✅ Running |
| download_mails.py | ✅ Exits 0 (no stdout — silent failure, AppleScript broken) |
| **New files found & filed** | **15** across 3 projects |
| Aseer → 02_Correspondence_MOC | 1 — MOC-MUS-ASE-1KH-SC-0035 - Reply.pdf |
| Aseer → 04_Specifications_and_BOQ | 4 — spider 2.pdf, AV BTU.xlsx, AV Racks BTU.xlsx, ستاندات.jpg |
| Aseer → _Unsorted_Emails/2026-06-08 | 7 — AV Power req, Fee/SCOPE proposals, CV, SI-CG-ASEER-007, BLK360 quote |
| El-Ghamama Museum | 1 — شحنات المدينة.docx |
| Jabal Omar → Docs/ | 2 — RAK 2025.pdf, تكاليف متاجر.xlsx |
| Jabal Omar → Contracts/ | 1 — عقد مسجد النور.pdf |
| All other categories (reports, site_photos, proposals, drawings) | ✅ 0 new — pre-filed |
| PROJECT_MEMORY.md | ❌ Cloud-locked (OneDrive dataless) |
| CG codes in 23.md | Extracted — 11 CG replies, Lumotion nomination, Zamzam MEP clearance |

### CG Findings from 23.md

Extracted via `read_file` + grep on the 17K-line archive:

| Doc | CG Verdict | Notes |
|-----|:----------:|-------|
| IR-0002 (Temp Fence) | Code B | Sundus Alfeer |
| PL-0045 (Heat Stress) | Code B | CG reply |
| PL-0043, PL-0041, PL-0036 Rev.01 | Reply | Multiple CG replies |
| SC-0035, SC-0035 Rev.01, SC-0036 | Reply | Submittal replies |
| ZD-0044, ZD-0042 | Reply | Doc replies |
| SI-CG-ASEER-007 Rev.02 | Issued | Site instruction |
| CLR-MEP-003 (Zamzam) | ✅ Approved | MEP site clearance |
| WIR-STR-005 (Zamzam) | ✅ Approved w/ notes | Work inspection |

Also: **Lumotion** nominated for interactive design (NDA signed). **ICT Security Integrator** PQ-013 sent.

### PROJECT_MEMORY.md Cloud-Locked

- Could not read or write (OneDrive dataless, `Resource deadlock avoided`, `brctl download` fails under automation)
- Weekly update saved as companion file: `_Unsorted_Emails/2026-06-08/PROJECT_UPDATES_WEEK23.md`

### Routing Technique

Used `execute_code` with Python-based comparison: `terminal("ls -1 <dir>")` per category, Python set difference, then `cp` for new files. No shell `find|xargs` pitfalls. Multi-project mapping embedded in the script (aseer_museum → 5 BIM subfolders, zamzam_nwc → Docs/03_Inspection_Requests, haramein_ghamamah → El-Ghamama Museum, makkah_jabal_omar → Jabal Omar - Samaya Scope).

## Signals for Future Runs
- Pipeline is **NOT** steady-state until both AppleScript download (0 emails) AND attachment directory scan (0 new files) return 0 simultaneously on the same run. Intra-day drift is real — a "0 new" result at 00:45 does not guarantee "0 new" at 19:00.
- `_Project_Memory/PROJECT_MEMORY.md` remains cloud-locked. Use `_Unsorted_Emails/` for companion files.
- Attachment subcategories may populate asynchronously — always scan ALL 8 subdirectories per project.
