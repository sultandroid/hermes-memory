Repo (~/aseer-museum-pm) is single source of truth for plan content — check before OneDrive files. ER/SoW compliance only, no Mostadam rating targets. CR registers: Excel, Open/Closed status. Fida's SMP: construction-phase focus, MOSTADAM Bronze framing — fix only contradictions (waste 60%, Oddy 14-day), keep his language.
§
SMP decisions per ER/SoW only: waste diversion 60% (not 75%), Oddy aging 14-day (not 49-day), code-compliance framing (not rating-target). 'Sustainability Specialist' preferred over 'Sustainability Manager' per Adel Darwish's comment.
§
DOCX: use Word heading styles (H1/H2/H3), RGB PNG images (not RGBA), cantSplit on tables, 9pt halftone #64748B for remark paragraphs. If images don't render in Word, replace SVG charts with styled tables.
§
ProLab Trading LLC (TRN 100552354100003) is UAE/Dubai distributor — NOT KSA. Aseer PQ register next free: PQ-0113 (after PQ-0112 Q-Sys NMK). OneDrive `Adel Darwish's files/07- Pre-Qualification Submittal/` blocks mkdir from terminal (uid mismatch) — create new PQ subfolders via onedrive.live.com web UI and copy files manually.
§
When determining scope boundaries between specialists, always check BOTH the SoW text AND the specialist's own submittal register. The SoW may list a narrow scope, but the CG-approved scope or the specialist's own deliverable schedule may extend it. Example: ZNA's SoW lists interior areas only, but CG comment #1 requires "all project different lighting systems, spaces" and ZNA's submittal register includes LG-024 "Exterior lighting design" under SoW §8.8. Never assume scope from the SoW alone.
§
DOCX generation: SVG charts must be rendered as RGB PNGs (not RGBA) via cairosvg + Pillow RGBA→RGB conversion, then embedded via python-docx add_picture(). Fix empty cNvPr names and add noChangeAspect for Word compatibility.
§
HTML page overflow fix: use CSS classes compact/tight/xtight on .page sections. xtight only for pages >75% density. Measure with table_rows*10 + svgs*100 + text*0.03 vs ~1972px available.
§
CG comment disposition: reference attached CR sheet only, never list full CG comments inline in the document. Remove 1.4 CG Comment Disposition Matrix section entirely.