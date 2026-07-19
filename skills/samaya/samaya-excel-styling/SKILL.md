---
name: samaya-excel-styling
description: Apply Samaya brand styling to Excel workbooks using openpyxl — headers, severity fills, heat maps, row striping, auto-fit, freeze panes, and formula-cell handling.
domain: productivity/samaya
triggers:
  - "Apply Samaya branding to an Excel file"
  - "Style/fix/format an Excel workbook or risk register"
  - "Excel formatting with openpyxl"
  - "Brand-colored Excel headers and fills"
---

# Samaya Excel Styling with openpyxl

Apply consistent Samaya-brand formatting to Excel workbooks (.xlsx) using openpyxl. Covers headers, fills, borders, severity coloring, heat maps, auto-fit, freeze panes, and the critical pattern for handling formula cells with no cached values.

## Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#1F3864` | Primary headers, titles, section accents |
| Gold | `#C9A84C` | Secondary headers (Treatment Plan, Cover metrics) |
| Light Grey | `#F2F4F7` | Alternating row stripes |
| Border Grey | `#D0D0D0` | Thin cell borders |
| Critical Red | `#FF4444` | Critical severity, heat-map top band |
| High Orange | `#FF8C00` | High severity, heat-map middle band |
| Medium Yellow | `#FFD700` | Medium severity, heat-map low band |
| Low Green | `#90EE90` | Low severity |

## Font

- **Default data**: Calibri 9pt
- **Headers**: Calibri 10pt bold, white font on navy/gold fill
- **Titles**: Calibri 14pt bold, navy
- **Severity**: Calibri 9pt bold, white on red/orange, black on yellow/green

## Dropdowns on ALL Controlled Columns — Mandatory

Every column where the user selects from a fixed set of values MUST have a DataValidation dropdown. No free-text entry for controlled fields. This prevents typos and ensures data consistency.

### Columns that need dropdowns

| Register | Column | Values |
|----------|--------|--------|
| PRR (Risk Register) | Category (C) | APP,AV,CNS,COM,CON,DES,FLS,HSE,LOG,MEP,OPS,PRC,QLT,SCH,SEC,SIT,STK,TCH |
| PRR | Probability P (G) | 1,2,3,4 |
| PRR | Severity S (H) | 1,2,3,4 |
| PRR | Response Strategy (K) | Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect |
| PRR | Status (M) | Open,Watch,Mitigated,Closed,Superseded |
| DRR | RBS Category (C) | SCH,TEC,PRO,EXT,QA,COM |
| DRR | Prob (G) | 1,2,3,4,5 |
| DRR | Impact (H) | 1,2,3,4,5 |
| DRR | Response Strategy (K) | same 6 options |
| DRR | Status (N) | Open,Watch,Mitigated,Closed,Superseded |
| HSE | Consequence C (E) | 1,2,3,4,5 |
| HSE | Likelihood L (F) | 1,2,3,4,5 |
| HSE | Residual C (H) | 1,2,3,4,5 |
| HSE | Residual L (I) | 1,2,3,4,5 |
| HSE | Status (M) | Ongoing,Completed,Pending,Not Required |

### Clear old validations before adding new ones

```python
ws.data_validations.dataValidation = []  # Clear all existing
```

### Add dropdown pattern

```python
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(type='list', formula1='"val1,val2,val3"', allow_blank=True, showDropDown=False)
dv.error = 'Select a valid option'; dv.errorTitle = 'Invalid'
ws.add_data_validation(dv)
dv.add(f'C{data_start}:C{data_end}')
```

## Dynamic Formulas — Never Hardcode Counts

RBS category counts and Dashboard severity/category counts MUST use COUNTIF formulas referencing the Risk Register sheet. Hardcoded numbers will be wrong after the first edit.

### RBS COUNTIF pattern

```python
PRR_SHEET = "'Risk Register'"
ws.cell(row=r, column=3).value = f'=COUNTIF({PRR_SHEET}!C{DS}:C{DE},"{code}")'
```

### Dashboard COUNTIF pattern

```python
ws.cell(row=row, column=2).value = f'=COUNTIF({PRR_SHEET}!J{DS}:J{DE},"{sev}")'
```

### Scoring Matrix formula pattern

Use hidden reference cells for P and S values, then `=F{r}*B$4` formulas in each cell:

```python
# Row 4: hidden S values (1,2,3,4 in B4:E4)
ws.cell(row=4, column=2, value=1).font = Font(size=1, color=WHITE)
# Column F: hidden P values (4,3,2,1 in F6:F9)
ws.cell(row=r, column=6, value=p_val).font = Font(size=1, color=WHITE)
# Formula: =F{r}*{col_letter}$4
cell.value = f'=F{r}*{col_letter}$4'
```

## Separate Sheets Per Register — Own Scoring Scale

Each register type gets its own sheet with its own severity scale and color mapping. Never mix scales in one sheet.

| Register | Scale | Severity Bands | Color |
|----------|-------|----------------|-------|
| PRR (Master) | P×S 1-4 | Critical≥12, High≥8, Medium≥4, Low<4 | Red/Orange/Yellow/Green |
| DRR (Design) | P×I 1-5 | Critical≥16, High≥10, Medium≥5, Low<5 | Same color scheme |
| HSE | C×L 1-5 | Critical≥16, High≥10, Medium≥5, Low<5 | Same color scheme |

### HSE severity coloring (both Init Score and Res Score)

```python
def hse_severity(score):
    if score is None: return None
    try: s = int(score)
    except: return None
    if s >= 16: return 'critical'
    if s >= 10: return 'high'
    if s >= 5: return 'medium'
    return 'low'
```

## Sheet Ordering

Always order sheets logically: Cover → Dashboard → Scoring Matrix → RBS → Risk Register → DRR → HSE

```python
desired = ['Cover', 'Dashboard', 'Scoring Matrix', 'RBS', 'Risk Register', 'Designer Risk Register (DRR)', 'HSE Risk Register (Fit-Out)']
for i, name in enumerate(desired):
    if name in wb.sheetnames:
        idx = wb.sheetnames.index(name)
        if idx != i:
            wb.move_sheet(name, offset=i - idx)
```

## Remove Register Control Sheet

The user does not want a revision history sheet. The Cover already has doc ref, revision, and date. Delete Register Control from the final file.

```python
if 'Register Control' in wb.sheetnames:
    del wb['Register Control']
```

## No AI Fingerprints — Mandatory

This user rejects any trace of AI generation in deliverables. Before saving any Excel file:

1. **Author column** — use real team role titles only (Technical Office, Project Manager, Risk Manager). Never use AI model names (Hermes, Claude, Grok, Kimi, OpenCode) or tool names (risk_sync.py).
2. **Notes and metadata** — remove all references to automation, repos, JSON sources, sync scripts, or AI tools. Write as if a human engineer prepared the file.
3. **Source references** — cite actual project documents (RMP, MoM, CG correspondence, NCR register, DRR). Never cite GitHub repos, JSON files, or auto-generation pipelines.
4. **Language** — plain English, active voice, British spelling. No "seamlessly", "robust", "cutting-edge", arrows, emoji, or AI cliches.
5. **Revision history** — describe what changed, not who or what tool made the change. "Added PRR-DES-07" not "Kimi added PRR-DES-07".
6. **Register Control sheet** — this user does not want a revision history sheet in the deliverable. The Cover already has doc ref, revision, and date. Remove Register Control from the final file.
7. **Cover notes** — no "Source of truth: 06_Risk_System/risks.json", no "Auto-synced by risk_sync.py", no "01_Registers/risk_register.md". Just clean notes: RMP submitted, handover date, append-only rule.
8. **Dashboard** — no duplicate headers, no orphaned data rows, no leftover old-format columns. Rebuild clean if the sheet has accumulated debris from multiple edit passes.
9. **Risk IDs are immutable** — never change a risk ID or risk number. The user references these IDs in other documents (submittals, RFIs, emails, CG correspondence). Changing a risk ID breaks cross-references across the project. Append new risks at the end with new sequential numbers; never renumber existing ones.
10. **Severity must be formula-based** — never hardcode severity text. Use `=IF(I>=16,"Critical",IF(I>=10,"High",IF(I>=5,"Medium","Low")))` for DRR (1-5 scale) or `=IF(I>=12,"Critical",IF(I>=8,"High",IF(I>=4,"Medium","Low")))` for PRR (1-4 scale). The user will catch hardcoded severity and ask for formulas.
11. **PxI must be formula-based** — never hardcode PxI scores. Use `=G*H` for initial and `=R*S` for residual. The user will catch hardcoded scores.
12. **Status color coding** — Status column must be color-coded: Open=Red, Watch=Orange, Mitigated=Yellow, Closed=Green, Superseded=Grey. Apply after every status update.
13. **DRR residual columns** — when populating Resid. Prob, Resid. Impact, Contingency Plan, Trigger, Linked Risks, and Evidence Source, assess each risk against current project status. Closed risks get 1×1=1. Mitigated risks get residual based on remaining exposure. Watch risks get 2×2 or 2×3. Open risks get honest current assessment. Every open risk needs a specific contingency plan and trigger/early warning signal.
14. **SI register** — when reading CG Site Instructions from OneDrive, create a markdown register at `01_Registers/si_register.md` with columns: SI#, Date, Subject, Key Instruction, Status, Related Docs, Linked Risks. Cross-reference each SI to its related PRR/DRR risks. Note missing or misfiled documents. The register is append-only.
15. **OneDrive read pattern** — when reading files from OneDrive, read one file at a time. Do NOT batch-read or use wildcard loops that trigger OneDrive sync contention. OneDrive hangs when multiple files are accessed simultaneously. Read each PDF with `pdftotext` individually, extract what you need, then move to the next. If the user says "one by one", respect that literally — no parallel reads, no background subagents for OneDrive paths.
16. **Repo frontmatter** — every register file in the repo must have YAML frontmatter with `last_updated`, `owner_agent` (set to "Technical Office", never "Hermes" or other AI names), `status`, and `source` (OneDrive path or document reference).
17. **Date Identified and Last Review columns** — the Risk Register must include Date Identified (col C) and Last Review (col O) columns. Date Identified should reflect when the risk first became apparent, not when it was formally added to the register. For a project at day 189, risks should date back to Feb-Mar 2026, not just the current revision date. Last Review should be updated to the current date on every review cycle.
18. **Construction Stage register** — when the old consolidated register has a Construction Stage sheet with site-level operational risks (C-001 to C-040), add it as a separate sheet in the C11. Do NOT merge into the master register. Construction risks are site-level operational items (labor, equipment, weather, theft, scaffolding) — different audience and review frequency from the strategic master risks. Style it with the same navy headers, severity colors, and freeze panes as the other sheets. Place it between DRR and HSE in the sheet order.
19. **Never skip a folder without reading a document** — folder names are misleading. 16- Safety Notices sounds low-value but may contain formal stop-work notices linked to SIs and NCRs. Always read at least one sample PDF from each folder before deciding to skip it. Document what you found even if you skip it — the user needs to know you checked.

## Risk Review Workflow — Present One by One, Grouped by Phase

When the user asks to review risks, do NOT dump them all at once. Present them one by one grouped by phase, and let the user discuss each risk before moving to the next.

### Phases (for DRR / design risks)

1. **Mobilisation & Contract Basis** — risks 1-9 (kick-off, liability, personnel, PTW)
2. **Existing Records & Surveys** — risks 10-18 (as-built, heritage, structural, MEP, electrical, FLS, IT, NRS stamping)
3. **DD Technical Design & Coordination** — risks 19-42 (Stramp, AV mounting, phase balance, smoke control, cooling, ceiling coordination, humidity, drainage, power, security, harmonics, graphics, lighting, WiFi, BIM, projection, light box)
4. **Critical Design Items** — risks 43-46 (MoC object list, conservation lighting, stamp compliance, NRS comments)
5. **Authority Approvals** — risks 47-53 (statutory review, Stramp rejection, stairs, SEC transformer, MOI security, FLS, CITC)
6. **Design Gates** — risks 54-59 (50% gate, 90% gate, PMC review, statutory float, BIM readiness, revision rounds)
7. **Procurement, Specialist & Mock-ups** — risks 60-71 (MoC vision alignment, interactive safety, showcase capability, model rejection, lighting fixture, AV lead time, Arabic text, patinated brass Oddy, finish matching, material Oddy, mock-up rejection, product compliance)
8. **Construction, Handover & Commercial** — risks 72-79 (catwalk coordination, dust/noise, as-built capture, ITCP failure, scope vs tender, variation dispute, statutory fees, design budget)

### Display format per risk

```
**N. RISK-ID** — Risk event summary
Score: P×I = Score (Severity)
Status: [Open/Watch/Mitigated/Closed]
What it means: [1-2 sentence plain-English explanation]
Linked to: [PRR references]
```

After each risk, wait for the user to respond before showing the next one. Do not auto-advance.

## Core Reusable Patterns

### Severity Fill Map
```python
SEVERITY_MAP = {
    "critical": (PatternFill(start_color="FF4444", end_color="FF4444", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="FFFFFF")),
    "high":     (PatternFill(start_color="FF8C00", end_color="FF8C00", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="FFFFFF")),
    "medium":   (PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="000000")),
    "low":      (PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid"),
                 Font(name="Calibri", size=9, bold=True, color="000000")),
}
```

### Auto-Fit Columns (CJK-aware)
```python
def auto_fit_columns(ws):
    for col_cells in ws.columns:
        max_len = 0; col_letter = None
        for cell in col_cells:
            if col_letter is None:
                col_letter = get_column_letter(cell.column)
            val = str(cell.value) if cell.value is not None else ""
            for line in val.split("\n"):
                length = sum(2 if ord(c) > 127 else 1 for c in line)
                if length > max_len: max_len = length
        if col_letter and max_len > 0:
            adjusted = min(max_len + 3, 55)
            ws.column_dimensions[col_letter].width = max(adjusted, 5)
```

### Navy Header Row
```python
def apply_navy_headers(ws, row, min_col, max_col):
    for col_idx in range(min_col, max_col + 1):
        cell = ws.cell(row=row, column=col_idx)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
```

### Alternating Row Stripes
```python
def apply_striping(ws, min_row, max_row, min_col, max_col):
    for row_idx in range(min_row, max_row + 1):
        fill = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid") \
               if (row_idx % 2 == 0) else PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        for col_idx in range(min_col, max_col + 1):
            ws.cell(row=row_idx, column=col_idx).fill = fill
```

### Thin Borders
```python
THIN_BORDER = Border(
    left=Side(style="thin", color="D0D0D0"),
    right=Side(style="thin", color="D0D0D0"),
    top=Side(style="thin", color="D0D0D0"),
    bottom=Side(style="thin", color="D0D0D0"),
)
```

## Unified Register Template (14-Column Standard)

All risk registers (PRR, DDR, HSE, AV) must use the **identical 14-column template** with same headers, widths, and column types:

| # | Column | Type | Notes |
|---|--------|------|-------|
| 1 | ID | Text | Risk identifier |
| 2 | Category / Discipline | Text | RBS category or discipline name |
| 3 | Risk Event | Text | What could happen |
| 4 | Cause / Hazard | Text | Root cause or hazard |
| 5 | Impact / Consequence | Text | Effect if risk materialises |
| 6 | Probability | Number | P score (1-4 or 1-5 per scale) |
| 7 | Severity | Number | S/I/C score (1-4 or 1-5 per scale) |
| 8 | Score | **Formula** | `=F{row}*G{row}` — P × S |
| 9 | Rating | **Formula** | `=IF(H{row}>=12,"Critical",IF(H{row}>=8,"High",...))` |
| 10 | Response Strategy | **Dropdown** | Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect |
| 11 | Mitigation / Controls | Text | Response actions or control measures |
| 12 | Risk Owner | Text | Named person |
| 13 | Target Close | Text | Target date |
| 14 | Status | Text | Open / LIVE / Mitigated / Closed |

```python
UNIFIED_HEADERS = [
    "ID", "Category / Discipline", "Risk Event", "Cause / Hazard",
    "Impact / Consequence", "Probability", "Severity", "Score",
    "Rating", "Response Strategy", "Mitigation / Controls",
    "Risk Owner", "Target Close", "Status"
]
UNIFIED_WIDTHS = [14, 22, 35, 30, 30, 10, 10, 10, 10, 18, 40, 20, 14, 14]
```

### Building a Unified Register Sheet

```python
def build_unified_sheet(ws, data_rows, score_formula, rating_formula):
    clear_sheet(ws)
    for ci, (h, w) in enumerate(zip(UNIFIED_HEADERS, UNIFIED_WIDTHS), 1):
        ws.cell(row=1, column=ci, value=h)
        ws.column_dimensions[get_column_letter(ci)].width = w
    style_header(ws, 1, len(UNIFIED_HEADERS))
    
    for ri, row_data in enumerate(data_rows, 2):
        alt = (ri - 2) % 2 == 1
        for ci, val in enumerate(row_data, 1):
            style_cell(ws, ri, ci, alt).value = val
        ws.cell(row=ri, column=8).value = score_formula(ri)
        ws.cell(row=ri, column=9).value = rating_formula(ri)
    
    # Dropdown for Response Strategy (col 10)
    dv = DataValidation(type="list",
        formula1='"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"',
        allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)
    dv.add(f'J2:J{len(data_rows)+1}')
    
    ws.auto_filter.ref = f"A1:N{len(data_rows)+1}"
    ws.freeze_panes = "A2"
```

### Dashboard Cross-Sheet Formulas

Dashboard metrics must use COUNTIF/COUNTIFS referencing the PRR sheet, not hardcoded numbers:

```python
prr_sheet = "'Master Risk Register'"
ws.cell(row=5, column=3).value = f'=COUNTIF({prr_sheet}!I2:I100,"Critical")'
ws.cell(row=5, column=4).value = f'=COUNTIF({prr_sheet}!I2:I100,"High")'
ws.cell(row=5, column=5).value = f'=COUNTIF({prr_sheet}!I2:I100,"Medium")'
ws.cell(row=5, column=6).value = f'=COUNTIF({prr_sheet}!I2:I100,"Low")'
```

Distribution by category uses COUNTIFS:
```python
ws.cell(row=ri, column=4).value = f'=COUNTIF({prr_sheet}!B:B,"*{category}*")'
ws.cell(row=ri, column=5).value = f'=COUNTIFS({prr_sheet}!B:B,"*{category}*",{prr_sheet}!I:I,"Critical")'
```

### Rating Formula by Scoring Scale

| Register | Scale | Score Formula | Rating Formula |
|----------|-------|---------------|----------------|
| PRR (Master) | P×S 1-4 | `=F{r}*G{r}` | `=IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low")))` |
| DDR (Design) | P×I 1-5 | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| HSE | C×L 1-5 | `=F{r}*G{r}` | `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))` |
| AV | P×S 1-4 | `=IF(F{r}="","",F{r}*G{r})` | `=IF(H{r}="","",IF(H{r}>=12,"Critical",...))` |

### Clearing Sheets with Merged Cells

When rebuilding a sheet that may have merged cells, unmerge first:
```python
def clear_sheet(ws):
    for mr in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(mr))
    for ri in range(1, ws.max_row + 1):
        for ci in range(1, ws.max_column + 1):
            ws.cell(row=ri, column=ci).value = None
```

### Dropdown (Data Validation) for Controlled Fields

Response Strategy and similar controlled fields must use dropdown lists, not free-text entry:

```python
from openpyxl.worksheet.datavalidation import DataValidation

strategies = '"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"'
dv = DataValidation(
    type="list",
    formula1=strategies,
    allow_blank=True,
    showDropDown=False  # False = show dropdown arrow; True = inline only
)
dv.error = "Please select a valid response strategy"
dv.errorTitle = "Invalid Strategy"
dv.prompt = "Select response strategy"
dv.promptTitle = "Response Strategy"
ws.add_data_validation(dv)
dv.add(f'J2:J{last_row}')  # Column J = Response Strategy
```

**Pitfall:** When rebuilding a sheet that already has data validations, old validations accumulate. Always clear them first:
```python
ws.data_validations.dataValidation = []  # Clear all existing
# Then add the single new one
```

### AV Register Blank-Handling Formulas

AV risks often have empty Probability/Severity (not yet scored). Use IF-blank formulas to avoid showing "FALSE" or 0:

```python
# Score formula — blank until P and S filled
ws.cell(row=ri, column=8).value = f'=IF(F{ri}="","",F{ri}*G{ri})'

# Rating formula — blank until score computed
ws.cell(row=ri, column=9).value = f'=IF(H{ri}="","",IF(H{ri}>=12,"Critical",IF(H{ri}>=8,"High",IF(H{ri}>=4,"Medium","Low"))))'
```

### Clearing Sheets with Merged Cells

When rebuilding a sheet that may have merged cells, unmerge first or `MergedCell` attribute errors occur:

```python
def clear_sheet(ws):
    for mr in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(mr))
    for ri in range(1, ws.max_row + 1):
        for ci in range(1, ws.max_column + 1):
            ws.cell(row=ri, column=ci).value = None
```

### Live Register Note Pattern

Any table showing live register data must carry a halftone note that the register is the authoritative source:

```python
note_text = "Data shown is a snapshot from the live Project Risk Register, which is the authoritative source and updated weekly."
# Insert as a paragraph element after the table in the body
p = OxmlElement('w:p')
# ... build paragraph with 9pt gray text ...
body.insert(table_idx + 1, p)
```

## Sheet Title Constraints — Invalid Characters

Excel sheet titles have strict character restrictions. The following characters are **invalid** in sheet names and will raise `ValueError` from openpyxl:

- `/` (forward slash)
- `\` (backslash)
- `[` `]` (square brackets)
- `*` (asterisk)
- `?` (question mark)
- `:` (colon)
- Sheet names also cannot exceed 31 characters.

### Common failure pattern

```python
# ❌ FAILS — ValueError: Invalid character / found in sheet title
ws.title = "Other / Logistics"

# ✅ WORKS — replace / with - or another safe separator
ws.title = "Other - Logistics"
```

This is easy to miss when the category name naturally contains a `/` (e.g. "Other / Logistics", "MEP / Fire Protection", "AV / IT"). The sheet title must use a safe separator like `-` or `—` even though the cell text content can still display the original name with `/`.

### Safe naming pattern

```python
# Sheet title (safe): use - instead of /
ws.title = "Other - Logistics"

# Cell content (unrestricted): can still show the original name
ws["A1"].value = "02_Holy_Quran_Gift_Shop — Other / Logistics Cost Details"
```

**Pitfall:** If you define the sheet title in a `build_*` function AND also pass the name to `wb.create_sheet()`, you must fix BOTH places. The `create_sheet()` call and the `ws.title = ...` assignment both validate the name. A search for `Other / Logistics` in the file will find the `create_sheet()` call but miss the `ws.title` line if it's inside the builder function — grep for both.

## Modifying Existing Formatted Workbooks (Preserve-Format Pattern)

When you need to update an existing formatted Excel file (CR Sheet, submittal form, template), **never rebuild from scratch or insert rows** — both destroy the original formatting, merged cells, column widths, and data validations.

### Correct Pattern: Copy + Targeted Cell Edits

```python
import shutil
from copy import copy

# Step 1: Copy the original file
shutil.copy(original_path, output_path)

# Step 2: Open the copy
wb = openpyxl.load_workbook(output_path)
ws = wb['Sheet1']

# Step 3: Make targeted cell value changes
ws['A1'].value = 'Updated Title'
ws['C5'].value = 'New reference source'

# Step 4: Append to existing cell content (preserves formatting)
old_val = ws['D10'].value
ws['D10'].value = old_val + "\n\nUPDATE: New information added."

# Step 5: Save
wb.save(output_path)
```

### Pitfall: `ws.insert_rows()` Breaks Merged Cells

`ws.insert_rows()` shifts all rows down but **does not shift merged cell ranges** — the old merged ranges stay at their original positions, causing `MergedCell` attribute errors when you try to read/write cells that are now inside a misaligned merge.

**Never do this on a pre-formatted file with merged cells:**
```python
ws.insert_rows(11)  # Breaks merged cell ranges
```

**Instead, append new content to existing cells** or, if you must add a new row, rebuild the sheet from scratch using the Unified Register Template pattern above.

### Pattern for Adding New Items to a CR Sheet

A Comment Response Sheet (CR Sheet) typically has numbered items. To add a new item:

```python
# Option A: Append to the last existing cell (safe, preserves format)
ws.cell(row=last_row + 1, column=1).value = new_item_number
ws.cell(row=last_row + 1, column=2).value = "New CG comment"
# Copy formatting from the row above
for c in range(1, 8):
    src = ws.cell(row=last_row, column=c)
    dst = ws.cell(row=last_row + 1, column=c)
    dst.font = copy(src.font)
    dst.alignment = copy(src.alignment)
    dst.border = copy(src.border)
    dst.fill = copy(src.fill)
```

**Key insight:** The `copy()` from `copy` module copies openpyxl style objects correctly. Always use `from copy import copy` for style copying.

### When to Rebuild vs. Modify

| Situation | Approach |
|-----------|----------|
| Simple value/text updates | Copy + targeted edits |
| Adding rows mid-table | Rebuild from scratch with Unified Register Template |
| Changing column structure | Rebuild from scratch |
| Updating formulas | Copy + edit formula strings |
| Adding new items at end | Append to last row + copy styles |

The most common issue when styling openpyxl workbooks: **formula cells created programmatically have no cached values**. Opening with `data_only=True` returns `None` for all formula cells — you cannot read the computed severity string.

**Never do this:**
```python
# Fails — data_only=True returns None for uncalculated formulas
wb = openpyxl.load_workbook(file, data_only=True)
val = ws.cell(row=r, column=12).value  # None if never opened in Excel
```

**Always do this — two-pass compute from source columns:**
```python
# Pass 1: Read the STATIC source columns that feed into the formulas
wb_cache = openpyxl.load_workbook(file, data_only=True)
severity_data = {}
for r in range(data_start, data_end + 1):
    i = wb_cache.cell(row=r, column=prob_col).value    # static int
    j = wb_cache.cell(row=r, column=impact_col).value   # static int
    if isinstance(i, (int, float)) and isinstance(j, (int, float)):
        score = int(i) * int(j)
        if score >= 12:      sev = "critical"
        elif score >= 8:     sev = "high"
        elif score >= 4:     sev = "medium"
        else:                sev = "low"
        severity_data[(r, rating_col)] = sev
wb_cache.close()

# Pass 2: Style with data_only=False (preserves all formulas)
wb = openpyxl.load_workbook(file)
for r in range(data_start, data_end + 1):
    cell = ws.cell(row=r, column=rating_col)
    sev_key = severity_data.get((r, rating_col), "")
    if sev_key:
        fill, font = SEVERITY_MAP[sev_key]
        cell.fill = fill; cell.font = font
wb.save(file)
```

**Rule of thumb:** For any formula-driven cell whose computed value you need for styling, trace the formula back to its leaf-level static-value inputs and compute manually. The formula `=IF(A*B>=12,"Critical",IF(A*B>=8,"High",...))` means you read columns A and B (static), compute `A*B`, map to bands.

## Heat Map Coloring

For a P×I matrix (probability rows × impact columns), color each cell by the score `P × I`:

```python
def heatmap_color(score):
    if score >= 12:  return "FF4444"  # Critical
    if score >= 8:   return "FF8C00"  # High
    if score >= 4:   return "FFD700"  # Medium
    return "90EE90"                   # Low

for row_idx, p in {6: 4, 7: 3, 8: 2, 9: 1}.items():
    for col_idx, i in {3: 1, 4: 2, 5: 3, 6: 4}.items():
        score = p * i
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.fill = PatternFill(start_color=heatmap_color(score),
                                 end_color=heatmap_color(score), fill_type="solid")
        cell.font = Font(name="Calibri", size=12, bold=True,
                         color="FFFFFF" if score >= 12 else "000000")
```

## Typical Sheet Structure Walkthrough

The session that produced this skill styled a 13-sheet risk register. Each sheet type has a pattern:

1. **Cover** — Title row 2, metrics with gold fill, sheet index
2. **Main Register** — Title rows, header row + data with formula-driven severity, freeze panes
3. **Dashboard** — KPI headers, severity-colored distribution headers, red watchlist header
4. **Matrix/Heat Map** — Navy labels, color-coded P×I cells, score bands
5. **Sub-registers** (HSE, AV, DRR) — Same navy header pattern, severity fills on rating column
6. **Change Log** — Navy headers, alternating row stripes

## OneDrive Read Pattern — One File at a Time

When reading files from OneDrive, read ONE file at a time. Do NOT batch-read or use wildcard loops that trigger OneDrive sync contention. OneDrive hangs when multiple files are accessed simultaneously.

### Correct pattern

```python
# Read one PDF at a time — never loop over all files
result = terminal(f'pdftotext -layout "{path}" - 2>/dev/null | head -40')
```

### Wrong pattern (causes OneDrive hangs)

```python
# NEVER do this — triggers sync contention
for file in os.listdir(folder):
    result = terminal(f'pdftotext -layout "{folder}/{file}" - ...')
```

When the user says "one by one", respect that literally — no parallel reads, no background subagents for OneDrive paths.

## OneDrive Write Pattern — /tmp First, Then Copy

OneDrive **reverts direct writes** to files inside the sync folder. If you write to a OneDrive path with openpyxl and immediately re-read it, the old version may still be there. This causes the user to see the old file even though your script reported success.

### Correct write pattern

```python
import shutil

# Step 1: Copy the original to /tmp
shutil.copy(onedrive_path, '/tmp/workbook_backup.xlsx')

# Step 2: Open and modify the /tmp copy
wb = openpyxl.load_workbook('/tmp/workbook_backup.xlsx')
# ... make all changes ...
wb.save('/tmp/workbook_backup.xlsx')

# Step 3: Copy back to OneDrive
shutil.copy('/tmp/workbook_backup.xlsx', onedrive_path)

# Step 4: Verify
wb2 = openpyxl.load_workbook(onedrive_path)
assert 'NewSheet' in wb2.sheetnames  # confirm write took
```

### Wrong write pattern (causes silent reverts)

```python
# NEVER do this — OneDrive may revert the file
wb = openpyxl.load_workbook(onedrive_path)
# ... make changes ...
wb.save(onedrive_path)  # May appear to succeed but OneDrive reverts
```

**Pitfall:** The revert is silent. Your script exits with code 0, the user opens the file, and the changes aren't there. Always verify by re-reading the OneDrive path after writing.

## Repo Register Creation Pattern

When creating markdown registers from OneDrive project folders (Letters, RFI, MOM, NCR, Weekly Reports, SIs):

### Required YAML frontmatter

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Technical Office
status: active
source: OneDrive/<path to source folder>
---
```

### Required columns per register type

| Register | Columns |
|----------|---------|
| Letters | Ref, Date, Subject, Key Content, Status, Linked Risks |
| RFI/TQ | Ref, Date, Subject, Key Query, Status, Linked Risks |
| MOM | Ref, Date, Meeting Type, Chair, Location, Key Topics, Minutes File, Status |
| SI | SI#, Date, Subject, Key Instruction, Status, Related Docs, Linked Risks |
| NCR | Ref, Date, Subject, Finding, Status, Linked Risks |

### Cross-reference to PRR/DRR

Every register entry should link to its related PRR or DRR risk IDs. Add a cross-reference summary table at the bottom of the file.

### Source traceability

- Reference the OneDrive path in the `source` field
- Note missing or misfiled documents
- Note date discrepancies between PDF headers and register logs
- Never copy PDFs into the repo — reference their OneDrive path

## DRR Risk Assessment Logic

When populating DRR residual columns (Resid. Prob, Resid. Impact, Contingency Plan, Trigger, Linked Risks, Evidence Source), assess each risk against current project status:

| Current Status | Residual P×I | Logic |
|----------------|:------------:|-------|
| Closed | 1×1=1 | Risk event passed or resolved |
| Mitigated | 1×2=2 or 2×2=4 | Controls in place, residual remains |
| Watch | 2×2=4 or 2×3=6 | Active mitigation, not yet resolved |
| Open | 2×3=6 to 4×5=20 | Honest current assessment |

Every open risk needs:
- **Contingency Plan** — specific fallback action if the risk materialises
- **Trigger / Early Warning** — what to watch for that signals the risk is materialising
- **Linked Risks** — cross-reference to PRR IDs
- **Evidence Source** — actual project documents, not generic references

## Construction Stage Register — Separate Sheet, RMP-Compliant

When the old consolidated register has a Construction Stage sheet with site-level operational risks (C-001 to C-040):

1. **Add as a separate sheet** — do NOT merge into the master register. Construction risks are site-level operational items (labor, equipment, weather, theft, scaffolding) — different audience and review frequency from strategic master risks.
2. **Place between DRR and HSE** in the sheet order.
3. **Convert to RMP-compliant scoring** — the old sheet uses text labels only (High/Medium/Low/Very High). Convert to numeric P(1-4) x S(1-4) with formula-driven PxI and Severity per RMP bands.
4. **Add Source and Linked PRR columns** — every Aseer-specific risk must reference its source document (SI, NCR, MOM) and linked PRR.
5. **Style consistently** — navy headers, severity colors, freeze panes, auto-filter.

### Text-to-numeric mapping

```python
text_to_num = {'low': 1, 'medium': 2, 'high': 3, 'very high': 4}
```

### Aseer-specific risks

Replace generic template risks with real project risks sourced from SIs, NCRs, and MOMs. Each Aseer-specific risk must have:
- Source document reference (e.g. SI-14, NC-1F0-007)
- Linked PRR cross-reference
- Numeric P and S scores based on actual project conditions

## Date Identified and Last Review Columns

The Risk Register must include Date Identified and Last Review columns. Best practice:

| Column | Placement | Content |
|--------|:---------:|---------|
| Date Identified | After Risk ID (col C) | When the risk first became apparent, not when formally added |
| Last Review | After Status (col O) | Updated to current date on every review cycle |

### Date mapping logic

For a project at day 189, risks should date back to the period when they first emerged, not just the current revision:

```python
# Feb 2026 — early project risks (mobilisation, permits, programme, commercial)
feb_risks = ['PRR-APP-01', 'PRR-APP-02', 'PRR-COM-01', 'PRR-SCH-01', ...]
# Mar 2026 — design risks, EOT claim
mar_risks = ['PRR-DES-01', 'PRR-FLS-01', 'PRR-MEP-01', 'PRR-COM-05', ...]
# Apr 2026 — procurement risks
apr_risks = ['PRR-PRC-01', 'PRR-PRC-02', 'PRR-AV-01', ...]
```

## Never Skip a Folder Without Reading a Document

Folder names are misleading. A folder called "16- Safety Notices" sounds low-value but may contain formal stop-work notices linked to SIs and NCRs.

**Mandatory workflow when auditing project folders:**

1. List the folder contents
2. Read at least one sample PDF from each folder using `pdftotext`
3. Document what you found even if you decide to skip it
4. Only then decide if the folder adds value to the repo

**Wrong pattern (what got corrected):**
```python
# Judged folders 14-20 as "low value" based on folder names alone
# without reading a single document inside them
```

**Correct pattern:**
```python
# Read at least one PDF from each folder before deciding
result = terminal(f'pdftotext -layout "{sample_pdf}" - 2>/dev/null | head -20')
# Now assess: does this add new information to the repo?
```

## Reference

See `references/risk-register-example.md` for the full script structure and sheet-by-sheet breakouts from the Aseer Museum risk register session.
See `references/onedrive-folder-audit-workflow.md` for the systematic pattern to audit OneDrive project folders and decide what to add to the repo.
See `references/risk-register-cleanup-patterns.md` for the full cleanup and formatting patterns from the C11 session.
See `references/drr-risk-assessment-logic.md` for the DRR residual scoring and evidence population logic.
