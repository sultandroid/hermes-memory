# Aseer Museum — Design Phase Risk Register (24 Evidence-Based Risks)

## Context

Built Jun 2026 for Aseer Regional Museum (Samaya Group, project 219). Contract: MoC × Samaya, lump-sum, NTP 01-Dec-25, complete 07-Sep-26. NRS (A2742) = interior arch + scenography. Rawasin = AV/IT/interactives per T2-09. CG PM: Elbaz.

## Source Mining

All 24 risks sourced from 4 project memory files (in order of yield):

| Source | Risks Extracted | Type of Data Mined |
|--------|----------------|-------------------|
| `PROJECT_MEMORY.md` (84KB, 1209 lines) | 10 | Dispute timelines, staffing gaps, meetings log, technical decisions, knowledge gaps |
| `disputes_and_rejections.md` (12KB, 152 lines) | 6 | SI-007 timeline, DMP rejection cycle, IFC-0004 block, Code-C inventory, fire pump NFPA |
| `code_c_d_inventory.md` (11KB, 119 lines) | 4 | Active Code-C submittals (10 items), resolved/rejected cycles, aggregate counts |
| `itc_integrity_technology.md` (8KB, 153 lines) | 4 | ITC variation claim, scope exclusions, symmetric renegotiation pattern |

Each Description field in the risk register includes the source reference for auditability.

## Risk Data Structure

```
Risk ID (R-D001 to R-D024)
RBS Code (RBS-1.1 through RBS-5.5)
Risk Category (Technical/Design, Programme/Schedule, Resources/Personnel, Commercial/Contractual, External/Environmental)
Risk Title (descriptive, references the actual SI/NCR/event number)
Description (Cause → Consequence narrative with project-specific details)
Probability (1-5)
Impact (1-5)
Response Strategy (Mitigate/Escalate/Accept)
Mitigation Measures (specific actions with dates and owners)
Owner
Status (Open/In Progress)
Target Date
```

## Severity Thresholds Used

| Severity | P×I Range | Count in Register |
|----------|-----------|-------------------|
| Critical (C) | 20-25 | 3 |
| High (H) | 10-19 | 19 |
| Medium (M) | 5-9 | 2 |
| Low (L) | 1-4 | 0 |

Calibration note: The 14-column design-phase register uses broader H/M bands (H≥10, M≥5) vs the 24-column full register (H≥12, M≥8). The lighter scoring suits phase-level granularity.

## RBS Used (5 categories, design-phase specific)

| Code | Category | Count |
|------|----------|-------|
| RBS-1.x | Technical / Design | 9 |
| RBS-2.x | Programme / Schedule | 4 |
| RBS-3.x | Resources / Personnel | 3 |
| RBS-4.x | Commercial / Contractual | 3 |
| RBS-5.x | External / Environmental | 5 |

## Workbook Structure

**Sheet 1 — Summary:**
- Merged title row
- Total count, C/H/M/L breakdown
- Distribution by RBS Category
- Source citation note

**Sheet 2 — Risk Register:**
- 14 columns with data validation dropdowns on: Severity (C,H,M,L,E), Probability (1-5), Impact (1-5), Status (Open,In Progress,Review,Closed), Response Strategy (Avoid,Mitigate,Transfer,Accept,Escalate)
- Freeze panes at A2, auto-filter on all columns
- Navy header (#1E293B), white/yellow alternating rows (FFF8DC)
- Severity column: red fill for C, orange for H, gold for M
- Status column: red tint (#FFE0E0) for Open, yellow tint (#FFF3CD) for In Progress
- Risk Score = P×I (computed, not hardcoded)

## Top 3 Critical Risks (P×I=20)

| ID | Risk | Evidence Source |
|----|------|----------------|
| R-D001 | SI-CG-ASEER-007: CG mandates 3D Render → Material Board → IFC | SI-007 upheld across 2 rounds, Samaya rebuttal, Article 16 dispute |
| R-D004 | NRS vs Rawasin (AV/IT) Interface Gap | Contract executed, Interface Register not formalised, Light box positions locked immutable |
| R-D020 | NCR-003 (NC-1E0-003) UNREAD | Email from Sundus Alfeer (24-May) unread, JSI 009/011 violations ongoing, partial site evacuation |

## Next Phases to Build (not yet created)

When the user requests:

- **Procurement Phase** — supplier onboarding delays, subcontractor PQQ rejections, long-lead showcase procurement, material sample approvals, BOQ zero-rates
- **Construction Phase** — site HSE incidents (FACP disconnection), microcement stoppage, MEP FCU damage, glass works Final Notice, site manpower shortage
- **Handover/Commissioning** — Civil Defence NOC, authority approvals, testing & commissioning, snagging, documentation handover
