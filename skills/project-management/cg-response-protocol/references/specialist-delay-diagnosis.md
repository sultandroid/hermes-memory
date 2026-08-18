# Diagnosing Which Specialist is Delayed — Pitfalls (Aseer, Aug 2026)

When asked "who is behind / delayed" across the design specialists, the wrong answer
comes from relying on a single source or stale registers. This file captures the
traps hit in the Aug 2026 recovery-plan investigation.

## The three pitfalls

### 1. Distinguish "not appointed" from "appointed but no work yet"
The Design Phase Deliverables Tracker shows a **Design Lead name** in the
"Contractor Design Lead" column even when **all other cells are blank** (no planned
date, no quantities, 0% progress, no status). A name in that column does NOT mean
the specialist is contracted or working.

- Landscape row had "Engr. Yahya" as lead but 0% progress and no schedule at all.
- The submission_tracker and the design-discipline risk register (DDR-LAN-001)
  both said "landscape designer is not appointed."
- Reality: the PQ had actually cleared (Evergreen PQ-0122 Code B 28-Jul) but the
  formal **appointment decision** was still open. So the accurate phrasing is
  "identified and PQ-approved but not yet appointed," not "no designer."

**Rule:** cross-check three sources before declaring a specialist unappointed:
(1) Design Phase Deliverables Tracker lead column, (2) prequalification register
Code for the shortlisted vendor, (3) the appointment/action-item status.

### 2. A low % in the tracker is NOT always a technical delay
A near-zero progress % can mean the discipline is **blocked administratively**,
not that its engineers are failing to deliver:

- **ICT/Security at 3%** — root cause was contractual: the system integrator
  (SPS, PQ-0135 Code B) had a contract that was **not signed, no first advance
  payment, PO not submitted to the Executive Director**. A separate CG NCR
  (NC-1E0-0010) existed for delaying the contracting. No technical meeting fixes
  this — it needs procurement sign-off.
- **Landscape** — blocked on an appointment decision, not engineering effort.

**Rule:** for any discipline with <10% progress, check the **contract/PO/appointment
status** (procurement register, action items) before blaming the technical lead.
Separate "delayed for technical reasons" (fix with a coordination meeting) from
"delayed for administrative/procurement reasons" (fix with a signature/payment/
appointment decision).

### 3. Stale registers vs today's emails — Acoustic was already resolved
The submission_tracker still listed acoustic prequalifications as "Under Review"
and 26/19 days silent. But by 18-Aug:

- TransOrient (PQ-0128 Code B 26-Jul) had a **signed contract** (17-Aug).
- The draft invoice for the 50% advance (SAR 86,250 incl. 15% VAT) arrived 18-Aug.
- Only remaining item: TransOrient requested CR + National Address + VAT cert.

If I had answered from the register alone I'd have said "acoustic can't proceed —
no approved resource." Wrong. Always re-check Outlook emails for the last 1-2 days
on the specific vendor before answering a "who's delayed" question.

## Correct workflow for a "who is delayed" question

1. Read the **Design Phase Deliverables Tracker** (the current one, dated) for
   per-discipline progress % and 50/90/100 gate dates. It is the authoritative
   progress view.
2. Cross-check the **submission_tracker** for CG response codes (A/B/C/D) per
   submittal — a discipline can have high volume submitted but 0 approved.
3. For any <10% discipline, check **procurement/appointment** status (is the
   contract signed? PQ approved? PO issued?).
4. Re-scan **today's/recent Outlook** for the vendor name — contracts get signed
   and invoices arrive between register updates.
5. Report in two buckets: (a) technically delayed (fix with meeting/commitments),
   (b) administratively blocked (fix with signature/payment/appointment).
