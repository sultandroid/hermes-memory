# DRR Risk Assessment Logic — Aseer Museum

When updating the Designer Risk Register (DRR) against project status, apply this logic per risk.

## Status Decision Rules

| Status | When to Use | Residual P×I |
|--------|-------------|:------------:|
| **Closed** | Risk event has passed (deadline expired, approval received, task completed). No further action needed. | 1×1 = 1 |
| **Mitigated** | Controls are in place and working. Residual risk remains but is managed. | 1×2 = 2 or 2×2 = 4 |
| **Watch** | Risk is active but controls are partially effective. Needs monitoring but not yet escalated. | 2×2 = 4 or 2×3 = 6 |
| **Open** | Risk is active, no effective controls yet, or controls not yet implemented. | 2×3=6 to 4×5=20 |

## Concrete Assessment (as of 19-Jul-2026, Day 189)

### Phase 1: Mobilisation / Contract Basis (risks 1-9)
- PR-Q-001 (24 docs in 14 days) → **Closed** — LOA/NTP Dec 2025, deadline passed
- DB-Q-001 (liability ambiguity) → **Open** — no novation secured, SI-007 proves the pattern
- PR-Q-007 (Key Personnel) → **Closed** — personnel approved
- RE-Q-001/002 (resource risks) → **Watch** — backup lists maintained
- RE-Q-003/004/005 → **Open** — ITCA, BIM, Arabic resources not yet needed
- ST-Q-002 (PTW) → **Mitigated** — PTW system operational on site

### Phase 2: Existing Records / Surveys (risks 10-18)
- All **Open** — surveys in progress or TBC
- DB-M-001 (MEP risers) → highest residual 3×4=12 — critical dependency for MEP design
- DB-X-003 (NRS stamping) → linked to PRR-DES-02

### Phase 3: DD Technical Design (risks 19-42)
- CO-X-004 (drawing numbering) → **Closed** — resolved
- CO-X-001 (ceiling/MEP clash) → high residual 3×4=12
- BI-B-001/002 (BIM) → **Watch** — BEP Code B, not unconditional
- All others **Open** — design coordination in progress

### Phase 4: Critical Design Items (risks 43-46)
- DDR-DES-005 (MoC object list) → highest residual 4×5=20 — **Critical**
- QA-Q-005 (NRS 57 comments) → **Watch** — partially dispositioned

### Phase 5: Authority Approvals (risks 47-53)
- All **Open** — no authority approvals received yet
- ST-S-001 (Stramp) and ST-E-001 (SEC transformer) → highest residual

### Phase 6: Design Gates (risks 54-59)
- PR-Q-002 (50% gate) → **Mitigated** — passed for most, structural still Code C
- PR-Q-003 (90% gate) → **Open** — not yet reached
- PR-Q-006 (LOD 300 BIM) → **Watch** — BEP Code B

### Phase 7: Procurement / Specialist / Mock-ups (risks 60-71)
- Most **Open** — procurement in progress
- DDR-MAT-001/002 (patinated brass) → high residual, linked to PRR-PRC-05
- EX-V-001 (AV hardware lead time) → linked to PRR-AV-02

### Phase 8: Construction / Handover / Commercial (risks 72-79)
- Most **Open** — construction not yet started
- COM-CM-001 (design scope vs tender) → linked to PRR-COM-06
- COM-CM-002 (variation dispute) → linked to PRR-COM-04

## Column Filling Rules

### Response Strategy
- **Avoid** — eliminate the risk by changing approach
- **Transfer** — shift risk to another party (insurance, subcontractor, contract clause)
- **Mitigate** — reduce probability or impact through controls
- **Accept (Active)** — acknowledge risk, monitor, have contingency
- **Accept (Passive)** — acknowledge risk, no active monitoring needed
- **SOW-Protect** — frame response to protect Samaya's contracted scope boundaries

### Residual Scores
- Resid. Prob × Resid. Impact = Resid. PxI (formula =R*S)
- Residual should be lower than initial after controls
- If risk is Closed, residual = 1×1=1
- If risk is Mitigated, residual should be 2-4 range
- If risk is Open with no controls yet, residual = initial score

### Contingency Plan Patterns
For each open risk, write a specific fallback action:
- **Survey/data gaps**: "Complete [survey type] as fallback if [primary action] incomplete"
- **Coordination risks**: "Run [coordination type] before [gate]"
- **Authority risks**: "Pre-application meeting with [authority]; prepare alternative [design]"
- **Procurement risks**: "Identify approved-equal alternatives; initiate early procurement"
- **Design risks**: "Produce [deliverable] from [source] if [primary] unavailable"

### Trigger / Early Warning Patterns
- "CG rejects [submission] in review"
- "[Design] submitted without [prerequisite]"
- "[Activity] not started by [date]"
- "[Specialist] appointment delay > [timeframe]"
- "MoC [action] at [gate] review"

### Linked Risks
- Cross-reference to PRR risks (e.g. PRR-DES-07, PRR-MEP-01)
- Cross-reference to other DRR risks (e.g. DDR-MAT-001, DDR-SHC-002)
- Only link if there is a genuine dependency chain

### Evidence Source
- Actual project document references, not generic
- Examples: "EL assessment reports 18-Jul", "GBH Letter 002", "MoM-14 M14-6.2"
- Never cite GitHub repos, JSON files, or AI tools

## Key Cross-References to PRR

| DRR Risk | Linked PRR | Dependency |
|----------|------------|------------|
| DB-S-001 | PRR-SIT-02, PRR-DES-07 | Structural capacity drives critical path |
| DB-M-001 | PRR-MEP-01 | MEP risers gate MEP design |
| CO-X-001 | PRR-MEP-01 | Ceiling coordination critical |
| DDR-DES-005 | PRR-DES-05 | MoC object list impact |
| DDR-MAT-001/002 | PRR-PRC-05 | Patinated brass Oddy |
| EX-V-001 | PRR-AV-02 | AV hardware lead time |
| COM-CM-001 | PRR-COM-06 | Design scope vs tender |
| DB-Q-001 | PRR-DES-06, PRR-STK-01 | Liability + SI-007 dispute |

## DRR Severity Scale (1-5)

| Score | Severity | Color |
|:-----:|:--------:|:-----:|
| 16-25 | Critical | Red #FF4444 |
| 10-15 | High | Orange #FF8C00 |
| 5-9 | Medium | Yellow #FFD700 |
| 1-4 | Low | Green #90EE90 |

Severity formula: `=IF(I>=16,"Critical",IF(I>=10,"High",IF(I>=5,"Medium","Low")))`
