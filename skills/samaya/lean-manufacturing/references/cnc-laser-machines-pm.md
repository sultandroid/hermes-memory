# Samaya Factory — CNC/Laser Machines & Odoo PM Data

Verified 2026-08-08 via XML-RPC to `samayainv.odoo.com` (credentials `~/.config/samaya/odoo.env`).

## Machine register (maintenance.equipment, category CNC id=4)

Workcenter: **CNC/Laser** (mrp.workcenter id=13, code `FCNC`, costs_hour=100, company Samaya Factory).

| id | Name | Model | Serial | Since |
|----|------|-------|--------|-------|
| 290 | CNC ROUTER | Ventire 313 Lbm5311 | 201150376 | 2013-01-01 |
| 291 | Co2 Laser Cut machine | 1325L | 240104L | 2024-05-29 |
| 292 | Fiber Laser Cutting machine | SF 3015G | 202107050 | 2021-05-29 |
| 329 | Nesting CNC JIYU | 25825 | — | 2025-09-21 |
| 338 | DUST COLLECTOR 7.5KW | 7.5KW | — | 2026-01-20 |
| 339 | Automatic Swing Head Gear Grinding | A.TOP | — | 2025-09-11 |
| 340 | Saw Blade Grinding MF1107 | MF1107 | — | 2025-09-11 |
| 341 | Saw Blade Sharpening Machine | A.TOP | — | 2025-09-11 |

All 8 machines: `technician_user_id=False`, `maintenance_team_id=False`, `cost=0`. **Owner for PM = Moin El-Din** (maintenance supervisor + CNC operator) — assign if requested.

## Odoo 18 gotchas hit while pulling this

- **`hr.employee.job_title` is the iqama/residency title, NOT the real role.** Moin El-Din (id 2760) shows "Carpenter" but is maintenance supervisor + CNC operator. Confirm real roles with the user.
- **`hr.employee.identification_id` requires group `Employees / Officer: Manage all employees`** — user 151 (Sultan) cannot read it → field-access Fault 4.
- **`mrp.workcenter.capacity` does NOT exist** in Odoo 18 → "Invalid field" ValueError. Use `name, code, costs_hour, time_efficiency, company_id`.
- **`maintenance.request.date_deadline` does NOT exist** → "Invalid field". Use `schedule_date` / `date`.
- All `maintenance.equipment` CNC machines sit under `category_id=4` ('CNC'); laser machines are tagged CNC category too (they're not a separate category).

## PM checklist key checks (by machine type — do NOT flatten)

- **CNC Router / Nesting:** chiller water level/temp/leaks, belts tension (5–10mm deflection)/cracks/alignment, spindle sounds/heat/collet, rails/ball screws lubrication, tools/bits wear.
- **CO2 Laser:** chiller water (must be distilled to prevent algae/rust), **focus lens + mirrors** clean/no-cracks (clean with cotton + isopropyl, never touch surface), assist gas, exhaust/filters, nozzle.
- **Fiber Laser:** chiller water (cools the expensive laser source), **focus lens + sacrificial protective window** (window replaced more often than lens), N2/O2 assist gas, nozzle, auto-focus sensor, cutting-table slats.
- **Support:** dust collector suction/filters/belts/fan; grinding/sharpening machines oil, grinding-wheel condition, belts, safety.

## Where the checklists live
`samaya-profile/03_Workshop/lean/04_preventive_maintenance/` — `cnc_router_checklist.md`, `co2_laser_checklist.md`, `fiber_laser_checklist.md`, `support_equipment_checklist.md`, `pm_log.md` (weekly log + spare-parts replacement log + monthly summary).
