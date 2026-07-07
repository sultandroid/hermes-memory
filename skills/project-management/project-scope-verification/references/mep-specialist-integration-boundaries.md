# MEP Designer Specialist Integration Boundaries (Aseer Museum)

**LAST UPDATED: 2026-07-02** — Added AD Electrical SOW RACI verification findings.

Project-specific knowledge about which specialist systems the MEP Designer integrates vs. does not design. Derived from `MOC-ASEER-SAM-SOW-SC-013_R01`, ER §3.0–3.9, the RACI Matrix (MEP/BMS/ICT/AV Interfaces), and AD Engineering's self-authored Electrical SOW draft (Jul.01, 2026).

## CRITICAL: How to Determine MEP vs Specialist Scope

**🚨 This is the #1 error pattern.** When reviewing an MEP scope document:

1. **Start from the subcontractor's document** — read what they claim as their scope
2. **Map each item to the project's subcontractor directory** — check if a specialist exists for that system
3. **If a specialist exists → MEP provides power/containment/coordination only (not system design)**
4. **If no specialist exists → MEP may need to design the full system**

**Systems are power-distribution-only for MEP unless there is no specialist covering them.**

## RACI-Based Boundary Verification (Jul.02, 2026)

The RACI Matrix (MEP/BMS/ICT/AV Interfaces, Final) is the definitive "who does what" for this project. When AD Engineering submitted their self-authored Electrical SOW (Jul.01, 2026), the RACI revealed several overreach items:

### AD's Correct Scope (RACI = R)

| RACI Ref | Interface Activity | AD's Role |
|----------|-------------------|-----------|
| DC-01→05 | MEP spatial coordination (risers, shafts, ceiling voids, plant rooms, structural openings) | R |
| DC-06, DC-07 | LOD 300/350 design model input — coordinated CAD for Samaya BIM | R |
| PC-01→06 | Power supply to BMS/ICT/AV, containment segregation, earthing | R |
| LS-02, LS-03 | Lighting control system (DALI) design, emergency lighting layout | R |
| FL-02, FL-03, FL-04 | Smoke management, fire damper coordination, emergency lighting with FA zones | R |
| AV-03 | AV heat load calculation for HVAC sizing | R |

### AD's Overreach (RACI says C or I, AD claimed R)

| AD's Claim in SOW | RACI Says | Problem |
|-------------------|-----------|---------|
| "Fully responsible for BMS design" | AD = C, BMS/ICT = R | Specialist leads BMS |
| "Responsible for ICT/structured cabling" | AD = C, BMS/ICT = R | Specialist leads ICT |
| "Responsible for CCTV/security" | AD = C, specialist = R | Specialist leads security |
| "Responsible for access control" | AD = C, specialist = R | Specialist leads ACS |
| "Responsible for PAVA" | AD = C, BMS/ICT = R, Namaa = R | Specialist scope |
| "Responsible for BIM/Revit models" | Samaya = R (DC-06/07) | Samaya BIM Unit handles |
| "Responsible for construction support" | Samaya = R (TC/DH rows), AD = I | AD is informed only |

### The "Fully Responsible" Language Trap

AD's SOW used "fully responsible" 8 times and included a blanket clause:
> *"Any engineering service... reasonably required to complete the Electrical Design... shall be deemed included without additional cost."*

This is dangerous because:
- Combined with "fully responsible" for specialist systems, it could be interpreted as requiring AD to produce specialist designs
- Creates open-ended scope obligation
- Removes AD's ability to claim variation for "reasonably implied" scope
- Shifts scope definition burden entirely onto the employer

**Verdict on AD's Electrical SOW:** Core electrical scope is correct. Low-current/BMS/ICT claims must be removed. BIM modelling claim must be downgraded to "provide coordinated CAD." Construction support must be downgraded to "design clarification on request." Blanket clause needs narrowing.

## Power Distribution Only (MEP provides power, containment, coordination only)

These systems are designed by specialist subcontractors. The MEP Designer provides ONLY:
- Power supply and distribution from MDB/SMDB
- Containment routing and conduits to equipment locations
- Connected load data on panel schedules
- Coordination with architectural/structural backgrounds

| System | Who Designs It | User Verified? |
|--------|---------------|----------------|
| **Lighting Design** | 02_Lighting_Designer (Studio ZNA) | ✅ Confirmed |
| **Audio & Video System** | AV/IT Contractor (Rawasin) | ✅ Confirmed |
| **PAVA (Voice Evacuation)** | AV/IT Contractor (Rawasin) — PAVA is an audio system | ✅ Confirmed — **DO NOT FLAG AS MEP GAP** |
| **Fire Alarm Detection** | Specialist (drawings exist in project LOD) | ✅ Confirmed — **DO NOT FLAG AS MEP GAP** |
| **CCTV Security System** | MOI/Security Specialist | ✅ Confirmed — Out of MEP design scope |
| **Access Control System** | Security Specialist | ✅ Confirmed — Out of MEP design scope |
| **BMS Network & Control** | Specialist (drawings exist in BMS LOD section) | ✅ Confirmed — **DO NOT FLAG AS MEP GAP** |
| **ELV (intercom, MATV, AV containment)** | Specialist | ✅ Confirmed — Out of MEP design scope |
| **Telecom/IT/Data** | CITC-Registered Telecom Engineer (separate subconsultant) | ✅ Confirmed — **NOT MEP design scope** |

## Full Design Required (MEP produces complete design)

These are the systems the MEP Designer must fully engineer:

| System | Source | Notes |
|--------|--------|-------|
| Power distribution (MV/LV, transformers, generators, UPS, SLDs) | ER §3.2 / SOW §2.2 | Core MEP scope |
| HVAC (load calcs, ductwork, CHW, ventilation, smoke management) | ER §3.7 / SOW §2.1 | Including HAP calculations (gallery env conditions covered here) |
| Fire protection (sprinkler, hose reel, clean agent FM200) | ER §3.9 / SOW §2.4 | FM200 is part of firefighting — no need to split |
| Plumbing — limited toilets only | ER §3.8 / SOW §2.3 | NOT expanded scope. "Limited toilets" is correct. |
| Earthing / Lightning protection / Surge protection | ER §3.2 / SOW §2.2 | Core MEP scope |
| Electrical containment and cable routing | ER §3.2 | Core MEP scope |

## What is NOT MEP Design Scope (Mistakes to Avoid)

| Item | Who Handles It | Why Not MEP |
|------|---------------|-------------|
| Existing services intrusive survey | Site PM team + MEP Contractor (10) | SOW §2.8 explicitly excludes from designer |
| External works coordination | Separate scope | Not in MEP designer brief |
| Kitchen hood suppression | Kitchen/fire specialist | Not MEP |
| Grease interceptors | Plumbing contractor | Not designer scope |
| Fire extinguisher schedule | FLS specialist | Not MEP |
| Construction support beyond RFI/shop drawing review | Not extended | Designer role is limited per SOW §2.12 |
| Cold room / café kitchen extract ventilation | Covered in floor drawings | Already exists as HVAC scope |
| Gallery environmental conditions | Covered in HAP calculations | Already part of HVAC load calcs |

## Document Quality Checklist for Arabic SOW Docs

When reviewing Arabic/English bilingual scope documents:

1. **Check section heading duplication** — "Scope of Mechanical & Fire Fighting Systems Design" appearing twice with different content underneath is a copy-paste error. First occurrence (before electrical list) should read "Scope of Electrical Systems Design."
2. **Verify title matches content** — if heading says "Mechanical" but content is Electrical → structural error
3. **Flag vague phrases** — "limited toilets" is CORRECT for this project (not an error)
4. **Check unnamed specialists** — "specialist designers" should ideally name ZNA, Rawasen, etc. but absence is not a gap
5. **Verify codes & standards** — SBC, NFPA, IEC, ASHRAE, SEC should all be listed

## Authority Approval Requirements

| Authority | System | What's Needed |
|-----------|--------|---------------|
| STC | Telecom/FTTH | FTTH Design Guidelines Rev 3.0 compliance |
| CITC | Telecom engineer registration | Valid CITC certificate required |
| Civil Defence | Fire alarm, PAVA, emergency lighting | Design approval before commissioning |
| SEC | Power distribution | Transformer capacity application |
| MOI | Security/CCTV network | Separate network per latest regulations |

## Revision History

| Date | Change | Reason |
|------|--------|--------|
| 2026-06-24 | Full rewrite: moved FA, CCTV, ACS, BMS, ELV, Telecom from "Full Design" to "Power Only" | User corrected scope boundaries — these are specialist-designed, not MEP |
| 2026-06-24 | Added "What is NOT MEP Design Scope" section | User corrected kitchen hood, grease interceptors, external works, existing survey, construction support, cold room, gallery env as not MEP scope |
| 2026-06-24 | Clarified "limited toilets" is correct | User confirmed limited scope is intentional |
| 2026-06-24 | Added drawing LOD cross-reference note | If a system has drawings in LOD (IT-TLC, IT-TFA, IT-ACS, AV-TAV, BM-BMS), a specialist designs it — MEP power-only is correct |
| 2026-07-02 | Added RACI-Based Boundary Verification section | AD Engineering submitted self-authored Electrical SOW — RACI revealed overreach on BMS, ICT, CCTV, ACS, PAVA, BIM, construction support |
| 2026-07-02 | Added "Fully Responsible" language trap | AD's SOW used this 8 times + blanket clause — scope creep risk documented |
