# Building a Fresh CRS from the Approved MOC Template

When CG returns **Code C** on a submittal and you must produce the Comment Resolution
Sheet (CRS) that accompanies the Rev 01 resubmission, do NOT build a new workbook from
scratch. **Copy the latest approved CRS template** (e.g. `MOC-MUS-ASE-1K0-ZD-0094 CRS.xlsx`)
and refill its header + comment rows. This preserves the exact approved layout, logo,
merges, and the MOC_HQ DESIGN & BUILD masthead.

## Workflow

1. `shutil.copy(template, new_path)` — never `openpyxl`-create a bare workbook.
2. Inspect the merge ranges first:
   ```python
   for mc in ws.merged_cells.ranges: print(mc)
   ```
   Writing to a MergedCell raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`.
   **Always write to the top-left cell of the merge range.**
3. Fill header, then append comment rows at row 11+ (rows below the existing data block).

## Exact Cell Map (verified against ZD-0094 template, 2026-08)

Header (write to top-left of each merged range):
| Field | Cell | Merge | Value |
|-------|------|-------|-------|
| PROJECT NAME | D4 | D4:H4 | project name text |
| CRS NUMBER | D5 | D5:F5 | `MOC-MUS-ASE-1E0-ZD-0102` |
| CRS Rev | H5 | (single) | `01` |
| DATE | K5 | K5:R5 | datetime |
| DOCUMENT No. | D6 | D6:F6 | same as CRS number |
| Doc Rev | H6 | (single) | `00` |
| DISCIPLINE | K6 | K6:R6 | e.g. `Electrical` |
| DOCUMENT TITLE | D7 | D7:H7 | full title |
| DOCUMENT TYPE | K7 | K7:R7 | `Document Submittal` |

Data rows (start at row 11; columns are 1-indexed):
| Column | Field | Merge | Notes |
|--------|-------|-------|-------|
| 1 | No. | | string `'1'` |
| 2 | Initial | | reviewer initials, e.g. `CG` |
| 3 | Sheet | C:D | section reference |
| 5 | Reviewer Comment | E:I | write to col 5 |
| 10 | Originator Reply | J:O | write to col 10 |
| 16 | Reply By | (single) | e.g. `AD Engineering` |
| 17 | Reply Status | Q:R | `Closed` / `Open` |

Rows 11-16 carry the template's own example comments — clear them or overwrite.

## Pitfalls
- **Column 15 (O) is part of the J:O Originator Reply merge — writing there throws MergedCell error.** Reply By lives in column 16 (P), Reply Status in column 17 (Q).
- DATE cell expects a `datetime`, not a string, or it renders oddly.
- Set every reply to `Closed` with an explicit acceptance statement — CG returns Code C on incomplete responses. Use `Accepted. <specific corrective action>` phrasing, and name the responsible party (AD Engineering / Samaya) in Reply By.
- CRS `.xlsx` is a **binary** — the aseer-museum-pm repo git-ignores it. Save to OneDrive project folder (e.g. `03_Design_Files/Electrical/Submission_Plan_CRS/`), not the repo. Only HTML/MD deliverables go in the repo.

## Confidentially-Routed Design Transition
When preparing MEP design scope/RACI docs for a prospective replacement designer (e.g. SG Group meeting) while AD Engineering still holds the contract, the scope doc should name both parties in one column (`AD Engineering (transitioning to SG Group)`) so the prospect sees the full responsibility without negotiating scope down. Keep these internal-coordination items out of CG-facing CRS files. Mark the meeting-prep action items `[CONFIDENTIAL]` in the action register.
