# NCR / Formal Letter Procedural Audit Against Approved Documents

When CG issues an NCR or formal warning letter (LT), audit its procedural validity before responding. This determines whether to contest (procedural defects) or comply (procedurally clean).

## Audit Checklist (5 Checks)

### 1. Communication Channel — Was it sent through the right channel?

Check the Communication Plan §6.1 (C1–C5 channels):

| Channel | Use | SLA |
|---------|-----|-----|
| **C1** Aconex CDE | Formal submittals, RFI, TQ, SI, NCR, VO | Per workflow |
| **C2** Email | Clarification, coordination, scheduling | ≤ 48h |
| **C3** Meetings | Minutes uploaded to Aconex within 48h | MOM ≤ 48h |
| **C4** Calendar | Standing cadence, milestones | 2-wk view |
| **C5** Site Notice | Urgent / on-site only | ≤ 24h |

Per §6.3, informal channels (WhatsApp, phone, ad hoc verbal) have **no contractual standing**.

**Flag if:** instruction sent via direct email (C2) instead of Aconex transmittal (C1), or referenced only in an informal channel.

### 2. Recipient — Was it sent to the right person/level?

Check the Communication Plan §7.1 Escalation Ladder:

| Tier | Level | Scope | SLA |
|------|-------|-------|-----|
| L1 | Site / Technical | Daily technical coordination | ≤ 48h |
| **L2** | Tech Office Manager | Submittal delays, resource conflicts | ≤ 5 WD |
| **L3** | Project Director | Programme, VO scope, contractual interpretation | ≤ 10 WD |
| L4 | CG Project Manager | Design deadlock, cross-party disputes | ≤ 14 WD |
| L5 | MoC / Employer | Strategic decisions, contract variation | ≤ 7 WD |

**Flag if:** sent to an L2 role (Tech Office Manager) when the matter is contractual/commercial (L3), or skipped tiers without documented justification (§7.4 Rule 1).

### 3. Scope — Is the demanded action actually in scope?

Check:
- **DMP (Design Management Plan)** — Is the task a programmed deliverable at this stage? Check sequencing (50% DD → 90% → 100% → IFC). If task is premature per the DMP, it's scope creep.
- **SOW / ER** — Is the task listed as a Contractor obligation? Check Appendix A/B, ER discipline sections.
- **Risk Register** — Is the issue already captured as a risk? If yes, the CG is treating a known risk as a non-conformance, which is procedurally wrong.

**Flag if:** the task is not a DMP deliverable at this stage, not in the SOW, or already recorded as a known risk.

### 4. Timeline — Is the deadline reasonable?

Check:
- **Communication Plan §7.1** for tier-appropriate SLAs (L1=48h, L2=5WD, L3=10WD)
- **DMP / ER §2.4.A** — 14 calendar days for conformance review
- Nature of the task — a full project-wide reconciliation is multi-week, a single document submission is days

**Flag if:** deadline is shorter than the applicable SLA for the tier, or obviously insufficient for the scope of work demanded.

### 5. NCR Validity — Is the NCR properly issued?

Check:
- **Communication Plan §8.5** — NCR flow: CG/Samaya QA → Samaya, per PQP, tracked in Aconex
- **DMP §8.5** — NCR is for non-conformance to approved documents/standards, not for scope disputes
- Was there a prior SI (Site Instruction) before the NCR? SI → NCR → LT is the proper escalation chain

**Flag if:** NCR used for a scope dispute (should be VO/change mechanism), or if the escalation chain was skipped (direct NCR without prior SI).

## Output

For each check, produce a verdict: PASS / FAIL with the specific clause reference. Compile violations into a table:

| # | Violation | Document Reference | Severity |
|---|-----------|-------------------|----------|
| 1 | Communication channel | Communication Plan §6.1 C1/C2 | Procedural |
| 2 | Wrong recipient | Communication Plan §7.1 L2 vs L3 | Procedural |
| 3 | Scope creep / not in DMP | DMP §6.1 / SOW Appendix A | Contractual |
| ... | ... | ... | ... |

## Tactical Use

- **Procedural defects** (channel, recipient, timeline) → rebut the NCR on procedural grounds. Raise at coordination meeting.
- **Substance defects** (scope, DMP sequencing) → cite the approved document. Harder for CG to rebut since they approved the documents.
- **Both defects present** → strongest position. Procedural defects are clean knockouts; substance defects are backup.

## Examples

| NCR | Primary Defect | Strategy |
|-----|---------------|----------|
| NC-1G0-0019 (BOQ reconciliation) | Wrong channel (email not C1), wrong recipient (Tech Office not PD), scope creep (not in DMP), unreasonable deadline (3 days) | Rebut all — strongest procedural case |
| LT-003 (Material approval warning) | Proper chain (SI-008 → NC-1A0-008 → LT-003) | Acknowledge, segment, comply — no procedural hook |
