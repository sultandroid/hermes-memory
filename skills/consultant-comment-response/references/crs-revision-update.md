# CRS Revision Update — Existing CRS to Rev 01+

## When to Use

CG has returned a CRS (Consultant Review Sheet) on a submitted document. The reviewer comments have been addressed in a document revision. You need to:
- Update the CRS to Rev 01 to reflect the resubmission
- Add originator replies to each comment
- Save the updated CRS alongside the source document

This is different from creating a CR Sheet from scratch (see `cr-sheet-workflow.md`). Here you are updating an existing CRS Excel workbook that already has CG comments, status codes, and partially filled response cells.

## Workflow

### 1. Read the existing CRS structure

Open with `openpyxl` and inspect merged cells first — CRS files are heavily merged:

```python
import openpyxl
wb = openpyxl.load_workbook("CRS.xlsx")
ws = wb.active

# Print merged cell ranges
for mr in ws.merged_cells.ranges:
    print(mr)
```

Key structural notes:
- Column A = comment number (usually a **string**, e.g. `'17'`, not integer `17`)
- Column B = reviewer initials
- Column C-D = section reference (merged)
- Columns E-I/J = reviewer comment (merged — check exact range)
- Column J-O = originator reply (merged `J{row}:O{row}`)
- Columns H5-H6 = revision field
- Column K5 = date field

### 2. Update revision and date

```python
# Update revision from 00 to 01
for row in ws.iter_rows(min_row=4, max_row=7):
    for cell in row:
        if cell.value == "00":
            cell.value = "01"

# Update date to today
from datetime import datetime
for row in ws.iter_rows(min_row=4, max_row=6):
    for cell in row:
        if isinstance(cell.value, datetime):
            cell.value = datetime.now()
```

### 3. Add originator replies to design-related comments

Find the comment row by scanning column A (string comparison):

```python
replies = {
    "19": "Noted. [Specific explanation of what was done in Rev 01].",
    "20": "Noted. [Contractual reference added/changed].",
}

for comment_no, reply_text in replies.items():
    for row in ws.iter_rows(min_row=11, max_row=55, min_col=1, max_col=1):
        if str(row[0].value) == comment_no:
            row_num = row[0].row
            # Find the J merge range for this row
            for mr in ws.merged_cells.ranges:
                if mr.min_col == 10 and mr.min_row == row_num:
                    tl_cell = ws.cell(row=mr.min_row, column=mr.min_col)
                    tl_cell.value = reply_text
                    tl_cell.font = Font(name='Calibri', size=10)
                    tl_cell.alignment = Alignment(wrap_text=True, vertical='top')
                    break
            break
```

### 4. Save and file alongside the source document

```python
import os
source_doc_folder = ".../02.3_PEP/01_Source_Files/03_Word/"
dst = os.path.join(source_doc_folder, "MOC-MUS-ASE-1K0-ZD-0086 CRS Rev 01.xlsx")
wb.save(dst)
```

Name the Rev 01 file with the same base name plus "Rev 01" suffix so the original is preserved.

## Originator Reply Patterns by Comment Type

### Schedule/Timeline Comments (e.g., "gates extend beyond contract duration")

Reply structure:
1. Acknowledge — "Noted."
2. Explain the mapping — what the reported numbers actually cover (e.g., G7-G8 are DLP/handover beyond the 10-month contract period)
3. State the update — "Section revised to clarify mapping in Rev 01."

### Contractual Reference Comments (e.g., "clarify contractual reference")

Reply structure:
1. Acknowledge — "Noted."
2. List the specific references added — "turnaround times per PL-0015 Rev 04 sec 19; escalation per PL-0015 Rev 04 sec 19 referencing Contract 0010 Sec 4"
3. State the update — "Updated in Rev 01."

### Data Accuracy Comments (e.g., "refer to actual Approvals Log")

Reply structure:
1. Acknowledge — "Noted."
2. State what was done — "section updated to reference actual Approvals Log with defined cut-off date"
3. Note cross-check performed — "cross-checked against latest Aconex Master Log count"

### Scope/Alignment Comments (e.g., "packages don't cover full scope")

Reply structure:
1. Acknowledge — "Noted."
2. Explain the current basis — "cadence aligned with Programme Baseline (W0-W64); listed packages cover critical-path work packages"
3. State what will follow — "Additional packages will be added as the submittal register develops."
4. State the update — "Clarified in Rev 01."

## Formal Code Mapping

When the CRS references the same documents the halftone annotations reference, use formal codes:

| Abbreviation | Formal Code |
|---|---|
| PEP Rev 04 | PL-0015 Rev 04 |
| DMP Rev C03 | PL-0013 Rev C03 |
| BEP Rev 01 | PL-0021 Rev 01 |
| SoW | Contract 0010 (SoW) |
| Contract Section 4 | Contract 0010 Sec 4 |
| EIR | Contract 0010 (EIR) |
| ER | Contract 0010 (Employer's Requirements) |

## Integration with Document Revision

When reviewing CRS comments against a document:
1. Read the document to understand which section each comment targets
2. Update the document's relevant sections (revision, content fixes, added references)
3. Update the CRS with originator replies that reference the document revision (Rev 01)
4. Save both files in the same folder

## Pitfalls

- **Column A values are strings**, not integers. Compare with `str(cell.value) == "19"`, not `cell.value == 19`.
- **J column is merged** (typically `J{row}:O{row}`). Write to the top-left cell of the merge range only. Do not write to other cells in the merge.
- **Preserve original formatting.** Do not unmerge cells or rebuild the workbook. Only change the specific cells needed (revision, date, originator replies).
- **Date cells may be `datetime` objects** or serial numbers. Check the type before assigning.
- **Multiple Rev fields exist** — there are separate `Rev.` fields for CRS Number (row 5) and Document No. (row 6). Both need updating.
- **The original CRS stays in Downloads** — copy it to the target folder via the save path, not by moving/deleting the original.
