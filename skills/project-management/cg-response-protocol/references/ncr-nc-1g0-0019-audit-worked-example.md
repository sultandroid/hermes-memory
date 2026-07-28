# NCR NC-1G0-0019 — Worked Example: BOQ/Drawings Reconciliation

**Date:** 28-Jul-2026
**NCR:** MOC-MUS-CG-ASE-NC-1G0-0019
**Subject:** Failure to Perform Reconciliation Between Contract BOQ and Contract Drawings
**Issued by:** Eng. Abobaker Elfaki (Sr Quantity Engineer) / Mansour Alrezeni (CG PD)
**Deadline:** 3 days (31-Jul-2026)

## Background

CG sent an email on 15-Jul-2026 instructing Samaya to reconcile the Contract BOQ against Contract Drawings. Reminders on 20-Jul and 23-Jul. No reconciliation submitted. NCR issued 28-Jul.

## 5-Check Audit

### Check 1 — Channel (§6.1, §6.3)
Original instruction was direct email only (C2). No Aconex transmittal number (C1).
- **Finding:** Channel violation — instruction has no contractual standing per §6.3
- **Comm Plan Ref:** §6.1 (C1 = formal, C2 = clarification only), §6.3 (out-of-channel rule)

### Check 2 — Recipient / Tier (§7.1)
Sent to Technical Office Manager (Eng. Mohamed Sultan). BOQ/drawings reconciliation is a contractual/commercial matter.
- **Finding:** Wrong tier — should go to L3 (Project Director), not L2 (Tech Office Mgr)
- **Comm Plan Ref:** §7.1 Ladder (L2 = submittal delays, L3 = contractual/scope), §7.4 Rule 1 (no skipped tiers)

### Check 3 — Scope
Risk register already records PRR-COM-09: "CG BOQ/drawing reconciliation request not in scope" (Score 9, High, Owner: Project Director).
- **Finding:** Scope dispute — not a non-conformance, should be handled via VO/change mechanism
- **Evidence:** `01_Registers/risk_register.md` PRR-COM-09

### Check 4 — Timeline
3-day deadline for a full project-wide BOQ/drawing reconciliation.
- **Finding:** Unreasonable — L3 SLA is 10 WD, this is a multi-week exercise
- **Comm Plan Ref:** §7.1 (L3 ≤ 10 WD)

### Check 5 — Response Path
User forwarded to PM/PD for discussion with CG — correct L2→L3 escalation.
- **Finding:** Correct response — user followed §7.3 escalation path
- **Comm Plan Ref:** §7.3 (Scope disagreement → L3 Samaya PD → CG)

## PD's Response Strategy

The PD drafted a response using **substance-only strategy**:

### Arguments Used
1. **DMP sequencing** — BOQ reconciliation is programmed post-50% DD per DMP Rev.02/C04 (Code B approved by CG)
2. **Contract priority** — Drawings/Specs rank above BOQ per Clause 2.5; Lump Sum basis means BOQ quantities are estimated

### Arguments Not Used (Procedural)
The PD did NOT mention:
- Channel violation (email vs Aconex — §6.1/§6.3)
- Wrong recipient (L2 vs L3 — §7.1)
- Unreasonable timeline (3 days vs 10 WD SLA)
- NCR misuse (scope dispute ≠ non-conformance)

### Strategy Assessment
| Element | Assessment |
|---------|------------|
| "Without prejudice" | ✅ Protects contractual position |
| Cites CG-approved DMP | ✅ CG would argue against their own approval |
| Offers to do work post-50% DD | ✅ Shows cooperation without accepting NCR |
| Requests reclassification | ✅ Clean ask |
| Missing procedural violations | ⚠️ Should be noted as supplementary ammunition |

## DMP Clause Verification

The PD's DMP claim was verified by:
1. Converting the DMP PDF (Rev.02/C04) to markdown at `00_Contracts/01_DMP/`
2. Cross-referencing RIBA checklists — BOQ/cost planning is Stage 3, not Stage 4 (Technical Design)
3. Checking SOW — Stage 4 gates are design deliverables, not cost exercises

**Result:** The PD's claim is consistent with the RIBA framework, SOW, and approved DMP.

## Rebuttal Evidence Pack

| Item | Location |
|------|----------|
| Communication Plan excerpts | `03_Plans/03_Communication/communication_plan.md` |
| Risk register entry (PRR-COM-09) | `01_Registers/risk_register.md` |
| Action items log | `00_Status/action_items.md` (BOQ matching task) |
| DMP as formal read-only | `00_Contracts/01_DMP/` |

## User Preference Note

When auditing the PD's response, always flag procedural violations that were not mentioned. The user expects these to be documented even if the PD chose a substance-only strategy. Offer them as supplementary rebuttal points in a brief note.
