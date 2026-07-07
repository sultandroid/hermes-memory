# MOS Page Layout Patterns — Aseer Museum LiDAR Survey

## Page Map (Final: 15 + 1 appendix)

| Page | Content | Section |
|------|---------|---------|
| 01 | Cover / Document Control & QC Sign-Off | — |
| 02 | Table of Contents | — |
| 03 | Introduction + Scope (4 Scan Rounds summary cards + level table) | 1–2 |
| 04 | Scan Rounds Schedule (Gantt bars table) + Inclusions/Exclusions | 2 cont. |
| 05 | Equipment Specs — Faro Focus Premium (spec strip + performance table) | 3 (1/2) |
| 06 | Support Equipment table (8 items) + Section 4 Surrounding Area (Element table, Neighbors 14-row table) | 3 (2/2) + 4 |
| 07 | 360° HDR Imagery + Point Cloud Workflow (5-stage pipeline SVG) | 5 & 6 |
| 08 | Execution Methodology — Pre-Mob through Field QC (7.1–7.5) | 7 (1/2) |
| 09 | Demobilisation + Project Team + Section 8 heading + 8.1 Registration | 7 cont. + 8 (1/2) |
| 10 | Post-Processing, Cross-Sections, Export table + SVG flowchart | 8 (2/2) |
| 11 | BIM Integration — Setup, LOD500 Modeling, 2D Drawing extraction, CDE folder | 9 |
| 12 | QC Plan — Stage 1–3 validation + Process overview | 10 (1/2) |
| 13 | Non-Conformance Procedure + QC Documentation list | 10 (2/2) |
| 14 | HSE Policy + Risk Register (11 items) + PPE + Emergency Contacts | 11 |
| 15 | Deliverables Schedule — Round A parallel tracks + Overall Schedule + Delivery Method | 12 |
| B1 | Appendix B — Certifications table (2 entries) | B |

## Merge Patterns Used

- **Pages 6+7 merged**: Support Equipment (sparse, 8-row table) + Section 4 Surrounding Area (7-row element table + 14-row neighbors table). Neighbors table font compressed to 0.48rem, paragraph to 0.5rem.
- **Pages 9+10 balanced**: Moved Section 8 heading + 8.1 Registration (7-step table) to page 9 to fill empty space below Project Team table. Page 10 keeps 8.2–8.4 + SVG.
- **Section 13 removed**: Approval & Sign-off page deleted entirely — cover page already carries Prepared/Reviewed/Approved. TOC "5 — APPROVAL" group heading removed.

## Font Size Guide for Compression

When merging dense content onto one A4 page:
- Neighbors-style tables: 0.48rem (vs default 0.46rem for eng-table)
- Intro paragraphs: 0.5rem (vs default 0.55rem body)
- Table cell padding: keep at CSS default 3px 6px — don't reduce further
- Section banners: keep at default
