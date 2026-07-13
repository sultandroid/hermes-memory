# RMP + DRR Reconciliation Workflow

## What

Cross-reference three documents to eliminate conflicts:
- **RMP DOCX** (formal CG submittal, Word)
- **RMP Repo** (internal source of truth, Markdown in repo)
- **DRR Excel** (Design Risk Register, Excel)

## When

- User attaches or references a RMP DOCX, DRR Excel, or both and asks "check this"
- User reports discrepancies between the formal document and what the team uses internally
- Before submitting any revision of the RMP to CG

## Reconciliation Checklist

### 1. Compare RMP DOCX vs Repo RMP

| Check | What to look for |
|-------|-----------------|
| Scoring scale | DOCX and repo must agree. If repo says 1-4 PxS, the DOCX must too |
| RBS categories | The DOCX RBS table must match the repo's full category list |
| Risk count | Master risk count (33), DRR count (76), HSE (41), AV (~30) |
| EMV values | Total, critical, high, medium must match repo (SAR 7.5M total) |
| Risk factors | Section 2 profile must reflect current project conditions |
| Principles | SOW-Protect must be present; old principles removed |
| Response strategies | SOW-Protect included; opportunity strategies (Exploit/Enhance/Share) removed for construction-phase projects |
| Register architecture | Must describe 4 registers (PRR, DRR, HSE, AV), not a single sample register |

### 2. Compare DRR Excel vs RMP Standards

| Check | What to look for |
|-------|-----------------|
| Scoring scale documented | P(1-4) x I(1-5), thresholds: Critical >=15, High 10-14, Medium 5-9, Low <=4 |
| Owner code legend | DSN-A = Design-Architecture, CTR PM = Contract-PM, etc. Must be defined |
| Status definitions | Open, Open-Materialising, Watch, Mitigated, Closed |
| Summary formulas | Must use SUMPRODUCT formulas, not hardcoded values |
| Column completeness | Every row needs: Risk ID, Category, Description, P, I, Mitigation, Owner, Status |
| No duplicate IDs | Every Risk ID must be unique (e.g. DB-A-001, CO-X-001) |

### 3. Cross-Register Checks

| Check | What to verify |
|-------|---------------|
| DRR count in RMP | RMP must say DRR has 76 risks (not 37) |
| DRR doc ref | DRR Excel doc number: MOC-ASEER-SIC-1K0-RR-0002 Rev P03 |
| Scoring note vs DRR | RMP says uniform scoring but DRR uses different scale -- acceptable if documented as separate register with its own scale |

## Common DOCX Fixes

- **Heading styles**: Apply Heading 1 (H1) to main sections, Heading 2 (H2) to sub-sections. Without these, the TOC cannot auto-generate.
- **cantSplit on tables**: Every table row needs `<w:cantSplit w:val="true"/>` to prevent rows splitting across pages.
- **rebuild_table() pattern**: When replacing table content in python-docx, use a `rebuild_table()` function that clears header cells, removes all rows after the first, then appends new rows with matching column count. Always verify the table grid (w:tblGrid) column count matches the new row cell count.
- **Paragraph updates**: Use set_run_text() to clear all runs before setting new text, avoiding text concatenation issues.

## Common Excel Fixes

- **Legend placement**: Add scoring thresholds, owner codes, and status definitions on the Cover sheet or above the data header row.
- **Summary formulas**: Replace hardcoded totals with SUMPRODUCT formulas that count by category and PxI threshold:
  ```
  =SUMPRODUCT((B$6:B$82="Category")*(E$6:E$82*F$6:F$82>=15))
  ```
- **Status column**: Add column I for status tracking. Default to "Open".
- **Column widths**: Set explicit widths; wrap header text; format header row.
- **Scoring note**: Add an italic note row above the data header explaining the scale.

## Pitfalls

- **DOCX table column mismatch**: When rebuilding a table, the number of cells in new rows must equal the number of `w:gridCol` elements. If not, Word renders extra blank columns. After rebuild, always check: `len(table.rows[0].cells)` vs `len(grid.findall(qn('w:gridCol')))`.
- **Paragraph indices shift**: Deleting paragraphs shifts indices of all subsequent paragraphs. If you delete paragraphs (e.g. old bullets), re-verify heading indices.
- **Excel summary mismatch**: Hardcoded summary values don't update when risks are added. Always use formulas.
- **Cover contract value**: The cell with the contract number is at Table 0 Row 1 (not Row 3). Verify before editing.
