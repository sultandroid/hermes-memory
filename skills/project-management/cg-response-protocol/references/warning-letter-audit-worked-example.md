# Warning Letter LT-003 - Worked Example: Material Approval Non-Compliance

**Date:** 28-Jul-2026
**LT Ref:** MOC-MUS-ASE-LT-003
**Subject:** Non-compliance with material approval requirements
**Issued by:** CG (Consultant Group)
**Deadline:** 14 working days

## Background

LT-003 references NCR NC-1A0-008 regarding failure to submit material prequalification documents, samples, and delivery schedule. The NCR had been open since 10-Jun-2026 (48 days without closure).

## Escalation Chain

```
SI-008 (09-May-2026) - Aconex ref MOC-MUS-CG-ASE-1KN-MA-008
  Requires: material prequal, samples, delivery schedule
  Status: OPEN (78 days without compliance)
       |
       v
NC-1A0-008 (10-Jun-2026) - NCR for no response to SI-008
  Status: OPEN (48 days without closure)
  Owner: Procurement Lead
  Linked risks: PRR-PRC-05, PRR-QLT-01
       |
       v
LT-003 (28-Jul-2026) - Formal warning letter
  14 working day deadline
  Demands: prequal docs, tech data, physical samples, delivery schedule, recovery plan
```

## 5-Check Audit

### Check 1 - Escalation Chain

| Step | Channel | Valid? |
|------|---------|--------|
| SI-008 (09-May) | Aconex C1 | Yes - proper formal channel |
| NC-1A0-008 (10-Jun) | Aconex follow-up | Yes - valid step |
| LT-003 (28-Jul) | Formal letter after 48-day open NCR | Yes - reasonable escalation |

**Finding:** Unlike NC-1G0-0019 (BOQ NCR) which had a defective chain (email-only, wrong tier), this LT follows a proper SI NCR LT chain through formal channels.

### Check 2 - Procedural History

| Step | Age at Next Step | Assessment |
|------|-----------------|------------|
| SI-008 to NC-1A0-008 | 32 days | Long gap but acceptable |
| NC-1A0-008 to LT-003 | 48 days | NCR open 7 weeks |
| Adel Darwish response (10-Jun) | Same day as NCR | Response sent but CG didn't accept |

**Finding:** Samaya did respond (Adel Darwish 10-Jun to Elbaz) but the response was insufficient to close the NCR. The LT is procedurally sound.

### Check 3 - DMP / Scope Support

| CG Claim | DMP Evidence | Assessment |
|----------|-------------|------------|
| Materials must be approved before IFC | DMP 8.2: "no material in IFC without Code A sample" | Supported |
| Material submittal is Contractor's responsibility | DMP 3.4: 14-item submittal structure | Supported |

**Finding:** Unlike the BOQ NCR, the material approval LT IS supported by DMP 8.2 and 3.4. CG has a legitimate basis.

### Check 4 - Design-Readiness Dependency

| Category | Can Submit Now? | Example |
|----------|----------------|---------|
| Design-ready (specified in approved schedules) | Yes - should have been submitted | Finishes from FF&E schedule |
| Design-pending (awaiting 50% DD decisions) | No - blocked by design gate | Bespoke setwork finishes |
| Technical blockers (Oddy, single-source) | No - technical issue | Patinated brass (PRR-PRC-05) |

**Finding:** Some materials should have been submitted. Others blocked by design stage or known Oddy issues.

### Check 5 - Feasibility

| Demand | Feasibility | Assessment |
|--------|-------------|------------|
| Material prequal documents | Partial | Reasonable for selected materials |
| Tech data sheets + certs | Reasonable | Standard documentation |
| Physical samples | Partial | Some available, some pending |
| Updated delivery schedule | Reasonable | Should be maintained anyway |
| Recovery Plan | New demand | Needs project-wide assessment |

**Finding:** 14 WD is more reasonable than the 3-day NCR deadlines. Demands are legitimate for design-ready materials.

## Key Distinction from NC-1G0-0019 (BOQ NCR)

| Aspect | NC-1G0-0019 (BOQ) | LT-003 (Materials) |
|--------|-------------------|-------------------|
| Procedural chain | Email only, wrong tier | SI NCR LT, all C1 |
| DMP support | BOQ scoped post-50% DD | DMP 8.2 supports material-first |
| Deadline | 3 days (unreasonable) | 14 WD (tight but plausible) |
| Scope issue | Not in contracted scope | Mixed - some ready, some blocked |
| Overall | Procedurally defective | Procedurally sound |

## Recommended Response

1. Accept procedural validity - don't challenge the chain
2. Segregate by readiness - list ready vs blocked materials
3. Demonstrate progress - show what's been submitted since SI-008
4. Provide delivery schedule update - low effort, high impact
5. Submit Recovery Plan - new but reasonable demand
6. Flag technical blockers - patinated brass (PRR-PRC-05)
7. Request clarification - which materials are CG prioritising?

## Sources

| Source | What It Provided |
|--------|-----------------|
| SI register (01_Registers/si_register.md) | SI-008 details, status, dates |
| NCR register (01_Registers/ncr_register.md) | NC-1A0-008 details, linked risks |
| DMP Part 4 (8.2) | Material approval before IFC rule |
| DMP Part 3 (6.1) | Stage 4 gate sequencing |
| Risk register | PRR-PRC-05 (patinated brass risk) |
| Communication Plan (6.1, 7.1) | Channel hierarchy, escalation tiers |
| Outlook SQLite | Email history (Adel Darwish response 10-Jun) |
