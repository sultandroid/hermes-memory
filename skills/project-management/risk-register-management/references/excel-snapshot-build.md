# Excel Snapshot Build (Template-Based)

## Overview

Use `/tmp/build_all_template_registers.py` to generate all four register Excel files (PRR, DDR, HSE, AVR) from a single formatted template. The template is the user's approved layout — NEVER regenerate it from scratch.

## Template Location

`webapp/templates/risk_snapshot_template.xlsx`

Copy it with `shutil.copy2()`, fill data with openpyxl.

## Template Layout

| Aspect | Detail |
|--------|--------|
| Header rows | Rows 1-3 merged (project title, doc ref, snapshot info) |
| Header labels | Row 5 (ID, CATEGORY, RISK, CAUSE, EVENT, CONSEQUENCE, P, S, SCORE, RATING, STATUS, OWNER, TARGET CLOSE, RESPONSE, EVIDENCE) |
| Data start | **Row 6** (not row 10) |
| Last data row | `5 + risk_count` |
| Footer | Last row merged (Samaya copyright) |

## Risk Register Column Mapping (row 6+)

| Col | Content | JSON Key |
|-----|---------|----------|
| A | ID | `id` |
| B | CAT | `category` (code like DES, PRC) |
| C | RISK | `title` or `event` |
| D | CAUSE | `cause` |
| E | EVENT | `event` |
| F | CONSEQUENCE | `consequence` |
| G | P (Probability) | `probability` (1-4) |
| H | S (Severity) | `severity` (1-4) |
| I | SCORE | `=G*H` formula (not stored) |
| J | RATING | `rating` (Critical/High/Medium/Low) |
| K | STATUS | `status` (Open/Mitigated/Closed/Watch) |
| L | OWNER | `owner` |
| M | TARGET CLOSE | `target_close` |
| N | RESPONSE / MITIGATION | `response_action` |
| O | EVIDENCE | `evidence` (join array with "; ") |

## Dashboard Formula References

All Dashboard COUNTIF/COUNTA/COUNTIFS formulas reference `'Risk Register'!$col$6:$col${last}`. The build script discovers the last row from risk count and updates all formula ranges by regex:

```python
re.sub(r'(\$[A-Z]+\$6:\$[A-Z]+)\$\d+',
       lambda m: m.group(1)+'$'+str(last), cell_value)
```

| Dashboard Section | Row(s) | Key Formulas | RR Columns Referenced |
|-------------------|--------|--------------|-----------------------|
| KPI cards | 6-7 | B=COUNTA(A), D=COUNTIF(J,"Critical"), F=COUNTIF(J,"High"), H=COUNTIF(J,"Medium"), J=COUNTIF(J,"Low"), L=COUNTIF(K,"Open") | A=ID, J=RATING, K=STATUS |
| Risk Matrix | 11-15 | COUNTIFS(G={P}, H={S}) | G=P, H=S |
| By Rating | 11-18 | COUNTIF(J, rating_label) | J=RATING |
| By Status | 16-18 | COUNTIF(K, status_label) | K=STATUS |
| Top Owners | 11-18 | COUNTIF(L, owner_name) | L=OWNER |
| Exposure by Category | 20-36 | COUNTIF(B, category_code) | B=CAT |
| Bar chart | Chart object | Data=D20:D36, Cat=B20:B36 | B=labels, D=counts |

The template already has all these formulas for all 17 category codes (PRC, COM, DES, CON, APP, SCH, CNS, STK, FLS, HSE, LOG, MEP, OPS, QLT, SEC, SIT, TCH). Only the last-row number needs updating per register.

## Action Plan Sheet

Columns: ID, CAT, RATING, RESPONSE, OWNER, TARGET, STATUS — same row index as Risk Register.

## Build Script Pattern (skeleton)

```python
import json, re, shutil
from pathlib import Path
from openpyxl import load_workbook

TEMPLATE = Path('webapp/templates/risk_snapshot_template.xlsx')
OUT = Path('/tmp/all_register_exports')

def setv(c, v):
    if c.__class__.__name__ != 'MergedCell':
        c.value = v

def build(name, filename, risks, revision, title, live_url):
    shutil.copy2(TEMPLATE, OUT/filename)
    w = load_workbook(OUT/filename)
    last = 5 + len(risks)

    # Common header
    for s in w.worksheets:
        setv(s['A1'], f'ASEER REGIONAL MUSEUM — {title}')
        setv(s['A2'], f'Doc No. EXP-RISK-{name} ... Rev {revision}')
        setv(s['A3'], f'Snapshot Date: ... Source: {live_url}')

    # Update Dashboard formulas
    dash = w['Dashboard']
    for row in range(1, dash.max_row+1):
        for col in range(1, dash.max_column+1):
            c = dash.cell(row, col)
            if c.value and isinstance(c.value, str) and 'Risk Register' in c.value:
                c.value = re.sub(r'(\$[A-Z]+\$6:\$[A-Z]+)\$\d+',
                               lambda m: m.group(1)+'$'+str(last), c.value)

    # Clear old data rows
    rr = w['Risk Register']; ap = w['Action Plan']
    for s in [rr, ap]:
        for row in range(6, s.max_row+1):
            for col in range(1, s.max_column+1):
                setv(s.cell(row, col), None)
        for rng in list(s.merged_cells.ranges):
            if rng.min_row >= 6:
                s.unmerge_cells(str(rng))

    # Write risks
    for i, r in enumerate(risks, 6):
        setv(rr.cell(i, 1), r.get('id',''))
        setv(rr.cell(i, 2), r.get('category',''))
        setv(rr.cell(i, 3), r.get('title',''))
        setv(rr.cell(i, 4), r.get('cause',''))
        setv(rr.cell(i, 5), r.get('event',''))
        setv(rr.cell(i, 6), r.get('consequence',''))
        setv(rr.cell(i, 7), r.get('probability',''))
        setv(rr.cell(i, 8), r.get('severity',''))
        setv(rr.cell(i, 9), f'=G{i}*H{i}')
        setv(rr.cell(i, 10), r.get('rating',''))
        setv(rr.cell(i, 11), r.get('status',''))
        setv(rr.cell(i, 12), r.get('owner','--'))
        setv(rr.cell(i, 13), r.get('target_close',''))
        setv(rr.cell(i, 14), r.get('response_action','') or 'See Action Plan')
        setv(rr.cell(i, 15), '; '.join(r.get('evidence',[]) or []))

        # Action Plan row
        for ci, val in enumerate([
            r.get('id',''), r.get('category',''), r.get('rating',''),
            r.get('response_action',''), r.get('owner','--'),
            r.get('target_close',''), r.get('status','')
        ], 1):
            setv(ap.cell(i, ci), val)

    # Clear rows below data
    for row in range(last+1, rr.max_row+1):
        for col in range(1, rr.max_column+1):
            setv(rr.cell(row, col), None)

    w.save(OUT/filename)
    os.chmod(OUT/filename, 0o644)  # web-readable
```

## Snapshot Download Naming

Browser `download` attribute is independent of server `href`:

```html
<a href="EXP-RISK-PRR-2026-040_RevC12_ACTIVE.xlsx"
   download="Aseer_Regional_Museum_PRR_2026-07-25_1430.xlsx">
```

Pattern: `{Project}_{Register}_{YYYY-MM-DD}_{HHMM}.xlsx`
- Project = `Aseer_Regional_Museum`
- Register = `PRR` / `DDR` / `HSE` / `AVR`
- Date/time = snapshot generation timestamp

Server filename stays as `EXP-RISK-{code}-{seq}_Rev{rev}_ACTIVE.xlsx`.

Implementation in template.html:
```html
<a href="__XLSX_HREF__" download="__XLSX_DOWNLOAD__" ...>
```
Replace in build script: `html.replace("__XLSX_HREF__", server_name).replace("__XLSX_DOWNLOAD__", download_name)`.

## File Permissions

openpyxl on macOS creates files with `-rwx------` (700) — web servers can't read these. Always set 644:

```python
os.chmod(path, 0o644)
# or rsync with:
rsync --chmod=644 ...
# or chmod on server:
ssh server "chmod 644 /path/*.xlsx"
```

## Pitfalls

- **Auto-increment drift**: `build_risk.py` increments sequence on every run. The HTML is written with the new seq but if the XLSX creation fails silently, the HTML points to a non-existent file. Always verify HTTP 200 after deploy.
- **Two build systems, different filenames**: `build_risk.py` (web deploy) and `build_all_template_registers.py` (standalone snapshots) use different seq numbering. Web HTML references the build_risk.py seq. The standalone script uses a fixed seq (030). Don't mix them — use build_risk.py's output for the submittal folder.
- **rsync -az preserves 700 permissions**: Files in /tmp/ created by openpyxl have 700 perms. Use `--chmod=644` or chmod before rsync.
- **openpyxl save can silently fail** on complex merged-cell workbooks. Check the file size after save — if 0 bytes, the save failed. Try unmerging problematic cells before writing.
- **Dashboard formula regex must match exactly**: The pattern `(\$[A-Z]+\$6:\$[A-Z]+)\$\d+` assumes the format `$A$6:$A$52`. If the template has a different format (e.g. absolute column refs without $), the regex won't match and formulas won't update.
