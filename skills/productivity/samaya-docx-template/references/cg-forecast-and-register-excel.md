# CG Response Forecasting & Risk Register Excel Generation

## CG Response Forecast Framework

| Factor | Code A (Approve) | Code B (Minor) | Code C (Revise) |
|--------|-----------------|----------------|-----------------|
| Methodology vs data | Pure methodology doc | Some TBCs/placeholders | Unfilled EMV, "in progress" registers |
| Internal references | None | Minor (file paths, .md) | Repo paths, internal tracking |
| Contradictions | None | Minor inconsistencies | Plan claims completeness but register is "in progress" |
| DC block | Actual names | Role titles only | Missing |
| Severity scales | Proportional to project | Generic/standard | Not aligned to project duration |
| Live register notes | Present on all data tables | Missing on some | None |

**Key principle:** If the plan describes *how* risks are managed (methodology) and the actual risk data lives in a live register, CG will approve on first review. If the plan contains unfilled data (TBCs, "in progress" registers, missing EMV values), expect Code C.

## Risk Register Excel — Sheet Structure (per RMP §9.1)

| Sheet | Code | Content |
|-------|------|---------|
| Dashboard | — | Metric boxes, distribution chart, top 5 critical, register status, review cadence |
| Master Risk Register | PRR | 20 cols: ID, Category, RBS Code, Event, Impact, P/S/Score, Rating, Response Strategy, Mitigation, Residual scores, Owner, Target Close, Status, Review Date |
| Design Risk Register | DDR | 14 cols: #, Risk ID, RBS Category, Event, Cause, Impact, P/I/PxI, Severity, Response Strategy, Action, Owner, Status |
| HSE Risk Register | HSE | 12 cols: Ref, Activity, Hazards, Controls, Initial C/L/Score, Residual C/L/Score, Responsibility, Status |
| AV Risk Register | AV | 10 cols: Ref, Risk Event, Hazard, Controls, P/S/Score, Rating, Responsibility, Status |
| Reference | — | Scoring scales, response strategies, status definitions |

## Implementation Rules

- **Unmerge cells before clearing** — `MergedCell` objects raise `AttributeError` on `.value = None`
- **Auto-filter + freeze panes** on every data sheet
- **Color-code severity**: Critical = red fill, High = amber fill
- **Dashboard chart**: remove old chart and recreate when data changes (chart.data reassignment doesn't work reliably)

## Client-Facing Content Filter

Before finalizing for CG/client submission:

| Don't include | Replace with |
|---------------|-------------|
| Internal formatting details | "REV00 - First issue for CG review" |
| File paths, repo references | Generic description |
| "To be recalculated" placeholders | Reference the live register |
| Role titles in DC block | Actual names (Eng. prefix) |
| Doc ref + revision in page header | Project name only |
| Section 13 referencing non-existent plans | Remove the section entirely |
| § symbol | "Sec." or "Section" |

## Table Structure Repair

When a DOCX table has mismatched column counts between rows:

1. **Diagnose**: `len(list(row._tr.findall(qn('w:tc'))))` per row
2. **Check gridSpan/vMerge**: merged cells cause python-docx to report fewer cells than grid columns
3. **Fix**: extract data from all rows, rebuild table from scratch with consistent column count
4. **Rebuild**: clear rows + gridCols, create new gridCols matching target count, rebuild each row
5. **Verify**: re-check all rows have matching tc counts

Common tables needing this: PxS matrices (6→5 cols), register summaries (12→4 cols), snapshot tables (9→5 cols), distribution tables (merged cells).

## First Page Layout for CG Submittals

1. Cover metadata table
2. DC block (QC — Prepared by / Reviewed by / Approved by with actual names)
3. Revision history
4. Document body

**Header**: Samaya logo (left) + project name only — no doc ref, no revision.
**Footer**: "Page X of Y" (Word fields) + company name.
