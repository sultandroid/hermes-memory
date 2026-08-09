# Odoo Lean Manufacturing — Design Detail & Open Questions

Session: 2026-08-08. User is planning the Odoo implementation of the Lean system. NOTHING executed yet — confirm before building.

## Native Odoo structure (user's framing)
- **Project** → contains **Stages** → each stage contains **Tasks**
- **Task fields:** start date, end date, description, comments, activities, images
- **Stages** = kanban columns; **Tags** = item type

## Recommended design
- **Project:** "Lean Manufacturing — التحسين المستمر"
- **Stages (3):** جديد (New) → قيد التنفيذ (In Progress) → مغلق (Closed)
- **Tags (type):** 🚶 Gemba · ⚡ Immediate action · 💡 Kaizen · 🔍 5 Whys · 🧹 5S
- **Task fields:** description (+ 5 Whys template when needed), start date (walk day), deadline, assignee, priority, comments (follow-up), activities (reminders/subtasks), images (before/after)

## Corrected flow (user-mandated)
- ~90% of Gemba observations = known process errors (wrong execution, employee delay, wrong ordering) → **immediate action, fixed same day, no Kaizen**
- Only improvement ideas → Kaizen; only recurring problems → 5 Whys
- Immediate fixes close same day with no analysis

## Open questions (ask before building)
1. **5S weekly scores** — as a recurring Task inside the same project, or in the separate **Quality** module (better for scores/reports)?
2. **Assignees** — which people? (Raoof رؤوف, Essam عصام, Ahmed Awad أحمد عواد, supervisors?)

## Alternative Odoo routes (if user asks)
- **Odoo Online + Studio** → custom "Kaizen"/"5 Whys" models with custom fields, no code
- **No Studio** → use existing Project + Quality + Maintenance modules, works today
- **Maintenance module** → real preventive-maintenance schedules per machine (directly fixes the classic 5 Whys root cause: "no PM system")
- **MRP work centers** → downtime, efficiency, capacity tracking
