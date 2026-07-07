# Aseer Museum — Approval Authority & Template Decisions

## Default Approval Authority: CG

**ALWAYS set Approval Authority to "CG" for all items in Aseer Museum submission plans**, unless the user explicitly specifies a different authority for a specific item (e.g., Civil Defense for FL-026).

This applies to:
- All gates (Gate 1 Detailed Design, Gate 2 Material Approval, Gate 3 Coordinated IFC)
- All disciplines (AV, FLS, MEP, Structural, Lighting, etc.)
- All item types (reports, drawings, models, material submittals, IFC packages, QA docs, handover docs)

Embed this in the generator script as the default:
```python
approval = 'CG'  # Default for Aseer Museum
```

Override only when the user says otherwise for a specific item.

## AV Template Copy Approach (Preferred for New Disciplines)

When creating a submission plan for a new discipline that should match the AV template format:

1. **Copy the AV xlsx as base** — use `shutil.copy2()` to preserve all formatting (fonts, fills, borders, column widths, merged cells)
2. **Rename the sheet** — change `ws.title` from `'AV Stage 04 Plan'` to `'{DISCIPLINE} Stage 04 Plan'`
3. **Update section headers** — replace AV-specific text with discipline-specific text
4. **Clear old data rows** — set cell values to None for rows 4-45 (keep header row 1 and section header rows)
5. **Fill with discipline items** — write items into the appropriate gate sections
6. **Set Approval Authority to CG** on every row

### Date Priority for Planned Submission Date
- Design items (Gate 1): Use 100% > 90% > 50% priority (final design submission date)
- IFC items (Gate 3): Use IFC/AFC date
- If user wants first submission date instead, flip priority to 50% > 90% > 100%

### Row Capacity Problem
The AV template has fixed row counts per section. If a discipline has more items than available rows, **build from scratch** instead of trying to insert rows into the copied template (insert_rows corrupts merged cells).

### Build-From-Scratch Pattern
When the AV template's fixed row capacity is insufficient:

1. Create a new workbook with `openpyxl.Workbook()`
2. Set column widths from AV template
3. Write header row (row 1) copying style from AV template row 1
4. Write section header rows (merged across all 13 columns) copying style from AV template
5. Write data rows copying style from AV template data rows
6. Each section gets exactly as many rows as needed — no fixed limits

Key: use `copy_style(src_cell, dst_cell)` to transfer font, fill, alignment, border from AV template cells.

## FLS Submission Plan — Section Categorization Pattern

When organizing FLS items into the 13-column gate format:

| Section | Items | Sub-Package |
|---------|-------|-------------|
| FLS Strategy & Design Criteria | FL-001 to FL-006 | FLS Strategy |
| Active & Passive Fire Protection Design | FL-007 to FL-018 | Active FP, Passive FP |
| FLS Coordination with Other Disciplines | FL-019 to FL-024 | Coordination |
| Commissioning & BIM | FL-025, FL-028, FL-036 | Commissioning, BIM |
| Gate 2 — Material Approval | (empty for FLS) | — |
| Gate 3 — IFC Packages | FL-026 to FL-035 | Commissioning, QA/Commissioning, Handover, Training, BIM |

## Register Audit — 10 Disciplines Still Missing

As of 01 Jul 2026, only AV and FLS have submission plans. Empty folders exist for:
FP, ID, IT, LV, MEP, SEC, ST, STR, TEL, WP

To build these, source data is needed (subcontractor scopes, MIDP, consultant deliverables schedules).
