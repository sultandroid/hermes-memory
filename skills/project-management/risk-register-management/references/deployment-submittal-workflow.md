# Risk Register Deployment & CG Submittal Workflow

## Excel File Deployment

### Template-Based Build Pipeline
1. Template lives at `webapp/templates/risk_snapshot_template.xlsx`
2. Build script: `/tmp/build_all_template_registers.py`
3. Generates 4 xlsx files to `/tmp/all_register_exports/`
4. Deploy via rsync to `samaya-factory.com`

### Template Preservation (User-Formatted)
When user downloads a snapshot, reformats it, and returns it:
1. Copy user's file over the template:
   `cp user_file.xlsx webapp/templates/risk_snapshot_template.xlsx`
2. Compare column layout: headers row, data start row, merged cells, formula references
3. Rewrite `build_all_template_registers.py` to match:
   - Update `data_row = 5` (headers) / `data_start = 6` (first data)
   - Update column letter mappings for each JSON field
   - Update Dashboard formula references (RATING=J, STATUS=K, OWNER=L, CAT=B, P=G, S=H)
   - Verify chart data ranges still valid
4. Test: run build script, verify all 4 xlsx files

### File Permission Fix
openpyxl on macOS writes xlsx as `-rwx------` (700). Web server returns 403/404.
**Fix**: `os.chmod(path, 0o644)` after every `Workbook.save()` before rsync.

### No Python on shared hosting server
Hostinger (samaya-factory.com) has no Python. To fix inline JSON on static HTML pages:
1. Download the HTML locally: `curl -s URL -o /tmp/page.html`
2. Fix locally with Python (openpyxl, json, re)
3. Rsync back to server
Never attempt python3/sed-based JSON fixes on the server. Use sed only for
simple string replacements (e.g., download filenames).

### Download Filename Fix
- `download` attribute: user-friendly name (e.g. `Aseer_Regional_Museum_PRR_20260725_1541.xlsx`)
- Use two placeholders in HTML templates: `__XLSX_HREF__` and `__XLSX_DOWNLOAD__`
- For DDR/HSE static pages (separate pipeline), fix via sed on the server:
  ### Download Filename Fix
  - `href` attribute: server filename (e.g. `EXP-RISK-PRR-2026-040_RevC12_ACTIVE.xlsx`)
  - `download` attribute: user-friendly name (e.g. `Aseer_Regional_Museum_PRR_20260725_1541.xlsx`)
  - Use two placeholders in HTML templates: `__XLSX_HREF__` and `__XLSX_DOWNLOAD__`
  - For DDR/HSE static pages (separate pipeline), fix via sed on the server:

  ## Web Server Structure

```
registers/Risk/
  index.html (PRR page)
  EXP-RISK-PRR-2026-040_RevC12_ACTIVE.xlsx
  DDR/index.html (static, separate pipeline)
  HSE/index.html (static, separate pipeline)
  AV/index.html (built by av/build_av.py)
```

- PRR: built by `build_risk.py` from `webapp/` — auto-increments sequence number
- AVR: built by `av/build_av.py` from `webapp/av/` — reads PRR page as template, patches values
- DDR/HSE: static files from separate pipeline — patch directly on server

## CG Submittal Prep

### Folder Cleanup
- Remove all `.md` files from the submittal folder
- Keep `00_Legacy_Archive/` with historical versions
- Download latest snapshots from live server, NOT from local build
  (server has the most recent auto-incremented version)
- Standard naming: `EXP-RISK-{PRR|DDR|HSE|AVR}-{seq}_Rev{rev}_ACTIVE.xlsx`

### CRS-to-Register Cross-Verification
1. Open the CRS xlsx file
2. Extract CG comments that reference specific risks
3. Search PRR/DDR/HSE/AVR registers by keyword for each referenced risk factor
4. When mapping RMP Section 2 (Project Risk Profile), check each:
   - Risk factor name → register ID match
   - Severity/rating alignment
   - If missing, add a new risk entry to the JSON data
5. CRS Comment 5 example: "Middle East Shipping Disruption" → PRR-PRC-06
