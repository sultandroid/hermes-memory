---
name: excel-submission-plan-routine
description: Standard routine for creating/editing Excel submission plans and registers. Clean, human-readable, no AI fingerprints. Apply to all disciplines (Arch, Structural, MEP, AV, etc.).
tags:
  - excel
  - submission-plan
  - register
  - openpyxl
  - template
---

# Excel Submission Plan & Register Routine

## Core Principles

1. **Submission plan = forward schedule only.** List what, who, when. No commentary — CR sheet holds the explanations.
2. **CR sheet = one sheet per submission package, all CG sources included.** Each submission package (e.g. Arch Submission Plan review) gets one CR sheet. If multiple CG reviewers comment on the same package (e.g. Mohammad Elbaz + Maged Zamzam), merge them into one sheet with separate numbering (CR-01 to CR-13 for Elbaz, CR-14 to CR-20 for Zamzam). One sheet per submission package. The Summary sheet lists all sources. Do NOT create separate sheets per reviewer.
3. **File naming.** Use `Rev00`, `Rev01`, `Rev02` — never `Modification`, `[7]`, `_final`, or other suffixes.
4. **Descriptions are short.** One sentence stating the deliverable. No AI-style verbose paragraphs.
5. **Dates = Excel serial numbers.** Store as integers (e.g. 46210 = 07/07/26). Apply `dd/mm/yy` format. openpyxl may not apply format reliably — user applies date format manually in Excel if serials show. Do NOT convert to text strings.
6. **No duplicates.** New items appear once under the correct floor/section.
7. **Response framing is from Samaya always.** Never say "NRS scope" or "by others" — say "to be coordinated" or "to be included in subsequent stages". Frustration on framing = immediate skill update signal.
8. **Section rows** are full-width merged: gates blue (`#D6E4F0`), floors grey (`#E8E8E8`).
9. **IFC descriptions** short — avoid repeating boilerplate.
10. **Linked Activity ID** — map to schedule (EN108, EN102, etc.).
11. **Submitted rows** get very light green (`#F0F8F0`).
12. **Response Code and Resubmit Date columns** after Status for CG codes.
13. **Remarks** minimal. C:Resubmit caveman style: "CG want: X, Y. Need to fix and resubmit."
14. **Only mark truly submitted.** Drafts = Pending.
15. **Separate registers** = no cross-links.
16. **C:Resubmit** = yellow, "BLOCKED - CG Code C." prefix.
17. **Corrupted files** = rebuild from scratch with hardcoded data.
18. **OneDrive** = copy to `/tmp/`, work there, delete target before copy-back.
19. **Discipline naming.** "1F" for structural, "First Floor" for arch.
20. **CG response PDFs** filed to `02_CG_Responses/{Discipline}/`.

## Project Repo Convention

The project repo (`aseer-museum-pm`) is **status-only**:
- Only markdown files (`.md`) - no binaries
- No PDFs, no xlsx, no docx, no dwg
- No images, no archives
- `.gitignore` blocks all binary formats
- Push only status updates, decisions, action items, and register summaries
- When creating submission plans/registers, the xlsx files live in OneDrive BIM path and the response folder, NOT in the git repo
- The git repo only gets a status update in `00_Status/project_status.md` noting what was done

## Two-Stream CG Response

When CG comments arrive, separate them into two streams:
1. **Submission Plan CR Sheet** (sent to CG) — what to submit, when, by whom
2. **Consultant Comment Register** (internal) — technical review details, Code C items

Never merge both streams into one response document.

## Response Framing (CR sheets)

### General Rules
- Caveman style: drop articles, filler, hedging. Short fragments. Technical terms exact.
- Samaya perspective always — never mention internal sub-consultant splits to CG.
- **Preserve the CG comment verbatim.** The CG Comment column (col 2) must contain the ORIGINAL text from the reviewer's email — never summarize, paraphrase, or rewrite. The Response column (col 4) is where you respond.
- Responses reflect the actual position of the party who prepared the deliverable. When NRS says "Stage 3 covers this, not typical Stage 4, but easy win for CG," the CR response should say that.

### NRS "Easy Win" Pattern
When NRS disagrees but complies, or when an item is already in the submission plan:

| Situation | Pattern |
|-----------|---------|
| Stage 3 already covers | "Stage 3 covers this. No changes. NRS draft [doc] as reference. Will submit as per submission plan." |
| Defined by Stage 3, no changes | "Stage 3 defines [scope]. No changes. NRS draft [doc] as reference. Will submit as per submission plan." |
| NRS flagged issues on Stage 3 | "NRS flagged [issue] on Stage 3 drawings. NRS prepared draft [doc] for reference. Will be submitted as per submission plan and drawing register." |
| Already in arch packages | "Already included in Arch packages in submission plan." |
| To be coordinated by another party | "[Scope] to be coordinated by [party]. Not in current arch package." |
| Covered in later stages | "Covered in 90% and IFC packages. [Detail] in drawings where needed." |

### Furniture Layout Rule
Furniture layout is an **architectural package deliverable**, not dependent on FF&E supplier. The layout plan showing furniture locations, dimensions, and clearances is part of the architectural package. The FF&E supplier provides the actual furniture items. CG comment is Closed when layout is on GA drawings and noted in submission plan. The supplier appointment is a separate procurement action. Response: "Furniture layout on GA. Separate plan noted. In drawing register & submission plan."

### Example Responses (caveman style)

**Architecture (submission plan):**
- "Stage 3 covers this. No changes to exhibition narrative or showcase locations. NRS draft 1820 as reference. Easy win for CG."
- "Furniture layout on GA. Separate plan noted. In drawing register & submission plan."
- "Stage 3 defines layout. No changes. NRS draft 1280 as reference. Will submit as per submission plan."
- "Life Safety scope. Not in arch package."
- "NRS flagged wayfinding discrepancies on Stage 3 drawings. NRS prepared draft 1260 for reference. Will be submitted as per submission plan and drawing register."
- "Stage 3 defines maintenance strategy. No changes. NRS draft 1270 as reference. Easy win for CG."

**Structure (submission plan):**
- "Noted. Rigging register created (RIG-001 to 007)."
- "Core testing under prep. Results in Design Criteria Report."
- "Geotech investigation arranged. Borehole for ramp area."
- "All loads in BOD per SBC. Showcase weights from mfr. Artwork TBC."
- "Noted. Existing building assessment first. Modifications later."

**Maged Zamzam reviews (scenography package):**
- "Covered by CR-01. 1820 draft in submission plan."
- "Showcase locations on GA. In drawing register."
- "Already included in Arch packages in submission plan." (showcase details)
- "Lighting design by ZNA. In lighting package."
- "NRS draft interactive locations in drawing register. AV and interactive specialist to finalize."
- "Covered in 90% and IFC packages. Finishes schedules in drawings where needed."
- "MEP scope. In MEP submittals register."

## Samaya Voice (CR Sheet Responses)

**WRONG (sub-consultant voice):**
- "NRS only provides bespoke setwork furniture. Other FF&E outside NRS scope sourced by Samaya."
- "NRS confirms these are outside their scope."
- "NRS prepared a draft copy..."
- "Graphics outside NRS scope."

**RIGHT (Samaya voice):**
- "Bespoke setwork furniture is shown on the GA drawings. Remaining FF&E will be coordinated and included from 50% to 90% to IFC. FF&E supplier to be appointed."
- "This will be in the Life Safety registers, not in the current architectural package."
- "Draft included in submission plan."
- "NRS flagged wayfinding discrepancies on Stage 3 drawings. NRS prepared draft for reference. Will be submitted as per submission plan and drawing register."

Key rules:
- Never say "NRS scope" or "by others" or "outside NRS scope" — say "to be coordinated" or "to be included in subsequent stages"
- Never say "NRS confirms" — say "this was completed at Stage 3" or "this will be in..."
- Never explain internal team structure to CG
- "Noted." for accepted items — not long explanations
- "FF&E supplier to be appointed. To be included from 50% to 90% to IFC." — not "NRS only provides bespoke..."

## Caveman Style (CR Sheet Responses)

All CR sheet responses must be in caveman style — short direct sentences, no articles, no filler. Pattern: [What happened / scope]. [Where tracked]. [Next step if any].

**Critical rule: Preserve the CG comment verbatim.** The CG Comment column (col 2) must contain the ORIGINAL text from the reviewer's email — never summarize, paraphrase, or rewrite. The response column (col 4) is where you respond. Many CG comments are long and detailed; truncate with ellipsis only if needed, but never rewrite the intent.

**Examples from this session:**
- Scenography: "Stage 3 done. NRS draft 1820 for ref. In submission plan & drawing register."
- Furniture: "Furniture layout on GA. Separate plan noted. In drawing register & submission plan."
- Life Safety: "Life Safety scope. Not in arch package."
- Signage: "NRS draft 1260 for ref. Wayfinding issues flagged on Stage 3. In submission plan."
- Maintenance: "Stage 3 done. NRS draft 1270 for ref. In submission plan & drawing register."
- Maged items: "Covered by CR-01. 1820 draft in submission plan." / "Showcase locations on GA. In drawing register." / "Showcase details in separate showcase package." / "Lighting design by ZNA. In lighting package." / "MEP scope. In MEP submittals register." / "Covered by Material Submittals Register. Gate 2 schedule."

**Furniture layout rule:** Furniture layout is an **architectural package deliverable**, not dependent on FF&E supplier. The layout plan showing furniture locations, dimensions, and clearances is part of the architectural package. The FF&E supplier provides the actual furniture items. CG comment is Closed when layout is on GA drawings and noted in submission plan. The supplier appointment is a separate procurement action. Response: "Furniture layout on GA. Separate plan noted. In drawing register & submission plan."

**When NRS says "Stage 3 covers this, not typical Stage 4, but easy win for CG":** Accept the draft they prepared, mark Closed, note in submission plan. The CR response should reflect NRS's position: "Stage 3 covers this. No changes. NRS draft [number] as reference. Easy win for CG."

## Section Structure (any submission register)

```
Gate 1 - Detailed Design
  ├── DD - [Floor Name]        (e.g. DD - Basement Floor)
  ├── DD - [Floor Name]
  ├── DD - General (All Levels)
Gate 2 - Material Approval
  ├── Material List - All Levels
Gate 3 - IFC (Issued for Construction)
  ├── IFC - All Floors
  ├── General - All Levels
```

## Column Layout

| # | Header | Notes |
|---|--------|-------|
| 1 | Gate | Section header (merged full-width) |
| 2 | Level / Zone | Floor level |
| 3 | Discipline | Architectural, Structural, etc. |
| 4 | Submission Category | Detailed Design, Coordinated IFC, etc. |
| 5 | Drawing Package / Item | Drawing number or package name |
| 6 | Submission Description | One-line deliverable description |
| 7 | Responsibility | Samaya or consultant code |
| 8 | Planned Submission Date | Excel serial number with dd/mm/yy format |
| 9 | Review Duration (Days) | Number of days |
| 10 | Approval Authority | CG or PMC |
| 11 | Linked Activity ID (Program) | Schedule activity ID (EN108, EN136, etc.) |
| 12 | Status | Submitted / Pending / In Progress / Planned / C:Resubmit |
| 13 | Response Code | CG code (A/B/C/D) — added after Status |
| 14 | Resubmit Date | Date for resubmission if Code C |
| 15 | Remarks | Minimal notes only |

## Style Rules

- Header: Navy `#1F3864`, white Calibri bold 10pt
- Gate headers: Navy Calibri bold 11pt, blue fill `#D6E4F0`, merged full-width
- Floor headers: Navy Calibri bold 10pt, grey fill `#E8E8E8`, merged full-width
- Body: Calibri 10pt
- Status colors: Green fill `#E2EFDA` for Submitted, Yellow `#FFF2CC` for Pending/In Progress/C:Resubmit
- Submitted row highlight: Very light green `#F0F8F0` across all cells
- Thin borders on all cells
- Wrap text, top vertical alignment

## File Organization (Registers folder)

```
04_Registers/
  ├── Arch_Submittal_Register/
  ├── Structural_Submittal_Register/
  ├── AV_Submittal_Register/
  ├── Risk_Registers/
  ├── [discipline]_Submittal_Register/
  └── (loose files only if no subfolder exists)
```

- Each discipline has its own subfolder
- No misplaced PDFs or DOCX in register folders
- No temp files (`~$` prefix)
- Separate rigging register if required by CG

## Activity ID Mapping (from Schedule)

### Architectural

| Activity | Description | Typical Date |
|----------|-------------|-------------|
| EN1000 | 3D Shot submission | 12-Jul-26 |
| EN108 | Architectural Technical Design 50% | 19-Jul-26 |
| EN109 | Architectural BIM Model 50% | 19-Jul-26 |
| EN110 | Product/Material Submittal Schedule 50% | 20-Jul-26 |
| EN111 | Approval of Architectural Technical Design 50% | 19-Jul-26 |
| EN134 | Exhibition Lighting Design 50% | 27-Jul-26 |
| EN135 | Showcase Design 50% | 27-Jul-26 |
| EN136 | Graphic Design 50% (Exhibitions + Wayfinding) | 27-Jul-26 |
| EN137 | AV Hardware Systems Design 50% | 27-Jul-26 |
| EN144 | Architectural Technical Design 90% | 19-Aug-26 |
| EN163 | BIM Model 90% | 03-Sep-26 |
| EN164 | Clash Detection Report 90% | 03-Sep-26 |

### Structural

| Activity | Description | Typical Date |
|----------|-------------|-------------|
| EN102 | Structural Design 50% (BOD, loading, analysis, gallery items) | 02-Jul-26 |
| EN103 | Structural BIM Model (LOD 300, 350) | 19-Jul-26 |
| EN104 | Structural Product/Material Submittal (core test, geotechnical, materials) | 15-Jul-26 |
| EN144 | Structural Design 90% (IFC packages all floors) | 19-Aug-26 |
| EN163 | BIM Model 90% (as-built) | 03-Sep-26 |

## Python openpyxl Quick Reference

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta

# Date to serial
def date_to_serial(d, m, y):
    base = datetime(1899, 12, 30)
    return (datetime(y, m, d) - base).days

# Serial to date string
def serial_to_date(serial):
    base = datetime(1899, 12, 30)
    return (base + timedelta(days=serial)).strftime('%d/%m/%y')

# Styles
header_font = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
header_fill = PatternFill(start_color='1F3864', end_color='1F3864', fill_type='solid')
section_font = Font(name='Calibri', bold=True, size=11, color='1F3864')
section_fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
floor_font = Font(name='Calibri', bold=True, size=10, color='1F3864')
floor_fill = PatternFill(start_color='E8E8E8', end_color='E8E8E8', fill_type='solid')
body_font = Font(name='Calibri', size=10)
light_green = PatternFill(start_color='F0F8F0', end_color='F0F8F0', fill_type='solid')
green_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
yellow_fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
wrap_align = Alignment(wrap_text=True, vertical='top')
center_align = Alignment(wrap_text=True, vertical='center', horizontal='center')
```
