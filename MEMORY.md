Repo (~/aseer-museum-pm) is single source of truth for plan content — check before OneDrive files. ER/SoW compliance only, no Mostadam rating targets. CR registers: Excel, Open/Closed status. Fida's SMP: construction-phase focus, MOSTADAM Bronze framing — fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
SMP decisions per ER/SoW only: waste diversion 60% (not 75%), Oddy aging 14-day (not 49-day), code-compliance framing (not rating-target). 'Sustainability Specialist' preferred over 'Sustainability Manager' per Adel Darwish's comment.
§
DOCX: Word heading styles, RGB PNGs, cantSplit tables, remark=add_remark() 9pt #64748B. SVG charts → styled tables if Word fails.
§
Scope boundaries: always check BOTH SoW text AND specialist's own submittal register — SoW alone isn't enough. CG comments or specialist's deliverable schedule may extend scope (e.g. ZNA).
§
CG comment disposition: reference attached CR sheet only, never list full CG comments inline in the document. Remove 1.4 CG Comment Disposition Matrix section entirely.
§
Aseer lane routing: classify task → master_dashboard.md → lane dashboard. Lane map: Design/NRS/RIBA→02, Submittals/SI→10, Procurement/PQ→07, Subcontractor→11, Materials→06, Risk/PRR→04, Sustainability/SMP→05, Quality/NCR→03, HSE→09, BIM→08, PM/decisions→01, Escalation→escalation_board.md. Always check plan CG status in plan_tracker.md first.
§
Delegate complex Excel/style fixes to Codex/Claude via claude -p. Samaya Excel style: base #F8FAFC, borders #CBD5E1 thin, severity fills per value, navy #0F172A header.
§
AD Engineering: internal contract split — Samaya Tech Office produces mechanical, AD reviews/stamps. ROE docs internally. To CG, AD is full MEP designer. Liability follows AD's stamp, not drafter.
§
Odoo contact creation: company contacts (`is_company=True`) require `"vat": "TBC"` or real VAT — Odoo rejects without it. Quotations use `sale.order` model, not `purchase.order`. Reference file at `~/.hermes/skills/software-development/odoo/references/contact-and-quotation-creation.md`.