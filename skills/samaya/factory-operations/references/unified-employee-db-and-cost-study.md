# Unified Employee DB (keyed by biotime) + Factory Separation Cost Study

Built 2026-09-04 in `samaya-workspace`. Reusable for any "give me the factory's
monthly cost / headcount / who-is-who" question.

## The unified employee database

**Canonical key = رقم البصمة (biotime_code).** One record per employee merging 4 sources:

| Source | Path | What it contributes |
|--------|------|---------------------|
| Salaries | `OT_SYSTEM/data/employees.json` | basic_salary, total_package, job, dept, manager, hire_date |
| Biotime mapping | `OT_SYSTEM/data/odoo_employees_biotime.csv` | odoo_id ↔ biotime_code (the join key) |
| Violations | `VIOLATIONS/*.md` | per-biotime violation list (parse `رقم البصمة` + `كود المخالفة` + `تاريخ المخالفة`) |
| Overtime | `OT_SYSTEM/employees/*.md` | YTD hours/cost (EID = biotime, strip leading zeros: `0102` → `102`) |

**Build script:** `samaya-workspace/scripts/build_employee_db.py`
- Outputs `DATA/employees_unified.json` (dict keyed by biotime) + `DATA/EMPLOYEES_MASTER.md` (human table).
- Re-runnable; regenerate after any source changes.

**Pitfalls hit while building:**
- `employees.json` keys are INCONSISTENT — some are odoo_id, some are biotime. Match by **name** (Arabic then English), not by key.
- `employees.json` has ~31 entries with **empty department + empty name** (just a job like حداد/نجار/عامل) and salary 0 — these are workshop workers with no Odoo record. Don't count them as salaried.
- The **authoritative salary source is `DATA/employees_full_details.csv`** (the Odoo export the user downloaded — 545 employees total, factory 64). Its `الباكدج` (package) column is **empty**; only `الراتب الأساسي` (basic salary) is populated. So report basic salary, and note package is higher (from evaluation files).
- `FACTORY_TEAM_RECORD.md` goes stale fast — regenerate from live Odoo (depts 18 Manufacturing, 49 Printing, 98 Warehouse, 71 Transportation = 85 employees as of 2026-09-04). The old file said 49.
- Two new employees may have **no biotime** (e.g. odoo 3639 محمد مصطفى كامل طه, 3487 نعيم انس) — they're in Odoo but not yet fingerprinted.

## Factory separation monthly cost study

To build the "فصل المصنع" cost baseline (what it costs to run the factory per month):

| Line item | Source | How |
|-----------|--------|-----|
| Salaries | `DATA/employees_full_details.csv` | sum `الراتب الأساسي` for factory depts (Manufacturing/Warehouse/Transportation/Printing) |
| Materials | Odoo `purchase.order` project_id=244 | classify by type via `factory_po_filter.classify_po_type()` |
| External labour | Odoo POs | vendor name contains Outsource/Mostafa mazen/عمالة |
| Services | Odoo POs | type=service |
| Utilities/maintenance | Odoo POs | keyword search (كهرباء/ماء/صيانة/تكييف) |

**Data gaps to flag (not in Odoo):** electricity/water/gas bills, factory rent,
outside-Riyadh worker salaries, shared-services cost allocation (HR/accounting/
procurement), asset depreciation. These are paid by Samaya parent directly, not
as factory POs — need a separate source.

**Result (2026-09-04):** ~397K SAR/month estimated — salaries 162K + materials
149K + external labour 55K + services 28K + utilities 2K.

## OneDrive deadlock on the OT folder

The `اوفر تايم` folder under `Orders/2026/0000 اداريات/` files (e.g.
`06 تقرير الأجر الإضافي - أغسطس 2026.xlsx`, `00 OT_INDEX.md`) hit persistent
`Resource deadlock avoided` (Errno 11) — even `ditto`, `cp`, and byte-read all
failed. `os.stat` works but `open()` fails. This is the known OneDrive files-on-
demand lock. Fix: quit OneDrive, wait ~30s, retry (per memory). The OT data for
Aug 2026 exists there but was not readable this session.
