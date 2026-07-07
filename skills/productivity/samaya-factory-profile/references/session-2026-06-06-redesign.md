# Session: 2026-06-06 — Full Profile Redesign + Overflow Audit + Prequalification Focus

## Pages Redesigned (24 of ~30)
Cover, TOC, About, Compliance, Capacity, Engineering, QA/QC, Scope, FF&E, 
Finishings, Display, Flagships 1-8, HSE, Approvals, After-Sales, Certifications, 
Financial, Back Cover

Remaining: Replicas (p13), Graphics/Wayfinding (p14-15), Sectorial Index, 
Landmark Deliveries, Materiality grid

## Key Changes Made
- Cover slogan RESTORED after Claude changed it — must protect brand text
- TOC updated with punchier bilingual labels
- Editorial pass: tighter narratives, active Arabic verbs, em-dash rhythm
- Flagship pages: alternating hero photo left/right by swapping DOM order
- Materiality grid: 48 cells → 93 cells (machine photos added from 05-machinery-cnc/)

## Overflow Audit Results
CRITICAL: p24c (Materiality) — 48 cells at 46mm = 588mm needed, only 170mm available
HIGH: p4 (Capacity) — 4 layers ~197mm > 174mm
MARGINAL: p24a (Key Projects), p13a (3D Scanning), p6 (QA)

## Overflow Fixes Applied
- Materiality cell height: 48mm → 22mm (later changed to 46mm, then 52mm with cover)
- Capacity hero: 62mm → 45mm, gallery tiles: 28→24mm
- Key Projects card gaps tightened
- 3D Scanning hero: 42mm → 36mm
- QA instrument height: 24mm → 20mm

## Prequalification Focus (second half of session)
- Profile now functions as a factory prequalification document
- Every section must show: machines, process flow, operations
- Text should be capability statements, not marketing
- Photos should show equipment and process, not just finished work

## New pages created
- **p13a-1**: 3D SCANNING PREQUALIFICATION — standalone specs page with 12-row parameter table, measurement samples, process flow. No brand names.

## QC Pipeline established
After any edit → Claude audits overflow → Kimi fixes CSS → Codex verifies TOC. Must never skip.

## CSS conflict found & fixed
- `.ed-spread .content` (20-redesign.css) overrode `.v4-scan-meth` (30-redesign.css) on p13a
- Fix: removed `ed-spread` class from p13a `<section>`

## TOC fixed
- Added 3 missing sub-entries: 11a (p13a), 11a-1 (p13a-1), 11b (p13b)
- Added `.v3-toc-entry--sub` CSS for indented sub-entries

## Aseer Museum removed
- منحف عسير الإقليمي removed from Key Projects section (confirmed absent via QC audit)
- Not to be added anywhere until project is complete

## Learnings
- write_file OVERWRITES entire CSS files — use patch() always
- Surge auth: never run `surge logout` — requires user password to recover
- Image compression: use `sips -Z 2000` to reduce 15MB RAW → ~500KB
- China Treasures photos assigned to vitrine types via Pillow analysis (brightness, edge detection)
- CSS restoration from v5 after write_file accident: 30-redesign.css went from 4276 → 3858 → 4276 lines
- Photo skill created: `samaya-profile-photo-assets` — directory of classified photo assets
- QC pipeline: Claude audits → Kimi fixes → Codex verifies TOC
- Always check TOC after adding/removing pages
- Aseer Museum should never appear in profile