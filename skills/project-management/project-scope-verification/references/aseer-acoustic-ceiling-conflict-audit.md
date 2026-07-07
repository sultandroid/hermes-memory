# Aseer Museum Acoustic Ceiling RFP — Cross-Contract Conflict Audit (Worked Example)

**Date:** 2026-07-03  
**RFP:** RFP-ASEER-AC-001 (Acoustic Ceiling Finishes Package)  
**Scope:** 3,211 m² across 6 finish codes (FI_CL_01–09)  
**Products:** BoSpray 25mm, BoCoustic 40mm, USG Celebretto baffles, Kvadrat Soft Cells, plasterboard ceilings

## Methodology

This audit followed the Cross-Contract Scope Conflict Audit workflow in the parent skill. Steps taken:

1. Read the Acoustic Ceiling RFP (SPEC.md, SCOPE_REQUEST.md, RFP_Acoustic_Ceiling_Package.xlsx)
2. Identified 7 affected subcontractors from the project directory
3. Read each subcontractor's scope documents (SPEC.md, SCOPE_REQUEST.md, SOWs)
4. Searched for acoustic-related references across all subcontractor files
5. Identified 12 conflicts across 4 types: physical incompatibility, scope gap, responsibility ambiguity, and sequencing risk
6. Cross-referenced against open issues (NRS Fire Alarm Comments Disposition Register)

## Conflict Register

### C-01 | MEP Contractor (10) — Duct Silencer Supply & NR 30 Compliance
- **Type:** Scope gap
- **Issue:** NR 30 target in galleries requires duct silencers. MEP Contractor BoQ has no silencer line items. MEP Designer (13) specifies silencers (design only). Acoustic specialist (not appointed) would specify silencers. No one supplies/installs them.
- **Severity:** 🔴 High
- **Resolution:** Add duct silencer line items to MEP Contractor BoQ. Make silencer supply/install a conditional gate.

### C-02 | MEP Contractor (10) — Sprinkler Integration in Acoustic Ceilings
- **Type:** Physical incompatibility
- **Issue:** BoSpray spray-on, BoCoustic seamless plaster, and Kvadrat Soft Cells fabric are not designed for sprinkler head penetration. No cut-out details in RFP.
- **Severity:** 🔴 High
- **Resolution:** Add sprinkler cut-out details to RFP D4. Require RCP federation @ LOD 300.

### C-03 | FLS Specialist (11) — PAVA Speaker & Detector Mounting
- **Type:** Physical incompatibility (already open issue F-03)
- **Issue:** Kvadrat Soft Cells (65 m²) and BoCoustic (40 mm, 120 m²) cannot support PAVA speakers or fire detectors. NRS already flagged F-03: "Detectors in fabric acoustic ceiling — unsuitable mounting surface."
- **Severity:** 🔴 High
- **Resolution:** Confirm ceiling finish for all Soft Cells/BoCoustic areas. Provide solid mounting plates or relocate to adjacent solid ceiling. Close F-03 before RFP award.

### C-04 | AV/IT Contractor (04) — 51 Ceiling Speakers in Acoustic Ceilings
- **Type:** Physical incompatibility
- **Issue:** 51 Yamaha VXC6 ceiling speakers need solid mounting. BoSpray cannot support weight. BoCoustic needs pre-formed recesses. Soft Cells cannot support speakers. AV "Coordinated Ceiling Plans" are PENDING.
- **Severity:** 🔴 High
- **Resolution:** Add speaker cut-out/integration to RFP D4. Coordinate speaker placement with acoustic modelling (Treble simulation).

### C-05 | Structural Contractor (12) — Baffle Suspension Loading
- **Type:** Responsibility ambiguity
- **Issue:** 1,653 m² of USG Celebretto baffles need M6 rod suspension from slab. RFP D5 requires acoustic contractor to provide fixing schedule. Unclear who provides slab anchors — Structural or Rigging contractor.
- **Severity:** 🔴 High
- **Resolution:** Clarify scope split: acoustic contractor provides fixing schedule + load calcs; Structural/Rigging provides slab anchors + pull-out testing.

### C-06 | Lighting Designer (02) — "Integrated Lighting" Undefined
- **Type:** Responsibility ambiguity
- **Issue:** FI_CL_01 (1,332 m²) and FI_CL_06 (41 m²) described as "with integrated lighting" — undefined whether embedded in panels or accommodated via cut-outs.
- **Severity:** 🟡 Medium
- **Resolution:** Define "integrated lighting" in RFP. Require Lighting Designer to provide cut-out locations.

### C-07 | CITC Telecom / BMS-ICT — WAP Mounting in Acoustic Ceilings
- **Type:** Physical incompatibility
- **Issue:** 43 WAPs need solid mounting. Soft Cells and BoCoustic areas cannot support WAPs without modification.
- **Severity:** 🟡 Medium
- **Resolution:** Add acoustic ceiling contractor to BMS/ICT coordination. Provide solid mounting plates in Soft Cells/BoCoustic areas.

### C-08 | Showcases Contractor (05) — Ceiling Interface
- **Type:** Physical incompatibility (limited)
- **Issue:** Floor-to-ceiling display cases interface with acoustic ceiling. No standard detail in RFP.
- **Severity:** 🟢 Low
- **Resolution:** Add standard ceiling-to-showcase interface detail (trim, seal, acoustic sealant).

### C-09 | Rigging Contractor (06) — Baffle Suspension Overlap
- **Type:** Scope overlap
- **Issue:** Rigging scope includes "ceiling grid, suspension points" and "any steel for ceilings." Acoustic baffle suspension not explicitly mentioned in either scope.
- **Severity:** 🟡 Medium
- **Resolution:** Clarify: Rigging provides slab anchors; acoustic contractor provides baffle-specific hardware below anchor point.

### C-10 | MEP Designer (13) — Acoustic Coordination Timing Risk
- **Type:** Sequencing conflict
- **Issue:** MEP Designer 50% gate is 19-Jul-2026. Acoustic specialist (SC-0019) not appointed. NR criteria coordination cannot happen without them.
- **Severity:** 🟡 Medium
- **Resolution:** Expedite acoustic specialist appointment. Use iAcoustics Strategy V2 as interim design basis.

### C-11 | MEP Designer (13) — No Ceiling Void in Spray/Seamless Areas
- **Type:** Physical incompatibility
- **Issue:** BoSpray (1,653 m²) and BoCoustic (120 m²) applied directly to soffit — no ceiling void for MEP services.
- **Severity:** 🟡 Medium
- **Resolution:** Identify all spray/seamless areas. Confirm MEP routing strategy (below treatment vs. embedded).

### C-12 | Exhibition Fit-Out (08) — Wall-Ceiling Junction
- **Type:** Responsibility ambiguity (future)
- **Issue:** Acoustic wall treatments (future package) will need coordination with ceiling finishes at junctions.
- **Severity:** 🟢 Low
- **Resolution:** Flag for future acoustic wall treatment procurement.

## Cross-Cutting Themes

1. **Specialist not appointed** — Acoustic consultant (SC-0019) pending, blocking NR criteria coordination, silencer specification, and commissioning
2. **No coordinated ceiling plan** — Multiple trades (FLS, AV, Lighting, BMS) all need ceiling element positions that don't exist yet
3. **Unsuitable mounting surfaces** — Soft Cells, BoCoustic, BoSpray all problematic for mounted equipment (speakers, detectors, WAPs)
4. **Undefined scope splits** — "Integrated lighting," baffle suspension anchors, sprinkler cut-outs

## Key Documents Consulted

| Document | Path |
|----------|------|
| Acoustic Ceiling RFP | `18_Acoustic_Specialist/_MANAGER_DASHBOARD/RFP_Acoustic_Ceiling_Package.xlsx` |
| Acoustic SPEC | `18_Acoustic_Specialist/_MANAGER_DASHBOARD/SPEC.md` |
| Acoustic SCOPE_REQUEST | `18_Acoustic_Specialist/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| Acoustic Situation Report | `18_Acoustic_Specialist/_MANAGER_DASHBOARD/SITUATION_REPORT.md` |
| iAcoustics Strategy V2 | `18_Acoustic_Specialist/02_Reference_Drawings/Acoustic_Design_Strategy/6930_Aseer_Acoustic Design Strategy _V2.md` |
| MEP Contractor SCOPE_REQUEST | `10_MEP_Contractor/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| MEP Designer SPEC | `13_MEP_Designer/_MANAGER_DASHBOARD/SPEC.md` |
| MEP Designer SCOPE_REQUEST | `13_MEP_Designer/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| FLS SCOPE_REQUEST | `11_FLS_Specialist_Contractor/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| FLS NRS Comments Register | `11_FLS_Specialist_Contractor/05_Returned_Submittals/NRS_Comments/NRS_Fire_Alarm_Comments_Disposition_Register.md` |
| AV Status Register | `04_AV_IT_Contractor/_MANAGER_DASHBOARD/AV_STATUS_REGISTER.md` |
| Lighting SCOPE_REVIEW_vs_RACI | `02_Lighting_Designer/_MANAGER_DASHBOARD/SCOPE_REVIEW_vs_RACI.md` |
| Lighting Designer SOW | `02_Lighting_Designer/00_Scope_of_Work_from_04/01_Designer_Subcontractor/Aseer_Lighting_Designer_Scope_of_Work_Rev01.md` |
| Structural SCOPE_REQUEST | `12_Structural_Contractor/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| Rigging SPEC | `06_Rigging_Contractor/_MANAGER_DASHBOARD/SPEC.md` |
| CITC Telecom SCOPE_REQUEST | `14_CITC_Telecom_Engineer/_MANAGER_DASHBOARD/SCOPE_REQUEST.md` |
| BMS/ICT SCOPE_REQUEST | `_MANAGER_DASHBOARD/SCOPE_REQUEST_BMS_ICT.md` |
