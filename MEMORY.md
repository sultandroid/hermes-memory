Repo is source of truth for plan content. ER/SoW compliance only. Fida's SMP: fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
Scope boundaries: always check BOTH SoW text AND specialist's own submittal register — SoW alone isn't enough. CG comments or specialist's deliverable schedule may extend scope (e.g. ZNA).
§
CG comment disposition: reference attached CR sheet only, never list full CG comments inline in the document. Remove 1.4 CG Comment Disposition Matrix section entirely.
§
AD Engineering: Samaya does mechanical design, AD reviews/stamps. To CG, AD is full MEP designer. Liability follows AD stamp.
§
Odoo: company contacts need vat='TBC', quotes use sale.order. Ref: ~/.hermes/skills/.../odoo/references/.
§
NEVER delete user files without explicit confirmation. User is very particular about this — even if user says 'remove', verify first. Do not act on deletion instructions without double-checking.
§
Risk Mgmt Plan REV00: footer='Page X of Y\tSamaya Investment Company' (Word fields). Header: Samaya logo + title. TOC: Word TOC field (Heading 1-2, hyperlinked, page numbers). Cover: REV00 - Issue for CG Review, 18 Jul 2026. DC block: QC table. Rev table: 1.0, C01, C02, REV00. 31 tables, 169 paragraphs, 15 H1 + 34 H2 styles.
§
Risk Register REV00: 1 bar chart (user adjusted), 4 sheets: PRR (49 risks), DDR/HSE/AV templates. 17 RBS categories roll up into PRR.
§
Logo docs: AGENTS.md + style guide + asset README. Public URLs on samaya-factory.com. Cross-check all files referencing the asset.
§
Graphit (graphics) is a sister company — no PO/subcontract, direct execution after SoW approval.
§
Before sending RFIs/TQs, audit content against repo data (registers, SOW_RACI, submission plans) to verify questions are accurate and not already answered.
§
User prefers validation before action: when proposing corrections, ask 'are these logical or wrong?' rather than applying directly.
§
Cron job 'Adel Darwish folder check' (5d1b58e4ef6f) runs daily 9AM/5PM KSA, delivers to Telegram. Need to verify Telegram chat ID is correct — user said 'telegram' without specifying chat_id, so it uses the default gateway channel.