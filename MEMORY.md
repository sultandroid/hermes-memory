Repo is source of truth for plan content. ER/SoW compliance only. Fida's SMP: fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
Scope boundaries: always check BOTH SoW text AND specialist's own submittal register — SoW alone isn't enough. CG comments or specialist's deliverable schedule may extend scope (e.g. ZNA).
§
CG comments: reference attached CR sheet only, never inline in doc. RMP updates: new risk factors go as rows in T4 table, not standalone paragraphs. T18 values say 'Deferred until BOQ finalised'. Plan body states factual position — never cite 'Per CG comment on ZD-XXXX' in formal docs. Insert before next body heading (Heading style, not toc). Verify TOC clean after insertions.
§
AD Engineering: Samaya does mechanical design, AD reviews/stamps. To CG, AD is full MEP designer. Liability follows AD stamp.
§
NEVER delete user files without explicit confirmation. User is very particular about this — even if user says 'remove', verify first. Do not act on deletion instructions without double-checking.
§
Logo docs: AGENTS.md + style guide + asset README. Public URLs on samaya-factory.com. Cross-check all files referencing the asset.
§
OneDrive: write /tmp first then cp to path. Read files one by one to avoid sync corruption.
§
Risk register multi-source update: when changing risk metadata, update ALL of: risks.json (master), dashboards/risks.json, risks.json.bak, index.html (auto-rebuilt by post-commit hook from risks.json), treatment/<risk_id>.md frontmatter, and Excel register. Deploy to server + git commit.
§
User HATES the `§` symbol (Unicode section sign). Never use it. Use `Section` or `Clause` instead. Also no AI symbols: `->`, `--` (em dash), `·` (middle dot), `•`, `✓`, `✗`. This is the #1 recurring error.
§
Outlook 16.90+: AppleScript `subject of message id N` fails. Use `item N of (every message of mail folder id <ID>)`. SQLite DB locked while Outlook runs.
§
SulKimiClaw Telegram: @SulKimiClaw_bot