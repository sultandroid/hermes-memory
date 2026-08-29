# CRS Template Structure & Programmatic Fill (openpyxl)

Reverse-engineered from `Technical_Office/Compliance_System/templates/CRS_TEMPLATE_BLANK.xlsx` (sheet `CRS`). Use this to build a Comment Resolution Sheet for any Code C submittal without hand-typing rows.

## Template layout (verified 2026-08-29)

Header cells (fill these):
| Cell | Field | Example |
|---|---|---|
| D4 | PROJECT NAME | `Project to rehabilitate and equip museum displays for the third regional museum (Aseer)` |
| A5 | CRS NUMBER | `CRS-1A0-1G-0012-01` |
| G5 | Rev. | `01` |
| I5 | DATE | `29-Aug-2026` |
| A6 | DOCUMENT No. | `MOC-MUS-ASE-1A0-1G-0012` |
| G6 | Rev. | `00` |
| I6 | DISCIPLINE | `Architectural` |
| A7 | DOCUMENT TITLE | full title |
| I7 | DOCUMENT TYPE | `Specifications (Master Format)` |

Data rows start at **row 11**. Column map:
- A = No. (e.g. `G1`, `S1`)
- B = Initial (e.g. `CG`)
- C = Sheet (e.g. `1`, `2`)
- E = Reviewer Comment (verbatim CG text) — merged E:I
- J = Originator Reply (our response) — merged J:O
- P = Reply By (owner) — merged P:Q? (verify; P is `Reply By`)
- Q = Reply Status by Reviewer (`Closed` / `Open`) — merged Q:R

Merged ranges per data row: `E:I`, `J:O`, `Q:R`. Set `wrap_text` + `vertical=top` on comment/reply cells, `center` on No/Initial/Sheet/Status.

## Fill pattern (openpyxl)

```python
import openpyxl
from openpyxl.styles import Alignment, Border, Side

wb = openpyxl.load_workbook('Technical_Office/Compliance_System/templates/CRS_TEMPLATE_BLANK.xlsx')
ws = wb['CRS']

# header fills (see table above)
ws['D4'] = '...'; ws['A5'] = '...'; ws['G5'] = '01'; ws['I5'] = '...'
ws['A6'] = '...'; ws['G6'] = '00'; ws['I6'] = '...'
ws['A7'] = '...'; ws['I7'] = '...'

thin = Side(style='thin', color='000000')
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical='top', horizontal='left')
center = Alignment(wrap_text=True, vertical='center', horizontal='center')

start_row = 11
for i, (no, initial, sheet, comment, reply, reply_by, status) in enumerate(comments):
    r = start_row + i
    ws.cell(r, 1, no).alignment = center
    ws.cell(r, 2, initial).alignment = center
    ws.cell(r, 3, sheet).alignment = center
    ws.cell(r, 5, comment).alignment = wrap
    ws.cell(r, 10, reply).alignment = wrap
    ws.cell(r, 16, reply_by).alignment = wrap
    ws.cell(r, 17, status).alignment = center
    for c in (1, 2, 3, 5, 10, 16, 17):
        ws.cell(r, c).border = border
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=9)
    ws.merge_cells(start_row=r, start_column=10, end_row=r, end_column=15)
    ws.merge_cells(start_row=r, start_column=17, end_row=r, end_column=18)
    # DO NOT hardcode height=60 — see "Formatting" below; auto-calc instead.

wb.save('02_CG_Responses/CRS_<DOC>_Rev01.xlsx')
```

## Formatting (MANDATORY — the user rejects the default fill as "format not good")

The template's default column widths are too narrow for real reply text, and a fixed row height truncates long replies. The user will bounce the file back with "format not good" if you skip this. Apply ALL of these before saving:

1. **Widen the text columns.** Comment spans E:I, reply spans J:O. Set each of E,F,G,H,I,J,K,L,M,N,O to width 18 (≈90 chars comment, ≈108 chars reply). Set P (Reply By) to 22, Q and R (Status) to 12.
2. **Auto-calculate row height** from wrapped line count — never a fixed 60px. Estimate lines by word-wrapping against the column char width, then `height = max(20, lines * 14 + 6)`:
   ```python
   def est_lines(text, width_chars):
       if not text: return 1
       lines, cur = 1, 0
       for w in text.split():
           if cur + len(w) + 1 > width_chars:
               lines += 1; cur = len(w)
           else:
               cur += len(w) + 1
       return lines
   # per row: max(est_lines(comment, 90), est_lines(reply, 108))
   ```
3. **Font size 11** (Calibri). The default renders ~8pt and is unreadable.
4. **Color-code the status cell** (Q): green fill `C6EFCE` + dark-green bold font `006100` for `Closed`; red fill `FFC7CE` + dark-red bold font `9C0006` for `Open`. Plain text, no emoji.

## Render-verify before delivering (soffice → pdftoppm → vision)

The user opens the file in Excel and judges it visually. Verify the layout yourself first:

```bash
soffice --headless --convert-to pdf --outdir /tmp <file>.xlsx
pdftoppm -png -r 100 -f 1 -l 2 /tmp/<file>.pdf /tmp/crs_page
# then vision_analyze /tmp/crs_page-1.png asking: text cut off? columns wide enough? rows tall enough?
```

Note: the vision model's OCR will misread header values (dates, project names) at low render resolution — trust the openpyxl cell values (`ws['D4'].value` etc.), not the OCR text, for content correctness. Use vision only for *layout* (truncation, column width, row height, color), not for content accuracy.

## Staged-evidence argument (key for spec-stage Code C)

When CG returns a **specifications** submittal Code C demanding test reports / certificates / warranties / mock-ups, the correct technical reply is that these are **Material Approval (MAR) / pre-installation stage deliverables**, not spec-stage deliverables. The specification's job is to *state the required criteria* (NRC, DCOF, fire class, compressive strength, VOC limits); the evidence is submitted later by approved suppliers.

Reply pattern:
1. **Embed the criteria** into each spec section (so they become contractually binding).
2. **Commit to the evidence** at the correct later stage per the Submission Plan / ITP.
3. Request CG agreement to this staged delivery (avoids front-loading MAR work into DD).

This is the same argument used in the Showcases CRS (`1G-0009_Showcases_CRS_Rev01.md`) — "COMPLIED AT 50% DD LEVEL … full detail to follow in shop drawings / IFC package."

## Status convention

- `Closed` = responded, no further action.
- `Open` = deliberately left open because we are asking CG for clarification (e.g. "confirm the specific design requirements the display case specs must satisfy"). Do NOT mark a vague CG comment "Closed" — flag it Open and ask CG to specify.
