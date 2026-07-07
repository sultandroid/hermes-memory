---
name: schedule-materials-audit
category: productivity
description: Audit contractor Primavera P6 schedules against design documents to extract material/supplier traceability matrices. Cross-reference schedule activities with design specs (Finishes, Luminaire, AV, FF&E schedules) to identify named brands and build a traceable Excel register.
---

# Schedule & Materials Audit — Contractor Submittal Review

Audit a contractor's Primavera P6 programme submission by cross-referencing schedule activities against the project's design documents. The goal is to identify which materials/systems have already been specified with named suppliers in the design, flag gaps, and build a traceability register.

## When to Load

- User shares a contractor schedule (P6 export, MS Project, PDF Gantt) and asks for a review or audit
- User asks to extract materials, suppliers, or brands from a schedule against design docs
- User needs a traceability matrix linking schedule activities → design spec references → named suppliers
- Task involves comparing multiple contractor/subcontractor offers

## Workflow

### Phase 1: Schedule Ingestion

1. **Extract the schedule text** — dump the P6 export to a text file:
   ```bash
   pdftotext -layout "Schedule.pdf" /tmp/schedule.txt
   ```
   or for A3 landscape exports:
   ```bash
   pdftotext -layout -W 1200 "Schedule.pdf" /tmp/schedule.txt
   ```

2. **Map the WBS structure** — identify top-level phases:
   - Milestones
   - Preliminaries / Mobilization
   - Assessment & Survey
   - Engineering / Design (50%, 90%, 100% IFC)
   - Procurement (Pre-qual → Supplier Approval → Specs/Data Sheets → PO → Delivery)
   - Construction (by floor/zone)
   - Testing, Commissioning & Handover

3. **Extract the relevant section** — stage 3 (Specifications & Data Sheet Materials) is typically the materials submittal phase. Read that section from the text dump.

### Phase 2: Design Document Discovery

Search the project folder for these design schedule files (typical locations):

| Document Type | Typical Location | What It Contains |
|---|---|---|
| Finishes Schedule | `Design Files/*/07-Lighting Design_rev A/Specifications & Schedules/` or `Xcel/` | Material ID, description, color, **supplier name** |
| Luminaire Specification | `*Lighting Design*/ZNA*_SP_01_01*` | Luminaire type, **manufacturer**, model, CRI, control protocol |
| AV BOQ | `06-AVHW + AV System Concept*/av_boq_v*` | AV hardware with **make/model** per item |
| FF&E Schedule | `*FF&E Schedule*` | Furniture items with **supplier/URL**, finish |
| Showcase Schedule | `*Showcase Schedule*` | Showcase types, dimensions, lock type, glass spec |
| Materials Register | `B.O.Q/Materials & Subcontractor Register*` | Material categories with design responsibility |
| Floor Finishing Detail | `B.O.Q/Floor-Finishing-Material-Detail*` | Floor finish materials with **supplier** |

### Phase 3: Cross-Reference & Brand Extraction

For each activity in the Stage 3 schedule, match the material description to a design document entry:

1. **Map material descriptions** — schedule may use generic names ("Submit Material for Porcelain Tiles 120x120cm Color Salt"), while the design schedule has the same item as `FI_FL_03` with a named supplier.

2. **Extract supplier/brand** from these columns in design schedules:
   - **Finishes Schedule**: Column 6 (Supplier)
   - **Luminaire Spec**: MANUFACTURER / SUPPLIER block
   - **AV BOQ**: Column 4 (make/model)
   - **FF&E Schedule**: Column 7 (Supplier URL/name)

3. **Handle scanned PDFs** (image-based, no text extraction):
   ```python
   import fitz
   doc = fitz.open("document.pdf")
   page = doc[0]
   pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
   pix.save("page.jpg")
   # Then use tesseract:
   # import pytesseract; text = pytesseract.image_to_string("page.jpg")
   ```

### Phase 4: Build the Traceability Matrix (Excel)

Create an Excel with columns:

| Column | Content |
|---|---|
| # | Sequential |
| Activity ID | From schedule (e.g., PR2880) |
| Material / Product | From schedule activity description |
| Design Spec / Ref | Design reference code + description (e.g., FI_FL_03: Glitch Porcelain) |
| Supplier / Brand | Named supplier from design document |
| Source Document | Which design file + row reference |
| Submittal Start | From schedule |
| Submittal End | From schedule |
| Float | Critical path indicator |
| Critical | Yes/No (0 float = critical) |

**Formatting:**
- Green highlight for cells with confirmed brands
- Red row highlight for critical-path items (0 float)
- Freeze header row, auto-filter enabled
- Source document column with specific row/file references for traceability

### Phase 5: Audit Findings

Report findings by severity:

| Severity | Criteria |
|---|---|
| **HIGH** | Items on critical path with TBC supplier; items where design named a brand but schedule doesn't reflect it; schedule logic errors (parallel 50%/90% design, surveys after design start) |
| **MEDIUM** | Missing coordination milestones; compressed durations (e.g., 9-day BIM+clash); isolated parallel workstreams with no integration points |
| **LOW** | Missing milestone dates; calendar/holiday assumptions; documentation gaps |

## Pitfalls

- **Scanned PDFs** — vendor proposals are often image-based. Use PyMuPDF to render pages, then tesseract OCR. Verify output quality.
- **Overlapping PDF extraction** — when extracting multiple PDFs to the same temp path, subsequent runs overwrite previous pages. Use unique prefixes (`/tmp/blu_p{i}.jpg`, `/tmp/ad_p{i}.jpg`).
- **Excel column widths** — supplier names can be long (multiple brands per row). Set widths generous (40-55 chars) and use `wrap_text=True`.
- **Schedule vs design spec name mismatch** — the schedule activity name may not match the design spec code. Map by color/material description, not by name.
- **AV hardware mapping** — 13" interactive screens are often **Beetronics** (not Q-Sys control panels). 16" pen displays are **Wacom Cintiq** (not Q-Sys). Control touch screens (5"-7") are **Q-Sys TSC-50/70**. Verify each against the AV BOQ.
- **Lighting brands** — a single "Lighting" schedule activity (PR3800) may cover 7+ sub-categories (EL-MAT-01 to EL-MAT-07), each from a different manufacturer. Compile all brands from the Luminaire Specification into one row.
- **Design source is authoritative** — the Finishes Schedule (from the exhibition designer) is the single source of truth for finish material suppliers. The schedule's Primavera export only shows generic material categories.
- **Offer comparison** — when comparing subcontractor offers, note whether the scope is "design review" vs "design production" — they are fundamentally different services with different fee structures.

## Reference Files

- `references/aseer-design-document-inventory.md` — Complete directory map of Aseer Museum design documents with confirmed brand mappings for finishes, lighting, AV, and MEP offers. Use this as a lookup table when auditing the Aseer Museum schedule; update it as new brands are confirmed from additional design packages.

## Verification Checklist

- [ ] All materials in Stage 3 schedule have been checked against design documents
- [ ] Source document + row reference noted for each brand entry
- [ ] Critical-path items flagged (red rows) with 0 float
- [ ] Excel has freeze panes, auto-filter, column widths set
- [ ] Green highlight on cells with confirmed supplier names
- [ ] Items with no design-time supplier marked as "TBC" (not blank)
