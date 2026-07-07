# Aseer Resource Mgmt Plan Rev C00 — KPR Sync Session (2026-06-19)

## Session context

Updated `aser_museum_resource_mgmt_plan_RevC00_CG_REVIEW.html` to align with KPR Rev C05 (2026-06-19).

## Changes made

### KPR cross-reference corrections
- Restored all on-board personnel names that had been blanked (Mohamed Samir, Dr. Waleed, Mohamed Ahmed, etc.)
- "Pending submission" → person IS on board → keep name, show "On board" (NOT "pending MoC submission")
- "Code C" sustainability → "submission in progress" (NOT "Code C (revise & resubmit)")
- Entity names corrected: "Nama Al Amal" → "Nama Consulting", "Glassbühne" → "Glasbau Hahn"
- NRS approved roles added: Scenographer and Interior Designer → "NRS — Approved 11-Feb"
- Tier 3 expanded: ITCA + Fire-Proofing Contractor rows added
- Tech Office Manager replaced with HSSE Manager in Tier 1 (not a KPR role)
- Ali A. Mostafa and Mohamed Mostafa added to Riyadh HO BIM Modelers list

### Content removals (client-facing cleanup)
- "PMBOK practices" / "PMBOK-compliant" — removed (3 instances)
- "aligned to Master Programme Rev.03" — removed from Phase Strip title
- "aligned to SMP Rev 03" — removed from Risk Register header
- "added Interactive Design, Lighting, ICT Security" — internal change note removed
- "WBS" — removed from Material Management
- "RBS" abbreviation — removed from header and section title
- "QS_Template.xlsx" → "QS Template" (internal filename removed)
- "Primavera P6" — removed (internal tool reference)

### Location references
- "Overseas" removed from all 4 BIM coord/lead rows
- "Dubai" removed from AD Engineering (Tier 2 table + Location Matrix)
- "London" removed from ZNA Studio and NRS Design Lead (Tier 2 table + Location Matrix)

### Personnel labels
- "on-site" → "appointed" for Ali A. Mostafa (not physically at site)
- Ali A. Mostafa line eventually removed from BIM Manager card entirely (he belongs in Riyadh HO BIM Modelers list, not as a BIM Manager sub-note)
- "pending MoC submission" removed from all status labels

### Equipment and materials
- "Laser scanner" → "FARO Focus Premium 200 laser scanner" (2 locations)
- Construction Materials expanded from 3 generic lines to 5 detailed lines with actual suppliers from finishes_schedule.json, showcase_schedule.json, av_equipment_schedule.json, lighting_schedule.json

### Table layout fix
- Global CSS: `table-layout:fixed` + `word-wrap:break-word` on td/th
- All pixel widths (60px, 70px, 22px, 30px) converted to percentages
- Explicit column widths added to all 19 tables

### Revision history
- Date changed from 2026-06-16 to 2026-06-19 (submission date = tomorrow)

## KPR source
`Docs/09_Registers/13_Key_Personnel_Register/Aseer_Museum_Key_Personnel_Register.xlsx`
Rev C05, 2026-06-19. Sheets: Cover, Key Personnel, Summary.

### Master Programme status verification
- Checked Register Log (.xlsb) at `Docs/09_Registers/_Master_Register_Index/Register Log.xlsb`
- Used `pyxlsb` library (not `xlrd` which doesn't support .xlsb)
- Found 4 submission cycles for MOC-ASEER-0PS-SH-006: R0 (15-Jan, Code C) → R1 (23-Feb, Code C) → R2 (04-Apr, Code B) → R3 (09-May, **Under Review**)
- Updated 4 references in the plan: "resubmitted after Code C" → "submitted 09-May-2026, Under Review by CG"
- Risk Register R5: "not approved (Code C received)" → "Under Review by CG since 09-May-2026"

## Key lessons
1. **First pass blanked all pending names** (treating "pending" as "not allowed"). User corrected: pending = on board, keep the name.
2. **Always check Register Log for doc status** — the plan said "resubmitted after Code C" but the register showed "Under Review" since 09-May. Never assume doc status from memory.

