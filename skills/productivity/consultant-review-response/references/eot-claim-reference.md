# EOT Claim Reference — Design Phase Delays

## First: Check the Actual Contract Conditions

Do NOT assume FIDIC. Many Saudi government contracts (MoC, etc.) use bespoke general conditions. Confirm with the user before drafting formal notices.

### If the Contract is NOT FIDIC:

- No formal 28-day notice requirement
- No 42-day detailed claim timeline
- But you still need a paper trail
- Strategy: **simple written requests via ACC/BIM 360**, not legal letters
- Reference: specific SOW clause showing it's the client's obligation
- No threats — just facts and requests

### If the Contract IS FIDIC:

Use the standard FIDIC notice framework below.

## Applicable Law (Saudi Arabia)

### Saudi Government Tenders & Procurement Law
- **Article 5**: If the employer (client) delays providing necessary data, site access, or approvals, the contractor is entitled to an extension of time equal to the delay period.
- **Article 62**: Extension of time must be formally requested in writing. Oral requests are not recognized.

### FIDIC-Based Contract Clauses
| Clause | Subject | Application |
|---|---|---|
| Sub-Clause 2.1 | Right of Access to Site | Employer must give access within the time stated. Failure = EOT under 8.5. |
| Sub-Clause 8.5 | Extension of Time | If delay caused by employer, contractor entitled to EOT even if concurrent delays exist. |
| Sub-Clause 20.1 | Contractor's Claims | Notice required within 28 days. Detailed claim within 42 days of end of delay event. |
| Sub-Clause 1.9 | Delayed Drawings or Instructions | Employer delay in providing necessary data = EOT. |

### Saudi Copyright Law
- Royal Decree M/41 — Copyright protection applies to all exhibition imagery.
- Client (MoC) is responsible for clearing all third-party image rights.
- Delay in providing licensed/copyright-cleared content = employer risk, not contractor risk.

## Notice Templates

### Day 1 Notice — Client Inputs Required

```
To: [Client PM]
CC: [Contracts Department]
Subject: EXHIBITION TEXT / COPYRIGHT / AV SOFTWARE — Required Per SOW

Dear [Name],

Pursuant to the Contract and FIDIC Sub-Clause 20.1, please accept this notice.

The following items are required by the contractually agreed date of [Day 0 / Date]
to enable design mobilization:

1. Exhibition text and object labels (per SOW Sec [X])
2. Copyright and licensing of exhibition imagery (per Copyright Law obligations)
3. AV software and media package (per SOW Sec 6.22)

As of today, none of the above have been received.

These items sit on the Critical Path. Graphic Design, AV Systems Design, and
Showcase Design cannot commence without them.

Please deliver by [Day 14 / Date]. If not received by this date, Samaya will be
entitled to an Extension of Time equal to the full delay period, plus associated
costs, per FIDIC Sub-Clause 8.5 and Saudi Government Tenders Law Article 5.

We request your confirmation of receipt and a committed delivery date within
7 days.

Best regards,
[Name]
Design Manager — Samaya
```

### Simple Notice (Non-FIDIC Contracts)

```  
To: [Client PM]
Subject: Exhibition Text Overdue — Per SOW Clause 2.12

Dear [Name],

Per SOW section 2.12, exhibition text and object labels are MoC's responsibility.  
These have not been received as of [date].  

Graphic design and exhibition layout cannot proceed without this content.  
Please advise when we can expect delivery.  

This delay affects the design schedule and we will need to adjust milestones accordingly.

Best regards,
[Name]
```

```
To: [Client PM]
CC: [Contracts Department / Consultant PM]
Subject: NOTICE OF DELAY — Extension of Time Claim per FIDIC Sub-Clause 20.1

Dear [Name],

Reference: our previous notices dated [Day 1 Date] and [Day 14 Date].

Pursuant to FIDIC Sub-Clause 20.1, we hereby provide formal notice that the
Project is delayed by the following client-dependent items that have not been
received to date:

1. Exhibition text & object labels — [X] days overdue
2. Copyright & licensing of imagery — [X] days overdue
3. AV software & media package — [X] days overdue
4. Site access for surveys — [X] days overdue [if applicable]

The cumulative delay to the Critical Path is estimated at [X] days as of today.

[Attach updated schedule showing original vs. adjusted dates].

We will submit our detailed EOT claim with full supporting documentation within
42 days per Sub-Clause 20.1.

We request your acknowledgement and confirmation of our EOT entitlement.

Best regards,
[Name]
Design Manager — Samaya
```

### Approval Overrun Escalation

```
To: [Consultant PM]
CC: [Client PM]
Subject: URGENT — Approval of [50%/90%/IFC] Design Package Overdue

Dear [Name],

Reference: Submission #[Number] dated [Date].

Per our agreed 3-day review turnaround, this submission was due for review on
[Date + 3 days]. It is now [X] days overdue.

This delay impacts the Critical Path. The subsequent design phase cannot
commence until approval is received.

Please provide your review by end of business today, or advise when we can
expect it.

Best regards,
[Name]
Design Manager — Samaya
```

## EOT Calculator Logic

```
For each client-dependent item:
  Delay Days = Actual Received Date - Required Date
  EOT Days = Max(0, Delay Days - Concurrent Contractor Delay Days)
  
  Note: Concurrent delay offset requires proof that contractor also delayed.
  Dominant cause principle means if client delay is the primary cause,
  full client delay period is allowed (FIDIC 8.5).
  
Total EOT = Sum of all EOT days on the Critical Path
            (adjusted for concurrency — do NOT double-count overlapping delays)
```

## Evidence Requirements

| Claim Element | Evidence |
|---|---|
| Notice was sent | ACC/BIM 360 timestamp + email receipt |
| Required date was known | Contract SOW section + submitted baseline program |
| Actual receipt date | ACC/BIM 360 file upload date, email date, or meeting minutes |
| Critical path impact | Updated baseline program showing delay propagation |
| Cost impact | Manhour records, extended site overhead, escalation letters |

## Aseer Museum (MoC) Specifics

- Contract: MoC x Samaya, lump-sum to 2026-09-30
- DMP: MOC-MUS-ASE-1K0-PL-0029
- Consultant: Moharram Bakhoum (CG PM: Elbaz)
- CDE: ACC/BIM 360 (all notices via this platform)
- Status: BEP approved, CDE ready, 3-day review agreed; team not staffed, client content not received

## Key Dates Reference

| Item | Contractual Date | Status |
|---|---|---|
| Exhibition text | Day 0 (01-Dec-25) | NOT RECEIVED |
| Copyright | Day 0 (01-Dec-25) | NOT RECEIVED |
| AV software | Day 0 (01-Dec-25) | NOT RECEIVED |
| Site access | Day 0 (01-Dec-25) | NOT RECEIVED |

Every day these remain open = 1 EOT day claimable.
