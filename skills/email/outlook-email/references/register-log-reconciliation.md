# Register Log Reconciliation — Cross-Reference Against Submission Plans

Cross-reference a Register Log Excel (exported from Aconex, or project register) against the submission plan to update actual submittal statuses with CG response codes.

## Trigger

User provides a Register Log Excel with columns: Document Number, Discipline, Description, Date Received, Date Reply, Status Code (A/B/C/D) — and wants the submission plan updated to match.

## Workflow

### Phase 1: Read Register Log

1. Open the Excel with `openpyxl` (use `read_file` for auto-extraction, then `openpyxl.load_workbook` for structured access)
2. Identify the sheet with material submittal / document data
3. Extract key columns: Document Number (MOC code), Discipline, Description, Date Received (R0), Date Reply (P0), Status Code (S0), Current Status
4. Convert Excel serial dates to readable: `base = datetime(1899, 12, 30); base + timedelta(days=serial)`

### Phase 2: Map Documents to Submission Plan

Match each log entry to a submission plan row using discipline + description keywords:

| Log Document Code | Discipline | Maps to Submission Plan |
|-------------------|------------|------------------------|
| `MOC-MUS-ASE-1A0-MA-0006` | AR (Arch) | MS-04 Showcase Materials |
| `MOC-MUS-ASE-1E0-MA-0001` | EL (Electrical) | MEP Electrical Equipment |
| `MOC-Asser-SIC-1A0-MA-0001` | AR (Arch) | Architectural Flooring Materials |

### Phase 3: Status Code Translation

| CG Code | Meaning | Submission Plan Status |
|---------|---------|----------------------|
| A | Approved | COMPLETED / APPROVED |
| B | Approved with Comments | CG RESPONSE: Code B |
| C | Revise and Resubmit | CG RESPONSE: Code C — flag as overdue |
| D | Rejected | CG RESPONSE: Code D — needs resubmission |
| E | Not Required | CLOSED |
| F | For Information | RECEIVED (information) |
| U | Under Review | IN PROGRESS |

### Phase 4: Update Submission Plan

For each matched row in the submission plan:

1. **Status** (col 13): Update from "Planned" / "RECEIVED" to actual CG code status
2. **Actual Date** (col 9): Set to CG reply date
3. **Remarks** (col 14): Add document number, submission date, CG reply date, and action required
4. **Last Updated** (col 15): Set to today
5. Color-code: Green for Code A/B, Red for Code C/D, Amber for IN PROGRESS

### Pitfalls

- **Sheet names may have trailing spaces** — use exact names from `wb.sheetnames` (e.g., `' Material Submittal '` not `'Material Submittal'`)
- **Document number variations** — log may use `MOC-Asser-SIC-` (old format) and `MOC-MUS-ASE-` (current format). Treat equivalently.
- **Multiple revisions** — log has R0, R1, R2 columns. Use the LATEST revision's status (column 30 = Current Status) not the R0 status.
- **Row numbers shift** — complex register files have merged cells and header rows. Use document number matching, not fixed row positions.
- **Already-updated rows** — check if Remarks already contains the document number before re-appending.
- **Serial dates still in cells** — after column inserts, old serial date values (e.g., `3`, `46062`) may leak into the Actual Date column. Scan and clean them.
