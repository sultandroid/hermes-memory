# SysLeaders Database Access

## cPanel Login
- URL: `https://www.sysleaders.com:2083/`
- Username: `sysleaders`
- Password: `1batagoniaA`
- SSH port 22: CLOSED
- MySQL remote port 3306: CLOSED
- Only localhost access via phpMyAdmin

## phpMyAdmin
Navigate: cPanel Dashboard → Databases → phpMyAdmin
URL pattern: `https://www.sysleaders.com:2083/cpsess{token}/3rdparty/phpMyAdmin/index.php`

## Database: `sysleaders_samaya`
Main application database — **has actual data**. Entity-based schema (EAV pattern).

## Database: `sysleaders_samaya2`
**Structure only — NO data.** This database contains only table schemas (CREATE TABLE statements), no INSERT data. A backup of this DB is useless for extracting records. Always target `sysleaders_samaya` for data queries.

## Backup Verification (CRITICAL)
**BOTH `sysleaders_samaya.sql` AND `sysleaders_samaya2.sql` backups are structure-only.** They have CREATE TABLE definitions but ZERO rows in entity tables (app_entity_21, app_entity_28, etc. all have 0 INSERT statements). The live data is ONLY on the server. A proper backup of `sysleaders_samaya` (the one with actual records) is needed for offline analysis.

## phpMyAdmin Error: "Disk quota exceeded"
The server `/home/sysleaders/tmp` is full. This blocks:
- Opening phpMyAdmin (session_start fails)
- Running SQL queries
- Any database operations that need temp space

Resolution: Free disk space on the server (clear temp files, old backups, or upgrade hosting plan). Until resolved, use the SysLeaders web API as fallback.

## cPanel Session Management
- **Session expires after ~5-10 minutes** of inactivity
- **Each login gets a new `cpsess{token}`** — the URL changes every time
- **Always check `window.location.href`** after login to get the current session token
- **cPanel API calls** need the current `cpsess{token}` in the URL path
- **phpMyAdmin direct URL** pattern: `https://www.sysleaders.com:2083/cpsess{token}/3rdparty/phpMyAdmin/index.php?route=/table/browse&db=sysleaders_samaya&table=app_entity_28`
- **SQL query URL** pattern: `https://www.sysleaders.com:2083/cpsess{token}/3rdparty/phpMyAdmin/index.php?route=/table/sql&db=sysleaders_samaya&table=app_entity_28&sql_query=SELECT+*+FROM+app_entity_28+LIMIT+10`
- **When session expires**, the page redirects to the cPanel login form — re-enter credentials and extract the new `cpsess{token}` from the URL

### Key Tables
| Table | Content | Size |
|-------|---------|------|
| `app_entity_28` | Tasks (largest — 2MB, ~43 rows) | 2.0 MiB |
| `app_entity_28_values` | Task field values | 4.1 MiB |
| `app_entity_49` | Items/POs (path=49 = Rateeb) | 144 KiB |
| `app_entity_49_values` | Item field values | 80 KiB |
| `app_entity_21` | Projects/entities | 128 KiB |
| `app_entity_21_values` | Project field values | 80 KiB |
| `app_entities` | Entity definitions | 16.5 MiB |
| `app_comments` | Comments/notes | 144 KiB |
| `app_attachments` | File attachments | 1.6 MiB |

### Entity-Value Pattern
The app uses EAV: `app_entity_N` has `id`, `parent_id`, `date_added`, `created_by` etc.
`app_entity_N_values` has `items_id` (FK to entity), `fields_id` (FK to field def), `value` (actual data).

To find field definitions: `app_entities_configuration` table maps entity types to field IDs.

### Task Table (app_entity_28) — Field Mapping
Columns discovered from phpMyAdmin structure view:
- `id` (PK, auto_increment)
- `parent_id` (FK to project entity)
- `parent_item_id`
- `linked_id`
- `date_added` (unix timestamp)
- `date_updated` (unix timestamp)
- `created_by`
- `sort_order`
- `field_254` — Task name / Product Name
- `field_255` — Description
- `field_256` — Hours worked
- `field_257` — Labor rate
- `field_262` — Worker name / Assign to
- `field_263` — Date
- `field_264` — BOQ code / DWG No#
- `field_267` — Status
- `field_381` — Priority
- `field_422` — Progress
- `field_516` — Due Date
- `field_526` — Link to Task
- `field_527` — Assign to (user)
- `field_538` — Category
- `field_951` — Remarks
- `field_969` — Amount
- `field_970` — ST.NO.

### Task Values Table (app_entity_28_values)
Columns: `id`, `items_id` (FK to app_entity_28.id), `fields_id` (FK to app_entities_configuration), `value` (actual data)

### Field Name Mapping
To find what field_254, field_255 etc. actually mean:
```sql
SELECT * FROM app_entities_configuration WHERE entities_id = 28;
```
This returns the field_id → human-readable name mapping for entity 28 (tasks).

### Query Pattern for Labor Data
```sql
-- Get task records for a specific project
SELECT e.id, e.date_added, e.field_254, e.field_255, e.field_256, e.field_257
FROM app_entity_28 e
WHERE e.parent_id = 282  -- Rateeb project entity ID
ORDER BY e.id;

-- Get field values for a specific task
SELECT v.fields_id, v.value
FROM app_entity_28_values v
WHERE v.items_id = 1  -- task ID
ORDER BY v.fields_id;
```

### Project Entity IDs
| Project | Entity ID | Path |
|---------|-----------|------|
| JN-Rateeb-Shop (متجر التمور) | 282 | 49 |
| JN-Qouran Musuem VIP Area | 176 | — |
| Khair Al-Khalq Exhibition | 186 | — |

## cPanel API
Base: `https://www.sysleaders.com:2083/cpsess{token}/execute/`

| Endpoint | Purpose |
|----------|---------|
| `Mysql/list_databases` | List databases |
| `Mysql/get_privileges_on_database?db=X&user=Y` | Check user privileges |
| `Mysql/get_restrictions` | Get naming restrictions |

No `execute_sql` function available in the Mysql module — must use phpMyAdmin for queries.

## Querying Labor Data
To populate the 1b_Labor_Timesheet sheet:
1. Open phpMyAdmin → `sysleaders_samaya` → `app_entity_28`
2. Browse table to see column structure
3. Filter by project entity ID (282 for Rateeb)
4. Join with `app_entity_28_values` for field values
5. Extract: worker name, date, hours, rate, BOQ code, status
6. Labor cost = hours × rate (calculated on-the-fly, not stored)

## SysLeaders Web API (alternative to DB)
When DB access is unavailable, use the web API:
- Login: `POST module=users/login&action=login` with CSRF token
- Tasks listing: `POST module=items/listing` with `reports_id=646&reports_entities_id=49&path=49`
- PO listing: `POST module=items/listing` with `reports_id=787&reports_entities_id=49&path=49`
- Task detail: `GET module=items/info&path=49-{task_id}`
- PO detail: `GET module=items/info&path=49-{po_id}`
- The web API returns HTML, not JSON — parse with regex
- Session cookie stored at `/tmp/sysleaders_cookies.txt`
