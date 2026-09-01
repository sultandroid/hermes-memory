# Drawing Register from a Stamped PDF Package (Aseer Arch template)

## When to Use

User points at a folder of stamped specialist drawing PDFs (e.g. ZNA lighting `*_NRS_stamp.pdf`)
and says "make an Excel drawing register as per the Aseer project template." The deliverable is
a `.xlsx` matching the Arch drawing-register layout (15 columns, navy header, dark title bar,
grey category bands, "Summary by Category" second sheet).

## The Aseer Arch Drawing Register Template (verified cell map)

Two sheets: `Drawing Register` + `Summary by Category`.

**Drawing Register sheet:**
- Row 1: `DOCUMENT ISSUE — DRAWINGS, SCHEDULES & SPECIFICATIONS` (Arial 13 bold, white on `FF1F3864`, merged A1:O1)
- Rows 2-6: meta block — `Project:` / `Client:` / `Contractor:` / `File Reference:` / `Source / Originator:` (label bold, value plain, Arial 10)
- Row 7: submission header (e.g. `1 ST SUBMISSION`) merged G7:M7
- Row 8: column headers — `No. | Drawing Number | Title | Scale | Size | Rev | Date | (7 date cols) | Cons. code | Reference` — Arial 10 bold white on `FF2E5496`
- Category rows: full-width merged, Arial 10 bold white on `FF808080`
- Data rows: Arial 10, thin borders, No./Scale/Size/Rev/Date centered, Drawing Number + Title left
- Total row: `TOTAL DOCUMENTS` merged A:E, count in F

**Column widths:** A=6, B=36, C=68, D=16, E=11, F=6, G..M=17-21, N=14, O=40.

**Summary by Category sheet:** `Category | Count` + TOTAL.

## Extracting title-block data from stamped PDFs

The specialist's PDFs carry a title block (often bilingual AR/EN) with the fields you need.
Extract with `pdftotext -layout` and parse:

- **Drawing Number / Name** — `Drawing Name:` line (e.g. `MOC-ASE-LI-LIG-LL-BF-DDD-3001`)
- **Scale** — the `Scale:` label; the value is often on the NEXT line (the "Samaya Checked By"
  line), not the same line. Parse: find `Scale:` then scan the following 1-2 lines for a
  `\d+\s*:\s*\d+` ratio. Detail sheets often show `-` (NTS).
- **Date** — `Submissin Date:` (note the typo "Submissin" in ZNA's block) → `28/08/26`
- **Suitability Code** — `Suitability Code:` → `D` (Draft) etc.
- **Page size** — `pdfinfo` → `Page size: W x H pts`. Map to A0/A1/A2/A3/A4 by area:
  A0=2384x3370, A1=1684x2384, A2=1191x1684, A3=842x1191, A4=595x842 (allow ±40pt).

## Cross-check against the specialist's OWN document register

The specialist usually ships a document register PDF alongside the drawings (e.g.
`3297 ARM ZNA Document Register _%50 Stage 4 DD Lighting Issue.pdf`). This is the
**authoritative source for drawing TITLES** — the title block often leaves the "Drawing Title"
field blank, so the register's `AUTHOR/ DRAWING TITLE` column is what you use. Parse it with
`pdftotext -layout`; it lists `DWG No. | AUTHOR/ DRAWING TITLE | STATUS` grouped by category
(Lighting Plans / Showcase Drawings / Schedule & Specification).

## Pitfalls

- **Title block "Drawing Title" is often empty** — the actual title lives in the specialist's
  document register, not the PDF title block. Don't guess titles from the drawing content.
- **Scale value is on the line AFTER `Scale:`** — a naive same-line regex returns None.
- **The register may list docs NOT in the stamped folder** (e.g. ZNA listed 2820/2821 showcase
  schedule/spec that weren't issued). Build the register from what's actually in the folder;
  flag the missing ones to the user rather than silently adding them.
- **Detail sheets (2800-series) have no scale** — mark `NTS` (not to scale) and confirm with user.
- **Schedules/specs are A3/A4, plans are A0** — size comes from `pdfinfo`, not the title block.
- **Deploy OneDrive-safe** — stage to `/tmp/`, then Finder `duplicate ... with replacing`
  (never write directly to the CloudStorage path).

## Reference: worked example

ZNA 50% Stage 4 Lighting Issue (25 docs, 3 categories) — see the session that produced
`Lighting_Drawing_Register_Aseer_Register.xlsx`. Category split: Lighting Plans (9), Showcase
Drawings (9), Schedule & Specification (7).
