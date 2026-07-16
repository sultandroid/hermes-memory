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

Required data:
- **Labor rates**: From Operation Management → Work Centers (`module=items/work_centers`)
- **Hours worked**: From project Tasks (`module=items/tasks` with project path)

The calculation: `labor_cost = SUM(hours_per_task × rate_per_work_center)`

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
