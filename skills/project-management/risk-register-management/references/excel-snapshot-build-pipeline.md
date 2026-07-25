# Excel Risk Register Snapshot Build Pipeline

## Overview

Generates downloadable `.xlsx` snapshot files for all four risk registers (PRR, DDR, HSE, AVR) from their JSON data sources, using a manually-formatted Excel template as the starting point.

## Key files

| Path | Purpose |
|------|---------|
| `/tmp/build_all_template_registers.py` | Master build script — copies template, populates data, updates formulas |
| `webapp/templates/risk_snapshot_template.xlsx` | User-formatted template (includes Dashboard layout, merged cells, chart, images) |
| `risks.json` | PRR risk data |
| `webapp/ddr/risks_ddr.json` | DDR risk data |
| `webapp/av/risks_av.json` | AVR risk data |

## Template layout (user's approved format)

### Risk Register sheet

| Col | Content | Width |
|-----|---------|-------|
| A | ID | 12 |
| B | CAT (category code) | 9 |
| C | RISK (title) | 38 |
| D | CAUSE | 32 |
| E | EVENT | default |
| F | CONSEQUENCE | default |
| G | P (probability) | 4 |
| H | S (severity) | default |
| I | SCORE (`=G*H` formula) | 6 |
| J | RATING | 10 |
| K | STATUS | 11 |
| L | OWNER | 18 |
| M | TARGET CLOSE | 13 |
| N | RESPONSE / MITIGATION | 38 |
| O | EVIDENCE | 30 |

- Row 5: Column headers
- Row 6+: Data rows
- Rows 1-3: Merged header area (A1:O1, A2:O2, A3:O3)
- Last row: Footer merged A{last}:O{last}

### Dashboard sheet

- Rows 1-3: Header (merged A1:N1, A2:N2, A3:N3)
- Rows 4-5: Live register info + URL
- Rows 6-7: KPI cards — COUNTA(A6:A{last}), COUNTIF(J6:J{last},"Critical"/"High"/"Medium"/"Low"), COUNTIF(K6:K{last},"Open")
- Rows 10-15: Risk matrix (COUNTIFS on G=Prob, H=Sev), By Rating (COUNTIF on J), Top Owners (COUNTIF on L)
- Rows 16-18: By Status (COUNTIF on K)
- Rows 20-36: Exposure by Category (COUNTIF on B) — all categories, formula rows
- Row 39: Footer (merged A39:N39)

### Chart

- 1 Bar chart, title "Risks by Category"
- Data reference: `Dashboard!$D$20:$D$36` (Count column)
- Category labels: `Dashboard!$B$20:$B$36`

## Build process

```python
shutil.copy2(TEMPLATE, OUT/filename)
w = load_workbook(OUT/filename)
last = 5 + len(risks)  # row 5 = headers, data starts row 6

# 1. Update header across all sheets
for s in w.worksheets:
    s['A1'] = f'ASEER REGIONAL MUSEUM  --  {title}'
    s['A2'] = f'Doc No. EXP-RISK-{name}-2026   Contract: {contract}   Rev {rev}   ACTIVE'
    s['A3'] = f'Snapshot Date: {date}   Source: {live}'

# 2. Update ALL Dashboard formulas with correct last row
# Pattern: $col$6:$col${NUM} -> $col$6:$col${last}
for row in range(1, dash.max_row+1):
    for col in range(1, dash.max_column+1):
        c = dash.cell(row, col)
        if c.value and isinstance(c.value, str) and 'Risk Register' in c.value:
            c.value = re.sub(r'(\$[A-Z]+\$6:\$[A-Z]+)\$\d+',
                             lambda m: m.group(1)+'$'+str(last), c.value)

# 3. Clear old data (row 6+), write new data
for i, risk in enumerate(risks, 6):
    rr.cell(i,1) = risk['id']
    rr.cell(i,2) = risk['category']
    # ... all 15 columns
    rr.cell(i,9) = f'=G{i}*H{i}'  # SCORE formula

# 4. Action Plan sheet
ap.cell(i,1) = risk['id']
ap.cell(i,2) = risk['category']
ap.cell(i,3) = risk['rating']
ap.cell(i,4) = response_action
ap.cell(i,5) = owner
ap.cell(i,6) = target_close
ap.cell(i,7) = status
```

## Pitfalls

### Template-based approach

- **Template IS the source of truth** for formatting. The build script only populates data and updates formula last-row references. Do NOT set cell styles, column widths, or chart properties in the script — those come from the template.
- **When the user provides a reformatted file**, replace the template and verify the build still works. Column layout changes require updating the build script column mapping.
- **Always check chart references**: after updating the template, verify chart series references still point to correct Dashboard cells. The bar chart uses `Dashboard!$D$20:$D$36` / `Dashboard!$B$20:$B$36`.

### Data range

- Data always starts at row 6 (row 5 = column headers).
- Last row = 5 + risk count. All Dashboard formulas reference `$col$6:$col${last}`.
- The `setv()` helper skips `MergedCell` objects to avoid errors when clearing old data near merged areas.

### Formula updates

- Dashboard formulas reference `'Risk Register'!$col$6:$col${last}` in a COUNTIF/COUNTIFS/COUNTA pattern.
- Regex `(\$[A-Z]+\$6:\$[A-Z]+)\$\d+` captures the column range and replaces the last row number.
- This handles ALL Dashboard formulas in one pass — no need to hardcode specific cells.

### Template replacement workflow

1. User provides reformatted .xlsx
2. Save as `webapp/templates/risk_snapshot_template.xlsx`
3. Check if column layout changed — update column headers and data writes in build script
4. Check if Dashboard formula column refs changed — update re.sub patterns
5. Clean build: delete `/tmp/all_register_exports/*.xlsx` and rebuild
6. Deploy all four registers
7. Verify: download each register, check data rows, check KPI counts, check chart

## Deployment

```bash
python3 /tmp/build_all_template_registers.py

rsync -az -e 'ssh -p 65002 ...' /tmp/all_register_exports/EXP-RISK-PRR-... \\
  user@samaya-factory.com:.../build/aseer/registers/Risk/
rsync -az -e 'ssh -p 65002 ...' /tmp/all_register_exports/EXP-RISK-DDR-... \\
  user@.../DDR/
rsync -az -e 'ssh -p 65002 ...' /tmp/all_register_exports/EXP-RISK-HSE-... \\
  user@.../HSE/
rsync -az -e 'ssh -p 65002 ...' /tmp/all_register_exports/EXP-RISK-AVR-... \\
  user@.../AV/
```

Deploy URLs:
- PRR: `https://samaya-factory.com/aseer/registers/Risk/`
- DDR: `https://samaya-factory.com/aseer/registers/Risk/DDR/`
- HSE: `https://samaya-factory.com/aseer/registers/Risk/HSE/`
- AVR: `https://samaya-factory.com/aseer/registers/Risk/AV/`

### 5. HSE Data Source (Remote HTML)

HSE risk data is NOT stored in a local JSON file. It's embedded as inline `const RISK = {...};` in the server's `index.html`. The build script fetches data from the live page URL at runtime via `remote()`.

To modify HSE ratings or data:
1. Download the HTML from the live HSE page URL
2. Parse the inline JSON, modify the data
3. Re-inject the JSON into the HTML (use `lambda` in `re.sub` to avoid `\u` escape conflicts)
4. Upload the fixed HTML to the server
5. Rebuild Excel snapshots — the build script fetches from the now-corrected live page

See `references/scoring-system-alignment.md` for the exact fix pattern.

### 6. File Permissions After Deployment

`rsync -az` (archive mode) preserves source permissions. Source `.xlsx` files in `/tmp/` have `-rwx------` (700) — the web server process cannot read them.

**Fix**: Either add `--chmod=644` to rsync, or run post-deploy:
```bash
ssh -p 65002 user@server "chmod 644 /path/to/registers/*/EXP-RISK-*.xlsx"
```

**Verify**: `ls -la *.xlsx` on the server should show `-rw-r--r--`.

### 7. Column Header Alignment (PxS vs PxI)

If the RMP document uses "Impact" (I) instead of "Severity" (S) in criteria tables, the register column header must match:

- Risk Register Col H: `S` → `I`
- Dashboard labels already say "Impact" — no change

This is cosmetic — formula references use column letters, not header text. Update the template file and rebuild.

### 8. Per-Register Rating Bands

The simple `rate()` function below returns correct results for PRR/AVR (4x4 scale, max 16) but gives FALSE positives for DDR (max 20) and HSE (5x5, max 25):

| Register | Wrong? | Correct Band |
|----------|--------|-------------|
| DDR score=20 | rate() says ≥12=Critical → matches (correct) | 12-20 Critical |
| HSE score=16 | rate() says ≥12=Critical → correct per 5x5, but rate() doesn't verify 5x5 band boundaries | 16-25 Critical |
| HSE score=15 | rate() says ≥12=Critical → WRONG per 5x5: 10-15=High | 10-15 High |

See `references/scoring-system-alignment.md` for the per-register band table and correct validation script.

## HTML download filename

The `download` attribute on the `<a>` tag controls the browser's save-as filename.
Server file stays as `EXP-RISK-PRR-2026-{seq}_RevC{rev}_ACTIVE.xlsx`.
Download file = `Aseer_Regional_Museum_{REG}_{date}_{time}.xlsx`.
