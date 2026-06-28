Aseer Museum: PD M.Waris Khan. MEP scope: power to specialist systems only. Namaa FLS: P01167 (SAR70k safety), P01449 (SAR23k survey). Not full FLS design.
§
RCRC proposal work: never blanket regex section tags — corrupts structure. Verify tag balance after edits. White pages = part dividers needing dark styling.
§
OneDrive macOS: Never write files directly to OneDrive path (CloudStorage or Group Containers) — both produce corrupt/placeholder files. Stage to /tmp, then AppleScript `duplicate src to dest with replacing` via Finder. Verify with `xxd -l 8` (must start PK\x03\x04).
§
SAMAYADOC: use SamayaDoc class, never hand-craft styles. add_h2(num,text). add_table(rows,headers). AppleScript copy to OneDrive.
§
Samaya logo: use bilingual PNG from _Style-Guides/logos archives/samaya-logo-trans.png (lowercase "samaya", red "a"). Never SVG text approximations. Use `<img>` with PNG, not inline SVG.
§
Proposal rules (RCRC): never reference self-created docs (SOW, ER) — use external standards only. No team member names in field reports, no photo quantities. Monochrome icons for formal docs; diverse TOC icons. Workflow descriptions prefer SVG charts. GitHub for version control. Remove exclusionary language (".33.1 Photographic Register section can be removed.
§
Odoo timesheets: unit_amount is in MINUTES (60=1hr, 120=2hrs). Descriptions: plain text only, no emoji/icons.
§
Project work: work directly in ~/Documents/{project-name}/ not /tmp (user explicitly corrected this).
§
Register column cleanup: exact header match only ("SOW §", "ER §", "ER §b"). NEVER substring-match "SOW" or "ER" — deletes "Submittal / Deliverable (per SOW)" description column.
§
Register building: preserve source file's organization hierarchy (level-based vs type-based). Stage columns (50%, 90%, 100%, IFC) hold planned dates, staggered by floor with 7-day review buffers.