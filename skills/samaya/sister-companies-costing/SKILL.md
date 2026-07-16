---
name: sister-companies-costing
title: Sister Companies — Costing Reports & SysLeaders Data
description: Build and maintain costing reports for Samaya's sister company projects (12 retail stores/cafes). Pull PO and labor data from SysLeaders, build Factory Work reports, manage the _Final folder structure, and handle cross-project cost reallocation.
triggers:
  - User mentions "Sister Companies" costing or reports
  - User asks to pull data from sysleaders.com/samaya
  - User asks to build Factory Work reports for a project (01-13)
  - User references the `_Final` folder or `Reports/Sister_Companies/`
  - User asks about cross-project cost reallocation between stores
---

# Sister Companies — Costing Reports

## Overview
12 retail projects (stores, cafes, gift shops) under 4 client companies. Each project has accounting costs (Ibrahim Shaban invoices), factory costs (POs + labor + fleet), and 10% engineering supervision. Cross-project reallocation moves costs between projects based on actual beneficiary.

## Project Map

| Code | Project | Client | JN | Area (m2) |
|------|---------|--------|----|-----------|
| 01 | Al Wahi Gift Shop | Tiba Gift | 367 | 240 |
| 02 | Holy Quran Gift Shop | Tiba Gift | 367 | 194 |
| 03 | Qahwatna Cafe | Qahwitna | — | — |
| 04 | Hira Cafe | Qahwitna | — | — |
| 05 | Jabal Omar VIP Stores | — | — | — |
| 06 | As Safiyyah Giftshop | Tiba Gift | — | — |
| 07 | Khair Al-Khalq Store | Tiba Gift | 403 | 173 |
| 08 | Qahwatna Al-Safiya Cafe | Qahwitna | — | — |
| 09 | Tzkarat Store | Tezkarat | — | 51 |
| 10 | Rateeb Store | Rateeb | 282 | 42 |
| 11 | Najdi Coffee | Qahwitna | — | — |
| 12 | Ice Coffee Shop | — | — | — |
| 13 | Hera Visitor Center | — | — | — |

## Paths
```
Base: ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Reports/Sister_Companies/
_Final: .../Sister_Companies/_Final/ (per-client folders)
Projects: .../Sister_Companies/{NN}_{Project_Name}/
Dashboard: .../Sister_Companies/_Management/Stores_Coffee_Shops_Dashboard.xlsx
```

## Cost Components Per Project
1. **Accounting Statement** — Ibrahim Shaban invoices, classified by category (construction/equipment/operations)
2. **Reallocation** — costs moved out to other projects + costs received from other projects
3. **Factory Cost** — POs (SysLeaders) + Labor + Fleet/Transport
4. **Supervision** — 10% of (Accounting + Factory) total
5. **Grand Total** — Accounting (net) + Factory + Supervision

## _Final Folder Structure
```
_Final/
├── Tiba Gift comp_/       (01, 02, 06, 07)
├── Qahwitna comp_/        (03, 04, 08, 11)
├── Tezkarat Trading Com_/ (09)
└── Rateeb Trading Com_/   (10)
```

## SysLeaders Data Extraction
See `references/sysleaders-access.md` for login, navigation, PO extraction, and project filtering patterns.

## Factory Work Report Template
See `references/factory-work-report-template.md` for the 3-sheet Excel structure.

## Key Rules
- **Supervision = 10% of (Accounting + Factory)** — apply to the sum, not just factory cost
- **All totals formula-based** — no hardcoded numbers in _Final files
- **Equipment and Operations** items go in separate sheets (not mixed with construction)
- **Shared items** split by area percentage; equal split when area unknown
- **Factory labor** from FCA analysis aggregated as one "Factory Labor Cost" line
- **Header** on every file: project name, location, area, JN, code

## Pitfalls
- SysLeaders project dropdown uses Arabic names — search by "التمور" for Rateeb, not "Rateeb"
- SysLeaders POs page path=49 is for project 49 (Rateeb) — path varies per project
- Archived task data may have labor costs embedded in BOQ unit prices — cross-check with FCA
- OneDrive sync can lock files — write to temp and copy
- Never delete/move OneDrive files with `mv` or `rm -rf` — corrupts sync
