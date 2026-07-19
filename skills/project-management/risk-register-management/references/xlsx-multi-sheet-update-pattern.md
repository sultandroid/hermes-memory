# XLSX Multi-Sheet Update Pattern — Adding Risks to the Live Register

When adding new risks to the Excel risk register, you must update **5 sheets** to keep the file internally consistent. Missing any one sheet creates a mismatch that the user or CG will catch.

## Sheets to Update

| # | Sheet | What Changes | Example (adding 2 Medium risks) |
|---|-------|-------------|----------------------------------|
| 1 | **Risk Register** | Append new rows at the end (row 55, 56) | 2 new rows with all 15 columns |
| 2 | **Cover** | Total Risks, Open count, Medium count | 52→54, 49→51, 23→25 |
| 3 | **Dashboard** | Severity counts + Category counts | Medium 22→24, AV 1→2, PRC 7→8 |
| 4 | **RBS** | Category counts | AV 1→2, PRC 7→8 |
| 5 | **Register Control** | New revision history row | C11 update entry |

## Column Layout (Risk Register sheet)

The xlsx has 15 columns (A-O):

| Col | Header | Type | Example |
|-----|--------|------|---------|
| A | # | Number | 53 |
| B | Risk ID | Text | PRR-AV-02 |
| C | Category | Text | AV |
| D | Risk Event | Text | AV hardware procurement delays... |
| E | Cause | Text | Rawasin AV hardware has 12-16 week... |
| F | Consequence | Text | AV integration testing compressed... |
| G | P | Number | 2 |
| H | S | Number | 3 |
| I | PxI | Formula | =G55*H55 |
| J | Severity | Text | Medium |
| K | Response Action | Text | Issue LOI early with 20% advance... |
| L | Owner | Text | AV Lead |
| M | Status | Text | Open |
| N | Target Close | Text | 2026-08-15 |
| O | Evidence | Text | PM Consolidated Risk Register... |

**Important:** Column I (PxI) is a **formula** (`=G{r}*H{r}`), not a hardcoded value. Always use the formula pattern.

## Style Copy Pattern

```python
from copy import copy

ref_cells = [ws.cell(row=last_risk_row, column=c) for c in range(1, 16)]

def copy_style(src, dst):
    if src.font: dst.font = copy(src.font)
    if src.alignment: dst.alignment = copy(src.alignment)
    if src.border: dst.border = copy(src.border)
    if src.fill: dst.fill = copy(src.fill)

for i, val in enumerate(risk_data):
    c = ws.cell(row=new_row, column=i+1, value=val)
    copy_style(ref_cells[i], c)
```

## Cover Sheet Cell Map

| Metric | Cell | 
|--------|------|
| Total Risks | C7 |
| Open | F7 |
| Watch | C8 |
| Mitigated | F8 |
| Critical | C9 |
| High | F9 |
| Medium | C10 |
| Low | F10 |

## Dashboard Cell Map

| Metric | Cell |
|--------|------|
| Critical count | C5 |
| High count | C6 |
| Medium count | C7 |
| Low count | C8 |
| Category counts (COM..TCH) | F5:F22 |

## RBS Sheet

Find the category row by scanning for the category code (e.g. 'AV', 'PRC'), then update the cell to its right (same row, column+1).

## Register Control Sheet

Append a new row at the bottom with:
- Col A: Version (e.g. "C11")
- Col B: Date (e.g. "2026-07-19")
- Col C: Author (e.g. "Hermes")
- Col D: Description (client-facing, e.g. "Added PRR-AV-02 and PRR-PRC-07 from consolidated register. Total: 54 risks.")

## Verification

After all updates, verify with a script that reads back the key values:

```python
# Verify new risks exist
ws.cell(row=55, column=1).value  # should be 53
ws.cell(row=55, column=2).value  # should be 'PRR-AV-02'

# Verify Cover
ws_cover['C7'].value  # should be 54

# Verify Dashboard
ws_dash['C7'].value  # should be 24 (Medium)
ws_dash['F7'].value  # should be 8 (PRC)

# Verify RBS
# Find AV row, check count = 2
```

## Common Pitfalls

- **Merged cells in Cover sheet** — unmerge before writing, re-merge after
- **Formula in PxI column** — use `=G{r}*H{r}`, not a hardcoded number
- **Style copy fails if ref row has empty cells** — only copy from a row that has all 15 columns populated
- **Dashboard category counts** — these are hardcoded numbers, not formulas. Update them manually
- **Register Control description** — must be client-facing, not internal notes. "Added 2 risks" not "Fixed formatting"
