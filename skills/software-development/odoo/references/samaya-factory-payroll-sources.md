# Samaya Factory Payroll — Data Sources & Permission Quirks

> Compiled 2026-09-04 from the factory-separation cost study. Use when computing
> factory/company labour cost, or when asked "basic vs package" for a worker group.

## Golden rule: Basic ≠ Package in Samaya Odoo

- The Odoo payroll **export** carries the **basic salary only**. The `الباكدج`
  (package) column is **empty string** in every export (`employees_full_details.csv`).
- The **only** source containing real package values is
  `DATA/workshop_employees_full_salary.csv` — but it covers **only 39 workshop
  workers**, NOT the print shop (المطبعة) nor the whole company.
- For the print shop (Printing Production / dept 49) there is **no package
  source**. The approved fallback is an **ESTIMATED package** = basic + housing 25%
  + transport 10% + 300 SAR flat. This is stored in `machine_census/print_staff.json`
  and `machine_census/PRINT_STAFF.md`, each row labeled `package_note=ESTIMATED`.

## Canonical payroll data files (in `samaya-workspace`)

| File | Content | Package? |
|---|---|---|
| `DATA/employees_detailed.csv` | Company-wide payroll export, **528 employees**, basic salary | ❌ no |
| `DATA/employees_full_details.csv` | 528 employees, basic + `الباكدج` col | ❌ col is empty |
| `DATA/employees_salary_workcenter.csv` | basic + cost/hour | ❌ no |
| `DATA/workshop_employees_full_salary.csv` | **39 workshop workers only** | ✅ real package |
| `DATA/company_employees.json` | Full-company DB built from detailed.csv (by odoo_id) | ❌ basic |
| `DATA/EMPLOYEES_MASTER.md` / `DATA/employees_unified.json` | Unified DB keyed by **biotime**, joins salary+violations+OT | basic |
| `reports/Payroll_Company_All.md` | Full-company payroll MD, 36 depts, 2,216,906 SAR/month | ❌ basic |
| `machine_census/print_staff.json` + `PRINT_STAFF.md` | Digital print shop (8 staff) | ✅ ESTIMATED |

## Factory labour split (agreed classification: عمالة ثابتة / مشرفين / إداريين)

- Classify by job-title substring. Match `supervisor|manager|coordinator` → مشرفين;
  `engineer|architecture|keeper` → إداريين; else عمالة ثابتة.
- **Watch out:** job titles carry stray spaces (e.g. `'Project  Manager '` with
  double space). Normalize with `.strip().lower()` before matching — naive exact
  match drops رؤوف (903), محمد عبد الكريم (981), etc.
- Factory = 4 depts: `hr.department` ids **18** (Manufacturing), **49** (Printing),
  **98** (Warehouse), **71** (Transportation). The Odoo export shows 64 in-factory
  employees under those 4 depts; the live `hr.employee` count was 85 because some
  workers physically at the factory sit under Eventech/Rawasin/Hoo depts.

## Odoo permission quirk (uid 151, sultan@samayainvest.com)

- `hr.employee` (incl. `job_title`, `department_id`, `active`) IS readable.
- `hr.contract` and `hr.payslip` (where the real package/net-gross wage lives)
  are **NOT readable** by uid 151 — need `Contracts/Administrator` /
  `Payroll/Officer` groups. If the user asks for real package values, either get
  HR to export the payroll, or request raised permission for this uid.
- `hr.attendance.overtime` exists but is **empty** (0 records) — OT is tracked
  manually from Raoof's monthly Excel files, not in Odoo. `hr.overtime` model does
  NOT exist.
- Overtime source-of-truth is `OT_SYSTEM/monthly/YYYY-MM.md`; the latest present is
  `2026-07.md`. Aug 2026 OT exists in OneDrive but was blocked by OneDrive deadlock.

## Pitfalls

- The unified employee DB is keyed by **biotime**, built by joining
  `employees.json` + `odoo_employees_biotime.csv` by **name** (Arabic then English),
  + violations by biotime, + OT by biotime. Employee filenames in
  `OT_SYSTEM/employees/` zero-pad the biotime (`0102.md` = biotime 102) — strip
  leading zeros when joining.
- New employees (e.g. محمد مصطفى كامل طه odoo 3639, نعيم انس odoo 3487) may have
  **no biotime** yet — they'll be missing from the unified DB until mapped.
- Rebuild generators:
  `python3 scripts/build_company_employees.py` (528 JSON),
  `python3 scripts/build_company_payroll_md.py` (payroll MD),
  `python3 scripts/gen_print_staff.py` (print shop from Odoo),
  `python3 scripts/build_employee_db.py` (unified biotime DB).
