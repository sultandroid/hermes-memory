---
name: lean-manufacturing
title: Samaya Factory Lean Manufacturing System (Gemba, Kaizen, 5S, 5 Whys, PM, CI)
description: Design and implement the Lean/continuous-improvement system for Samaya Factory — Gemba walks, Kaizen, 5S, 5 Whys, preventive maintenance, and the central CI register. Covers the corrected observation flow, the repo-first data-collection path (Smart Factory Telegram group), the Odoo implementation plan (Project→Stages→Tasks), the Lean≠accounting scope guard, the machine-specific PM checklists, Odoo machine data, and the user's planning-first preference.
triggers:
  - User says "lean manufacturing" / "التحسين المستمر" / "تطبيق نظام" for the factory
  - User asks about Gemba walk, Kaizen, 5S, 5 Whys, continuous improvement, preventive maintenance
  - User wants to structure the Lean system in Odoo
  - User references the lean/ folder in samaya-profile
  - User asks about CNC/Laser machine maintenance checklists
  - User asks for machine PM data from Odoo (maintenance.equipment / mrp.workcenter)
---

# Samaya Factory — Lean Manufacturing System

## 🎯 Scope
A practical Lean/continuous-improvement system for Samaya Factory. Five tools: **Gemba Walk, Kaizen, 5S, 5 Whys, Continuous Improvement**. Files live in `samaya-profile/03_Workshop/lean/` (README + per-tool folders + `continuous_improvement_register.xlsx` built by `build_register.py`).

## ⚠️ CRITICAL — The corrected observation flow (user-mandated)
**NOT every Gemba observation needs a Kaizen.** The user explicitly corrected this. ~90% of problems seen on a Gemba walk are **known process errors** — wrong execution, employee delay, wrong ordering — and the action is taken **immediately, on the spot, without Kaizen**.

```
Gemba walk → observation
  ├─ ~90% known process error / delay → ⚡ immediate action → fixed same day → closed
  ├─ improvement idea → 💡 Kaizen → in-progress → closed
  └─ recurring problem → 🔍 5 Whys → root-cause analysis → action → closed
```

Only **Kaizen** (improvement ideas) and **5 Whys** (recurring problems) pass through a real execution phase. Immediate fixes close the same day with no analysis. Do NOT route every observation into Kaizen — that was the original mistake.

## 🏗️ Odoo implementation plan (user's structure understanding)
The user wants to implement this in Odoo. Understand the native structure first:

**Project → Stages → Tasks**
- **Task fields:** start date, end date, description, comments, activities, images.
- **Stages** = kanban columns. **Tags** = type of item.

**Recommended design (single project, not one per tool):**
- **Project:** "Lean Manufacturing — التحسين المستمر"
- **Stages (3):** جديد (New) → قيد التنفيذ (In Progress) → مغلق (Closed)
- **Tags (type):** 🚶 Gemba · ⚡ Immediate action · 💡 Kaizen · 🔍 5 Whys · 🧹 5S
- **Task fields:** description (+ 5 Whys template when needed), start date (walk day), deadline, assignee, priority, comments (follow-up), activities (reminders/subtasks), images (before/after).

Rationale for ONE project: all Lean items share the same lifecycle (new→executing→closed), so one kanban board = the whole CI register, filterable by tag. Separate projects per tool would fragment it.

## 🚦 Planning-first rule
The user is **still planning** — do NOT execute anything on Odoo (no project/task creation, no field changes) without explicit confirmation. Present the structure and ask before building. This matches the user's general plan-first preference.

## 📊 Data-collection-first decision path (user-mandated 2026-08-08)
The user's chosen sequence — do NOT jump to Odoo:
1. **Build the system on the repo first** (`samaya-profile/03_Workshop/lean/`).
2. **Collect real data** from the **Smart Factory Telegram group** (chat `-5440607372`, "Factory") — convert group messages into Lean-system entries.
3. **Only after data accumulates**, decide whether to move to Odoo.

**Checklist rollout preference:** before launching the system, **design the checklists together with the user** (Mostafa / Raoof will fill them daily). Do NOT ship checklists cold — the user explicitly wants to co-design them first so the team isn't confused ("قبل انطلاق السيستم علشان ما نشتتش الناس").

## ⚠️ Scope guard — Lean ≠ accounting
The user rejected adding **machine value / asset cost / depreciation** tracking. That is accounting/asset management, NOT Lean. Lean tracks **waste**: downtime, efficiency, capacity, rework, waiting, motion. Keep the system to waste metrics only; never add asset-value fields to Gemba/Kaizen/5S/5 Whys forms.

## 📁 Repo layout (already built 2026-08-08)
```
03_Workshop/lean/
├── README.md                        # overview + 30-day rollout
├── 01_gemba_walk/  gemba_checklist.md, gemba_log.md
├── 02_kaizen/      kaizen_form.md, kaizen_register.md
├── 03_5s/          5s_audit_checklist.md, 5s_scores.md
├── 04_5whys/       5whys_form.md, 5whys_analysis_2026.md
├── 04_preventive_maintenance/  README + machine PM checklists + pm_log.md
├── 05_continuous_improvement/  ci_register.md
├── 06_lean_input/  lean_input_register.md + merged_whatsapp_2026.json
├── 07_forms/       README.md (index of all data-collection forms)
├── continuous_improvement_register.xlsx   # 6 sheets, navy/gold
└── build_register.py               # regenerates the xlsx
```

## 🌐 Bilingual requirement (user-mandated 2026-08-08)
**ALL forms, checklists, and registers must be bilingual — Arabic + English side by side.** The user said "should be bilingoul". Every field label carries both: `Date / التاريخ`, `Machine / الماكينة`, `Inspector / المنفذ`. Do NOT write a form in Arabic-only or English-only. This applies to the `.md` checklists AND the Excel forms. The PM checklists were rewritten to this format after the user asked.

## 📊 Excel data-collection forms (16 forms, built 2026-08-08)
The user asked to design **all** data-collection forms as Excel, grouped by frequency, and to **send them to him for review** (deliver the zip, don't just commit). Structure in `07_forms/` (built by `build_forms.py` in `/tmp/lean_forms/`):

- **Daily (5):** Gemba Walk Log, Production Output, Machine Downtime, Safety Observation, Worker Attendance
- **Weekly (7):** PM CNC Router, PM Co2 Laser, PM Fiber Laser, PM Support Equipment, 5S Audit, Kaizen Suggestion, Quality Non-Conformance
- **Monthly (4):** CI Register Review, KPI Dashboard, 5 Whys Analysis, Monthly Production Report

**Excel form conventions (Samaya style):** navy `#1F3864` header / white bold text, gold section fills, thin borders, `✅/❌/N/A` checkbox columns, dropdown-legend rows (e.g. "Status: Open/In-progress/Closed"), owner + date fields at bottom. Machine downtime form carries the CNC rate (100 SAR/h, workcenter FCNC) as a cost hint. KPI dashboard has 9 KPIs with target + trend columns.

**Delivery preference:** when the user asks for forms "to review", zip them and send via `MEDIA:` — do not just commit to the repo. He reviews the Excel files directly.

## 📥 WhatsApp export → Lean input (technique, 2026-08-08)
The user sends WhatsApp chat `.zip` exports (Samaya Factory group + التركيبات group) to seed the Lean system. Parsing technique:

- **LRM prefix gotcha:** WhatsApp lines often start with a Left-to-Right Mark `\u200e` before the `[`. A regex anchored with `^\[` fails silently (0 matches). Use `re.match(r"\[(\d{2}/\d{2}/\d{4}), ([0-9:]+)[\u202f ]([AP]M)\] (.*?): (.*)$", line.strip())` — the `\u202f` is the narrow no-break space WhatsApp uses before AM/PM.
- **Filter to current year** (e.g. `date.endswith("/2026")`) — the export spans years (2021→2026, 48k lines).
- **Keyword classification** into Lean categories (Maintenance, Gemba/Safety, Immediate/Process, Kaizen, 5S, Materials) — but the raw keyword match is **noisy** (picks up greetings, Islamic phrases, "تسلم ياريس"). Curate with a NOISE blocklist + a stricter ACTIONABLE keyword set before writing to the register.
- **Merge multiple groups** (Samaya Factory + التركيبات) and de-dup by (date, sender, text).
- **Seed the registers** from the real items: 5 Whys analyses for recurring problems (dimensions, machine breakdowns, material shortage, acoustic panel fall), CI register entries with owner+deadline, PM log spare-parts rows, Kaizen register ideas.
- Raw merged JSON saved to `06_lean_input/merged_whatsapp_2026.json` for traceability.

## 🔧 Preventive Maintenance (PM) tool — added 2026-08-08
Sixth tool: **weekly machine-specific PM checklists** that prevent breakdowns (directly solves the "machine stopped → no PM schedule" 5-Whys root cause). Lives in `04_preventive_maintenance/`. Executor = **Moin El-Din** (معين الدين, maintenance supervisor + CNC operator).

Files:
- `cnc_router_checklist.md` — CNC Router (Ventire 313) + Nesting JIYU: **chiller water**, **belts**, spindle, rails/ball screws, tools.
- `co2_laser_checklist.md` — Co2 Laser (1325L): **chiller water**, **lenses + mirrors** (clean/no cracks), assist gas, exhaust, nozzle.
- `fiber_laser_checklist.md` — Fiber Laser (SF 3015G): **chiller water**, **focus lens + protective window**, N2/O2 gas, nozzle, auto-focus.
- `support_equipment_checklist.md` — Dust collector + gear/saw-blade grinding & sharpening machines.
- `pm_log.md` — weekly tracking table + spare-parts replacement log + monthly summary.

**PM scope rule:** checks are organized **by machine type** (CO2 vs fiber laser lenses differ; fiber uses a sacrificial protective window replaced more often than the focus lens). Don't write one generic checklist — the checks genuinely differ.

**Lean integration:** every weekly check → ✅ logged in pm_log.md; any ❌ → 5 Whys in ci_register.md; replacement idea → Kaizen; spare part → Odoo PO.

## 🖥️ Odoo CNC/Laser machine data (verified 2026-08-08)
All 8 machines under `maintenance.equipment` category **CNC (id 4)**, workcenter **CNC/Laser (id 13, code `FCNC`, cost 100 SAR/hr)**:
CNC Router (id 290), Co2 Laser Cut (291), Fiber Laser Cutting (292), Nesting CNC JIYU (329), Dust Collector 7.5KW (338), Swing Head Gear Grinding (339), Saw Blade Grinding MF1107 (340), Saw Blade Sharpening (341).

**Odoo data gotchas for factory machines:**
- `hr.employee.job_title` is the **iqama/residency title, NOT the real role** — e.g. Moin El-Din shows "Carpenter" (id 2760) but is really maintenance supervisor + CNC operator. Never trust job_title for factory roles; ask the user or infer from context.
- `mrp.workcenter` field `capacity` does NOT exist in Odoo 18 (raises Invalid field). Use `name/code/costs_hour/time_efficiency`.
- `maintenance.request` has no `date_deadline`; use `schedule_date`/`date`.
- All 8 CNC machines have `technician_user_id = False` (unassigned) — Moin is the natural owner for their PM.

## 📎 Reference files
- `references/odoo-lean-design.md` — the Odoo Project→Stages→Tasks mapping and open design questions (5S scoring location, assignees).
- `references/smart-factory-group-data-source.md` — where Smart Factory Telegram group data lives (chat `-5440607372`), and the going-forward capture plan for seeding the Lean system.
- `references/cnc-laser-machines-pm.md` — full CNC/Laser machine register from Odoo (all 8 machines + workcenter FCNC), the Odoo 18 field gotchas hit while pulling it, and the per-machine-type PM check keys.
- `references/whatsapp-lean-parsing.md` — the WhatsApp `.zip` export → Lean-input parsing technique (LRM regex fix, year filter, keyword classification, noise filtering, register seeding).

## 🔗 Related skills
- `factory-operations` — daily MRP/PO/email review (different class; do not conflate).
- `odoo` — Odoo connection, field schemas, SSL fix.

## ⚠️ Pitfalls
- **Do not route every Gemba observation into Kaizen** — 90% are immediate-fix process errors.
- **Do not create one Odoo project per Lean tool** — one project with tags is cleaner.
- **Do not touch Odoo while the user is still planning** — confirm before any execution.
- **Do not add machine value / asset cost** — Lean tracks waste (downtime, efficiency, capacity), not accounting.
- **Do not trust `hr.employee.job_title` for factory roles** — it's the iqama/residency title, not the real job (e.g. Moin El-Din is "Carpenter" in Odoo but is maintenance supervisor + CNC operator). Confirm the real role with the user.
- **Write PM checklists by machine type, not one generic list** — CO2 laser (lenses+mirrors) differs from fiber laser (focus lens + sacrificial protective window) differs from CNC router (spindle/collet). The checks genuinely differ; do not flatten them.
- **Do not ship checklists cold** — co-design them with the user first; Mostafa/Raoof fill them daily.
- **Do not write forms in one language** — every form/checklist/register must be bilingual (AR/EN side by side).
- **Do not trust raw WhatsApp keyword matches** — filter noise (greetings, Islamic phrases) with a blocklist + stricter actionable keywords before seeding registers.
- **Do not anchor WhatsApp regex with `^\[`** — the LRM `\u200e` prefix breaks it; use `line.strip()` + the `\u202f` space pattern.
- Factory Odoo is normally read-only; applying Lean in Odoo is an explicit user decision, not a standing permission.
