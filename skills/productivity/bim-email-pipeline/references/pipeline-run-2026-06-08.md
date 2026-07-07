# Pipeline Run — 08 Jun 2026 (Week 23)

## Context (Morning Run)
**Thursday morning cron execution.** User instructions explicitly demanded a report (step 5), so `[SILENT]` override applied.

## Results (Morning Run)

| Metric | Value |
|--------|-------|
| Outlook running | ✅ Yes |
| `download_mails.py` result | 0 new emails ("Everything is up-to-date!") |
| AppleScript failure | `Can't get default account. (-1728)` — persistent on New Outlook 16.109.1+ |
| Attachments in `mails/attachments/` | **208 files** (even though 0 new emails) |
| Already filed in BIM OneDrive | **168** (80.8%) |
| **New files copied to BIM** | **63** (40 unique + 50 site photos, some overlap) |
| Total data transferred | ~40.6 MB |

## Results (Afternoon Run — Override Pipeline)

| Metric | Value |
|--------|-------|
| `download_mails.py` result | 0 new emails, **found 1413 archived emails** (script worked from `scripts/` subdirectory) |
| AppleScript signal | `Can't get default account. (-1728)` — styled as **fail-fast pattern** (script continued, did not hang) |
| Attachments in `mails/attachments/` | **208 files** (unchanged from morning) |
| Already filed in BIM OneDrive | **187** (89.9% — up from 168 after morning run filed ~40 files) |
| **New files copied to BIM** | **3** (Leica BLK360 G2 SpecSheet, RTC360 DS, CloudWorx for Revit DS → `04_Specifications_and_BOQ/`) |
| **Files locked by macOS provenance** | **6** — cannot be read at all (EDEADLK); see Unrecoverable list below |
| Other project files (no target) | 12 (admin_hr, haramein_ghamamah, makkah_jabal_omar) |
| PROJECT_MEMORY.md | ✅ Write succeeded (no OneDrive lock) |
| Zamzam PROJECT_MEMORY.md | ❌ Locked (OneDrive sync, 2043-byte stub) |

### Unrecoverable Provenance-Locked Files

These 6 files have `com.apple.provenance` extended attribute and all copy tools fail (cat, cp, dd, ditto, rsync, shutil.copy2, `os.remove + cp -X`). **Do not retry in automated runs** — require manual Outlook re-export:

| File | Size | Target |
|------|------|--------|
| `general/technical_specifications/11-Leica Cyclone 3DR DS 897703 1121 en LR.pdf` | 3.4 MB | `04_Specifications_and_BOQ/` |
| `general/technical_specifications/13-Leica_CloudWorx_for_Navisworks_DS_en.pdf` | 323 KB | `04_Specifications_and_BOQ/` |
| `general/technical_specifications/9-Leica_CloudWorx_for_AutoCAD_DS_en.pdf` | 570 KB | `04_Specifications_and_BOQ/` |
| `general/technical_specifications/Artec Spider II.pdf` | 10.8 MB | `04_Specifications_and_BOQ/` |
| `general/schedules/Leica Cyclone REGISTER 360 PLUS DS 864328 0223 en.pdf` | 2.3 MB | `Design Files/00_Scope_and_Proposals/` |
| `general/schedules/Leica-Cyclone-REGISTER-360-BLK Edition-FLY-902865-0221-en-LR.pdf` | 1.4 MB | `Design Files/00_Scope_and_Proposals/` |

**Pattern:** All 6 are Leica/Artec product spec sheets and schedule PDFs. All were downloaded by a previous AppleScript run but the `com.apple.provenance` attribute prevents any read. These will remain stuck unless the user re-exports from Outlook or clears the attribute.

### CG Codes Added to PROJECT_MEMORY.md (Afternoon)

New entries not in the morning run's update:

| Document | Code | Date | Notes |
|----------|:----:|:----:|-------|
| MOC-MUS-ASE-1C0-IR-0002 (Temp Fence) | **B** ✅ | 4-Jun | Sundus Alfeer |
| MOC-MUS-ASE-1KH-PL-0045 (Heat Stress) | **B** ✅ | 2-Jun | Mohammad Elbaz |
| MOC-MUS-ASE-1KH-PL-0046 (Lifting Ops) | **C** ❌ | 2-Jun | Mohammad Elbaz |
| ZAM-NWC-MUM-SDR-STR-019 Rev.05 (Zamzam Exit Stair) | **Resubmit** ❌ | 4-Jun | EGEC |

### Critical Items Added (Afternoon)

- **EinScan LIBRE Demo**: TODAY Jun 8, 10AM AST — Teams with Khabab elamin (SITML)
- **Nissen Richards Studio**: Joshua Broomer on leave until Jun 9; CG 3D Render Code B forwarded, urgent: info@nissenrichardsstudio.com
- **CloudWorx for Revit**: 15-day eval license `00112-83549-00041-30595-B4265`
- **Leica BLK360 G2**: Special discount quotation from Ahmed Ali (SITML)
- **Aseer Weekly Meeting 11** (18-05-2026): minutes PDF filed

## CG Verdicts Found in 23.md

| Document | CG Code | Date | Reviewer |
|----------|:-------:|:----:|----------|
| ZD-0033 Rev.01 (3D Render) | **B** ✅ | 6-Jun | Hossam Mabrouk |
| PL-0043 Rev.01 (Temp Electrical) | **B** ✅ | 2-Jun | Mohammad Elbaz |
| PL-0045 (Heat Stress) | **B** ✅ | 1-Jun | Mohammad Elbaz |
| PL-0046 Rev.01 (Lifting Ops) | **B** ✅ | resolved | from Code C |
| PL-0018 Rev.01 (Comm. Plan) | **C** ❌ | 25-May | Mohammad Elbaz |
| ZD-0053 (HSE Induction) | **D** ❌ | 6-Jun | Anwar Sadat |
