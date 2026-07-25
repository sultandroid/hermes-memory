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

### Snapshot Excel Builder — Per-Register Snapshot Pipeline

When building Samaya-styled **risk register Excel snapshots** for the Aseer Museum (PRR/DDR), follow this pattern. See the live example at `06_Risk_System/webapp/build_xlsx.py` and `06_Risk_System/webapp/build_snapshots.py`.

### Pipeline (build_snapshots → build_risk/build_ddr → deploy.sh)

1. **build_snapshots.py** generates the xlsx (one per register) via `build_xlsx.py:build()`
2. **build_risk.py** / **build_ddr.py** discover the latest versioned xlsx and embed its name in the HTML's Excel button
3. **deploy.sh** runs all three steps then rsyncs to Hostinger

### Per-Register Separation — RMP-Compliant

The RMP Section 9.1 defines four linked risk registers with **different scoring scales**. Never merge them into one view:

| Register | Scale | Count |
|----------|-------|-------|
| PRR (Master) | P x S 1-4 | 52 |
| DDR (Design) | P x I 1-5 | 79 |
| HSE | C x L 1-5 | 41 |
| AV | P x S 1-4 | ~30 |

Each register gets its own Excel snapshot and its own webapp page. The webapp uses a shared `template.html`; DDR is at `/aseer/registers/Risk/DDR/` (uppercase to dodge Hostinger case-sensitivity cache).

### Cover Block Layout (rows 1-9, every sheet)

```
Row 1: "ASEER REGIONAL MUSEUM — <Register Name>" (Calibri 18pt bold, Navy #1E293B)
Row 2: "Doc No. <EXP-RISK-YYY-YYYY> · Contract: <...> · Rev <C11> · <ACTIVE>"
Row 3: "Snapshot No. <NNN> · Date: <YYYY-MM-DD> · Time: <HH:MM (Asia/Riyadh)> · Source: <URL>"
Row 4: (blank)
Row 5: KPI numeric cards — B5=total, C5=Critical, D5=High, E5=Medium, F5=Low, G5=Open
Row 6: KPI labels — B6=TOTAL, C6=CRITICAL, D6=HIGH, E6=MEDIUM, F6=LOW, G6=OPEN
Row 7: (blank)
Row 8: QR code (left, cell A8, 110px) + Samaya logo (right, cell G8, ~28px tall)
Row 9: "Scan to open live register → <URL>" (italic 8pt gray)
```

- KPIs use 1-column-per-card (B..G), NOT merged cells (avoids MergedCell ValueError)
- Logo: fetch from `_Style-Guides/logos archives/samaya-logo.png` (repo path)
- QR: `segno.make(url, error="m")` saved to /tmp PNG, loaded as XLImage (fallback if segno absent)

### Heatmap Risk Matrix (dashboard sheet, rows 11+)

```
Row 11: "RISK MATRIX" (merge B-J)
Row 12: "P ↓ / S →" | "S1" | "S2" | "S3" | "S4"   (navy headers, white font on Navy bg)
Row 13: "P4" | cell | cell | cell | cell            (P rows high-to-low: P4..P1)
Row 14: "P3" | cell | cell | cell | cell
Row 15: "P2" | cell | cell | cell | cell
Row 16: "P1" | cell | cell | cell | cell
```

- Cells with risks get **band-colored fill** (RATING_FILL by P*S score, white bold font)
- Empty cells: Light Gray (#F1F5F9) fill
- Score-to-band: P*S≥12=Critical, ≥8=High, ≥4=Medium, <4=Low (PRR 4x4)
- For DDR 5x5: P*I≥16=Critical, ≥10=High, ≥5=Medium, <5=Low

### Charts (Dashboard sheet)

Two openpyxl-native charts, no matplotlib:
1. **Doughnut chart** for severity split (proportion, best practice). Data source: by-rating table counts.
2. **Bar chart** for category exposure (comparison, best practice). Data source: category table. Sorted by count descending, with category labels.

```python
from openpyxl.chart import DoughnutChart, BarChart, Reference
```

### Page Header/Footer (all sheets)

```python
ws.oddHeader.left.text = "Samaya Investment · Technical Office"
ws.oddHeader.center.text = f"Snapshot No. {snapshot_no}"
ws.oddHeader.right.text = f"{doc_no} · Rev {revision} · {status} · {register} · {page_url}"
ws.oddFooter.left.text = "RESTRICTED · Project use only"
ws.oddFooter.center.text = f"Generated {datetime}"
ws.oddFooter.right.text = "Page &P of &N"
# All 8pt, gray (#64748B)
```

### Page Setup (A4 portrait per Samaya Style Guide §2.1)

```python
ws.page_setup.orientation = "portrait"
ws.page_setup.paperSize = 9  # A4
ws.page_setup.fitToWidth = 1
ws.page_margins = PageMargins(left=1.5, right=1.5, top=2.0, bottom=2.0, header=0.8, footer=0.8)
ws.print_options.horizontalCentered = True
```

### Snapshot Counter Management — CRITICAL (prevents drift bug)

**The bug:** `build_xlsx.py` auto-incremented the counter every time called. The caller also managed it. This created two key families in `snapshot_counter.json` ("PRR" vs "Master Risk Register (PRR)") with different numbers. The xlsx content said "Snapshot No. 006" but the filename said "001".

**How to avoid drift:**

1. `build_xlsx.build()` accepts an explicit `snapshot_no` parameter. When provided (caller-managed), it uses that number without touching the counter. When None (legacy mode), it auto-increments.
2. `build_snapshots.py` (the builder) manages the counter via `--bump` flag. Idempotent by default (no counter advance on repeated runs during testing). Only `--bump` advances the number.
3. Snapshot number is resolved BEFORE the `build()` call — xlsx content number always matches the output filename.
4. Only two register keys in `snapshot_counter.json`: "PRR" and "DDR". Never use the human-readable register name as a counter key.

```python
# Correct — caller manages counter, number known before build
snapshot_no = cur + 1 if args.bump else cur if cur > 0 else 1
bx.build(data, str(out_path), snapshot_no=snapshot_no, ...)

# WRONG — build_xlsx.py should NOT auto-increment or bump inside build()
build(data, out_path)  # no snapshot_no passed -> auto-increment (not recommended)
```

```json
{"PRR": {"last_snapshot": 1, "last_date": "2026-07-24", "last_revision": "C11"},
 "DDR": {"last_snapshot": 1, "last_date": "2026-07-24", "last_revision": "C11"}}
```

### File Naming Convention (per Engineering Chart Framework §1.4)

`EXP-RISK-<REG>-YYYY-NNN_Rev<rev>_<STATUS>.xlsx`
Example: `EXP-RISK-PRR-2026-001_RevC11_ACTIVE.xlsx`

Old non-versioned names (`Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx`) are superseded. The versioned snapshot is the authoritative download.

### Hostinger Deployment — Case-Sensitive Directory 404

When creating a new subdirectory under `/aseer/registers/Risk/` on Hostinger LiteSpeed:

- **Lowercase directories get stuck in a 404 cache** after first accidental access. The 404 page carries `last-modified: Tue, 22 Apr 2025` (Hostinger default) and persists even after the file is on disk with correct perms.
- **Fix: use UPPERCASE for the first directory name** (e.g. `DDR/` not `ddr/`). The uppercase path bypasses the cache because no 404 was ever cached for that exact path string.
- Add `.htaccess` with cache-disabling directives:
  ```
  <IfModule mod_headers.c>
      Header set Cache-Control no-cache, no-store, must-revalidate
  </IfModule>
  <IfModule LiteSpeed>
      CacheDisable public /
  </IfModule>
  ```
- If the directory MUST be lowercase, create it as UPPERCASE first, wait for 200, then rename to lowercase. Or keep uppercase permanently.

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

## User-Provided Workbook Templates (Highest Priority)

When the user supplies a manually formatted `.xlsx` and asks to use it as a template, treat that workbook as the visual and structural source of truth. First copy it into a stable project template path and inspect every sheet's row/column layout, merged ranges, charts, images, freeze panes, filters, and formulas. Preserve those conventions before changing values.

For risk-register snapshots, the template must retain:
- Dashboard layout, charts, Samaya logo, QR/live-register link placement
- `Risk Register` Owner, Target, Response / Action, and Evidence columns
- An `Action Plan` sheet populated from structured actions; when no structured action array exists, use the source `response_action` text as the action entry rather than showing an empty sheet
- Existing manual formatting and column widths

Never claim owners or target dates that are absent from the source data. Keep `—` or `TBC` and report the source-data gap explicitly.

A reference template from the DDR correction session is stored as `templates/risk_snapshot_template.xlsx` in the project webapp when available. See `references/user-template-preservation.md` for the inspection and rebuild procedure.

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

### Construction Stage Risk Audit — Generic vs Duplicate vs Promote

When auditing a secondary risk register (e.g. Construction Stage C-001 to C-060) for potential promotion to the PRR master, classify each risk into one of three buckets:

#### 1. Generic / No meaning for this project (reject)

Risks that are generic construction-site items not specific to this museum fit-out project. Examples:
- Concrete pump failure during casting (no mass concrete works)
- Utility damage during excavation (minimal excavation)
- Pandemic or infectious disease outbreak (post-COVID generic)
- Heavy rain / extreme weather (not Aseer-specific)
- Fuel shortage for equipment, theft/vandalism, poor housekeeping
- Generic HSE items already in the HSE register (confined space, electrical shock, fall from height)
- Vague/unmeasurable items ("failure to achieve planned productivity")

#### 2. Already covered by existing PRR (duplicate — omit)

Map to the existing PRR risk that covers the same territory. Overlap is checked per-risk, not per-category:
- Schedule delays -> PRR-SCH-01
- Subcontractor performance -> PRR-PRC-04, PRR-PRC-07
- Interface conflicts -> PRR-CON-02
- Non-conformance / quality -> PRR-QLT-01
- Testing and commissioning -> PRR-TCH-01
- Communication breakdown -> PRR-STK-01, PRR-STK-02
- Inspection approval delays -> PRR-APP-02, PRR-APP-04
- Design clarification delays -> PRR-DES-05

#### 3. Meaningful and missing (promote to PRR)

Risks that are project-specific, not covered by any existing PRR entry, and significant enough for executive attention. Add as new PRR-XXX-NN risks:
- Material shortage at remote Aseer site -> PRR-CON-05 (High)
- Site access restrictions at Abu Malha Heritage Palace -> PRR-LOG-02 (High)
- Work permit delays for heritage building works -> PRR-APP-05 (High)

#### Promoting a risk to the PRR

When adding a promoted risk:
1. Use the next available number in the category (e.g. PRR-CON-05 follows PRR-CON-04)
2. Write the title in plain English, project-specific
3. Set probability/severity based on the source register's P and S
4. Link evidence back to the source register (e.g. "C11 Construction Stage Register C-002")
5. Add a history entry documenting the promotion
6. Update the JSON total count

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

## Multi-register dashboard layout and owner integrity

When a user supplies a manually formatted PRR/DDR workbook, save it as the canonical template and regenerate PRR, DDR, HSE, and AVR from the same template. Do not revert to a generic builder for one register only.

For dashboard tables:

- Refresh both category names and codes from the current payload; never leave stale template labels beside current codes.
- Clear stale category/status/owner rows before writing new rows.
- Split long Exposure by Category tables into two side-by-side blocks with Category, Code, Count, and % of total columns. Wrap category names.
- Position Top Owners after the taller category/status block. If the section exceeds the footer, move the footer down. Never rely on fixed row 37 or another fixed row.
- Use formulas against the Risk Register sheet for category, rating, status, owner, percentage, and matrix counts. Keep probability/severity in hidden helper columns if the visible approved template lacks them.
- Preserve the Owner, Target, Response / Action, and Action Plan fields in every register. If structured actions are absent, populate Action Plan from the source response/action text.
- For DDR, assign owners only from documented discipline responsibility. Do not invent owner names; use role titles such as Planner, Design Manager, BIM Coordinator, MEP Lead, AV Lead, Conservation Consultant, Approvals Consultant, QA/QC Director, Commercial Manager, Procurement Lead, or Security Specialist. If the source is genuinely unassigned, retain `—` and report the gap.

Verification must inspect formula strings with `data_only=False`, check for stale/blank category rows, assert Top Owners starts below the preceding tables, and verify the live XLSX download returns HTTP 200.

## Multi-register dashboard layout and owner integrity

When a user supplies a manually formatted PRR/DDR workbook, save it as the canonical template and regenerate PRR, DDR, HSE, and AVR from the same template. Do not revert to a generic builder for one register only.

Dashboard rules:

- Refresh both category names and codes from the current payload; never leave stale template labels beside current codes.
- Clear stale category, status, and owner rows before writing new rows.
- Split long Exposure by Category tables into two side-by-side blocks with Category, Code, Count, and % of total columns. Wrap category names.
- Position Top Owners after the taller category/status block. If the section exceeds the footer, move the footer down. Never rely on fixed row 37 or another fixed row.
- Use formulas against the Risk Register sheet for category, rating, status, owner, percentage, and matrix counts. Keep probability/severity in hidden helper columns if the visible approved template lacks them.
- Preserve Owner, Target, Response / Action, and Action Plan fields in every register. If structured actions are absent, populate Action Plan from the source response/action text.
- If formulas have no cached results, preserve the formulas and inject cached dashboard values into the worksheet XML so Excel Preview and other viewers display the dashboard immediately. Verify with both `data_only=False` and `data_only=True`.
- Before inserting rows into a formatted template, unmerge body/footer ranges at or below the insertion point. Otherwise merged footer rows can swallow target or action-plan cells.
- For DDR, assign owners only from documented discipline responsibility. Use role titles such as Planner, Design Manager, BIM Coordinator, MEP Lead, AV Lead, Conservation Consultant, Approvals Consultant, QA/QC Director, Commercial Manager, Procurement Lead, or Security Specialist. Do not invent personal names; retain `—` and report the gap where the source is genuinely unassigned.
- Every DDR risk must have a target date in both Risk Register and Action Plan. Use current rating and remaining programme to set working-day milestones, avoiding Fridays.

Verification must inspect formula strings with `data_only=False`, cached values with `data_only=True`, stale/blank category rows, Top Owners placement below preceding tables, Owner/Target fields in both sheets, and HTTP 200 for each live XLSX download.

## Reference

See `references/risk-register-example.md` for the full script structure and sheet-by-sheet breakouts from the Aseer Museum risk register session.
See `references/onedrive-folder-audit-workflow.md` for the systematic pattern to audit OneDrive project folders and decide what to add to the repo.
See `references/risk-register-cleanup-patterns.md` for the full cleanup and formatting patterns from the C11 session.

## Public Register Controls and Source Visibility

- Never expose internal-only evidence in public HTML or XLSX. Before publishing, search generated HTML, JSON, workbook shared strings, and evidence/history fields for internal register names, private dashboards, repo paths, or documents not issued to CG. Replace only with approved CG-visible evidence or neutral wording such as `Project risk review` when the source cannot be cited publicly.
- Use plain human engineering English. Remove AI fingerprints, decorative symbols, em dashes, bullets, arrows, checkmarks, and phrases such as `seamlessly`, `robust`, and `cutting-edge` from public outputs.
- Treat a user-supplied manually formatted workbook as the common visual template for every register. Preserve owner, target, response/action, evidence, logo, QR, charts, and merged-cell layout. Clear old rows before repopulating.
- Dashboard sections must be formula-driven and dynamic. Split long category tables into two blocks, wrap labels, and place Top Owners below the taller preceding block. Do not use fixed row 37. If inserting rows, unmerge body/footer ranges first.
- The downloaded Risk Register must show Probability, Severity, Score, and Rating. Score must be a formula (`Probability * Severity`) and Rating must be a formula based on the register scoring bands. Preserve formulas and inject cached results where previewers otherwise show blanks.
- Public web dashboards should make Risk Matrix, Exposure by Category, By Status, and Top Owners headings clickable links to one schedule anchor. Verify each page has one anchor and working smooth-scroll handlers.
- Keep only `Download Snapshot` in the page controls when requested. Remove Print and CSV controls from both visible HTML and stale button markup.
- Final verification: inspect public HTML for prohibited source names/symbols, inspect XLSX formulas with `data_only=False`, inspect cached values with `data_only=True`, confirm no stale rows or overlaps, and test every live download with HTTP 200.
See `references/drr-risk-assessment-logic.md` for the DRR residual scoring and evidence population logic.
