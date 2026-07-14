Repo (~/aseer-museum-pm) is single source of truth for plan content — check before OneDrive files. ER/SoW compliance only, no Mostadam rating targets. CR registers: Excel, Open/Closed status. Fida's SMP: construction-phase focus, MOSTADAM Bronze framing — fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
SMP decisions per ER/SoW only: waste diversion 60% (not 75%), Oddy aging 14-day (not 49-day), code-compliance framing (not rating-target). 'Sustainability Specialist' preferred over 'Sustainability Manager' per Adel Darwish's comment.
§
DOCX: use Word heading styles (H1/H2/H3), RGB PNG images (not RGBA), cantSplit on tables, 9pt halftone #64748B for remark paragraphs. If images don't render in Word, replace SVG charts with styled tables.
§
When determining scope boundaries between specialists, always check BOTH the SoW text AND the specialist's own submittal register. The SoW may list a narrow scope, but the CG-approved scope or the specialist's own deliverable schedule may extend it. Example: ZNA's SoW lists interior areas only, but CG comment #1 requires "all project different lighting systems, spaces" and ZNA's submittal register includes LG-024 "Exterior lighting design" under SoW §8.8. Never assume scope from the SoW alone.
§
CG comment disposition: reference attached CR sheet only, never list full CG comments inline in the document. Remove 1.4 CG Comment Disposition Matrix section entirely.
§
DOCX: Word heading styles, cantSplit on tables, RGB PNGs. Remarks = add_remark() halftone #64748B 9pt (not add_body). Fix empty cNvPr + noChangeAspect for Word image compat.
§
Aseer lane routing: classify task → master_dashboard.md → lane dashboard. Lane map: Design/NRS/RIBA→02, Submittals/SI→10, Procurement/PQ→07, Subcontractor→11, Materials→06, Risk/PRR→04, Sustainability/SMP→05, Quality/NCR→03, HSE→09, BIM→08, PM/decisions→01, Escalation→escalation_board.md. Always check plan CG status in plan_tracker.md first.
§
Delegate complex Excel/style fixes to Codex/Claude via claude -p. Samaya Excel style: base #F8FAFC, borders #CBD5E1 thin, severity fills per value, navy #0F172A header.