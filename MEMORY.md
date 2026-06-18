Aseer Museum team (SMP Rev03): PD Eng. Waris Sultan (Exhibitions, 13-Jun), BIM Mgr Dr. Waleed Salah, QA/QC Mgr vacant, HSSE Mgr Eng. Mohamed Ahmed, Tech Office Mgr Eng. Mohamed Sultan, Proj Eng. Ahmed Salah, Arch. BIM Lead Eng. Ali Abdelrahman Mostafa (Samaya TO, Riyadh, formally on Aseer — 12+ yrs TO & BIM Mgr level), Procurement Hani Alghamdi, Doc Controller Eng. Hesham Abdelhamid.
§
For material showcase app: hotspot data dir outside deploy. Never modify original Excel data. Click-to-pin: 3-layer state (pinnedRef+clickedRef+pinnedCode). Cross-component nav uses CustomEvent. Light/formal theme (#E8E3DB bg, #C8A45C gold). RAL regex uses `(?!\d)`. Check `pointer-events:none` first. Active schedules for presentation stage: Finishes, Setwork, Showcase, Graphic, Wayfinding, FF&E, AV Equipment, Lighting.
§
SSH to deploy server: use hostname `samaya-factory.com` port 65002 (raw IP 92.113.28.249 times out). Deploy script at ~/Desktop/deploy.sh. Note: `*` in the cron job triggers the scheduler even when repeat=1 — use `no_agent=True` for script-only cron jobs.
§
Odoo: aggressive deadlines (2-5d per baseline). BOQ→Procurement 39, mfg/install→659, design→36. MAIN→SUB, Kanban sorted. English only. HTML emails: Calibri 11pt, gray borders, no plain text, no brand colors. Project separation strict: Moqtana/Tqanny commercial paint coatings ≠ Aseer/Samaya construction.
§
Aseer materials.json uses lowercase keys (`description`, `finish`, `colour`, `supplier`, `substrate`) while individual schedule JSON files use Title Case. Always verify keys against materials.json, not the schedule files.
§
Viz shot layout: MOC-MUS-ASE-1A0-ZD-0031 Rev.01 — General Layout Plan for Proposed 3D Viewpoints (RIBA Stage 3), approved B on 19-May-2026 by CG (Mohammad Elbaz). This is the agreed camera shots scope doc. CG cannot contradict its own approved layout. Key evidence for floor-by-floor and excluded galleries (G7/G10/G13).
§
Use git for version control — initialize repo with `git init`, commit after every significant change, push to GitHub (`sultandroid` account) when asked. The Aseer Museum viz app is at github.com/sultandroid/aseer-museum-viz.