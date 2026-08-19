# Odoo Task References & Aseer DD Design-Stage Structure

## Task References Must Be Hyperlinks (User Preference)

When presenting task numbers anywhere a human clicks to review (MD mapping files, status reports, Telegram/chat task lists), render each task number as a **clickable link to the Odoo task** — never a bare `#NNN`. Sultan Issa's standing rule: "رقم التاسك يكون لينك للتاسك لسهوله فتحته للمراجعه" (task number is a link to the task for easy click-to-review).

| Instance | Task URL pattern |
|----------|------------------|
| Samaya | `https://samayainv.odoo.com/odoo/task/<id>` |
| Moqtana | `http://167.99.224.43:8069/odoo/task/<id>` |

Markdown pattern:
```md
[#352](https://samayainv.odoo.com/odoo/task/352) | Study & Work Plan
```

---

## Aseer Museum (project 219) — DD Design-Stage (stage 36) Task Structure

Used for design-stage gap analysis: does the design deliverable tree match the packages in Odoo?

**Parent packages in DD stage** (each with 5–44 children):
- `00 — General`, `01 — Architecture`, `02 — Structural`, `03 — MEP & IT`, `04 — Life Safety`, `05 — Projects Plans`
- Specialist/scenography packages (SC = subcontractor series): `06 — Model Maker (SC-01)`, `07 — Lighting (SC-02)`, `08 — Graphics (SC-03)`, `09 — Showcases (SC-05)`, `10 — Rigging`, `11 — FF&E`, `12 — Exhibition Fit-Out`, `13 — Interactives`, `14 — FLS (Life Safety)`, `15 — MEP Designer`, `16 — CITC / IT-Data`, `17 — Acoustic`, `18 — Architectural Visualization & 3D Presentation`

**Specialist design packages (SC-XX) follow a recurring 6-subtask template:**
- 2 discipline-specific deliverables (e.g. `LG-001` / `LG-002`, `AC-001`/`AC-002`, `FF-001`/`FF-002`, `IN-001`/`IN-002`)
- Then 4 staged submission gates: `50% Design Package`, `90% Design Package`, `100% Design Package`, `IFC/AFC Package`
- These 50/90/100%/IFC gates mirror the compressed design timeline and are the standard shape for any new specialist package.

**Data-quality check that surfaced this session** (project 219): 6 tasks missing `date_deadline` (5 Project Plans PL-0060..64 + `18 — Arch Viz`), 5 missing `date_assign`, 27 with no assignee (mostly Initiation plans + Procurement S00101 subcontract packages). When asked "does the project need task updates?", run this scan:
```python
# per project, count tasks missing date_deadline / date_assign / user_ids
tasks = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['project_id','=',219]]],
    {'fields':['id','name','stage_id','date_assign','date_deadline','parent_id','user_ids']})
# stage_id is a list [id]; parent_id False = package
```
`stage_id` in search_read returns a list like `[36]`, not an int — index `[0]` before aggregating.
