# Aseer Museum — Document Source Mapping (Jul 2026)

Verified source-document mappings for the Design Management & BIM Execution Plan Summary (PL-0017).

## Document Status Hierarchy

| Source | Code | Status | Can Cite? |
|--------|------|--------|-----------|
| DMP Rev 02 | PL-0029 | **Code B — Approved** 19-May-2026 | Design sections |
| BEP Rev 01 | PL-0021 | **Code B — Approved** 17-Mar-2026 | BIM sections |
| Contract 0010003521 | — | **Signed** 01-Dec-2025 | All |
| PEP Rev 04 | PL-0015 | **For CG Approval** (not approved) | Avoid — submitted only |
| DMP Rev C03 | PL-0013 | **Issued for CG Resubmission** (not approved) | Avoid — submitted only |

Rule: Only cite approved documents. If content only exists in an unapproved doc, note that.

## Approved Source: DMP Rev 02 (PL-0029)

Primary source for all design management sections.

| Summary section | DMP section | Content |
|----------------|-------------|---------|
| 6 heading | 5, 6, 9 | Org, design process, interface mgmt |
| 6.1 Governance | 5 (Organization) | Org chart, roles, RACI matrix |
| 6.2 Stage Gates | 6.2 (Stage Gate Reviews) | Decision gates DG-0 to DG-7 |
| 6.2.3 Turnaround | 6.15.4 (Resolution Timeframes) | SLA: Design 10 WD, Shop 10/5, MS 5/2, Sub 10/5, RFI 5/2, CO 10 |
| 6.3 Drawing Submission | 6.3 (Submission Workflow), 12.9.1 (Numbering) | Review workflow, MOC-ASEER-SIC numbering |
| 6.4 Shop Drawings | 6.12 (Design-Construction Integration) | 8-step integration flow |
| 6.5 RFI | 6.3.2 (RFI/TQ Routing) | All queries logged to Register AA |
| 6.5.4 Comms | 6.14 (Communication and Reporting Plan) | Meeting cadence |
| 6.6 Interface | 9 (Interface Management) | Internal/external interfaces, penetration registers |
| KPI Framework | 15 (KPIs) | KPI framework overview, scorecard |

## PEP Rev 04 (PL-0015) — Unapproved, cite only for content not in DMP or BEP

| Content | PEP section |
|---------|------------|
| Interface Register INT-01 to INT-10 | 21.1 |
| MEP Cross-Trade Register INT-M01 to INT-M10 | 21.1.M |
| ICE Coordination Wheel (6-step) | 21.2 |
| Coordination Meetings | 21.3 |
| Drawing Register stats (~567 rows, ~158 Rev A) | 20 |
| Mock-Up Master Schedule (zone-based) | 11.5 |
| Aconex CDE registers | Submission Plan |
| Comms Cadence Ladder | 17 |

## BEP Rev 01 (PL-0021) — Approved

| Summary section | BEP section | Notes |
|----------------|-------------|-------|
| 7.1 Objectives | 2.1 | 6 generic objectives (not 7 specific) |
| 7.2 Software | 4 | Revit 2026, not 2025+. No Aconex in BEP. |
| 7.3 Naming | 6 | ISO 19650 naming; BEP uses different file template |
| 7.4 LOD | 2.3 + 8.7 | LOD 350/400/500 values match; gate mapping differs |
| 7.5 Clash | 7 | 4 severity levels (Critical 24h, High 3WD, Med 1WK, Low) |
| 7.6.2 CDE Codes | 6.3-6.4 | ISO 19650 sub-codes S0-S4, A1-A7, AR |

## Contract 0010003521

| Ref | Content | Verified? |
|-----|---------|-----------|
| Sec 4, Art 1 | General obligations (permits, quality, site, insurance) | Yes |
| Sec 4, Art 2 | Not found in extracted Sec 4 file | Unverified |
| SoW 5.5 | Key Personnel include Design and BIM Manager | Yes |
| SoW 6.20 | BIM model requirements, LOD, clash detection | Yes |
| SoW 8.1 | General Requirements (management/planning) | Yes |

What is NOT in Contract Sec 4:
- Day+1/+3/+5 escalation protocol (project-developed procedure)
- RFI classification TQ/SI/NCR/Authority types
- Review turnaround times

## CG Review Codes (Verified from ZD-0006)

| Code | Meaning |
|------|---------|
| A | Approved |
| B | Approved with Comments |
| C | Revise and Resubmit |
| D | Rejected |

Codes E, F, U are internal project statuses, NOT CG codes.

## KPI Targets (No Source — Internal to Summary)

| KPI | Target |
|-----|--------|
| K-1 | CDE adoption 100% |
| K-3 | RFI average response 7 WD or less |
| K-5 | MoM turnaround 48h or less, 95%+ compliance |
| K-7 | L4+ escalations less than 4 per quarter |
| K-8 | NCR closure 30 WD average or less |

These targets exist only in the Summary document. Not found in PEP, BEP, DMP, or any other project plan.

## Source Documents Saved as MD in Repo

| Original File | MD Location |
|---------------|-------------|
| CG Baseline Schedule Review ZD-0006 | 02.3_PEP/03_Supplementary/CG_Baseline_Schedule_Review_MOC-MUS-ASE-1K0-ZD-0006.md |
| CG Site Instruction SI-CG-ASEER-007 Rev.02 | 05_SIs/05.1_Instructions/SI-CG-ASEER-007_Rev02.md |
| SoW extracted text | 01.3_Contractors_SOW/SoW_Extracted.md |
| DMP Rev 02 CG Approval form | 02.1_DMP/03_Registers_and_Lists/DMP_Rev02_CG_Approval.md |
| Contract Sec 4 EN | 01_Contracts/01_Main_Contract/Contract_0010003521_Sec4_Contractor_Responsibilities_EN.md |

## Common Pitfalls

1. DMP section numbers differ from Summary claims: The Summary originally cited DMP sections 4-7 for content that was actually in DMP sections 5, 6, 9, 12, 15. Always verify section numbers against the actual DMP TOC.
2. PEP is not approved: The PEP Rev 04 is For CG Approval only. Do not cite as an authoritative source. Replace with DMP refs where possible.
3. CG codes only A/B/C/D: The CG rule defines only 4 codes. E, F, U are internal project codes.
4. Aconex not in BEP: The BEP specifies Autodesk BIM 360/Docs as its CDE. Aconex presence in the Summary comes from PEP section 18.1, not BEP.
5. Software versions: BEP specifies Revit 2026; Summary says 2025+.
6. KPI targets have no source: K-1/K-3/K-5/K-7/K-8 are internal to the Summary document. Not found in any project plan.

## PEP Rev 04 (MOC-ASEER-SIC-1K0-PL-0015)

| Section | Content | PEP Source |
|---------|---------|------------|
| 4 | Stage Gate & Cost Control | §4.1 G0-G8 gates (3-tier: Critical/Hard/Procedural) |
| 5 | Project Organization | §5.1 4-tier org chart, BIM Mgr dual-reporting line |
| 8 | Execution by Discipline | §8.3 Exhibition Systems |
| 9 | BIM & Digital Delivery | §9.1 LOD 200/350/400/500, §9.2 BIM Ownership |
| 11 | Procurement | §11.5 Mock-Up Master Schedule (68 mock-ups, 8 cluster gates) |
| 17 | Communications | §17.1 Comms Cadence Ladder (daily/weekly/monthly) |
| 18 | Document Control | §18.2 MOC-ASEER-SIC numbering, §18.3 revision control |
| 19 | Engineering & Shop Drawings | §19.1 8-step workflow, 14-day standard |
| 20 | Review Procedure | §20.1 turnaround SLA (10/5 WD, 5/2 WD, etc.) |
| 21 | Coordination & Interface | §21.1 INT-01 to INT-10, §21.1.M INT-M01 to INT-M10, §21.2 ICE Wheel (6-step), §21.3 Coordination Meetings |

**Note:** PEP §4.1 gate model has different names than Summary. PEP gates: G0=Contract Award, G1=DD Complete, G2=IFC/AFC NOC, G3=Submittal/Mock-up, G4=First Fix, G5=Finishes, G6=Exhibition Systems, G7=Commissioning, G8=Final Handover. Timeline extends through W52 but contract end is W43 (Sep-2026).

## BEP Rev 01 (MOC-ASEER-SIC-1K0-PL-0021)

| Summary claims | BEP actual section |
|----------------|-------------------|
| §7.1 BIM objectives ← BEP §3 | BEP §2.1 (6 generic objectives, no metrics/owners) |
| §7.2 Software ← BEP §5 | BEP §4 (Revit 2026, Navisworks 2026, no Aconex) |
| §7.3 Naming ← BEP §6 | BEP §6 (file naming uses 041-SIC-XX-XX-3DM-AR-50001 format) |
| §7.4 LOD ← BEP §7 | BEP §2.3 + §8.7 (LOD 350/400/500 values match; gate mapping differs) |
| §7.5 Clash ← BEP §8 | BEP §7 (4 severity levels: Critical 24h / High 3WD / Medium 1WK / Low) |
| §7.6 CDE ← BEP §9 | BEP §6.3-6.4 (ISO 19650 containers WIP/S0-S4/A1-A7/AR) |

**Key mismatches:**
- Aconex not mentioned anywhere in BEP. BEP CDE = Autodesk BIM 360 / Autodesk Docs.
- Software versions: BEP says 2026, Summary says 2025+.
- KPIs K-1/K-5/K-7/K-8 are not in BEP. BEP Table 104 defines different metrics.
- Clash severity: BEP has 4 levels, Summary has 3. BEP Critical=24h, Summary says 48h.
- Legal entity in BEP: "Samaya Investment Company" not "Samaya Investment".

## Contract 0010003521

| Section | Content |
|---------|---------|
| Sec 4, Art 1 | General obligations (permits, quality, site, insurance) |
| Sec 4, Art 2 | Not found in the Sec 4 file — may be in a different section |
| Sec 4, Art 10-13 | Electricity/water, properties, worksite, insurance |

**What is NOT in Contract Sec 4:**
- Day+1/+3/+5 escalation protocol (project-developed procedure)
- RFI classification TQ/SI/NCR/Authority types
- Review turnaround times

## CG Submission Rule (MOC-MUS-ASE-1K0-ZD-0006)

Verified status codes from the CG rule document (Rev 05, approved Code B 12-Jul-2026):

| Code | Status |
|------|--------|
| A | Approved |
| B | Approved with comments |
| C | Revise and Resubmit |
| D | Rejected |

**Codes E, F, U are NOT CG codes.** They are internal project statuses only. Always check the actual CG rule document before claiming code definitions.

## SoW (Contract 0010003521 — Statement of Work)

| Clause | Content | Used For |
|--------|---------|----------|
| 5.5 | Staffing and Deployments — Key Personnel include Design & BIM Manager | Design & BIM Manager role reference |
| 6.20 | BIM — model requirements, LOD, clash detection, weekly updates | BIM Manager responsibilities |
| 6.20.1 | BIM Resources — licensed Revit/Navisworks, skilled staff | Software requirements |
| 8.1 | General Requirements (Part 3: Off-Site Fabrication) | MEP Coord (management/planning) |

**Note:** SoW 8.1 is a general management clause ("all management, control, administration and planning"), not MEP-specific.

## Programme Baseline (Time Schedule Rev.05)

- Approved by PMC with Code B on 12-Jul-2026
- CG Response Date: 05-Apr-2026 (for earlier revision)
- CG Project Director: Mohammed Elbaz

## References
- Summary doc: `02.3_PEP/01_Source_Files/03_Word/ASM_Design_Management_and_BIM_Execution_Plan_Summary.docx`
- PEP source: `02.3_PEP/01_Source_Files/01_HTML/00_PEP_Plan_Rev04.html`
- BEP source: `02.2_BEP_MIDP_TIDP/01_Source_Files/03_Word/00-BIM-Execution-Plan-REV 01.docx`
- Contract: `01_Contracts/01_Main_Contract/Contract_0010003521_Sec4_Contractor_Responsibilities_EN.md`
- Full contract ref: `01_Contracts/01_Main_Contract/CONTRACT_REFERENCE.md`
