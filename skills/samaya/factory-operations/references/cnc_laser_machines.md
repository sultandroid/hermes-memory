# Samaya Factory — CNC/Laser Machines (from Odoo)

All under `maintenance.equipment` category **CNC (id 4)**, workcenter **CNC/Laser (id 13, code FCNC, 100 SAR/hr)**. All currently have `technician_user_id=False` (unassigned) — Moin El-Din (maintenance supervisor + CNC operator) is the natural PM owner.

| # | Machine | Model | Serial | Since | Type |
|---|---------|-------|--------|-------|------|
| 1 | CNC ROUTER | Ventire 313 Lbm5311 | 201150376 | 2013-01-01 | Router |
| 2 | Co2 Laser Cut | 1325L | 240104L | 2024-05-29 | Laser |
| 3 | Fiber Laser Cutting | SF 3015G | 202107050 | 2021-05-29 | Laser |
| 4 | Nesting CNC JIYU | 25825 | — | 2025-09-21 | Nesting |
| 5 | Dust Collector 7.5KW | 7.5KW | — | 2026-01-20 | Support |
| 6 | Swing Head Gear Grinding | A.TOP | — | 2025-09-11 | Grinding |
| 7 | Saw Blade Grinding MF1107 | MF1107 | — | 2025-09-11 | Grinding |
| 8 | Saw Blade Sharpening | A.TOP | — | 2025-09-11 | Sharpening |

**Odoo gotchas:**
- `mrp.workcenter` has NO `capacity` field (throws ValueError) — use `costs_hour` + `time_efficiency`.
- `maintenance.request` has NO `date_deadline` field — use `schedule_date`.
- Query equipment by `category_id=4` (CNC) captures both CNC and Laser — Laser machines are grouped under CNC, not a separate category.
- Reading `hr.employee.identification_id` requires "Officer: Manage all employees" rights (fails as user 151). Drop it if not needed.
- `mrp.production` uses `date_start`/`date_finished` (NOT `date_planned_start`/`date_planned_finished`).

## Weekly PM checks by machine type

**CNC Router / Nesting:** chiller water (level/temp/leaks), belts (tension 5-10mm deflection/cracks/age), spindle (sounds/heat/collet), rails & ball screws, dust collector, tools/bits.
**CO2 Laser:** chiller water (MOST critical — cools laser tube, neglect = tube failure), focus lens + mirrors (clean/no-crack/no-coating-peel), assist gas, exhaust filters, nozzle, motion.
**Fiber Laser:** chiller water (cools laser source — expensive), focus lens + protective window (replaced most often), N2/O2 gas, nozzle, auto-focus/height sensor, cutting table slats.
**Support (dust collector / grinding / sharpening):** suction + filters, oil, belts, grinding wheels (no cracks/wear), E-stop.
