## Whole-company payroll DB (for "كم راتب موظفي X للشركة كلها" questions)

A full-company roster generator was added so any "salaries of a department / the
whole company" query can be answered from one canonical file:

| Artifact | Path | Contents |
|----------|------|----------|
| Generator | `samaya-workspace/scripts/build_company_employees.py` | Reads `DATA/employees_detailed.csv`, writes JSON, prints summaries |
| Output | `DATA/company_employees.json` | **528 employees**, keyed by odoo_id |

**Rebuild:** `python3 scripts/build_company_employees.py`

Each record carries: `odoo_id`, `name_ar`, `job`, `department`, `base_salary`,
`hire_date`, `manager`, `contract_state`, `category` (عمالة ثابتة/مشرفين/إداريين),
`is_factory` (True if `department` contains Manufacturing/Warehouse/Transportation/Printing).

**Company-wide numbers (2026-09-04):** 528 employees, total payroll 2,216,906 SAR/mo
basic — factory 64 = 162,233, other 464 = 2,054,673.

**Confirm the salary basis before reporting a department's total.** The payroll
column is `الراتب الأساسي` (BASIC) — the `الباكدج` (package) column is empty in
both `employees_detailed.csv` and `employees_full_details.csv`. Only the workshop
evaluation file (`workshop_employees_full_salary.csv`, 39 workers) has real package
numbers (~121K/mo). So a factory/department monthly salary figure is a **basic-salary
minimum**, always below the true cost. State this caveat instead of implying the
figure is full payroll.
