# SQL Dump Analysis — sysleaders_samaya2

## Source
`/Volumes/MIcro/Work/Sysleaders/DataBase Backup/sysleaders_samaya2.sql.gz` (5.1 MB gzipped, 30.5 MB raw)
Dumped from MariaDB 10.6.27 on Linux (x86_64)

## Key Finding: NO DATA
This backup contains **table structures only** — CREATE TABLE statements with no INSERT data. All entity tables (app_entity_1 through app_entity_100+) exist as empty schemas. The actual data lives in `sysleaders_samaya` (not samaya2).

## Entity 28 (Tasks) — Column Structure
```
id              int(11) unsigned NOT NULL AUTO_INCREMENT
parent_id       int(11) unsigned DEFAULT 0       -- FK to project entity
parent_item_id  int(11) unsigned DEFAULT 0
linked_id       int(11) unsigned DEFAULT 0
date_added      bigint(20) NOT NULL DEFAULT 0    -- unix timestamp
date_updated    bigint(20) NOT NULL DEFAULT 0    -- unix timestamp
created_by      int(11) unsigned DEFAULT NULL
sort_order      int(11) DEFAULT 0
field_254       bigint(20) NOT NULL DEFAULT 0    -- Task name / Product Name
field_255       text NOT NULL                     -- Description
field_256       text NOT NULL                     -- Hours worked
field_257       text NOT NULL                     -- Labor rate
field_262       bigint(20) NOT NULL DEFAULT 0    -- Worker name / Assign to
field_263       bigint(20) NOT NULL DEFAULT 0    -- Date (unix timestamp)
field_264       float NOT NULL                    -- BOQ code / DWG No#
field_267       int(11) NOT NULL                  -- Status
field_381       varchar(1) NOT NULL               -- Priority
field_422       varchar(1) NOT NULL               -- Progress
field_516       varchar(1) NOT NULL               -- Due Date
field_526       varchar(1) NOT NULL               -- Link to Task
field_527       varchar(1) NOT NULL               -- Assign to (user)
field_538       text NOT NULL                     -- Category
field_951       varchar(1) NOT NULL               -- Remarks
field_969       int(11) NOT NULL                  -- Amount
field_970       int(11) NOT NULL                  -- ST.NO.
```

## Entity 28 Values (app_entity_28_values)
```
id          int(11) NOT NULL AUTO_INCREMENT
items_id    int(11) NOT NULL DEFAULT 0    -- FK to app_entity_28.id
fields_id   int(11) NOT NULL DEFAULT 0    -- FK to app_entities_configuration
value       text NOT NULL                  -- actual data
```

## Field Name Mapping
To find what field_254 etc. mean:
```sql
SELECT * FROM app_entities_configuration WHERE entities_id = 28;
```
This was NOT available in the samaya2 backup (no data). Must query live `sysleaders_samaya` database.

## What We Know from Web API
From the SysLeaders web API (report 646), entity 28 tasks have these visible columns:
- Product Name (field_254)
- DWG No# (field_264 — BOQ code)
- Priority (field_381)
- Status (field_267)
- Assign to (field_262 — worker name)
- Due Date (field_516)
- Progress (field_422)
- Link to Task (field_526)

## Labor Cost Calculation
Labor cost = hours × rate, calculated on-the-fly by SysLeaders. NOT stored in the database.
- field_256 = hours worked
- field_257 = labor rate
- field_969 = total cost (may be pre-calculated or 0)

## Next Steps to Get Timesheet Data
1. Get a backup of `sysleaders_samaya` (not samaya2) — this has the actual records
2. Or query live via phpMyAdmin: `SELECT * FROM app_entity_28 WHERE parent_id = 282` (Rateeb)
3. Join with `app_entity_28_values` for field values
4. Join with `app_entities_configuration` for field name mapping
5. Extract: worker name, date, hours, rate, BOQ code, status per row
