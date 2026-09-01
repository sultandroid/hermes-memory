# Drawing Register (Arch Template) — Format + PDF Extraction

The **Drawing Register** is a DIFFERENT format from the 9-column submittal register.
It is the "DOCUMENT ISSUE — DRAWINGS, SCHEDULES & SPECIFICATIONS" sheet used for
per-discipline drawing packages (Arch, Lighting, AV, etc.). Reference template:
`02_Submittals/03_DD Documents/Arch DD Package 29-6-26/Drawing_Register_Aseer_Register.xlsx`.

## Exact template structure (match this, don't improvise)

Two sheets: `Drawing Register` + `Summary by Category`.

### Sheet 1 — Drawing Register (15 columns A:O)

| Row | Content | Style |
|-----|---------|-------|
| 1 | `DOCUMENT ISSUE — DRAWINGS, SCHEDULES & SPECIFICATIONS` (merged A1:O1) | Arial 13 bold, white on `#1F3864` |
| 2–6 | Meta: `Project:` / `Client:` / `Contractor:` / `File Reference:` / `Source / Originator:` (label col A, value col B) | label bold, value normal, Arial 10 |
| 7 | Submission headers `1 ST SUBMISSION` … `3RD SUBMISSION REV` (merged G7:M7 for single issue) | Arial 10 bold |
| 8 | Column headers | Arial 10 bold, white on `#2E5496`, centered, wrap |
| 9+ | Category band rows (e.g. `LIGHTING PLANS`) merged A:O | Arial 10 bold, white on `#808080` |
| data | drawing rows | Arial 10, thin black borders |

Columns (A:O): `No.` `Drawing Number` `Title` `Scale` `Size` `Rev` `Date` ×7 submission
date columns `Cons. code` `Reference`.

Column widths: A=6, B=36, C=68, D=16, E=11, F=6, G–M≈17–21, N=14, O=40.

Last row: `TOTAL DOCUMENTS` (merged A:E) + count in F.

### Sheet 2 — Summary by Category
`Category` / `Count` table + `TOTAL` row. Simple, no styling beyond bold headers.

## Extracting data from stamped PDFs (the reliable path)

1. **Authoritative titles come from the specialist's own document register PDF**, not
   the title blocks. ZNA ships `3297 ARM ZNA Document Register _%50 Stage 4 DD Lighting Issue.pdf`
   with a clean `DWG No. | AUTHOR/ DRAWING TITLE | STATUS` table. Parse that first —
   it has the real titles ("Basement Floor High Level Lighting Plan", "Showcase Type-1
   Lighting Detail", etc.) that the drawing title blocks leave BLANK.
2. Title-block fields via `pdftotext -layout`:
   - `Drawing Name:` → the MOC-ASE-* number (confirms filename).
   - `Scale:` value is on the line **AFTER** the `Scale:` label (the "Samaya Checked By"
     line), NOT the same line. Regex `Scale:\s*\n?\s*([0-9]+\s*:\s*[0-9]+|-)`.
   - `Submissin Date:` (sic — ZNA's typo) → `28/08/26`.
   - `Suitability Code:` → A/B/C/D (D = Rejected).
3. **Page size** via `pdfinfo` → `Page size: 2384 x 3370 pts (A0)` etc. Map pts to
   A0=2384×3370, A1=1684×2384, A2=1191×1684, A3=842×1191, A4=595×842 (tolerance ±40).
4. Detail sheets (2800-series showcase details) and the control diagram have **blank
   scale** in the title block → mark `NTS` (not to scale). Schedules/specs/reports →
   `N/A` scale, A3/A4 size.

## Pitfalls

- The register must reflect what is **actually issued** in the stamped folder. ZNA's
  register may list docs (e.g. 2820/2821 Showcase Schedule+Spec) that are NOT in the
  stamped folder — leave them out and flag to the user rather than inventing rows.
- `File Reference:` uses the discipline code, e.g. `MOC-ASE-LI-LIG-GEN-DDD-DIS`
  (Lighting) vs `MOC-ASE-AR-ARC-GEN-DDD-DIS` (Arch).
- `Source / Originator:` = the specialist (Studio ZNA), not NRS.
- Deploy to OneDrive via Finder `duplicate` (AppleScript), never direct write — same
  OneDrive-safe rule as the submittal register.
