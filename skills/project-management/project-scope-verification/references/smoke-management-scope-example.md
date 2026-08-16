# Smoke Management System — Aseer Museum Scope Verification (worked example)

Question answered: "Is the smoke management system in our scope per the contract, ER, and SOW?"

**Verdict: YES — in scope.** Design by AD Engineering (MEP designer), strategy/authority validation by FLS specialist (Nama), installation by the (to-be-awarded) MEP contractor.

## Evidence chain (all from `~/aseer-museum-pm/`)

| Source | Clause | What it says |
|--------|--------|--------------|
| ER §1.2 Purpose of Works Table | item (l) | "Smoke management system and control" listed as a required measurement & validation item |
| ER (existing systems survey) | — | "Currently, there is no smoke control system or staircase pressurization system… will be validated by the FLS consultant appointed by the contractor during DD" |
| ER (ventilation/exhaust) | §VI | "Design and install smoke ventilation systems and make-up air system… as specified by the fire life safety consultant" |
| AD Engineering MEP Designer SOW | Smoke Management System | "Preparation of Smoke Management System calculation, ductwork layout, selection and sizing of equipment, project specification" |
| Deliverables register | S-P-20 | "Measurement and Validation — Smoke Management \| MEP \| ER §3.1.A.1.a" |
| Drawing register | F-D-L-002 | "100% Final Smoke Detector Upgrade Design \| FLS \| ER §3.5" |

## Scope split (design vs install)

| Role | Party | Responsibility |
|------|-------|----------------|
| **Design** | AD Engineering (MEP designer) | Smoke management system design, calcs, ductwork, equipment sizing |
| **Strategy / authority compliance** | FLS specialist (Nama) | Validate smoke control strategy, tenability, Civil Defence submission |
| **Install** | MEP Contractor | Supply + install smoke vents, dampers, exhaust fans, make-up air |

## Caveats
- **MEP Contractor not yet awarded** (12–16 wk lead) — install scope is contractually required but unassigned to a firm.
- **Smoke Control Assessment** flagged 🔴 PENDING in the FLS register — "TBC if required." The ER says the FLS consultant validates whether a full smoke control/pressurization system is needed; the smoke **ventilation** system itself is a firm requirement.

## Reusable pattern
Smoke management is a **three-way split**, not a single-owner item:
1. **Design** → MEP designer (AD Engineering) — the system design, calcs, equipment sizing
2. **Strategy/authority** → FLS specialist (Nama) — whether a full smoke control/pressurization system is even required, tenability, Civil Defence submission
3. **Install** → MEP Contractor — supply + install of vents, dampers, fans, make-up air

When asked "is X in scope," always resolve the design-vs-strategy-vs-install split before answering — a system can be contractually required (in scope) while its sub-parts are owned by different parties, some of whom may not yet be appointed.

## Scope vs Design-Feasibility — Don't Call a Constraint a Scope Gap

Follow-up question this session: "my mechanical engineer said there are problems on smoke management system — no place for big smoke fan on the roof, needs 9 fans and big duct sizes, not applicable to achieve."

**Verdict: this is a DESIGN FEASIBILITY issue, NOT a scope gap.** The system stays contractually required regardless of physical difficulty. The fix is to resolve the design strategy, not to drop the requirement.

### Workflow for a feasibility complaint on a required system

1. **Confirm the system is contractually required** (ER/SOW) — it stays required no matter how hard it is to build.
2. **Check whether the design package is submitted/approved.** If still **In Progress** (not frozen), the constraint is resolvable in design development — raise it before the package freezes. Aseer smoke package: `MOC-ASE-ME-MHV-SM-2F-DDD-20025-00` (In Progress, not yet submitted).
3. **Identify the missing upstream input.** On Aseer, the FLS specialist (Nama) must issue the smoke-control strategy BEFORE AD Engineering designs the smoke-extract system. If the FLS strategy is still "TBC if required" (FLS Status Register), AD is designing in a vacuum and defaults to brute-force schemes (e.g. 9 roof fans).
4. **Challenge the scheme, not the requirement.** Ask for alternatives: fewer/larger fans in a plant room (not roof), natural smoke vents, zoning to cut fan count, pressurization instead of extraction.
5. **Log it in the design risk register** (Aseer: DDR-FLS-004 already flags "smoke extraction or tenability criteria may fail") as an open design issue, not a scope change.

### Why this matters
The user's engineer raised a legitimate physical constraint. The correct response is NOT "smoke management is out of scope" (it isn't) and NOT "just make it fit" (it may not). It's: **force the FLS strategy to be defined first, then have AD redesign the smoke approach to fit the building.** The missing FLS strategy is the root cause — AD defaulted to a brute-force 9-fan extraction because no validated smoke-control strategy existed to constrain the design.
