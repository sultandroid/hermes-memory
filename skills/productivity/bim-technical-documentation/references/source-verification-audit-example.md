# Source-Verification Audit Example — Design Management & BIM Summary vs PEP/DMP/BEP

**Session:** 25-Jul-2026  
**Audited:** `ASM_Design_Management_and_BIM_Execution_Plan_Summary.docx` (MOC-ASEER-SIC-1K0-PL-0017 Rev 01)  
**Sources:** PEP Rev 04 (PL-0015), DMP Rev C03 (PL-0013), BEP Rev 01 (PL-0021)

## Methodology

1. Extracted all source-referenced claims from the Summary (42 halftone annotation lines)
2. Grouped by source document: PEP (20 claims), DMP (4 claims), BEP (12 claims)
3. Dispatched 3 parallel sub-agents via `delegate_task`, each reading one source document
4. Each sub-agent extracted actual data from source sections and compared against Summary claims
5. Integrated findings into a consolidated discrepancy report
6. Fixed all mismatches in one pass

## Key Findings

| Source | Total Claims | MATCH | PARTIAL | NOT_FOUND | MISMATCH |
|--------|-------------|-------|---------|-----------|----------|
| PEP Rev 04 | ~20 | 5 | 3 | 4 | 8 |
| DMP Rev C03 | 4 | 0 | 0 | 0 | 4 (all wrong) |
| BEP Rev 01 | 12 | 0 | 5 | 2 | 6 |

## Specific Issues Found

### Wrong Section References (8 occurrences)

| Summary claim | Actual section in source |
|---|---|
| PEP §18 (gates) | PEP §4.1 |
| PEP §20 (numbering) | PEP §18.2 |
| PEP §21 (RFI) | PEP §17.1 |
| BEP §3 (objectives) | BEP §2.1 |
| BEP §5 (software) | BEP §4 |
| BEP §7 (LOD) | BEP §2.3 + §8.7 |
| BEP §8 (clash) | BEP §7 |
| BEP §9 (CDE) | BEP §6 / PEP §18.1 |

### Content Not Found in Source (10 occurrences)

| Claim | Source claimed | Actual |
|---|---|---|
| ICE coordination wheel | DMP §7 | Not in DMP |
| INT-01 to INT-M10 interfaces | DMP §7 | Not in DMP |
| C1–C5 communication hierarchy | PEP §21 | PEP uses Comms Cadence Ladder |
| Status codes D/E/F/U | PEP §20 | PEP defines A/B/C only |
| RFI step-by-step workflow | PEP §21 | No standalone procedure |
| Escalation Day+1/+3/+5 | PEP §19 | Not tabulated |
| BIM 7-objective table with owners | BEP §3 | BEP has 6 generic objectives |
| K-1/K-5/K-7/K-8 targets | BEP §9 | Different KPIs in BEP |
| Dual-platform CDE (ACC+Aconex) | BEP §9 | BEP uses BIM 360 only |
| Zone codes BF/LGF/GF/1F/RF/LS | BEP §6 | Not in BEP |

### Data Discrepancies (6 occurrences)

| Claim | Summary value | Source value |
|---|---|---|
| Software version | 2025+ | 2026 |
| Clash severity levels | 3 (Critical/Major/Minor) | 4 (Critical/High/Medium/Low) |
| Clash SLA Critical | 48 hours | 24 hours |
| Clash SLA Major | 7 WD | 3 WD (High) |
| Legal entity | "Samaya Investment" | "Samaya Investment Company" (BEP) |
| LOD matrix format | Discipline-by-gate table | Element-level matrix |

## Corrective Actions Applied

1. All 42 halftone refs rewritten with correct section numbers
2. False DMP refs (7) replaced with PEP §4.1 or "project-developed" attribution
3. BEP section refs shifted: §3→§2.1, §5→§4, §7→§2.3+§8.7, §8→§7, §9→§6
4. Software version caveated: "2026, not 2025+"
5. Aconex CDE refs redirected to PEP §18.1 (Aconex not in BEP)
6. Caveats added where Summary deviates from source (3-level vs 4-level severity, etc.)
7. Body text intro sections corrected to match actual PEP sections

## Pitfalls for Future Sessions

- **Wrong file path for source doc** — the DMP PDF found at `02.2_BEP_MIDP_TIDP/` was a submittal form, not the actual DMP. The real DMP was at `02.1_DMP/`. Always check page 1 content before dispatching.
- **Section numbering offset** — external section labels in Task Info Boxes may not match actual document section numbering. Verify by reading the source heading.
- **Aconex not in BEP** — The BEP specifies Autodesk BIM 360 as the CDE. Do not cite BEP for Aconex-related content.
- **KPI targets may come from a different source** — K-coded KPIs (K-1, K-3, K-5, K-7, K-8) appear in the KPI Dashboard, not in the BEP. Verify source before attributing.
- **Software versions are easy to guess wrong** — always extract the actual version string from the source. "2025+" vs "2026" is a 1-year difference that matters for procurement.
