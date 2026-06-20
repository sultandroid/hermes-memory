Aseer Museum team (SMP Rev03): PD Eng. Waris Sultan (Exhibitions, 13-Jun), BIM Mgr Dr. Waleed Salah, QA/QC Mgr vacant, HSSE Mgr Eng. Mohamed Ahmed, Tech Office Mgr Eng. Mohamed Sultan, Proj Eng. Ahmed Salah, Arch. BIM Lead Eng. Ali Abdelrahman Mostafa (Samaya TO, Riyadh, formally on Aseer — 12+ yrs TO & BIM Mgr level), Procurement Hani Alghamdi, Doc Controller Eng. Hesham Abdelhamid.
§
Aseer finishes suppliers: Ceramiche Piemme, Concept Tiles, Domus, Tarkett, Asona, Knauf, Kvadrat, Clay-works, Corian, Hi Macs, Smile Plastics, Valchromat, Viroc, ARPA, GF Smith. Source: Pre-Appointment Exhibition Schedules.
§
Viz app at github.com/sultandroid/aseer-museum-viz, live at samaya-factory.com/aseer/. Source: OneDrive/Kimi_Agent_Interactive.../app/. Shot layout per MOC-MUS-ASE-1A0-ZD-0031 Rev.01 (CG-approved 19-May-2026). Showcase info cards: compact, no size/dimension fields — only Type, ID, Exhibit, functional display fields (Glass Sides, AR, Lighting, Climate). Configured via SCHEDULE_FIELD_GROUPS in Gallery.tsx.
§
Appendix B = authoritative specialist packages. BIM Mgr: weekly online coord + monthly visits + on-site support: Eng. Ali A. Mostafa. No PMBOK/WBS. Only Riyadh/Abha. "Pending submission" = on board.
§
CG handling: email > PDF. "Pending submission" = on board, keep name. No "pending MoC"/"Overseas"/"Code C"/"on-site". No PMBOK/WBS/RBS. Materials from schedules not generic. Only Riyadh/Abha. Appendix B authoritative for specialist packages. CG site instruction = include with remark. Check Register Log (xlsb) for doc status. Keep KPR + plans in sync.
§
Print PDF Samaya style: dark header #1A1D23, gold accent line, gold labels, footer. Use A3 landscape if A4 can't fit images without cropping. `object-fit: contain` on both clean & annotated views for pin alignment.
§
Deploy: scp -P 65002 dist/{index.html,assets/*.{js,css}} to hostinger build/aseer/. Build with `node build.mjs` (npm run build hangs on OneDrive JSON). Strip ALL `crossorigin` from dist/index.html (both script AND link tags) before deploy — Hostinger has no CORS headers, module scripts silently fail with empty error msgs.