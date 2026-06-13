# Rules & Conventions

## Golden Rules
- **Never ask permission** — baseline first, reality later
- **Always verify scope** before adding activities
- **Source-verifiable** — never assert without a doc reference
- **English-only** for formal output
- **Omit or flag TBC** rather than infer
- **Confirm task completion** — report what was done, changed, issues — never "ok done"

## NEVER Do
- `rm -rf` any path (OneDrive propagates immediately)
- Create new Excel files for registers (only append rows)
- Move unknown/non-project files from Downloads
- Reference /tmp paths in Odoo descriptions
- Auto-update sibling registers unless explicitly asked

## Entity Isolation
Samaya folders must NEVER contain Moqtana/Tqanny/Sada_Uhud/Sayyid al-Shuhada files, and vice versa.

## Excel Style
- Formulas, number formatting (never "SAR" as text)
- Navy headers (#1E293B) with white text
- Alternating white/light rows
- openpyxl

## Schedule Audit
- File ending at IFC gate = design-phase-only, NOT full project
- Look for "DESIGN PHASES" in name
- Activity prefixes: PE/AS/EN/PR (design) vs CN/IN/TC/HD (construction)
- Check contract completion date before flagging unrealistic timelines
- OneDrive-locked PDFs → use EXTRACT_*.md in 07.5 Audit Report instead

## Communication
- Short directives, no fluff
- English for formal output
- Arabic OK for direction
- Inline Telegram text preferred (MEDIA: doesn't arrive)
