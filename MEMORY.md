Repo is source of truth for plan content. ER/SoW compliance only. Fida's SMP: fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
Scope boundaries: always check BOTH SoW text AND specialist's own submittal register — SoW alone isn't enough. CG comments or specialist's deliverable schedule may extend scope (e.g. ZNA).
§
Snapshot counter: use --bump flag to advance, never auto-increment. Content number must match filename. Short codes only (PRR/DDR/HSE) as counter keys, never human-readable names.
§
AD Engineering: Samaya does mechanical design, AD reviews/stamps. To CG, AD is full MEP designer. Liability follows AD stamp.
§
NEVER delete user files without explicit confirmation. User is very particular about this — even if user says 'remove', verify first.
§
Logo docs: AGENTS.md + style guide + asset README. Public URLs on samaya-factory.com. Cross-check all files referencing the asset.
§
OneDrive: write /tmp first then cp to path. Download files ONE BY ONE sequentially, never batch.
§
Risk register multi-source update: update ALL of risks.json, dashboards/risks.json, risks.json.bak, index.html, treatment/<id>.md frontmatter, and Excel. Deploy + git commit.
§
User hates: §, ->, -- (em dash), ·, •, ✓, ✗ and AI cliches (seamlessly, robust, cutting-edge, etc.). This is the #1 recurring error.
§
Odoo mark-as-done: set progress=1.0 only, NEVER change stage_id. Stage = work phase, not completion. User correction 2026-07-24.
§
Hostinger LiteSpeed 404 cache is case-sensitive + persistent: lowercase new subdirs (e.g. `ddr/`) stay 404-cached even after file is on disk with correct perms. Use UPPERCASE (e.g. `DDR/`) for new subdirs to bypass. Symptom: HTTP 404 with `last-modified: Tue, 22 Apr 2025` (cached error page) on a file that exists.
§
Construction risk audit: classify as generic (reject like pandemic, concrete pump), duplicate of existing PRR (omit), or missing project-specific risk (promote to PRR with next available number).