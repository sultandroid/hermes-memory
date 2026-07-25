# PEP / BEP / DMP Section Mapping — Aseer Museum

Actual section mappings verified against source documents (Jul 2026).

## PEP Rev 04 (PL-0015)

| Topic | Common Mis-Reference | Actual Section |
|-------|---------------------|----------------|
| Stage gates G0-G8 | sec 18 | sec 4.1 |
| Programme gates PG1-PG4 | sec 18 | sec 4.1 |
| Org structure, governance roles | — | sec 5.1 |
| BIM integration | — | sec 9 |
| Document numbering | sec 20 | sec 18.2 |
| Revision control | sec 20 | sec 18.3 |
| CDE / Aconex registers | — | sec 18.1 |
| Shop drawing process | — | sec 19.1 |
| Submission turnaround SLA | — | sec 19.1, sec 20.1 |
| Review procedure | — | sec 20 |
| RFI management | sec 21 | sec 17.1 (native Aconex, no standalone workflow) |
| Communication hierarchy | sec 21 (C1-C5 claimed) | sec 17 (Comms Cadence Ladder - Daily/Weekly/Monthly) |
| KPI targets | — | sec 17.1 dashboard cards |
| Legal entity naming | — | sec 4 |
| Interface coordination | — | sec 4.1 (delivery spine) |

## BEP Rev 01 (PL-0021)

| Topic | Common Mis-Reference | Actual Section |
|-------|---------------------|----------------|
| BIM objectives | sec 3 | sec 2.1 |
| Software / technology | sec 5 | sec 4 |
| Naming conventions | — | sec 6 |
| LOD matrix | sec 7 | sec 2.3 + sec 8.7 |
| Clash detection | sec 8 | sec 7 (with 4 severity levels, not 3) |
| CDE / BIM 360 | sec 9 | sec 6.3-6.4 (not Aconex) |
| QA/QC | sec 9 | sec 9 |

Key notes:
- Aconex is NOT mentioned in BEP. BEP specifies Autodesk BIM 360 / Autodesk Docs.
- Software versions in BEP are 2026 (Revit, Navisworks, ReCap), not 2025+.
- Clash severity: 4 levels (Critical 24h / High 3WD / Medium 1WK / Low next-milestone), not 3.
- K-coded KPIs (K-1, K-3, K-5, K-7, K-8) are not in BEP. BEP Table 104 has different CDE metrics.
- BEP uses "Samaya Investment Company" (full name), not "Samaya Investment".

## DMP Rev C03 (PL-0013)

| Claim | Verdict |
|-------|---------|
| Section 4 defines stage gates | FALSE — DMP does not define G0-G8 |
| Section 5 defines document numbering | FALSE — numbering is in PEP sec 18.2 |
| Section 6 defines submission turnaround | FALSE — turnaround is in PEP sec 19.1/sec 20.1 |
| Section 7 defines ICE wheel + INT interfaces | FALSE — ICE wheel is project-developed, INT registers are project-developed |

The DMP Rev C03 contains design management procedures but does NOT contain operational process tables for gates, numbering, turnaround, or coordination interfaces. Those are in PEP Rev 04.
