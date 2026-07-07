# Samaya Profile Design Workflow

## Task delegation
- **Design/redesign** → delegate_task to **Claude**
- **CSS fixes / overflow fixes** → delegate_task to **Kimi**
- **QC, TOC verification, overflow audit** → delegate_task to **Codex**

## Overflow audit pipeline (MANDATORY after ANY edit)
1. Claude audits page-by-page (check height:calc, overflow:hidden, content vs 174mm)
2. Kimi fixes flagged pages (reduce sizes, remove height constraints)
3. Codex verifies (check TOC accuracy, page count, no broken styles)

## Key constraints
- Slogan "صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art." — NEVER change
- Aseer Museum (متحف عسير الإقليمي) NEVER appears in profile
- No brand/device names in 3D scanning sections
- Always update TOC (id="p2") when pages added/removed/renumbered
- Cover slogan is fixed — never alter it

## Photo rules
- Replace photos in-place (same block) — never add new blocks unless asked
- Photos from macOS Downloads/WhatsApp need custom copy (ditto or Python)
- For Materiality grid: use background-size: contain; height: 22mm (or 52mm if user wants bigger)
- Classify photos by folder: machinery-cnc/, qa-lab/, hardware/, packaging/, projects/from-work/, projects/from-graphite/, projects/from-website/, scope-*/process/

## Page layout rules
- A4 landscape (297×210mm), RTL, bilingual AR/EN
- Content height: calc(210mm - 22mm - 14mm) = 174mm (print: 170mm)
- Overflow fix: remove height:calc and overflow:hidden on .content; use min-height:210mm; height:auto; overflow:visible on .page
- .ed-back-cover: fixed height: 210mm; overflow: hidden
- Flagship pages: alternate hero photo left/right
- For backward cover, QR inline beside text not below

## Deploy
- Surge domain: samaya-factory-profile.surge.sh (mohamedsultanabbas@gmail.com)
- Build from v6/ directory
- Copy to /tmp/samaya-profile-deploy/, replace ../assets/ → assets/, run copy_assets script, surge
- Do NOT deploy major redesigns without user approval
