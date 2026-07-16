---
name: sysleaders-api
description: Extract POs, tasks, and labor data from the SysLeaders.com/samaya project management system via curl + session-cookie API. Use when you need factory work reports, PO details, labor costing from SysLeaders.
triggers:
  - "SysLeaders"
  - "sysleaders.com/samaya"
  - "pull POs from sysleaders"
  - "extract labor costs from sysleaders"
  - "factory work report from sysleaders"
---

# SysLeaders API Data Extraction

Extract purchasing orders, tasks, labor costs from `sysleaders.com/samaya` (Samaya Investment's project management system). Data is behind a PHP session login; the "API" is standard `module/action` endpoints that return HTML. No REST/JSON API exists — parse HTML responses.

## Authentication

Two-step flow with CSRF token:

```bash
# Step 1: GET login page, extract CSRF token
curl -s -c /tmp/sysleaders_cookies.txt \
  'https://www.sysleaders.com/samaya/index.php?module=users/login' \
  | grep -o 'form_session_token.*value="[^"]*"'

# Step 2: POST login with token
TOKEN="<extracted_token>"
curl -s -L -c /tmp/sysleaders_cookies.txt -b /tmp/sysleaders_cookies.txt \
  -X POST \
  -d "username=sultan&password=1batagoniaA&form_session_token=${TOKEN}" \
  'https://www.sysleaders.com/samaya/index.php?module=users/login&action=login'
```

Credentials (in env, never hardcode in prompts): user `sultan`, pass `1batagoniaA`.

Session cookie is stored in `/tmp/sysleaders_cookies.txt`. Reuse across calls with `-b` / `-c` flags.

After login, extract the new token from any page: `grep -o 'token=[A-Za-z0-9]\{10\}'`.

## Project Discovery

Projects have two IDs:
- **entity_id**: Numeric ID used in select dropdowns (e.g., Rateeb = 282)
- **path**: URL path for module calls (e.g., Rateeb = 49)

To find a project's IDs, navigate the browser to Projects → search for the project name → inspect the select option values or links.

Known mappings for Sister Companies:

| Code | Name | entity_id | path | JN |
|------|------|-----------|------|-----|
| 10 | Rateeb Store | 282 | 49 | JN-Rateeb-Shop |

## PO Extraction

Use the listing API endpoint with the reports system:

```bash
# Fetch POs for a project (reports_id=780 for POs)
curl -s -L -b /tmp/sysleaders_cookies.txt \
  -H "X-Requested-With: XMLHttpRequest" \
  -H "User-Agent: Mozilla/5.0" \
  -X POST \
  -d "reports_id=780&reports_entities_id=<path>&path=<path>&page=1&redirect_to=report_780&listing_container=entity_items_listing780_<path>" \
  'https://www.sysleaders.com/samaya/index.php?module=items/listing'
```

Response is HTML `<tr>` rows. Parse with regex:
- PO numbers: `PO(\d+)` 
- PO paths: `path=(\d+-\d+)` (filter those starting with project path)
- Costs: `(\d+\.?\d*)SAR`

## PO Detail

```bash
# Get PO info + items
curl -s -L -b /tmp/sysleaders_cookies.txt \
  'https://www.sysleaders.com/samaya/index.php?module=items/info&path=<path>-<id>'
```

The info page contains two tables:
1. **Info table**: `<tr><td>key</td><td>value</td></tr>` — fields: ID, Status, Estimated Cost, Created By, Approved By, etc.
2. **Order Items**: Loaded via AJAX subentity — NOT in the main page. May require separate listing call with subentity path.

## Labor Costs

Labor costs are **calculated on-the-fly** (rate × hours), NOT stored in the database.

### Database Schema (full mapping)
The SysLeaders system uses Rukovoditel CRM with an EAV (Entity-Attribute-Value) pattern. Each entity has a main table (`app_entity_N`) and a values table (`app_entity_N_values`). Relationships are stored in `app_related_items_X_Y` tables.

Key entities for Sister Companies costing:

| Entity | Table | Purpose |
|--------|-------|---------|
| 21 | `app_entity_21` | Projects (Rateeb = id 282) |
| 22 | `app_entity_22` | Tasks/BOQ Items (parent_id → project) |
| 27 | `app_entity_27` | Technicians/Workers (field_241=name) |
| 28 | `app_entity_28` | Labor Time Records (field_254=date, field_255=worker_id, field_256=hours, field_257=rate) |
| 49 | `app_entity_49` | Purchase Orders (field_622=PO#, field_626=description) |
| 52 | `app_entity_52` | Invoices |
| 53 | `app_entity_53` | Expenses |
| 54 | `app_entity_54` | Fleet Requests |
| 63 | `app_entity_63` | Raw Materials |
| 72 | `app_entity_72` | Delivery Notes |

Relationship tables: `app_related_items_21_28` (Project↔Labor), `app_related_items_22_28` (Task↔Labor), `app_related_items_27_28` (Worker↔Labor).

Full schema with field mappings is in `sister-companies-costing` skill at `references/sysleaders-database-schema.md`.

### Browser Extraction Method (most reliable)
When cPanel/phpMyAdmin/API are all blocked, use the browser to navigate the SysLeaders web app:
1. Login at `https://www.sysleaders.com/samaya/index.php?module=users/login`
2. Navigate to project: `index.php?module=items/info&path=21-{entity_id}`
3. The project page shows ALL subentities (Tasks, POs, Fleet, Delivery Notes, Labor) in a single scrollable view
4. Use `browser_console` with `expression` to extract table data via JavaScript
5. Parse the extracted JSON to get worker names, dates, hours, rates, BOQ codes, PO numbers

### Backup File Analysis
ALL backup files examined are structure-only (CREATE TABLE, no data):
- `sysleaders_samaya.sql` — no entity data
- `sysleaders_samaya2.sql` — no entity data
- `backup-7.15.2026_23-42-47_sysleaders.tar.gz` — same structure-only SQL files
- `sysleaders_samaya2 (1).sql` — has entity_28 data but from 2020-2021 (old factory records, not Rateeb)

The live data is ONLY on the server. A proper backup of `sysleaders_samaya` (the one with actual records) is needed.

**Local backup folder:** `/Volumes/MIcro/Work/Sysleaders/Database backup_claude/` — contains full API dump (5.9MB JSON), 211 projects, 870 POs, 4422 cost records, Rateeb live data, schema reference, and Sister Companies project list. See `README.json` in that folder for the index.

## Pitfalls

1. **Python subprocess.run() truncates curl output** when using `capture_output=True`. Always use `-o <tmpfile>` and read the file.
2. **macOS grep lacks `-P`** (Perl regex). Use `-E` (extended) or Python's `re` module.
3. **CSRF token in HTML line-split**: The token `value="XXX"` may be on a different line from `name="form_session_token"`. Use regex `form_session_token.*?value="([^"]+)"` (non-greedy across lines).
4. **Session expires**: The PHP session times out. Always re-login if you get redirected to `/users/login`.
5. **Entity path ≠ project ID**: The `path` in URLs is an internal entity ID, not the JN or visible project number. Discover it from the browser or the PO data.
6. **Order Items are AJAX-loaded**: The items table on PO detail pages loads via JavaScript after page render. curl alone may not capture them; use the listing API with the correct subentity path.

## Script

See `scripts/extract.py` for the full Python implementation (login + PO extraction + parsing).

## Reference

- `references/project-registry.md` — Known project entity_id/path mappings and API endpoint catalog.
