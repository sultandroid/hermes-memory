Aseer Museum team (SMP Rev03): PD Eng. Waris Sultan (Exhibitions, 13-Jun), BIM Mgr Dr. Waleed Salah, QA/QC Mgr vacant, HSSE Mgr Eng. Mohamed Ahmed, Tech Office Mgr Eng. Mohamed Sultan, Proj Eng. Ahmed Salah, Arch. BIM Lead Eng. Ali Abdelrahman Mostafa (Samaya TO, Riyadh, formally on Aseer — 12+ yrs TO & BIM Mgr level), Procurement Hani Alghamdi, Doc Controller Eng. Hesham Abdelhamid.
§
Aseer materials.json uses lowercase keys (`description`, `finish`, `colour`, `supplier`, `substrate`) while individual schedule JSON files use Title Case. Always verify keys against materials.json, not the schedule files.
§
Viz app at github.com/sultandroid/aseer-museum-viz, live at samaya-factory.com/aseer/. Source: OneDrive/Kimi_Agent_Interactive.../app/. Shot layout per MOC-MUS-ASE-1A0-ZD-0031 Rev.01 (CG-approved 19-May-2026). Showcase info cards: compact, no size/dimension fields — only Type, ID, Exhibit, functional display fields (Glass Sides, AR, Lighting, Climate). Configured via SCHEDULE_FIELD_GROUPS in Gallery.tsx.
§
Use git for version control — initialize repo with `git init`, commit after every significant change, push to GitHub (`sultandroid` account) when asked. The Aseer Museum viz app is at github.com/sultandroid/aseer-museum-viz.
§
CG handling: email text status > PDF text. When CG contradicts own approved docs, reference doc number+date. CG reviewers (Mansour, Maged, Elbaz, Hossam) don't always coordinate — cross-check. Prefer sample approval before rendering to avoid double work. Check Riba 4 Remarks for past CG instructions.
§
Print PDF Samaya style: dark header #1A1D23, gold accent line, gold labels, footer. Use A3 landscape if A4 can't fit images without cropping. `object-fit: contain` on both clean & annotated views for pin alignment.
§
Deploy: scp -P 65002 dist/{index.html,assets/*.{js,css}} to hostinger build/aseer/. Build with `node build.mjs` (npm run build hangs on OneDrive JSON). Strip ALL `crossorigin` from dist/index.html (both script AND link tags) before deploy — Hostinger has no CORS headers, module scripts silently fail with empty error msgs.