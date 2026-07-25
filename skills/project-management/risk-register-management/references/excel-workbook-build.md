# Excel Workbook Build Patterns

Building risk register workbooks from JSON with openpyxl template copy, Aseer Museum project.

## Template Preservation
- Copy template via `shutil.copy2`, then `load_workbook` the copy
- **Never overwrite Dashboard cells with static data** — the template has formulas, charts, images, merged cells
- Use `setv(c,v)` that skips MergedCell: `if c.__class__.__name__!='MergedCell': c.value=v`

## Column Layout Changes
When changing Risk Register column layout:
- Update headers on row 9
- Write data from row 10
- Update ALL Dashboard formulas for new col refs:
  - Risk Matrix COUNTIFS: Prob col M→D, Sev col N→E
  - By Rating COUNTIF: Rating col C→G
  - By Status COUNTIF: Status col E→H
  - Top Owners COUNTIF: Owner col F→I
  - Category COUNTIF: update last-row reference per register

## Dynamic Category Table
- Extract unique categories from data, sort by count desc
- Map codes to full names (PRC→Procurement, COM→Commercial, etc.)
- Write COUNTIF formulas per row, SUM row at end
- If categories overflow row 38, shift TOP OWNERS section:
  - Unmerge B39:C39 first
  - Copy bottom-up from row 55 to 38
  - Fix relative formula refs: `re.sub(r',B\d+\)$',f',B{row})',c.value)`
  - Re-merge at new position
- Update Bar chart ref to `Dashboard!$D$28:$D${last_cat}`

## Chart Cache
- Clear numCache to force recalculation:
  ```python
  ch.series[0].val.numRef.numCache = None
  ch.series[0].cat.strRef.strCache = None
  ```

## Download Filename
- Server: `EXP-RISK-{REG}-{year}-{seq}_Rev{rev}_ACTIVE.xlsx`
- Download attr: `Aseer_Regional_Museum_{REG}_{date}_{time}.xlsx`
- Use `__XLSX_HREF__` / `__XLSX_DOWNLOAD__` placeholders in HTML

## Build Pipeline
- `webapp/build_risk.py` → PRR (deployed to `registers/Risk/`)
- `webapp/av/build_av.py` → AVR (deployed to `registers/Risk/AV/`)
- DDR/HSE: separate pipelines outside repo
- `/tmp/build_all_template_registers.py` → all 4 Excel files to `/tmp/all_register_exports/`
