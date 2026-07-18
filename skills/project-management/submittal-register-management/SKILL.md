---
name: submittal-register-management
title: Submittal Register Management
description: Create, clean, and manage BIM submittal registers with stage-date columns (50%/90%/100%/IFC), category-staggered scheduling, and OneDrive deployment. Covers the standard 9-column template, date- vs mask-based formats, regenerative repair, and OneDrive-safe file handling for Aseer Museum and similar projects.
trigger: user asks to create/clean/organize a submittal register, add dates, fix columns, or regenerate .xlsx from .py
tags: [bim, submittal-register, aseer, openpyxl, excel, schedule]
---

## RFI/TQ Register — Status Semantics

**Critical rule: RFI status = whether CG answered, not the folder it sits in.**

| Status | Meaning |
|--------|---------|
| OPEN | Submitted, no CG answer yet |
| CLOSED | CG answered (any outcome) |
| REJECTED | CG rejected the query itself |

Never use "PENDING APPROVAL" or "PENDING REVIEW" — those describe folder state, not answer state. An RFI in an "Approval/" subfolder is still OPEN until CG responds.

See `references/rfi-register-design.md` for the full pattern: column design, revision handling, Adel's folder bank cross-check, and naming anomalies to watch for.

## AV Prequalification Package Handling

When processing AV equipment supplier prequalifications (suppliers to Rawasin, the AV contractor):

### Document Organization

File under `04_Submittals/AV/` with three subfolders: Prequalifications/, Product_Datasheets/, Scope_of_Work/.

### Submittal Statement Format (to CG)

Keep statements **very short** — the user explicitly rejected verbose framing. Format:

> This prequalification complies with the project [specifications/AV design]. Equipment types and technical specs match the approved design.

**Details:**
- Supplier: [Name] ([Brand] authorized distributor — KSA)
- Contractor: [Main contractor name]
- Proposed Ref: MOC-MUS-ASE-1K0-PQ-XXXX

**Provided files:**
1. [File 1]
2. [File 2]
...

Do NOT add explanations about quantity variances, compliance analysis, or background context in the statement itself. Those go in the email draft to the DC, not the CG submittal statement.

The user explicitly corrected: "dont talk too much, you can just mention as package" and "tell this prequalification complay with projects specs please submit the prequalification under datils : and write the statment here , with the provid files"

### Register Tracking

Add new items to the **In Preparation** section at the top of `01_Registers/submittal_register.md`:

| Ref | Subject | Discipline | Status | Notes |
|-----|---------|------------|--------|-------|
| MOC-MUS-ASE-1K0-PQ-00XX | [Supplier] [Product] Prequalification | AV | **In Preparation** | Supplier to [contractor]. Equipment: [list]. Complies with [design]. |

### Repo Rule: Markdown-Only

The project repo is **markdown-only**. Never copy binary files (PDFs, xlsx, images) into the repo. Instead:
- Create a `.md` summary with YAML frontmatter + OneDrive source path
- Reference the original file by its OneDrive path
- Cross-link to related files in the repo

### Register Tracking

Before submitting to Aconex, track packages in a dedicated "In Preparation" section at the top of the submittal register with status **In Preparation**.

### Compliance Check

Compare supplier scope against the DHD AV design. Qty variances are procurement issues to reconcile with Rawasin. Equipment type and technical spec compliance is what matters for prequalification approval.

### Known AV Suppliers (Aseer Museum)

| Supplier | Brand | Equipment | Role |
|----------|-------|-----------|------|
| NMK | Q-Sys | Core 510i DSP, TSC-50-G3, TSC-70-G3 | Supplier to Rawasin |
| Adawliah | Yamaha | VXC6, VXS8, XMV8140-D | Supplier to Rawasin |

# Submittal Register Management

## Standard Template

### Column Layout
```python
hdrs = ['Ref #', 'Submittal / Deliverable', 'Discipline', '50%', '90%', '100%', 'IFC/AFC', 'Sub-Package', 'Remarks']
cww  = [7, 50, 14, 14, 14, 14, 14, 22, 28]
```

### Item Tuple Format
```python
(ref, description, discipline, [date_50, date_90, date_100, date_ifc], sub_package, remarks)
```

- Date format: `'29/06/2026'`
- `'—'` (em-dash) = N/A at that stage
- Items with `'—'` for a stage are hidden from that stage's sheet

### Stage Sheets
4 sheets: `50% Design`, `90% Design`, `100% Design`, `IFC AFC Construction`

Each sheet only shows its own stage's date. Other stage columns show `'—'`:
```python
show_dates = ['—','—','—','—']
show_dates[stage_idx] = dates[stage_idx]
vs = [ref, desc, disc, show_dates[0], show_dates[1], show_dates[2], show_dates[3], spkg, rm]
```

### Category Grouping
```python
cn = {1:'A — CATEGORY NAME', ...}
cn_keys = sorted(cn.keys())
next_cat = {k: cn_keys[i+1] if i+1 < len(cn_keys) else 999 for i, k in enumerate(cn_keys)}
# In loop:
grp = [it for it in its if int(it[0].split('-')[1]) >= rn and int(it[0].split('-')[1]) < next_cat[rn] and it[3][si] != '—']
```
Use `next_cat` dict instead of hardcoded range formulas to handle non-uniform category sizes.

## Stage-Columns Purpose

The 50%, 90%, 100%, IFC columns hold **planned submission dates**, NOT stage indicators:

| Column | Holds |
|--------|-------|
| 50% | Date of 50% submission |
| 90% | Date of 90% submission |
| 100% | Date of 100% submission |
| IFC/AFC | Date of IFC/AFC submission |
| `—` | This stage does not apply |

Items appear in a sheet only if their date for that stage is NOT `'—'`.

## Staggered Scheduling Pattern

Group items by category/floor/package. Each successive category gets +7 days for review buffering:

```python
cat_bases = {
    'Cat A': '29/06/2026',
    'Cat B': '06/07/2026',  # +7d
    'Cat C': '13/07/2026',  # +14d
}
# Per item within category:
d50 = base_date
d90 = add_30_days(d50)    # e.g. '29/07/2026'
d100 = add_30_days(d90)   # e.g. '28/08/2026'
difc = '28/08/2026'       # fixed IFC target
```

### IFC-Only Items
QA/Commissioning/Handover items: `['—','—','—','28/08/2026']`

### Per-Floor Architecture Submission

User submits Architecture drawings by floor, NOT all at once. 4 floors staggered +7d:

| Floor | 50% Date | 90% Date (+30d+7d) | 100% (+60d+14d) |
|-------|----------|-------------------|-------------------|
| BF (Basement) | 29 Jun | 06 Aug | 12 Sep |
| LGF (Lower Ground) | 06 Jul | 13 Aug | 19 Sep |
| GF (Ground Floor) | 13 Jul | 20 Aug | 26 Sep |
| 1F (First Floor) | 20 Jul | 27 Aug | 03 Oct |

**3D Viz** is submitted in 2 batches (not per-floor):
- Batch 1 (BF+LGF): 29 Jun (same day as BF drawings)
- Batch 2 (GF+1F): 02 Jul (separate from GF/1F drawings)

Keep "Visualisation Location Plans (1210)" per-floor — those are actual drawing sheets. Only batch the "3D Visualisation Shots" (renders/presentations).

## No Icons or Emoji — Hard Rule

**NEVER** use emoji, Unicode symbols, or icon characters in formal deliverables:
- Status indicators (⏳ ✅ ❌ 🟡 🟢 🔴 ⚠️ ★)
- Stage header prefixes (▲ ◆ ● ●)
- Geometric shapes or dingbats (■ □ ✓ ✗)
- Any character in Unicode ranges U+1F300-U+1F9FF, U+25A0-U+25FF, U+2700-U+27BF, U+2600-U+26FF, U+23F0-U+23FF, U+2500-U+257F (box drawing), U+2580-U+259F (block elements), U+2B00-U+2BFF (misc symbols and arrows)
- Real catches in this session: U+2500 `─` (box drawing in Landscaping comments), U+2550 `═` (double line in Master script separators), U+2588 `█` (full block in Master legend), U+23F3 `⏳` (hourglass user called out), U+2705 `✅` (checkmark in dashboard data)

**Use plain text only:**
- ❌ `⏳ Pending client data` → ✅ `BLOCKED — pending client data (RFI sent Jun 2026)`
- ❌ `✅ Complete` → ✅ `Complete`
- ❌ `🟡 Design coord` → ✅ `Design coordination in progress`

**If user calls you out for adding an icon** (happened: added ⏳ icon after being told no icons), immediately:
1. Remove icon from source .py — replace with plaintext
2. Scan ALL .py scripts in `_scripts/` for residual icons across ALL unicode ranges listed above
3. Regenerate all affected .xlsx
4. Deploy to OneDrive
5. Verify by loading xlsx and checking cell values for residual Unicode symbols
6. Apologize — icons don't belong in formal project documents

### Cleanup Verification
```python
# Scan for icons in .py scripts
icon_ranges = [(0x25A0, 0x25FF), (0x2700, 0x27BF), (0x1F300, 0x1F9FF), (0x2600, 0x26FF), (0x23F0, 0x23FF)]
for fname in os.listdir(scripts_dir):
    with open(f) as fh:
        for c in fh.read():
            cp = ord(c)
            for lo, hi in icon_ranges:
                if lo <= cp <= hi:
                    # FOUND — remove and regenerate
```

### Full Icon Cleanup Protocol

When removing icons from scripts:

1. **Remove stage header icons** in the stage-loop header line:
   ```python
   # BEFORE (has ▲):
   c.font = Font(...'\\\\u25b2' + pn...)
   # AFTER (clean):
   c = ws.cell(row=row, column=1, value=pn)
   ```
2. **Remove emoji/status markers** from data strings — replace ✅ with `[OK]`, ⏳ with `BLOCKED`, 🔴🟡🟢 with plain text status.
3. **Remove box-drawing chars** from comment separators: `─` → `-`, `═` → `=`, `█` → `##`.
4. **Regenerate xlsx** after cleaning .py scripts and deploy to OneDrive.
5. **Verify** all Python files compile with `compile(content, fp, 'exec')`.
6. **Verify xlsx** by loading with openpyxl and checking for residual Unicode in icon ranges.

### Comprehensive Unicode Scan Ranges

When scanning scripts for icons, check ALL of these ranges (not just emoji):

```python
icon_ranges = [
    (0x25A0, 0x25FF),   # Geometric Shapes ■□▲▼◆○ etc
    (0x2600, 0x26FF),   # Misc Symbols ☀★☎☠☹⚠ etc
    (0x2700, 0x27BF),   # Dingbats ✀✁✂✓✗✘✙✚ etc
    (0x2B00, 0x2BFF),   # Misc Symbols and Arrows ⬤⭐ etc
    (0x1F000, 0x1FFFF), # Emoji 🟠🟡🟢🔴🟣 etc (includes 1F300-1F9FF)
    (0x2300, 0x23FF),   # Misc Technical ⌂⌃⌄⌅⏳ etc
    (0x2500, 0x257F),   # Box Drawing ─│┌┐└┘
    (0x2580, 0x259F),   # Block Elements ▀▄█▌▐
    (0xFE00, 0xFE0F),   # Variation Selectors
    (0x200D, 0x200D),   # Zero Width Joiner
]
```

For each file, iterate through all characters and flag any whose codepoint falls in any of these ranges. Fix by replacing the character with its plain-text equivalent.

## Before-Category Preliminary Items

To insert an item BEFORE the first category (e.g., Digital Material Board before Basement Floor DD):

1. Start `ref` counter at `0` instead of `1`:
   ```python
   its = []; ref = 0
   its.append((f'AR-{ref:03d}', 'Digital Material Board — Basement Floor', ...))
   ref += 1
   ```
2. Add category entry at key `0`:
   ```python
   cn = {0:'PRELIMINARY — DIGITAL MATERIAL BOARD', 1:'A — BASEMENT FLOOR', ...}
   ```
3. `next_cat` dict handles non-uniform category sizes automatically.

This produces `AR-000` which sorts before `AR-001`.

## OneDrive Folder Name Changes

OneDrive may rename folders by adding an underscore prefix (e.g., `scripts/` → `_scripts/`) during sync. Always verify folder exists before batch operations:

```python
import os
scripts_dir = '/path/to/scripts'
if not os.path.isdir(scripts_dir):
    # Try underscore-prefixed version
    alt = os.path.join(os.path.dirname(scripts_dir), '_' + os.path.basename(scripts_dir))
    if os.path.isdir(alt):
        scripts_dir = alt
```

## Batch Date Shifting Workflow

To shift all dates across all register scripts by N days:

1. **Python regex replace** on all .py files:
   ```python
   date_pat = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
   def shift(m):
       d, mon, y = int(m[1]), int(m[2]), int(m[3])
       return (datetime(y, mon, d) + timedelta(days=N)).strftime('%d/%m/%Y')
   ```
2. **Run each .py script** to regenerate its .xlsx
3. **Copy .xlsx to OneDrive** via Finder (AppleScript)
4. **Verify** — check a sample date in the first data row

Note: Scripts save to `/tmp/` or `/tmp/DATED_REGISTERS/` — inspect the save path before copying. Some scripts use non-standard filenames (e.g., `FFE_Dated.xlsx` vs `FFE_Submittal_Register.xlsx`).

## Column Widths Standardisation

Standard widths for all register sheets (matching Arch template):
```python
COL_WIDTHS = {'A': 32, 'B': 55, 'C': 14, 'D': 10, 'E': 10, 'F': 10, 'G': 10, 'H': 22, 'I': 28}
```
When standardizing widths across all registers, update generator scripts and regenerate:

```bash
sed -i '' 's/cww = \[[^]]*\]/cww = [7, 50, 14, 14, 14, 14, 14, 22, 28]/' *.py
for f in *.py; do python3 "$f"; done
```

Then copy regenerated .xlsx to OneDrive.

## Critical Pitfalls

### Column Cleanup — Exact Header Match Only
**NEVER** use substring matching (`'SOW' in header`) to identify columns for removal. The header `'Submittal / Deliverable (per SOW)'` contains "SOW" as a substring but is NOT a SOW column — it's the deliverable description.

**CORRECT:** match exact header strings:
```python
sow_er_headers = {'SOW §', 'ER §', 'ER §b', 'SOW', 'ER'}
if str(cell.value).strip() in sow_er_headers:
    # Safe to remove this column
```

### OneDrive File Saves
NEVER write files directly to OneDrive CloudStorage paths — produces corrupt placeholder files. ALWAYS stage to `/tmp/` first, then use AppleScript Finder duplicate:
```applescript
tell application "Finder"
    set src to POSIX file "/tmp/{filename}"
    set destFolder to POSIX file "{oneDrivePath}/"
    duplicate src to destFolder with replacing
end tell
```

### Data Tuple Regeneration
When .py generator scripts get corrupted (broken tuples from comma-in-string issues):
- DON'T try to repair individual tuples with regex — too error-prone
- Find original data from session history (`session_search`)
- OR rebuild data from .xlsx using `openpyxl`
- OR regenerate from a clean template with known-correct data

### Date Format in openpyxl — Objects vs Strings

When writing stage dates to cells, use `datetime.date` objects with `number_format='DD/MM/YYYY'` — Excel handles these as real dates. **Do NOT write preformatted strings** like `'29/06/2026'` — Excel treats them as plain text and they won't sort/filter as dates.

But date objects cannot mix with `EM` (em-dash `\u2014`) in the same cell sequence. Build display lists conditionally:
```python
show_dates = [EM, EM, EM, EM]
show_dates[stage_idx] = dates_raw[stage_idx]
# Convert any date objects to formatted strings before passing to openpyxl
show_dates = [d.strftime('%d/%m/%Y') if isinstance(d, date) else d for d in show_dates]
```

The `read_file` tool shows `date` values as serial numbers (e.g. `46202`) — this is a display quirk; they render correctly in Excel with DD/MM/YYYY format.

### Date Shifting
To shift all dates across scripts by N days:
```python
import re
from datetime import datetime, timedelta
date_pat = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
def shift(m):
    d, mon, y = int(m[1]), int(m[2]), int(m[3])
    return (datetime(y, mon, d) + timedelta(days=1)).strftime('%d/%m/%Y')
```
Then run each script to regenerate .xlsx.

## Register Deletion Workflow

When a register's scope is fully covered by another (e.g., Exhibition Fit-Out → Architecture):

1. **Verify** the target register covers ALL items (do a side-by-side comparison)
2. **Delete folder + xlsx**:
   ```bash
   rm -rf "/path/to/04_Registers/Register_Name"
   ```
3. **Delete .py script**:
   ```bash
   rm -f "/path/to/04_Registers/_scripts/Register_Name.py"
   ```
4. **Note it in session** so the user knows it's gone

## Register Scope Decisions

> Full object/schedule data for Aseer subcontractors: see `references/aseer-object-schedules.md`
> Dependency-based scheduling table: see `references/aseer-logic-map.md`
> Per-register internal dependency tier analysis: see `references/aseer-dependency-tiers.md`
> Aconex transmittal sync from Outlook (4x daily cron, dedup logic, SQLite query): see `references/aconex-outlook-sync.md`

> Approval Authority default (CG) + AV template copy approach + FLS categorization: see `references/aseer-approval-authority-and-template.md`
> Submission calendar (live dates): see `references/aseer-submission-calendar.md`
> Structural register worked example (39 items, 5 categories, 4 tiers): see `references/aseer-structural-register-pattern.md`
> Master Plan generator script: `scripts/master_submission_plan.py`
> Appending submission plan sheets to existing register: `references/appending-submission-plan-sheets.md`
> Icon cleanup scanner: `scripts/scan_icons.py` — run it against any `_scripts/` directory to verify zero icons
> Gates plan gap analysis (Aseer Mech cross-reference): see `references/gates-plan-gap-analysis.md` — raw comparison data with per-system numbering ranges, stage-mismatch items, and the audit script

### What NRS (Architecture Register) Covers
- GA plans, sections, elevations (all levels)
- Specifications
- BIM Model
- General arrangement drawings
- Material presentations
- **Graphic signage/wayfinding** — NRS scope
- Showcase schedules, object mount schedules (coordination)
- Models & Replicas schedules (coordination)

### What Needs Separate Registers
- **Graphic content & design** — separate contractor (not NRS)
- **Showcases** — standalone specialist package
- **Models & Replicas** — standalone Model Maker package
- **Interactives** — standalone specialist package
- **AV/IT** — standalone specialist
- **Lighting** — standalone designer
- **Fire Life Safety** — standalone specialist
- **MEP** — standalone engineering package

### FFE Register Purpose
FFE register should track **vendor procurement**, not design:
- Vendor prequalification documents
- Catalogs, brochures, product cut sheets
- TDS (Technical Data Sheets), MSDS
- Samples, finish swatches, color boards
- Compliance certificates, warranties, O&M
- NOT FFE design/schedules — NRS covers that in Architecture register

**Scope:** Only loose furniture (from BOQ 004. Furniture). Fixed/bespoke items are joinery scope.

**Structure:** By BOQ zone (Lobby, VIP, Children's Ed, Café/Terrace, Circulation, Library).
Zones staggered +7d. Each product in a zone tracks 7 procurement steps (Catalog → TDS → Cut Sheet → Sample → Compliance → Warranty → O&M).

### Interactives Register
- **Source:** `24_Subcontractors/09_Interactive_Design_Contractor/01_Schedule_and_BOQ/6930_Aseer_Tactile & Manual Interactives Schedule.xlsx`
- **Items:** 6 actual interactive objects from the schedule (Manual, Tactile, Hybrid types)
- **Categories:** By object (Architecture Interactive, Making Space, Al Qatt, Sensory Smell, Archaeology Touch, Archaeology Rubbing)
- **Start date:** 15/07/2026, staggered +7d per object
- **Steps per object:** Concept Approval → Material Approval → Prototype → Production → QC → Installation → QA → O&M

### QA / Commissioning / Handover Consolidated Register
Create a single tracking register for all packages' close-out items:

**8 common items per package (all IFC-stage):**
1. Material Submittals — product data sheets, certifications
2. ITP — Inspection & Test Plan
3. AFC Documentation — Designer certification
4. Commissioning Reports
5. Record Drawings / As-Built
6. O&M Manuals
7. Training for MoC
8. Spares (1-year period)

**Structure:** One row per package per item type, organized by package as categories.

## Pre-Build — Check Existing Deliverables First (OneDrive/Project Files)

**CRITICAL workflow step:** Before creating ANY register from template defaults, always check the actual project files for existing deliverables. Template defaults assume nothing is done — this is often wrong.

### Workflow

1. **Check OneDrive project folders** — look for the structural/design discipline directory under `03_Design_Files/` for:
   - **BOD Reports** (Basis of Design) — already submitted documentation
   - **Loading Plans** — DWG/PDF files per floor
   - **Existing structural reports** — SD Reports, Design Philosophy docs, schematic design reports
   - **Specifications** — demolition, material specs
   - **As-Built drawings** — existing building record drawings
   - **Steel stairs** — check if shop drawings already exist (GA, SAP2000, Tekla, CNC, calc notes)

2. **Mark completed items as amber** — in the xlsx generator, set `cell.fill = AMBER` for rows that already exist. Use actual submission dates, not planned dates.

3. **Refine scope based on what exists** — don't list stairs as "new design" if shop drawings already exist. Don't list reports as pending if they're already filed. Adjust the register items to reflect current status.

### Completed Item Pattern

```python
AMBER = PatternFill('solid', fgColor='FFF4B942')
REM = 'Submitted'

its.append(('ST-001', 'BOD Report — 17p (26 Jun 2026)', 'Structural',
    d(2026,6,26), EM, EM, EM, 'Design', f'{REM}'))

# In the sheet-writing loop:
if 'Submitted' in str(rm) or 'Submitted' in str(desc):
    cell.fill = AMBER
```

This pattern produces amber-highlighted rows with actual dates in the 50% column and `Submitted` in Remarks — clearly distinguishable from white pending rows.

### Examples of Existing Deliverables to Check (Aseer Museum Structural)

| Item | Where to Check | File Pattern |
|------|---------------|-------------|
| SD Report | `03_Design_Files/*/Structural/Report/` | `*SD Report*Rev*.pdf` |
| Design Philosophy | `03_Design_Files/*/Structural/` | `*Design Philosophy*` or `*Structural Philosophy*` |
| BOD Report | `03_Design_Files/26_Structural/` | `*BOD*Report*.pdf` |
| Loading Plans | `03_Design_Files/26_Structural/` | `Loading_Plans*/` |
| Structural Drawings | `03_Design_Files/*/Structural/Drawings/` | `BH3092-*.pdf` or `*DRG-ST-*.pdf` |
| Steel Stairs | `03_Design_Files/*/Structural/New Steel Staires WD/` | `Stair With 2 Flights/`, `Stair With 3 Flights/` |
| Specifications | `03_Design_Files/*/Structural/Specifications/` | `*.pdf` |
| As-Built Drawings | `03_Design_Files/*/Structural/As-Built/` | `STRUCTURE/`, `Arch/` |

## Gallery-Specific Structural Items (per Design Philosophy)

For disciplines like Structural that have gallery-specific modifications, create items per-floor per-gallery based on the Design Philosophy document (usually prepared by LON or similar consultant).

### Workflow

1. **Extract by-floor items** from Design Philosophy document — each gallery/commission typically needs its own structural support design
2. **Assign per-floor stagger** — Basement starts at baseline, LGF +7d, GF +14d, 1F +21d, etc.
3. **Use mk() with start override** for staggered per-floor items

### Example (Aseer Museum Structural — from LON Design Philosophy P02)

```python
# Per-floor gallery items with staggered starts
BASE = d(2026, 6, 29)

# Basement
its.append(mk('ST-019', 'G7 — Contemporary Art Commission support (BF)', 'Structural', 2, 'BF Galleries', 'Needs Arch GA'))
its.append(mk('ST-020', 'G12 — Tom Nicholson Art Commission support (BF)', 'Structural', 2, 'BF Galleries', 'Needs G7 complete'))
its.append(mk('ST-021', 'CL1 — New stairs structural integration (BF)', 'Structural', 2, 'BF Galleries'))

# LGF (+7d from baseline)
lgf_start = BASE + timedelta(days=7)
its.append(mk('ST-022', 'G14 — Contemporary Art Commission support (LGF)', 'Structural', 2, 'LGF Galleries', '', start=lgf_start))
its.append(mk('ST-023', 'TG — Opening in external wall assessment (LGF)', 'Structural', 2, 'LGF Galleries', '', start=lgf_start))

# GF (+14d)
gf_start = BASE + timedelta(days=14)
its.append(mk('ST-024', 'CL1 — Lobby Hanging Artwork suspension (GF)', 'Structural', 2, 'GF Galleries', 'Ceiling point loads', start=gf_start))
its.append(mk('ST-025', 'LB1 — Lobby Artwork Commission support (GF)', 'Structural', 2, 'GF Galleries', '', start=gf_start))

# 1F (+21d)
f1_start = BASE + timedelta(days=21)
its.append(mk('ST-026', 'CL1 — Ramp modifications (1F)', 'Structural', 2, '1F Galleries', '', start=f1_start))
its.append(mk('ST-027', 'CA2 — Terrace Balustrade support (1F)', 'Structural', 2, '1F Galleries', '', start=f1_start))
```

## Data Sourcing Priority

When creating or updating a submittal register, check these sources IN ORDER — earlier sources are more authoritative:

1. **Subcontractor folder** (`24_Subcontractors/<package>`) — check for existing `*_Submittal_Register/` folder with `.xlsx`. That register may already have the full item list with sub-packages and stage assignments. Use it as reference.
2. **Subcontractor Schedule/BOQ** (`24_Subcontractors/<package>/01_Schedule_and_BOQ/`) — actual procurement schedules, BOQ extracts, and replica/object schedules. These show what items are actually priced and scoped.
3. **Master BOQ** (`05_BOQ/`) — the canonical BOQ has every priced line item. Sheet names correspond to work packages. Use for cross-checking scope boundaries.
4. **NRS Tender Package** (`14_Completed_Tender_Package_From_NRS/`) — design drawings and specs define NRS-scoped items (which go in Architecture register, NOT subcontractor registers).
5. **Previous register** (fallback) — only if none of the above exist.

**Verification:** After writing items from source data, spot-check against the BOQ sheet for that package. Every priced line item should be traceable to a register item (or explicitly noted as design-only in Architecture).

## No-Dates Pattern (RFI Pending / Client Data Pending)

When a register's items depend on client-provided research, data, or object lists that are still pending, use **stage markers** instead of dates.

**Column widths** — narrower for stage columns when showing markers instead of dates:
```python
cww = [7, 55, 14, 7, 7, 7, 10, 22, 28]  # stage cols ~7 chars (markers), not 14 (dates)
```

```python
# Mask-based approach (dates are blank):
# Stage columns show blank if applicable, '\\u2014' (em-dash) if not
mask = [1, 1, 0, 0]  # [50%, 90%, 100%, IFC] — 1 = applicable, 0 = not
vs = [ref, desc, disc,
      '' if mask[0]==1 else '\\u2014',
      '' if mask[1]==1 else '\\u2014',
      '' if mask[2]==1 else '\\u2014',
      '' if mask[3]==1 else '\\u2014',
      spkg, rm]
```

- **Legend sheet** must note: `"Dates TBC — RFI raised to client for research/data."`
- Stage headers remain the same (`50% Design`, `90% Design`, etc.)
- Each sheet only shows items applicable to that stage
- Apply to: **Graphics** (client content research pending), **Model Maker** (object/research data pending)
- Do NOT apply to **Interactives** — has its own start date (15/07/2026) even though content research may be pending; user specifically set a timeline

## FLS Register Full Replacement Pattern

When a subcontractor already has a real submittal register (at `24_Subcontractors/<package>/<Package>_Submittal_Register/`):

1. **Extract all items** from the subcontractor's xlsx (openpyxl data_only=True)
2. **Keep exact refs, descriptions, sub-packages** — these are the canonical items
3. **Remove SOW/ER columns** (not in our 9-column template)
4. **Add planned dates** using staggered schedule per category
5. **Keep original categories** as they are (don't rename to generic letters)
6. **Output** → 04_Registers/ folder replacing any previous version

**Example (FLS):** Subcontractor register had 36 items (FL-001 to FL-036) across 7 categories (FLS Strategy, Active FP, Passive FP, Coordination, Commissioning, QA/Commissioning, Handover). Kept all refs and descriptions verbatim, just removed SOW/ER cols and added dates.

## Internal Register Dependency Tiering

Within a single register, items have internal dependencies — you can't design before surveying. Use a **tier system** with staggered start dates per tier:

### 4-Tier Model (Survey → Design → Coordination → IFC)

**Special case — BIM models:** All BIM items (Arch, MEP, FLS, Structural Existing) start AFTER survey completion, not at the project baseline. The cloud survey, dilapidation, and as-built review must be done first to have accurate geometry.

Per the BEP (`00-BIM-Execution-Plan-REV 01.docx`), BIM deliverables are split into **Existing Conditions Model** and **Scope/Design Model** per discipline:

| Discipline | Existing (LOD 300) | Scope/Design (LOD 300→350→500) |
|------------|-------------------|-------------------------------|
| Architecture | BIM — Existing Conditions Model | BIM — Scope / Design Model |
| Structural | BIM — Existing Conditions Model | BIM — Scope / Design Model |
| MEP | BIM — Existing Conditions Model | BIM — Scope / Design Model |
| FLS | — (included in design model) | BIM — FLS Design Model |
| AV | — | BIM — AV Design Model |

**Existing Conditions Models:** Start 15 Jul (after cloud survey data available), only go to 90% (LOD 300 handoff). No 100% or IFC dates.

**Scope/Design Models:** Start 15 Jul, run through 90%, 100%, and IFC (LOD 500).

**Other BIM activities per BEP:**
- **Clash Detection:** Weekly, starts before 100% stage, runs parallel with 90%. Track as a recurring activity in Master Plan, not as a line item in discipline registers.
- **4D Planning:** Weekly schedule integration. Track separately from design BIM deliverables.
- **BIM Uses (from BEP Table 9):** 3D Architectural/Structural/MEP Existing + Designed Modeling, Clash Detection, Quantity Take-off, 4D Planning, Construction Documentation, As-Built Model, FM/COBie Model.

**Reference:** BEP document at `04_Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/01_Source_Files/03_Word/00-BIM-Execution-Plan-REV 01.docx`

No register should have BIM starting at 29 Jun. Move BIM items to Tier 2 start date (e.g., 27 Jul or 15 Jul per BEP timing) to ensure survey data is available.

```python
# Define date tiers at top of script
def mk(ref, desc, disc, tier, spkg, rm=''):
    dates = {
        1: ['29/06/2026', '29/07/2026', '28/08/2026', M],  # Tier 1: Immediate — criteria, load estimates, surveys
        2: [M,           '29/07/2026', '28/08/2026', M],  # Tier 2: Needs Arch GA/Structural survey — layouts, system design
        3: [M,           M,            '28/08/2026', M],  # Tier 3: Needs all disciplines — coordination, installation details
        4: [M,           M,            M,            IFC], # Tier 4: IFC only — submittals, ITP, AFC, O&M, Record Drawings
    }
    return (ref, desc, disc, dates[tier], spkg, rm)

its.append(mk('ST-001', 'Dilapidation survey — full building condition survey', 'Structural', 1, 'Survey'))
its.append(mk('ST-004', 'Slab and weight loading assessment', 'Structural', 2, 'Assessment', 'Needs ST-001/002/003'))
its.append(mk('ST-007', 'Ceiling support system design', 'Structural', 3, 'Design', 'Needs assessment + Arch GA'))
```

### Structural Register Pattern (applies to any survey->design register)

> For museum fit-out projects with gallery-specific items, see `references/structural-gallery-per-floor-pattern.md` — the per-floor per-gallery item generation pattern with staggered start dates.

| Category | Items | Tier | Date | Remarks Column |
|----------|-------|------|------|----------------|
| A — Surveys | Dilapidation, cloud survey, as-built review | 1 (Immediate) | **29 Jun** | 'Immediate' |
| B — Assessment | Loading, criteria, site report | 2 (After surveys) | **29 Jul** | 'Needs ST-001/002/003' |
| C — Detailed Design | Ceiling, sunshade, balustrade | 3 (After assessment) | **28 Aug** | 'Needs assessment + Arch GA' |
| D — IFC/Handover | Reinforcement, anchoring details, ITP, AFC, Record | 4 | **IFC** | '' |

The Remarks column documents WHY a date is later — serves as visible dependency flag in the register.

### MEP Register Tier Pattern (applies to any discipline with criteria→layouts→coordination)

- **Tier 1** (29 Jun): Design criteria documents, cooling/heating load estimates, BIM model start
- **Tier 2** (29 Jul): All system layouts (power, HVAC, FF, plumbing, lighting, BMS, low current) — need Arch GA + structural survey completion
- **Tier 3** (28 Aug): Coordination drawings, installation details, cross-trade integration — need all other discipline layouts
- **Tier 4** (IFC): Submittals, ITP, AFC, commissioning, O&M, Record Drawings

### How to Apply

1. **Analyze** — for each register, identify which items can be submitted immediately (method statements, design criteria, surveys) vs items that need inputs from other disciplines
2. **Assign tier** — Tier 1 = immediate, Tier 2 = needs base building defined, Tier 3 = needs all disciplines, Tier 4 = IFC only
3. **Use Remarks** to document blockers (e.g., "Needs Arch GA", "Needs client object list", "Needs MEP power requirements")
4. **Stagger** — within each tier, categories can still have +7d per-category stagger for review buffer

### When NOT to Use Tiering
- Registers that track production objects (Model Maker, Graphics, Interactives, Showcase) — each object/prototype follows its own timeline, not a survey→design→coordination chain
- Client-dependent registers (Graphics, Model Maker) — no dates at all
- Architecture — organized by floor/category with all items starting at the same per-floor 50% date

### Recommended mk() Helper Pattern

```python
def mk(ref, desc, disc, tier, spkg, rm=''):
    dates = {
        1: [s, add30(s, 1), add30(add30(s, 1), 1), M],  # Immediate: criteria, surveys
        2: [M, s + timedelta(days=30+REVIEW), s + timedelta(days=60+2*REVIEW), M],  # Survey-dependent
        3: [M, M, s + timedelta(days=60+2*REVIEW), M],  # Coordination-dependent
        4: [M, M, M, IFC], # IFC only: ITP, AFC, O&M, Record
    }
    return (ref, desc, disc, dates[tier], spkg, rm)
```

**⚠ Date arithmetic pitfall:** Never do `add30(s, 1) + REVIEW` — `add30()` returns a `date` object and `+ int` fails with `TypeError: unsupported operand type(s) for +: 'datetime.date' and 'int'`. Always compute date offsets as a single expression:

```python
# CORRECT:
d90 = s + timedelta(days=30 + REVIEW)
d100 = s + timedelta(days=60 + 2*REVIEW)

# WRONG (raises TypeError):
d90 = add30(s, 1) + REVIEW
```

The `rm` (Remarks) field documents WHY an item is in a later tier — serves as a visible dependency flag in the xlsx:
- `'Needs ST-001/002/003'` — needs survey completion
- `'Needs Arch GA + structural assessment'` — needs base building geometry
- `'BLOCKED — pending client object list (RFI sent Jun 2026)'` — external dependency

## 7-Day Review Buffer Between Stages

When a stage needs approval before the next stage starts, add 7 calendar days for review:

```python
REVIEW = 7  # days for review buffer
# Example: Arch 50% (29 Jun) -> Review 7d -> Arch 90% (29 Jun + 30 + 7)
dates_50 = '29/06/2026'
dates_90 = add_days('29/06/2026', 30 + REVIEW)
dates_100 = add_days('29/06/2026', 60 + 2*REVIEW)
```

Apply to the same package's sequential stages (50→90, 90→100). Cross-package handoffs run in parallel, not sequential.

## Parallel Submission Tracks

Multiple packages submit on the same date when no dependency chain ties them. Use Parallel Groups:

| Group | Description | Examples |
|-------|-------------|----------|
| 0 — Foundation | No deps, start baseline | Arch, Acoustic, CITC, FFE, FLS Strategy, Showcase Design |
| 1 — Structural-feed | Need Structural survey | MEP Layouts, Rigging |
| 2 — Arch-feed | Need Arch GA or sections | AV System Design, Lighting Layouts, Interactives |
| 3 — Late | Need Arch 90%+ | Landscaping |
| 4 — Client-dep | Need client data | Graphics, Model Maker |
| 5 — IFC only | Close-out | All ITP/AFC/O&M items |

## Master Submission Plan Generation

Create a consolidated xlsx with 3 sheets:

**Sheet 1 — Master Plan:** All packages x stages with dates, dependency chains, parallel group numbers, review buffer flags, notes. Architecture broken out by floor. Blue shading = parallel same-day submissions.

**Sheet 2 — Dependency Network:** "If THIS is delayed -> it blocks" table with lag estimates and critical path marking.

**Sheet 3 — Parallel Tracks:** Chronological view by date showing what each Track 0-5 submits.

```python
REVIEW = 7  # days for review buffer between stages
TRACKS = [
    ('Architecture — BF (Basement)', [
        '29/06/2026', ad('29/06/2026', 30+REVIEW),
        ad('29/06/2026', 60+2*REVIEW), '28/08/2026'
    ], '', 0, '16 drawings + Viz Batch 1 (BF+LGF).'),
    ('Architecture — LGF (Lower Ground)', [
        '06/07/2026', ad('06/07/2026', 30+REVIEW),
        ad('06/07/2026', 60+2*REVIEW), '28/08/2026'
    ], '', 0, '16 drawings. Viz already done with BF batch.'),
    ('Architecture — GF (Ground Floor)', [
        '13/07/2026', ad('13/07/2026', 30+REVIEW),
        ad('13/07/2026', 60+2*REVIEW), '28/08/2026'
    ], '', 0, '16 drawings + Viz Batch 2 (GF+1F).'),
    # ...
]
```

Sort by 50% date, group by date with colored subheaders. Parallel flag when same group + same date.

### Viz Batch Pattern

When Viz (3D visualisation shots) is submitted alongside Architecture drawings, batch in 2-floor groups:

```python
VIZ_ITEMS = [
    ('BF-LGF', '3D Visualisation Shots — Batch 1 (Basement + Lower Ground)',
     '29/06/2026', '29/07/2026', '28/08/2026', '—', '3D Viz'),
    ('GF-1F', '3D Visualisation Shots — Batch 2 (Ground + First Floor)',
     '13/07/2026', '12/08/2026', '11/09/2026', '—', '3D Viz'),
]
```

Generate refs: `MOC-ASE-AR-ARC-{batch_code}-DDD-Viz-00` (batch_code = BF-LGF, GF-1F).

Remove per-floor Viz items from `DRAWINGS_PER_FLOOR`. Keep Viz Location Plans (1210) per-floor — those are actual drawing sheets, not renders.

### Real Submission Dates Override

When the user provides real submission dates that differ from the template defaults (e.g., "Submit AV and MEP 1st submission on 01 Jul" instead of 29 Jun), treat the user's dates as authoritative and update ALL downstream dependent schedules:

1. Change the source register (e.g., set AV/MEP Tier 1 to 01 Jul)
2. Update any register that depends on the delayed item (e.g., AV Tier 2 shifts from 29 Jun→29 Jul since it needs Arch 50% available)
3. Regenerate both the affected register xlsx AND the Master Submission Plan
4. Recalculate review buffers for dependent items

Template defaults are rough estimates — user's real project schedule always wins.

## Consolidation Pattern

When a register's scope logically belongs under another (e.g., Rigging -> Structural):

1. Confirm items genuinely belong to same contractor/discipline
2. Add items into parent as a new category (E - RIGGING)
3. Delete child folder + script
4. Preserve dependency references in Remarks column
5. Update category map

### Worked Example: Structural + Rigging Merged

**Rigging items** (3 items from old register) merged into Structural as Category E:
| Ref | Item | Tier | Remarks |
|-----|------|------|---------|
| ST-016 | Rigging design philosophy | 1 (29 Jun) | Immediate |
| ST-017 | Rigging load schedule | 1 (29 Jun) | Needs Arch GA + ST-004 |
| ST-018 | Ceiling suspension point layout | 3 (28 Aug) | Needs slab assessment + Arch ceilings |
| ST-019 | Rigging design details | 3 (28 Aug) | After layout approval |
| ST-020 | Anchor pull-out test | 4 (IFC) | Construction phase |
| ST-021 | Rigging ITP | 4 (IFC) | |
| ST-022 | Rigging O&M | 4 (IFC) | |

**Deleted:** `Rigging_Submittal_Register/` folder + xlsx + `_scripts/Rigging_Submittal_Register.py`

Structural now 22 items across 5 categories: A-Surveys, B-Assessment, C-Design, D-IFC/Handover, E-Rigging.

## Real Submission Dates Override

When the user provides real submission dates that differ from template defaults, treat user's dates as authoritative and shift ALL downstream dependent schedules:

1. **Change the source register** (e.g., set AV/MEP Tier 1 to 01 Jul instead of 29 Jun)
2. **Update dependent schedules** — any register that needs the delayed item's output shifts proportionally (e.g., AV Tier 2 shifts from 29 Jun to 29 Jul because it needs Arch 50% available)
3. **Regenerate** both the affected register xlsx AND the Master Submission Plan
4. **Recalculate review buffers** for dependent chains

**Example — Session learnings from Aseer Museum:**
- User said "today 29 Jun: Arch, Viz, Structural design bases. 01 Jul: AV, MEP 1st submission" → override the template default of all-Level-1 registers starting 29 Jun
- Result: MEP Tier 1 moved to 01 Jul, MEP Tier 2 (layouts) shifted to 27 Jul (needs structural survey + arch review), AV Tier 1 to 01 Jul, AV Tier 2 to 29 Jul
- Template defaults are rough estimates — user's real schedule always wins

## Submittal Logic Map — Dependency-Based Scheduling

When planning start dates across all registers, use the 4-level dependency model:

### Level 0 — Foundation (no dependencies)
- Architecture (NRS), Structural, Oddy Testing, Acoustic
- Start: Project kick-off (e.g., 29 Jun)
- These define base building geometry and constraints

### Level 1 — Needs Arch 50%+ (space geometry defined)
- MEP, FLS, Lighting, AV/IT, Showcase, Rigging, CITC/Telecom
- Start: 2-4 weeks after Arch 50% (or when subcontractor appointed)
- Depend on Arch GA plans for routing, placement, ceiling zones

### Level 2 — Needs Arch 90%+ (finalized design)
- Landscaping (terrace/roof finalized), Interactives
- Start: When Architecture reaches 90% milestone (e.g., 29 Jul)
- Cannot begin detailed design before Arch is substantially complete

### Level 3 — Needs Client Data
- Graphics (content research), Model Maker (object list/reference data)
- Status: TBC — no dates until client provides required input

### Level 4 — Close-Out
- QA/Commissioning/Handover consolidated register
- Active only at IFC milestone (e.g., 28 Aug)
- Consolidates close-out items across ALL packages

### Cross-Register Stagger Principles
- If upstream register is delayed, downstream dates shift proportionally
- Architecture is the **critical path** — any Arch delay cascades to Levels 1-2
- Graphics + Model Maker are **client-dependent** — set no dates, use mask-based markers with Legend note: "Dates TBC — RFI raised to client"
- Each Level 1 register has +7d stagger per category for review buffer (same as per-floor stagger)
- Landscaping starts at Arch 90% date, not the general 29 Jun baseline

### Recommended Default Start Dates (Aseer Museum)
| Register | 50% Start | Dependency |
|----------|-----------|------------|
| Architecture (BF) | 29 Jun | Kick-off |
| Structural | 29 Jun | Independent |
| Oddy Testing | 29 Jun | Independent |
| Acoustic | 29 Jun | Arch 50% |
| MEP | 29 Jun | Arch 50% |
| FLS | 29 Jun | Arch 50% |
| AV/IT | 29 Jun | Arch 50% |
| Showcase | 29 Jun (+stagger) | Arch 50% |
| Rigging | 29 Jun | Arch 50% |
| CITC/Telecom | 29 Jun | Arch 50% |
| Lighting | 10 Jul | ZNA appointment |
| Interactives | 15 Jul | Arch 50% + client object list |
| Landscaping | 29 Jul | **Arch 90%** |
| Graphics | TBC | Client research |
| Model Maker | TBC | Client object list |

The MOC Drawing Numbering System (`Drawing Numbering System.docx`) defines format:

```
MOC-ASE-XX-XXX-XX-DDD-XXXX-00
│    │   │  │    │   │   │    └ Rev
│    │   │  │    │   │   └────── Category (1000-1999 Plans, 4000-4999 Sections, 5510 Elevations, etc.)
│    │   │  │    │   └────────── Drawing Stage (DDD=Detailed Design for 50%)
│    │   │  │    └────────────── Floor (BF, LGF, GF, 1F)
│    │   │  └─────────────────── Sub-Discipline (ARC=Architectural)
│    │   └────────────────────── Discipline (AR=Architectural)
│    └────────────────────────── Project (ASE=Aseer)
└─────────────────────────────── Organization (MOC=Ministry of Culture)
```

**When to apply:**
**When to apply:**
- **Architecture** register — tracks actual drawing sets by floor and category
- **MEP** register — the subcontractor's actual LOD (List of Drawings) uses MOC-ASE-EL and MOC-ASE-ME prefixes. Map each MEP subsystem to a unique number range (e.g., MOC-ASE-EL-EPS-GEN-DDD-0001-00 = Power system SLD). NOT per-floor (use GEN) — MEP drawings are system-based, not floor-based like Architecture.
- NOT for system-based registers (Structural, AV, Lighting, FLS) — they track deliverables, not individual drawings
- NOT for production/procurement registers (Graphics, Model Maker, FFE, Showcase, Interactives)
- NOT for subcontractor registers that follow NRS drawing numbers (already tracked via Architecture register)

## Stage 4 Technical Design — Scope Boundaries

**Critical:** Stage 4 (Technical Design / Detailed Design Development) is NOT the same as Concept or Developed Design stages.

### What NOT to include in a Stage 4 DD submittal plan

| Item | Stage | Verdict |
|------|-------|---------|
| Design Basis Report | Stage 2-3 (Concept / Developed) | Do NOT include — already produced by concept designer (e.g. DHD v1.11) |
| Design Philosophy & UX Strategy | Stage 2-3 | Do NOT include |
| AV Design Criteria Report | Stage 2-3 | Do NOT include |
| Concept design documents | Stage 2-3 | Do NOT include |

### What IS Stage 4 scope

| Category | Examples |
|----------|----------|
| **Technical drawings** | Floor plans, RCPs, sections, elevations per floor (NRS-stamped PDFs + DWGs) |
| **Schedules** | Equipment, cable, power/heat loads, containment |
| **Calculations** | Power, heat, UPS, structural loading |
| **System diagrams** | Signal flow, network architecture, block diagrams |
| **Rack elevations** | Per-rack layouts with power/heat |
| **Control system** | Programming requirements, UI design, hierarchy |
| **Studies** | Speaker coverage, sightline/projection, mounting details |
| **Coordination** | Interface register, setwork housings, showcase AV, DALI/BMS |
| **Material submittals** | Equipment cut sheets, datasheets, compliance certs |

### Register must include ALL gates (don't strip during cleanup)

When cleaning a register to "Stage 4 only", do NOT remove the DD drawings or the IFC/handover gates. The full structure is:

- **DD Drawings** (NRS-stamped floor plans + RCPs) — the core technical content CG reviews
- **DD Schedules, Calculations, Diagrams, Control, Rack Elevations, Studies** — supporting Stage 4 deliverables
- **Coordination items** — Samaya scope (interface register, setwork, structural, IT/ELV, BIM)
- **IFC Packages** — Future Gate (per-floor IFC sets, specs, ITP, spares)
- **Testing & Handover** — Future Gate (FAT, SAT, cable certs, O&M, training)

A "Stage 4 register" means items appropriate for the Stage 4 review (technical design content), NOT a stripped-down register missing the actual drawings or future gates.

### When user corrects you on stage scope

If the user says "we're in Stage 4, not design stage" — immediately:
1. Remove any Design Basis Report / Design Philosophy items from the plan
2. Confirm the remaining items are all Stage 4 technical deliverables
3. Apologize — the distinction matters for CG submission
4. If you accidentally removed DD drawings or future gates during cleanup, restore them

### Scope boundary: confirm floors in scope

Before generating a register, confirm which floors are in scope. The user may have already excluded some floors (e.g., "2nd Floor and Roof are NOT in scope"). Do NOT assume all 6 floors are needed — verify against the user's statement or project docs. Wrong assumption = wrong register.

## Drawing Code Floor Prefix — Do NOT Assume

**Pitfall:** Drawing codes like `MOC-ASE-AV-TAV-BF-DDD-1230-00` may use `BF` as a **project prefix** (e.g., "Building Fit-out" or project code), NOT "Basement Floor". The actual floor is in the title block text.

**Always verify by reading the title block** — extract text from the PDF/DWG title block area to find the actual floor name:

```python
# Extract title block text from PDF to find actual floor
import fitz
doc = fitz.open(pdf_path)
page = doc[0]
text = page.get_text()
for line in text.split('\n'):
    if 'FLOOR PLAN' in line.upper() or 'RCP PLAN' in line.upper():
        floor = line.strip()  # e.g. "BASEMENT FLOOR PLAN FOR AUDIO VISUAL SYSTEM"
        break
```

**Aseer Museum example:** All 8 drawings had `-BF-` in the code but actually covered 4 different floors (Basement, Lower Ground, Ground, First). The `BF` was a project code, not a floor indicator.

## CG-Facing Register — No Internal Responsibility Split

**Critical rule:** When submitting a register to CG (Consultant), do NOT show internal responsibility splits (AV Designer vs Samaya). CG sees everything as "Samaya" — they don't care who inside Samaya's team produces what.

### Before (internal view — DO NOT send to CG)
```
Section 1 — AV Designer Scope (Submitted)
Section 2 — Samaya Scope (Pending)
```

### After (CG-facing view)
```
All items under Samaya. Status = Submitted / Pending / Future Gate.
```

### Implementation
- Set all `Responsibility` column values to `'Samaya'`
- Use only 3 status values: `Submitted` (green), `Pending` (yellow), `Future Gate` (grey)
- Remove any party/scope column that distinguishes subcontractor from main contractor
- Remove any section headers that say "AV Designer Scope" or "Samaya Scope"
- Keep the item descriptions and codes unchanged — CG needs to know WHAT, not WHO

### When to apply
- Always for CG submission registers
- Never for internal tracking registers (keep the split for TO oversight)
- If the same register serves both purposes, maintain two versions or use a hidden column

## Responsibility-Split Register Pattern

When a subcontractor does NOT handle coordination drawings, BIM models, or cross-trade integration (those are done by the main contractor), split the register into clear sections:

### Register Structure

```
SECTION 1 — SUBCONTRACTOR SCOPE (Detailed Design Submittals)
  - All technical drawings, schedules, calculations, system diagrams
  - Rack elevations, control system, material submittals
  - Per-floor IFC packages, ITP, testing, handover docs

SECTION 2 — MAIN CONTRACTOR SCOPE (Coordination & Integration)
  - Interface Register (NRS/MEP/Lighting/Showcase)
  - Setwork housing drawings (equipment in joinery)
  - Showcase AV interface (GBH coordination)
  - Structural loading calculations (subcontractor provides weights)
  - DALI/BMS interface specification
  - Wireless coverage / heat map study
  - CCTV/ELV system design
  - Acoustic integration report
  - Content-hardware interface matrix
  - Cybersecurity hardening report
  - BIM models (LOD 300/350/500)
  - Network configuration & VLAN scheme
```

### Notes Column Pattern

For each main-contractor-scope item, add a note explaining the data flow:
```
"Samaya maintains; AV Designer provides system data"
"Samaya BIM — AV Designer provides equipment data"
"Samaya Structural — AV Designer provides equipment weights"
```

This makes it clear that the subcontractor still has an obligation to provide input data, even though they don't produce the final deliverable.

### AV Submittal Plan Reference

A complete worked example (AV Stage 04, 69 items, 4 gates, responsibility split) is at:

### CRS-to-Drawing-Register Mapping

When CG returns a CRS Excel for a DD Gate package, see [`references/crs-to-drawing-register-mapping.md`](references/crs-to-drawing-register-mapping.md) for the mapping workflow — extract codes per drawing, handle mixed B/C/U.R results, and update the register.
`02_Submittals/04_Registers/AV_Submittal_Register/AV_Stage04_Submittal_Plan.xlsx`

The generator pattern:
- Sections 1-6: AV Designer scope (DD drawings, schedules, diagrams, control, racks, audit)
- Section 7: Samaya scope (coordination, BIM, structural, IT/ELV, acoustic)
- Sections 8-9: Future gates (IFC, testing & handover)

## Package Code Convention — Project Standard, Not Invented

When generating package codes for a submittal register, **use the project's real MOC numbering convention**, not invented codes.

### MOC Numbering Pattern
```
MOC-MUS-ASE-1E0-SCH-0001
│   │   │   │   │   │
│   │   │   │   │   └─ Sequential number per category
│   │   │   │   └───── Type (SCH, CAL, DWG, REP, SYS, SPC, REG, COO, BIM, IFC, QA, FAT, SAT, CBL, HO, NET, SEC)
│   │   │   └─────────── Discipline (1E0 = Electrical, 1A0 = Architectural, 1M0 = Mechanical, 1K0 = General, 1KH = HSE)
│   │   └────────────── Project (ASE = Aseer)
│   └────────────────── Client (MUS = Museum)
└────────────────────── Organization (MOC = Ministry of Culture)
```

### Don't invent codes like `ASE-AV-xxx`

**Wrong:** `ASE-AV-SCH-001`, `ASE-AV-CAL-002` (made up by the agent, not from project docs)
**Right:** `MOC-MUS-ASE-1E0-SCH-0001`, `MOC-MUS-ASE-1E0-CAL-0002` (actual project standard)

If the user does not specify codes, ask before generating. If they say "use project standard", look up the discipline prefix in the project's Drawing Numbering System document.

### File name conventions

- Use proper capitalization: `AV Hardware Schedule.xlsx` (not `AV hardware schedule .xlsx`)
- No trailing spaces before extensions
- Fix typos in file names (e.g., "requieremnts" → "Requirements")
- For duplicated files (NRS-stamped vs non-stamped), keep only the stamped version and delete the plain copy

## "Future Gate" Status — Leave Blank, Not Text

When items belong to a future gate (IFC, testing, handover) but are not yet due, the status column should be **left blank**, not labeled "Future Gate".

```python
# WRONG
status = 'Future Gate'

# RIGHT
status = ''  # blank cell
```

CG does not need to see "Future Gate" labels in a register — they see blank cells and understand these are upcoming. The grouping by category (e.g., "IFC Packages", "Testing & Handover") communicates the same information structurally.

When removing "Future Gate" text from existing registers:
- Set status cell to empty string
- Also remove "(Future Gate)" suffix from any group/category headers (e.g., "IFC Packages (Future Gate)" → "IFC Packages")
- Color coding can still use grey fill for these items (visual distinction without text label)

## Register Dates — Match Actual Submission

In a submittal register:
- **Submitted items** → set Planned Date to the actual submission date (e.g., `05-07-2026`)
- **Pending items** → leave Planned Date blank
- **Future gate items** → leave blank or set to TBC

Do NOT use future placeholder dates (like `2026-07-25` or `2026-09-14`) for items being submitted today. The user will read the date column and expect it to match the cover letter / Aconex transmittal date.

### Response Folder Creation

When a CG comment response package is assembled (CR sheet + updated registers + draft drawings + correspondence), create a dated response folder under `02_Submittals/`:

```
02_Submittals/2026-07-08_CG_Comments_Response/
  ├── 01_CR_Sheet/          → CR Sheet Excel
  ├── 02_NRS_Draft_Drawings/ → Draft PDFs from designer
  ├── 03_Registers/          → Updated submission plans and registers
  └── 04_Correspondence/     → Email PDFs
```

### Register Folder Cleanup

When organizing the `04_Registers/` folder:

1. **Move loose risk registers** into a `Risk_Registers/` subfolder
2. **Move misplaced files** (PDFs, DOCX, temp files) out of discipline folders
3. **Remove temp files** (files starting with `~$`)
4. **Keep CR sheets at root** of registers folder (they reference multiple disciplines)
5. **Each discipline folder** should contain only its own register files
6. **Remove misplaced PDFs** (Submission Comments + Arch.pdf) from Structural and Arch folders
7. **Remove misplaced DOCX** (Structural Audit Report Template) from Structural folder
8. **Remove misplaced PDFs** (MOC-MUS-ASE-MEP-ZD-0068.pdf) from Electrical and Mechanical folders
9. **Remove temp RACI files** (`~$RACI_*.tmp`) from RACI_Matrix folder

## In-Place Editing Without Rebuilding

When a CG comment requires splitting a specialized scope into a separate register (e.g., Rigging Systems), do NOT rebuild the main register from scratch. Follow this pattern:

### Step-by-step

1. **Extract the rows** to be moved into a Python list (read values only, no formatting)
2. **Create the new register** workbook with proper headers, title, and section structure
3. **Unmerge merged cells** in the affected rows of the original workbook:
   ```python
   for merge_range in list(ws.merged_cells.ranges):
       for r in range(start_row, end_row + 1):
           if merge_range.min_row <= r <= merge_range.max_row:
               ws.unmerge_cells(str(merge_range))
               break
   ```
4. **Clear cell values** in the affected rows (column by column):
   ```python
   for row in range(start_row, end_row + 1):
       for col in range(1, max_col + 1):
           try:
               ws.cell(row=row, column=col).value = None
           except AttributeError:
               pass  # MergedCell — already unmerged above
   ```
5. **Add a reference note** in the first column of the first cleared row:
   ```python
   ws.cell(row=start_row, column=1).value = 'Scope — See separate Register Name'
   ```
6. **Save in place** — do NOT rebuild the workbook. All other formatting, merged cells, colors, borders, and column widths remain untouched.

### What NOT to do

- Do NOT rebuild the entire workbook from collected row data — this destroys template formatting
- Do NOT use `ws.insert_rows()` or `ws.delete_rows()` on sheets with merged cells — this corrupts adjacent rows
- Do NOT apply new styles to any cells outside the cleared range
- Do NOT change column widths, row heights, or freeze panes

### Verification

After saving, re-read the file and check:
- Only the intended rows were cleared
- Reference notes are present
- All other rows have their original values and formatting
- No merged cells were corrupted

## Register Format Standardisation (Template Copy)

When asked to "fix format same as Arch" or "unify format for all sheets":

### Arch Register Template Spec
| Element | Font | Fill | Alignment | Border | Row Ht |
|---------|------|------|-----------|--------|--------|
| Row 1 — Column headers | Calibri 11 Bold White (#FFFFFF) | Dark blue #1F4E79 solid | Center H, Top V, Wrap | Thin all | 16 |
| Row 2 — Sheet title | Calibri 12 Bold White (#FFFFFF) | Medium blue #2E75B6 solid | Left H, Center V | Thin all | 16 |
| Section headers (A — Name) | Calibri 10 Bold Green (#375623) | Light green #E2EFDA solid | Left H, Center V | Thin all | auto |
| Data rows | Calibri 10 Regular (#000000) | None | Top V, Wrap | Thin all | auto |
| Submittal count | Calibri 10 Bold (#000000) | None | Left H, Center V | Thin all | auto |

### Column Widths (Arch standard)
```python
COL_WIDTHS = {'A': 32, 'B': 55, 'C': 14, 'D': 10, 'E': 10, 'F': 10, 'G': 10, 'H': 22, 'I': 28}
```

### Apply to Any Register (openpyxl)
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

dark_blue_fill = PatternFill(start_color='FF1F4E79', end_color='FF1F4E79', fill_type='solid')
med_blue_fill  = PatternFill(start_color='FF2E75B6', end_color='FF2E75B6', fill_type='solid')
light_green_fill = PatternFill(start_color='FFE2EFDA', end_color='FFE2EFDA', fill_type='solid')
white_font     = Font(name='Calibri', size=11, bold=True, color='FFFFFFFF')
title_font     = Font(name='Calibri', size=12, bold=True, color='FFFFFFFF')
section_font   = Font(name='Calibri', size=10, bold=True, color='FF375623')
normal_font    = Font(name='Calibri', size=10, color='FF000000')
thin_border    = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))

for ws in workbook.worksheets:  # apply to ALL sheets
    # Row 1 — headers
    for c in range(1, 10):
        cell = ws.cell(row=1, column=c)
        cell.font = white_font
        cell.fill = dark_blue_fill
        cell.alignment = Alignment(horizontal='center', vertical='top', wrap_text=True)
        cell.border = thin_border
    ws.row_dimensions[1].height = 16

    # Row 2 — sheet title (50% Design, 90% Design, ...)
    for c in range(1, 10):
        cell = ws.cell(row=2, column=c)
        cell.font = title_font
        cell.fill = med_blue_fill
        cell.alignment = Alignment(horizontal='left', vertical='center')
        cell.border = thin_border
    ws.row_dimensions[2].height = 16

    # Section headers: detect by letter-prefix (A — , B — , ... or A -, B -, etc.)
    section_prefixes = ['A —', 'B —', 'C —', 'D —', 'E —', 'F —', 'G —', 'A -', 'B -', 'C -', 'D -', 'E -', 'F -', 'G -']
    for r in range(3, ws.max_row + 1):
        ref = ws.cell(row=r, column=1).value
        if not ref: continue
        v = str(ref).strip()
        is_section = any(v.startswith(p) for p in section_prefixes)
        is_subtitle = v in ('50% Design', '90% Design', '100% Design', 'IFC  AFC  Construction')
        is_count = 'submittal(s)' in v
        for c in range(1, 10):
            cell = ws.cell(row=r, column=c)
            if is_subtitle:
                cell.font, cell.fill, cell.alignment = title_font, med_blue_fill, Alignment(horizontal='left', vertical='center')
            elif is_section:
                cell.font, cell.fill, cell.alignment = section_font, light_green_fill, Alignment(horizontal='left', vertical='center')
            elif is_count:
                cell.font, cell.fill, cell.alignment = Font(name='Calibri', size=10, bold=True), PatternFill(), Alignment(horizontal='left', vertical='center')
            else:
                cell.font, cell.fill, cell.alignment = normal_font, PatternFill(), Alignment(vertical='top', wrap_text=True)
            cell.border = thin_border

    # Fix column widths
    for col_letter, width in COL_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

    # Convert string dates to proper date objects
    from datetime import date
    for r in range(3, ws.max_row + 1):
        for c in [4, 5, 6, 7]:
            cell = ws.cell(row=r, column=c)
            v = cell.value
            if isinstance(v, str) and v.strip() and '/' in v:
                try:
                    parts = v.strip().split('/')
                    d = date(int(parts[2]), int(parts[1]), int(parts[0]))
                    cell.value = d
                    cell.number_format = 'DD/MM/YYYY'
                except: pass
```

### Critical Pitfall — openpyxl insert_rows Corrupts Merged-Cell Sheets

When using `ws.insert_rows()` or `ws.delete_rows()` on an Excel sheet with **merged cells** (common in styled register templates with section headers spanning columns), the operation corrupts adjacent row data. Symptoms:
- `MergedCell` objects become read-only — writing to any cell in a formerly merged range raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`
- Adjacent rows lose cell values (descriptions, dates, discipline, sub-package) while the ref column (Col A) survives
- The corruption propagates through subsequent insertions because each insert reshuffles merged cell references

**Fix: unmerge before insert/delete, then rebuild from in-memory list:**
```python
# Step 1: Unmerge all cells first (prevents MergedCell corruption)
for mc in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(mc))

# Step 2: Read ALL rows into a Python list
all_rows = []
for r in range(1, ws.max_row + 1):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, 10)]
    if any(v is not None for v in row_vals):
        all_rows.append(row_vals)

# Step 3: Build ordered new row list with insertions (manipulate list, not sheet)
new_rows = []
for vals in all_rows:
    # ... renumber, filter ...
    new_rows.append(vals)
# Insertions: process bottom-up so earlier positions stay valid
for anchor_ref, new_item_vals in reversed(sorted_insertions):
    idx = next(i for i, v in enumerate(new_rows) if v[0] == anchor_ref)
    new_rows.insert(idx + 1, new_item_vals)

# Step 4: Clear sheet entirely
for r in range(ws.max_row, 0, -1):
    ws.delete_rows(r, 1)

# Step 5: Write everything back
for ri, vals in enumerate(new_rows):
    for c, v in enumerate(vals):
        cell = ws.cell(row=ri + 2, column=c + 1)  # row 1 = header
        cell.value = v
        if isinstance(v, date):
            cell.number_format = 'DD/MM/YYYY'
```

**Date handling key:** Write `datetime.date` objects with `number_format='DD/MM/YYYY'`. String dates like `'29/06/2026'` are treated as plain text by Excel. The text-extraction tool (`read_file`) shows `datetime.date` values as serial numbers (e.g. `46202`) — this is a read-file display quirk; they render correctly in Excel with DD/MM/YYYY format.

### MEP Gates Submission Plan — Drawing Number Source of Truth

The consultant (AD Engineering) provides a **Gates Submission Plan xlsx** (`Aseer_Mech_Gates_Submission_Plan.xlsx`) that contains the authoritative drawing list with real numbers and planned submission dates. When this file exists, use it INSTEAD of generating MEP drawing numbers from a template.

**Key format differences from Architecture:**
- MEP uses **per-floor sub-discipline codes** in the drawing number, not `GEN`:
  - `MOC-ASE-ME-MHV-AC-BF-DDD-30001-00` (AC=Air Conditioning, BF=Basement Floor)
  - `MOC-ASE-ME-MHV-VE-LGF-DDD-30007-00` (VE=Ventilation, LGF=Lower Ground)
  - `MOC-ASE-ME-MHV-CH-GF-DDD-30013-00` (CH=Chilled Water, GF=Ground Floor)
  - `MOC-ASE-ME-MHV-CD-1F-DDD-30019-00` (CD=Condensate Drain, 1F=First Floor)
  - `MOC-ASE-ME-MHV-SM-2F-DDD-30025-00` (SM=Smoke Management, 2F=Second Floor)
- Drawing numbers are **sequential within a sub-system AND unique per floor** (30001-30006 for AC floors, 30007-30012 for VE floors, 30013-30018 for CH floors, 30019-30024 for CD floors, 30025 for SM), not category-based like Architecture
- Common pitfall: register often simplifies to `-30001-00` for all floors in a sub-system — this differs from the Gates plan's unique per-floor numbers

#### Register vs Gates Plan Gap Analysis (Cross-Reference Audit)

When updating a register to match the consultant's Gates submission plan, do a **programmatic comparison** using openpyxl:

```python
# Load Gates plan — extract all MOC refs
wb_gates = openpyxl.load_workbook(path_to_gates_xlsx, data_only=True)
ws = wb_gates['Mech Stage 04 Submission Pl']
gates_refs = set()
for row in ws.iter_rows(min_row=4, values_only=True):
    ref = row[4]  # Column E = Drawing No
    if ref and str(ref).strip().startswith('MOC-ASE'):
        gates_refs.add(str(ref).strip())

# Load register — extract all MOC refs across all sheets
wb_reg = openpyxl.load_workbook(path_to_register_xlsx, data_only=True)
reg_refs = set()
for sname in wb_reg.sheetnames:
    if sname == 'Legend': continue
    for row in wb_reg[sname].iter_rows(min_row=3, values_only=True):
        ref = row[0]
        if ref and str(ref).strip().startswith('MOC-ASE'):
            reg_refs.add(str(ref).strip())

missing = gates_refs - reg_refs
extra = reg_refs - gates_refs
```

**3 categories of gaps found (Aseer Mech example):**

| Category | Nature | Count | Action |
|----------|--------|-------|--------|
| A — Numbering mismatch | Gates uses unique per-floor sequence (30001-30006), register uses single 30001 | ~35 items | Ask user: align to Gates numbering or keep simplified? |
| B — Wrong stage | Items exist in register but only at 100%/90% while Gates expects at Detailed Design (50%) | ~12 items | Add to 50% sheet with appropriate dates |
| C — Genuinely missing | Not in any register sheet | 1 item | Add from scratch |

**Determine if "missing" items are numbering mismatches:**

If a Gates ref `MOC-ASE-ME-MHV-AC-LGF-DDD-30002-00` is "missing" but the register has `MOC-ASE-ME-MHV-AC-LGF-DDD-30001-00` — it's the same deliverable with a different sequence number. The register's convention (all floors = same sequence) is simpler but doesn't match consultant's. Let the user decide, but flag the discrepancy clearly.

**Stage-mismatch check — items in register at later stages but Gates wants at 50%:**

Run a second pass checking the 50% Design sheet specifically:
```python
ws_50 = wb_reg['50% Design']
reg_50_refs = set()
for row in ws_50.iter_rows(min_row=3, values_only=True):
    ref = row[0]
    if ref and str(ref).strip().startswith('MOC-ASE'):
        reg_50_refs.add(str(ref).strip())

needs_50 = gates_refs - reg_50_refs  # Items that should be in 50% but aren't
```
These are typically detail/installation items (GEN-DDD-2000X) and fire fighting schedule/riser items that were added at 100% stage but the Gates plan expects at Detailed Design.

**After audit:**
1. Present 3-category breakdown clearly
2. Ask user about numbering alignment (Type A) before editing
3. Add Type B items to 50% sheet (back-fill dates from Gates plan)
4. Add Type C items as new rows
5. Regenerate xlsx
- Fire Fighting uses separate sub-discipline: `MOC-ASE-ME-MFF-{Floor}-DDD-30001-00`
- Water Supply uses: `MOC-ASE-ME-MPL-WS-{Floor}-30001-00` (note: no DDD! Check source)
- Drainage uses: `MOC-ASE-ME-MPL-DRN-{Floor}-30001-00`
- Irrigation: `MOC-ASE-ME-MPL-IRR-GEN-30001-00`

**Items already submitted** (marked as 50% complete at baseline):
- HVAC Design Base Report (DBR) — 07 Jun in gates plan
- Cooling Load Estimation, Chilled Water System Design
- Legend and General Notes, Chiller flow diagram, Riser diagrams, Equipment Schedules

**Items pending:**
- HVAC 1st submission — 06 Jul (design basis items)
- Fire Fighting DBR — 16 Jul
- Condensate Drain — 26 Jul
- Per-floor layouts — 27 Jul (needs structural survey completion)

**When the gates plan exists, extract ALL items from it:**
1. Open with openpyxl data_only=True
2. Read column 5 (Drawing No) and column 6 (Description)
3. Group by header rows (HVAC Systems, Fire Fighting, Water Supply, Drainage)
4. Parse dates from column 8 (may be Excel datetime objects or text strings like "2026-06-07" or "26/7/2026")
5. Map each system to sub-packages using the drawing number prefix (MH-, MFF-, MPL-WS, MPL-DRN, MPL-IRR)
6. Assign dates: already-submitted items at D_ALREADY (29 Jun), others at their gates plan dates or staggered from baseline

**Structure by system (from actual gates plan):**
- **HVAC General** (15 items): DBR, Calc (2), Legend, Duct Details (3), Piping, Equipment, Chiller, Air Riser, CW Riser, Equip Sched (2)
- **HVAC Per-Floor** (24 items): AC (6 floors), VE (6), CH (6), CD (5 — no RF), SM (1)
- **Fire Fighting** (14): DBR, Calc, Legend, Details (2), Pumps Room, Pump Sched, Riser, FF Layouts (6 floors)
- **Water Supply** (8): Legend, Details, WS Layouts (6 floors)
- **Drainage** (8): Legend, Details, DRN Layouts (6 floors) + Irrigation

**Drawing number format (from gates plan):**
```
MEP numbering pattern (from actual ELE + MECH LOD documents):
| Prefix | Discipline | Sub-Discipline | Example |
|--------|-----------|---------------|---------|
| MOC-ASE-EL-EPS | Electrical, Power Supply | EPS | MOC-ASE-EL-EPS-GEN-DDD-0001-00 |
| MOC-ASE-EL-EPB | Electrical, Panel Board | EPB | MOC-ASE-EL-EPB-GEN-DDD-0006-00 |
| MOC-ASE-EL-ELE | Electrical, General | ELE | MOC-ASE-EL-ELE-GEN-DDD-0008-00 |
| MOC-ASE-EL-ELC | Electrical, Low Current | ELC | MOC-ASE-EL-ELC-GEN-DDD-0011-00 |
| MOC-ASE-EL-ECR | Electrical, Cable Routing | ECR | MOC-ASE-EL-ECR-GEN-DDD-0016-00 |
| MOC-ASE-EL-EER | Electrical, Earthing | EER | MOC-ASE-EL-EER-GEN-DDD-0007-00 |
| MOC-ASE-ME-MHV | Mechanical, HVAC | MHV | MOC-ASE-ME-MHV-GEN-DDD-0018-00 |
| MOC-ASE-ME-MFF | Mechanical, Fire Fighting | MFF | MOC-ASE-ME-MFF-GEN-DDD-0027-00 |
| MOC-ASE-ME-MPL | Mechanical, Plumbing | MPL | MOC-ASE-ME-MPL-GEN-DDD-0033-00 |

MEP items use GEN (general) for floor since drawings are organised by system, not per-floor like Arch.

**Item generation pattern:**
```python
FLOORS = [('BF', 'Basement Floor', 0), ('LGF', 'Lower Ground Floor', 7), ...]
DRAWINGS_PER_FLOOR = [('1100', 'Existing GA Plans'), ('1200', 'Proposed GA Plans'), ('4000', 'Existing Sections'), ...]
for floor_code, floor_name, stagger in FLOORS:
    for cat, desc in DRAWINGS_PER_FLOOR:
        ref = f'MOC-ASE-AR-ARC-{floor_code}-DDD-{cat}-00'
        ...
```

## Register Audit Workflow

When user points to subcontractor data to validate a register:

1. **Extract items** from subcontractor register or schedule (openpyxl data_only=True)
2. **Count & categorize** — note categories/sub-packages used in source
3. **Compare** against current 04_Registers version — note gaps, duplications, scope shifts
4. **Identify NRS-scoped items** — if found, they belong in Architecture register, not subcontractor register
5. **Decide replacement strategy:**
   - **Full replacement** (FLS pattern): Subcontractor has an existing register with real items → keep all refs, descriptions, categories verbatim; strip SOW/ER cols; add dates
   - **Data-driven rebuild** (Graphics/Model Maker pattern): Subcontractor has schedule/BOQ but no register → build register items from the actual objects/line items in the schedule
6. **Rewrite register** to match actual subcontractor scope:
   - Discard generic template items
   - Use real object IDs and descriptions from schedule
   - Group by actual categories from subcontractor data
   - Apply dates or no-dates pattern per user direction
7. **Delete obsolete registers** whose scope is fully covered by another (e.g., Exhibition Fit-Out → Architecture)

### Showcase Register Pattern (GBH — Full Supply Subcontractor)

Showcase is a **full supply & design subcontractor** (Glasbau Hahn — GBH) with shop drawings already submitted.

**Source data:** `24_Subcontractors/05_Showcases_Contractor/07_Registers_and_Logs/Aseer_Museum_Showcase_Drawing_Register.xlsx`

**Structure:**
- 8 case types (Type 1 through Type 6B) across 4 galleries
- 27 total case positions, each with specific Qty, Exhibit Number, Showcase ID
- Shop drawings already submitted in batches (Sub-01 to Sub-11+, tracked in Drawing Register)
- Items per type: Design spec → Lighting integration → Shop drawings → Prototype → Production → Delivery → QA → O&M → Spares

**Steps per type (10 steps):**
1. Showcase design specification (50%)
2. Lighting integration design (50%)
3. Shop drawing submission — case GA, sections, details (50%)
4. Prototype fabrication & approval (90%)
5. Production — quality check per case (100%)
6. Material certificates — glass, steel, finishes (IFC)
7. Delivery to site & installation report (IFC)
8. QA Documentation / Compliance (IFC)
9. O&M manual — showcase maintenance (IFC)
10. Spares — glass panels, hinges, LED modules (IFC)

**Dates:** Stagger case types +7d starting 29 Jun. IFC = 28 Aug.

### Lighting Register Pattern (Studio ZNA — Designer Subcontractor)

Lighting is a **design consultancy** (not supply/install). Map deliverables to ZNA scope sections 1.1–1.8:

| ZNA Scope | Register Cat | Items |
|-----------|-------------|-------|
| 1.1 Lighting Layout & Control Plans | B — Preliminary / C — Detailed | LI-005–009 |
| 1.3 Details & Installation | H — IFC | LI-027–029 |
| 1.4 Electrical Load & Control Strategy | A — Design Philosophy, C — Detailed | LI-002, LI-006, LI-013 |
| 1.5 Technical Studies & Calculations | C — Detailed | LI-011 |
| 1.6 Conservation & Fixture Requirements | E — Conservation | LI-018–021 (+ IES/LDT files) |
| 1.7 BOQ & Value Engineering | F — BOQ & VE | LI-022–024 |
| 1.8 Mock-Ups & Sample Review | G — Mock-Up | LI-025–026 |

**Categories:** A-Design Philosophy, B-Preliminary, C-Detailed, D-Coordination, E-Conservation, F-BOQ/VE, G-Mock-Up, H-IFC/Handover.

**Dates:** Start 10/07/2026, stagger +7d per category. IFC items at 28/08/2026.

**Scope boundary:** ZNA designs only (RIBA Stage 4). IFC items (AFC, O&M, Training, Spares, Record Drawings) are Samaya internal tracking, not ZNA deliverables — keep them in the register for TO oversight but note the boundary.

**Source:** Always extract actual scope from ZNA's `Aseer 2026 SCOPE of works 010625_StudioZNA.pdf` or the derived markdown `Aseer_Lighting_Designer_Scope_of_Work_Rev01.md`. The scope doc defines 8 deliverable sections — use them as category anchors.

### Schedule-to-Register Rebuild Pattern (Model Maker / Graphics)

When the subcontractor has an **object/line-item schedule** (not a pre-built register), rebuild from the actual schedule items:

1. **Extract all objects/line items** from the schedule
2. **Define production steps** that apply to every object (same pattern for all):
   ```python
   STEPS = [
       ('Step Name', stage),  # stage=0 (50%), 1 (90%), 2 (100%), 3 (IFC)
   ]
   ```
3. **Nest:** For each object → for each step → generate row:
   ```python
   for obj_id, obj_desc in OBJECTS:
       for step_name, stage_idx in STEPS:
           dates = self.stage_dates(obj_id_stagger, stage_idx)
           items.append((ref, step_name, obj_desc, dates, ...))
   ```
4. **Categories** = one per object (A — Object 1, B — Object 2, etc.)

**Model Maker (5 replica objects from 6930_Aseer_Model & Replica Schedule):**
- Steps: Material Approval → Fab Spec → 50% Inspection → 100% QC → Delivery → QA
- No dates (RFI pending client research data)

**Graphics (39 panel line items from BOQ_QTY_EXTRACT.md, 5 groups):**
- Steps: Artwork Proof → Material Approval → Colour Proof → Production → Delivery/Install → QA
- No dates (RFI pending client research/data)
- Group panels by size/type (Large Format, Medium, Room Pointers, Large Signage, Special/Interactive)
- Each group has its own stagger for reference

### FFE Register Audit Pattern

When auditing FFE scope, always check:

1. **BOQ** (`05_BOQ/` or `24_Subcontractors/<package>/01_Schedule_and_BOQ/`) for actual furniture item list
2. **NRS tender package** — NRS designs all FF&E (schedules, layouts, material selections)
3. **Existing registers** — don't duplicate (e.g., display cases already in Showcase register)

**Decision tree:**
- Design items (schedules, layouts, specs) → Architecture register (NRS scope)
- Fixed/bespoke items (reception desks, shelving, counters, railings) → Joinery subcontractor, not FFE
- Display cases → Showcase register
- **Loose furniture only** (sofas, chairs, tables, rugs, curtains, outdoor) → FFE register, BY ZONE from BOQ
- Each zone tracks: Catalog → TDS → Cut Sheet → Sample → Compliance → Warranty

### Sub-Package → Section Header Organization (Multi-Discipline Registers)

When a register has items from multiple sub-packages (e.g., MEP: HVAC, Fire Fighting, Water Supply, Drainage, Irrigation, BIM), **organize every item under its proper section header** — no stragglers before/between headers.

**Detection pattern — assign items to sections by ref prefix:**

```python
# Example: MEP register with sections A-G
SECTION_NAMES = {
    'A': 'A - HVAC GENERAL',
    'B': 'B - HVAC PER-FLOOR LAYOUTS',
    'C': 'C - FIRE FIGHTING',
    'D': 'D - WATER SUPPLY',
    'E': 'E - DRAINAGE',
    'F': 'F - IRRIGATION',
    'G': 'G - BIM',
}

def sub_pkg_key(vals):
    ref = vals[0] or ''
    sub = vals[7] or ''  # Sub-Package column
    sub_str = str(sub).strip()
    
    if sub_str == 'HVAC':
        # Per-floor items (contain -BF-, -LGF-, -GF-, -1F-, -2F-, -RF-) go under B
        floor_codes = ['-BF-', '-LGF-', '-GF-', '-1F-', '-2F-', '-RF-']
        has_floor = any(fc in str(ref) for fc in floor_codes)
        return 'B' if has_floor else 'A'
    
    return SECTION_MAP.get(sub_str, 'Z')
```

**Rebuild procedure (in-memory, avoid insert_rows):**
```python
from collections import OrderedDict

# 1. Collect items, ignoring existing section headers (we re-add them)
items = []
for vals in all_rows[2:]:  # skip header + title
    ref = vals[0]
    if ref and str(ref).startswith('MOC-ASE'):
        items.append(vals)

# 2. Group by section key
sections = OrderedDict()
for vals in items:
    key = sub_pkg_key(vals)
    sections.setdefault(key, []).append(vals)

# 3. Build ordered data: header → title → section headers → grouped items → count
ordered = [header_row, title_row]
for sk in section_order:  # ['A','B','C','D','E','F','G']
    if sk in sections and sections[sk]:
        ordered.append([SECTION_NAMES[sk], None, None, None, None, None, None, None, None])
        ordered.extend(sections[sk])
ordered.append([f'{count} submittal(s)', None, None, None, None, None, None, None, None])

# 4. Clear sheet + write all rows at once
for r in range(ws.max_row, 0, -1):
    ws.delete_rows(r, 1)
for ri, vals in enumerate(ordered):
    for c, v in enumerate(vals):
        ws.cell(row=ri + 1, column=c + 1).value = v
```

**Common items that end up before their section header (fix by grouping):**
- DBR (Design Base Report) → goes under its discipline's GENERAL section, not standalone
- Calculation items (CALC) → same section as DBR
- GEN items (legends, details) → same section
- Any item whose sub-package doesn't match the preceding section header → it's in the wrong place

### Missing Floor Addition to All Stage Sheets

When a floor-level item is missing from ALL register sheets (e.g., RF=Upper-Roof Condensate Drain in Mechanical), the same ref must be added to **every applicable stage sheet** (50%, 90%, 100%) with the correct stage-specific date:

```python
CD_RF_DATE = {'50% Design': date(2026, 7, 26), '90% Design': date(2026, 8, 26), '100% Design': date(2026, 9, 25)}

for sname in ['50% Design', '90% Design', '100% Design']:
    ws = wb[sname]
    # Check if CD-RF exists
    found = any(ws.cell(row=r, column=1).value and '-CD-RF-' in str(ws.cell(row=r, column=1).value)
                for r in range(3, ws.max_row + 1))
    if not found:
        # Find last CD item in this sheet
        last_cd = max((r for r in range(3, ws.max_row + 1)
                       if ws.cell(row=r, column=1).value and '-CD-' in str(ws.cell(row=r, column=1).value)),
                      default=None)
        if last_cd:
            # INSERT after last CD item — prefer in-memory rebuild over insert_rows
            # (see merged-cells pitfall above)
            ...
```

When adding to 90% or 100% sheets, the date goes in the **stage column** (col 5 for 90%, col 6 for 100%) — NOT in col 4 (50% column). Common mistake is putting the date in col 4 for all sheets.

### Section-Specific Date Override

When the user says "start Section X from date Y" — apply as a **bulk date override** for all items under that section:

```python
# Find section boundaries
section_ranges = {}  # section_header_ref → [(start_row, end_row), ...]
current_section = None
section_start = None

for r in range(3, ws.max_row + 1):
    ref = ws.cell(row=r, column=1).value
    if ref and any(str(ref).startswith(p) for p in ['A -', 'B -', 'C -', 'D -', 'E -', 'F -', 'G -']):
        if current_section:
            section_ranges[current_section].append((section_start, r - 1))
        current_section = str(ref).strip()
        section_start = r + 1
    elif r == ws.max_row:
        if current_section:
            section_ranges[current_section].append((section_start, r))

# Override dates for a specific section
target_date = date(2026, 7, 7)
for start, end in section_ranges.get('A - HVAC GENERAL', []):
    for r in range(start, end + 1):
        cell = ws.cell(row=r, column=4)  # 50% date column
        cell.value = target_date
        cell.number_format = 'DD/MM/YYYY'
```

This pattern applies to any bulk section-date change the user requests.

### Register Audit — Sub-Package Mixing Check

When asked to audit or clean a register, always check: **do any items appear before their section header?**

```python
issues = []
current_section = None
for r in range(3, ws.max_row + 1):
    ref = ws.cell(row=r, column=1).value
    sub = ws.cell(row=r, column=8).value
    if ref and any(str(ref).startswith(p) for p in ['A -', 'B -', 'C -', 'D -', 'E -', 'F -', 'G -']):
        current_section = str(ref).strip()
    elif ref and str(ref).startswith('MOC-ASE') and current_section is None:
        issues.append((r, str(ref)[:40], str(sub)[:20]))
```

If any issues found, warn user and suggest in-memory rebuild.

## MEP-Style Gate-Based Submission Plan (13-Column Flat Format)

An alternative to the 4-stage-sheet format. Used when the user provides an MEP "Stage 04 Submission Plan" xlsx as the template to follow. This format uses a **single sheet** with flat rows organized by gate (Detailed Design → Material Approval → Coordinated IFC).

**When to use:** The user says "follow the same template" referencing the MEP Submission Plan file. Use this format for discipline submission plans, not the 9-column stage-sheet format.

### Column Layout

```
Gate | Level / Zone | Discipline | Submission Category | Drawing Package / Item |
Submission Description | Responsibility | Planned Submission Date | Review Duration (Days) |
Approval Authority | Linked Activity ID (Program) | Status | Remarks
```

13 columns total. Column widths:

```python
COL_W = [18, 24, 14, 22, 42, 50, 16, 22, 20, 22, 28, 16, 40]
```

### Row Types & Styling

| Row Type | Font | Fill | Notes |
|----------|------|------|-------|
| Header row (R1) | Calibri 10 Bold, white | #366092 | Frozen at top |
| Gate header (Gate 1 / 2 / 3) | Calibri 12 Bold, white | #1F4E79 | Merged across all 13 cols, 28px h |
| System sub-header | Calibri 11 Bold, black | #BDD7EE | Merged across all 13 cols, 22px h |
| Data rows | Calibri 10, black | None | Center aligned, 20px h |

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HDR_FILL    = PatternFill('solid', fgColor='FF366092')
GATE_FILL   = PatternFill('solid', fgColor='FF1F4E79')
SYS_FILL    = PatternFill('solid', fgColor='FFBDD7EE')
HDR_FONT    = Font(name='Calibri', size=10, bold=True, color='FFFFFFFF')
GATE_FONT   = Font(name='Calibri', size=12, bold=True, color='FFFFFFFF')
SYS_FONT    = Font(name='Calibri', size=11, bold=True, color='FF000000')
DATA_FONT   = Font(name='Calibri', size=10, color='FF000000')
CENTER      = Alignment(horizontal='center', vertical='center', wrap_text=True)
THIN_B      = Border(left=Side('thin', 'FFD9D9D9'), right=Side('thin', 'FFD9D9D9'),
                     top=Side('thin', 'FFD9D9D9'), bottom=Side('thin', 'FFD9D9D9'))
```

### Gate Structure

| Gate | Title Suffix | Status | Review Duration |
|------|-------------|--------|-----------------|
| Gate 1 | DETAILED DESIGN | Submitted / In Progress / Planned | 7 days |
| Gate 2 | MATERIAL APPROVAL (Material Submittals Register) | Planned | 7 days |
| Gate 3 | COORDINATED IFC (Issued For Construction) | Planned | 14 days |

Gate headers are inserted at transition points between gate groups. Detect gate from the `gate` column value:
- `'Detailed Design'` → Gate 1
- `'Material Approval'` → Gate 2
- `'Coordinated IFC'` → Gate 3

### Sub-Headers Within Gates

Insert merged sub-header rows (light blue #BDD7EE) between logical groups within a gate. Detect insertion points by checking the Drawing Package / Item code for the first item in each group:

```python
sub_sections = [
    ('Completed Studies & Existing Data', lambda d: 'REP-001' in str(d[4])),
    ('Structural Analysis & Design (per BOD)', lambda d: 'MDL-004' in str(d[4])),
    ('Gallery-Specific Structural Items', lambda d: 'GAL-001' in str(d[4])),
    ('All Floors — IFC Packages', lambda d: '-IFC-' in str(d[4])),
]
```

### Drawing Package Numbering Convention

For disciplines without an MOC drawing number system (Structural, Rigging, etc.), use `ASE-{DISC}-{TYPE}-{NNN}`:

| Prefix | Type | Example |
|--------|------|---------|
| `ASE-STR-REP-NNN` | Reports | ASE-STR-REP-001 |
| `ASE-STR-DWG-NNN` | Drawings | ASE-STR-DWG-002 |
| `ASE-STR-MDL-NNN` | Models | ASE-STR-MDL-004 |
| `ASE-STR-CAL-NNN` | Calculations | ASE-STR-CAL-001 |
| `ASE-STR-GAL-NNN` | Gallery-specific | ASE-STR-GAL-001 |
| `ASE-STR-RIG-NNN` | Rigging | ASE-STR-RIG-001 |
| `ASE-STR-BIM-NNN` | BIM | ASE-STR-BIM-002 |
| `ASE-STR-MAT-NNN` | Material submittals | ASE-STR-MAT-001 |
| `ASE-STR-QA-NNN` | QA/Commissioning | ASE-STR-QA-001 |
| `ASE-STR-HO-NNN` | Handover | ASE-STR-HO-001 |
| `ASE-STR-BOQ-NNN` | BOQ | ASE-STR-BOQ-001 |
| `ASE-STR-SPC-NNN` | Specifications | ASE-STR-SPC-001 |

For IFC packages per floor: `STR-300001-IFC-{BF|LGF|GF|1F|2F|RF}`

### Completed Item Highlighting (Amber)

Mark already-submitted items with amber fill #F4B942 so they're visually distinct from pending white rows:

```python
AMBER = PatternFill('solid', fgColor='FFF4B942')

# In write loop:
if 'Submitted' in str(rm) or 'Submitted' in str(desc):
    cell.fill = AMBER
```

### Data Row Pattern

Define an `add()` helper to keep row definitions compact:

```python
def add(gate, zone, cat, pkg, desc, resp, dt, review='7',
        approver='Consultant / PMC', link='--', status='Planned', rm=''):
    rows.append([gate, zone, 'Structural', cat, pkg, desc, resp,
                 fmt(dt), f'{review} days', approver, link, status, rm])
```

For dates that are month-only approximations (not exact), use `add_str()` instead with a text date:

```python
def add_str(gate, zone, cat, pkg, desc, resp, dt_str, review='7',
        approver='Consultant / PMC', link='--', status='Planned', rm=''):
    rows.append([gate, zone, 'Structural', cat, pkg, desc, resp,
                 dt_str, f'{review} days', approver, link, status, rm])
```

### Example: Structural Gate 1 Items

```python
# Completed studies
add('Detailed Design', 'All Levels', 'Detailed Design',
    'ASE-STR-REP-001', 'Structural Schematic Design Report — ASG Rev.D',
    'Samaya TO', d(2025,3,6), status='Submitted',
    rm='Structural validation for scenography/fit-out.')

# Pending analysis
add_str('Detailed Design', 'All Levels', 'Detailed Design',
    'ASE-STR-CAL-002', 'Structural analysis — existing building (gravity + lateral)',
    'Samaya TO', 'Aug 2026', rm='Per BOD scope item 3.')

# Gallery-specific
add('Detailed Design', 'Basement (BF)', 'Detailed Design',
    'ASE-STR-GAL-001', 'G7 — Contemporary Art Commission support structure',
    'Samaya TO', d(2026,7,6), rm='Needs Arch GA + loading confirmation.')
```

### Template Script Location

A complete worked example (Structural Stage 04 Plan, 64 items, 3 gates) lives in the generator script. Copy and modify for other disciplines:

- **Generator:** `~/Desktop/Structural_Submittal_Register.py` (Aseer Museum project)
- **Output:** `.../03_Design_Files/NN_{Discipline}/Structural_Submittal_Register.xlsx`

### Pitfalls

- **Extra positional arg in `add()` calls** — The `add()` function takes exactly 7 positional args (gate, zone, cat, pkg, desc, resp, dt) + 5 keyword args. 8 positional args cause `TypeError: got multiple values`. Common mistake: passing `'BIM'` as an extra 3rd positional when the Submission Category (pos 4) already has 'Detailed Design'. Fix: use `'BIM'` as cat only when the MEP template uses 'BIM' as Submission Category (for BIM-specific rows).
- **Sheet name < 31 chars** — openpyxl warns if title > 31 chars. Keep sheet name short: `'Structural Stage 04 Plan'` not `'Structural Stage 04 Submission Plan'`.
- **Date format consistency** — The MEP template uses mixed date formats: `2026-07-07 00:00:00` for most, `26/7/2026` for a few. Use `dd/mm/yyyy` strings for consistency unless the user's template has a specific format.
- **cp to OneDrive** — Direct `cp` to OneDrive path works on macOS (verified 15 KB file). Fall back to AppleScript Finder duplicate only if `cp` produces a corrupt placeholder.

## 🔴 Stale CG_STATUS.md — Always Verify from Primary PDFs

**Critical pitfall:** The `CG_STATUS.md` files in each plan's `02_CG_Responses/` folder are often **stale** (last updated 29-May-2026 in Aseer Museum). They are secondary summaries generated by an earlier agent session and are NOT authoritative.

**Always verify CG response status from the actual CG Reply PDF** in the same folder:

```python
# Extract approval code from CG Reply PDF
import subprocess
result = subprocess.run(['pdftotext', 'CG_Reply.pdf', '-'], capture_output=True, text=True, timeout=30)
lines = result.stdout.split('\n')
for line in lines:
    if 'Code' in line and ('A:' in line or 'B:' in line or 'C:' in line or 'D:' in line 
                           or 'Code A' in line or 'Code B' in line or 'Code C' in line or 'Code D' in line):
        print(f'{fname}: {line.strip()[:150]}')
        break
```

**Real example (Aseer Museum, Jul 2026):** The CG_STATUS.md said DMP Rev.02 was "Pending" and several HSE plans had wrong codes. Actual CG Reply PDFs showed:
- DMP Rev.02 = **Code B** (not Pending)
- PL-0036 Fire Prevention Rev.01 = **Code B** (not C)
- PL-0040 Site Security = **Code C** (not B)
- PL-0043 Temp Electrical = **Code C** (not B)
- SC-0035 HSE Deliverables = **Code A** (not Mixed A/B/C)

**Workflow:**
1. When updating plan statuses, always open the actual CG Reply PDF in `02_CG_Responses/`
2. Extract the Code line using pdftotext
3. Cross-reference against CG_STATUS.md — if they differ, the PDF wins
4. Update both the register AND the CG_STATUS.md with the correct status
5. Update the `last_updated` timestamp in CG_STATUS.md

## CG Code C on Design Gateway — Register Iteration Pattern

When a design gateway submission (e.g., 50% Design Gateway BOD + Loading Plans) receives **Code C — Revise & Resubmit** from CG, the register must be updated to a new revision that:

1. **Adds pre-requisite items** that CG requires BEFORE any design work can proceed:
   - Structural engineering team approval (submit CVs, credentials, organogram)
   - Audit report on previous design stage
   - Separate risk assessment reports

2. **Updates existing items** to reflect resubmission scope:
   - BOD Report → Rev.01 (addressing all CG comments)
   - Loading Plans → Rev.01 with loading notation schedule, masonry standards, concrete cover compliance, wind/seismic table references, seismic importance factor, load combination definitions

3. **Adds new items** for CG-requested studies not previously scoped:
   - Temperature differential analysis (regional climate)
   - Revised loading plans for unaddressed areas (external staircases, solped planting zones)
   - Final loading plans after Arch/MEP/artwork/landscape approval

4. **Shifts all downstream dates** — analysis items push later since BOD resubmission is delayed

5. **Expands the CG Comments Compliance sheet** with the new comments

### Tracking Resolved vs Pending Comments

After a Code C response, CG comments can be resolved in meetings or by formal submissions. Track status explicitly in the CG Comments Compliance sheet:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `✅` (in register) | Register item exists addressing the comment | When the item was added to the plan |
| `RESOLVED — meeting dd/mm/yy` | Comment resolved verbally/in meeting | User says "we solved comment #X" |
| `RESOLVED — submission approved dd/mm/yy` | Comment resolved via formal submission | CG accepted the resubmission |
| `PENDING` | Still needs action from subcontractor/engineer | Default for open items |

**When user says "we solved comment #X" — update the register AND produce a filtered action list:**

1. Update the compliance sheet row: change status from `✅` to `RESOLVED — meeting dd/mm/yy`
2. Keep the original numbering for traceability (don't re-number)
3. Produce a **filtered action list** showing only open items, with resolved ones greyed out

### Filtered Action List Pattern (for subcontractor/engineer)

When asked "what's next for [engineer]" after some comments resolved:

```
## Actions Required from [Engineer Name]

| # | CG Ref | Item | Due | Blocked By |
|---|--------|------|-----|------------|
| ✅ | **#1** | **Team approval** — resolved in meeting | **Done** | — |
| 2 | #2 | Audit report on previous design stage | 07-Jul | — |
| 3 | #5 | Separate risk assessment reports | 07-Jul | — |
| ... | ... | ... | ... | ... |
```

- ✅ rows use strikethrough or grey fill to indicate done (in xlsx)
- In text/tables: keep the row but add `✅` prefix and `—` in status fields
- Remaining items re-ordered by urgency/due date for clarity
- Include a "Critical path" note highlighting the nearest deadline

### Common CG Comment Categories on 50% Design Gateway (from 1G-0001)

| Category | CG Comments | Register Action |
|----------|-------------|-----------------|
| **Pre-requisite** | Team approval, audit report, risk assessment | Add as new items BEFORE Gate 1 with earlier dates |
| **Loading methodology** | Notation schedule, masonry weight standard, concrete cover, wind/seismic tables, seismic importance factor, load combination definitions | Update existing Loading Plans item description to include all requirements |
| **Regional analysis** | Temperature differential for local climate | Add new item |
| **Unaddressed areas** | External staircases, solped planting zones | Add new item(s) |
| **Cross-discipline dependency** | All Arch/MEP changes reflected, final loading after Arch/MEP/artwork/landscape approval | Add new item with TBC date (post-Arch approval) |
| **Site investigation** | Core testing, geotechnical report (seismic parameters) | Already covered in Rev.01 — update descriptions |

### Register Revision Naming

```
Structural_Submittal_Register_Rev00.xlsx  (original)
Structural_Submittal_Register_Rev01.xlsx  (after Submission Plan CG comments)
Structural_Submittal_Register_Rev02.xlsx  (after 1G-0001 Code C)
```

Each revision keeps the same 3-sheet structure (Main Plan, Rigging Register, CG Comments Compliance) with the Compliance sheet growing to cover new comments.

### CG Comments Compliance Sheet Growth Pattern

| Revision | CG Source | Comments Covered |
|----------|-----------|-----------------|
| Rev.00 | — | 0 (no compliance sheet) |
| Rev.01 | Submission Plan CG | 7 comments |
| Rev.02 | 1G-0001 (50% Gateway) | 22 comments (7 original + 15 new) |

## 🔴 CRITICAL: Date Logic Validation (O&M / Handover / Close-Out Items)

**O&M, handover, close-out, as-built, commissioning, training, spare parts, warranty, and record-drawing items MUST only have dates in the IFC/AFC column (position 3 in the date array).** They must NEVER appear in the 50%, 90%, or 100% columns.

**Rationale:** These deliverables are produced at project handover, not during design stages. Placing them in early-stage columns creates false schedule logic and misrepresents project progress. The user explicitly enforces this rule.

### Keywords to Scan

| Category | Keywords |
|----------|----------|
| Handover | O&M, Operation, Maintenance, Handover, Close-out, Closeout |
| As-Built | As-Built, As Built, Record Drawing, Record Drawings |
| Commissioning | Commissioning, ITP, Inspection & Test Plan |
| Training | Training, Spare, Spares, Warranty |
| Close-out | AFC, AFC Documentation, Designer Certification |

### Validation Checklist (run before finalizing any register)

1. Scan all items for the keywords above
2. For each match, verify the date array has `'—'` in positions 0-2 (50%, 90%, 100%) and the actual date only in position 3 (IFC/AFC)
3. **Exception:** Existing-building surveys documenting pre-design conditions may legitimately appear in the 50% column — but their description must clearly say "Existing Building Survey" or "Existing Condition" not "As-Built" to avoid confusion with project handover as-builts
4. Run the audit script (`scripts/audit_register_dates.py`) before finalizing any register

### Audit Script

```bash
python3 /path/to/scripts/audit_register_dates.py <register.xlsx>
```

The script checks all sheets, flags any O&M/handover item with a non-`'—'` date in 50%/90%/100% columns, and reports pass/fail per register.

### Example: Correct Date Arrays

```python
# Handover items — IFC only
its.append(('ST-055', 'Structural O&M manual', 'Structural',
    ['—', '—', '—', '28/08/2026'], 'Handover', ''))

# Existing building survey — legitimate at 50% (description must say "Existing")
its.append(('ST-003', 'Existing Building Survey — structural drawings', 'Structural',
    ['06/03/2025', '—', '—', '—'], 'Survey', 'Submitted — pre-design condition record'))
```

## Preferred Workflow

1. **Source data first** — check 24_Subcontractors, BOQ, NRS packages (see Data Sourcing Priority above)
2. Determine scope boundaries — design items → Architecture register, subcontractor items → package register
3. **Present a plan first** — when asked to build multiple discipline plans, show a summary of what data is available per discipline, estimated item counts, and date ranges. Do NOT build all at once. Wait for explicit go-ahead per discipline.
4. Create `.py` generator script with standard template
5. Define items as tuples with date arrays (or mask arrays for no-dates registers)
6. Define categories (`cn`) and compute `next_cat`
7. **Validate date logic** — run the date logic audit (see 🔴 CRITICAL section above) before generating the xlsx
8. Generate `.xlsx` to `/tmp/` first
9. **Open the file immediately** — after generating, run `open <filepath>` so the user can inspect it. Do not wait for them to ask.
10. Copy to OneDrive via Finder (AppleScript)
11. Copy `.py` to `scripts/` folder
12. Verify — load xlsx, check headers, dates/samples, sample rows
