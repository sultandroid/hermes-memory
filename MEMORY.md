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
Logo docs: AGENTS.md + style guide + asset README. Public URLs on samaya-factory.com. Cross-check all files referencing the asset.
§
OneDrive: write /tmp first then cp to path. Read files one by one to avoid sync corruption.
§
Risk register multi-source update: when changing risk metadata, update ALL of: risks.json (master), dashboards/risks.json, risks.json.bak, index.html (auto-rebuilt by post-commit hook from risks.json), treatment/<risk_id>.md frontmatter, and Excel register. Deploy to server + git commit.
§
PRR-SCH-01 created = 2025-12-01 (NTP date).
§
Risk owner rule: site/construction/FLS risks = Construction Manager, not Technical Office Mgr.
§
Mohamed Samir (Construction Manager): always audit his submissions — copy-pastes from other projects with wrong dates/contract type.
§
User HATES the `§` symbol (Unicode section sign). Never use it. Use `Section` or `Clause` instead. Also no AI symbols: `->`, `--` (em dash), `·` (middle dot), `•`, `✓`, `✗`. This is the #1 recurring error.