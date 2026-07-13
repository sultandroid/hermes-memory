# Stakeholder Plan Post-Approval Audit — Worked Example

**Plan:** ZD-0020 Rev.02 (Stakeholder Management Plan)
**Approved:** Jun 18-24, 2026
**Audit Date:** Jul 13, 2026
**Project:** Aseer Regional Museum

## Audit Sources Used

| Source | Key Findings |
|--------|-------------|
| PROJECT_MEMORY.md (03 Jul 2026) | AD Engineering appointed, Fida appointed, Rawasin contract executed, Interactive Specialist gap, Waris Sultan as PD, PMC weekly mandates, CG new numbering system |
| CG_STATUS.md | 19 CG comments from Rev.01, all dispositioned in Rev.02 |
| PMBOK Structure Audit (Rev 03) | 5 residual gaps (G-01 to G-05), 9.0/10 PMBOK 6 score |
| Submittal dashboard | ZD-0020 Rev.02 approved, PL-0020 Rev.00→Rev.01→Rev.02→ZD-0020 |
| **specialist_register.md** | Waris Sultan as PD from 13-Jun, QA/QC vacant, AD Engineering as MEP Designer |
| **resource_management_plan.md** | Hani Alghamdi as Procurement Manager, QA/QC vacant (Samir acting) |
| **Review_Email_to_Fida.md** | Adel Darwish instruction: "Sustainability Specialist" not "Manager" |

## CRITICAL: Cross-Reference Personnel Against Multiple Repo Sources

**Do NOT trust PROJECT_MEMORY.md alone for personnel data.** It's a high-level summary and can be wrong or outdated. Every name must be verified against at least two repo sources:

| Source | What It Contains | Reliability |
|--------|-----------------|-------------|
| `PROJECT_MEMORY.md` | High-level status updates, new appointments, departures | Good for signals, but may use wrong titles |
| `Technical_Office/Specialist_Management/specialist_register.md` | Tier 1-2 specialist register with MoC approval status | **Authoritative for specialist roles** |
| `03_Plans/10_Resource/resource_management_plan.md` | Full team org chart with names, statuses, reporting lines | **Authoritative for management roles** |
| `03_Plans/12_SMP/Review_Email_to_Fida.md` | Adel Darwish's instructions on role naming | **Authoritative for role title corrections** |
| `aseer_weekly_dashboard_comprehensive_report.md` | Weekly status with personnel changes | Cross-reference only |

### Known Pitfalls from This Project

| Pitfall | Example | Resolution |
|---------|---------|------------|
| PROJECT_MEMORY.md uses wrong title | "Sustainability Manager" → should be "Sustainability Specialist" per Adel Darwish | Check Review_Email_to_Fida.md for title corrections |
| PROJECT_MEMORY.md has outdated PD | Says "Adel Darwish" as Project Director | specialist_register.md says "Eng. Waris Sultan" (Exhibitions PD from 13-Jun). Adel Darwish is Samaya-level Projects Director, not project-level PD. |
| PROJECT_MEMORY.md has departed staff still listed | "Abdelmohaimen Medhat" as QA/QC Manager | Left 15-Jun. resource_management_plan.md says "Vacant (Samir acting)". |
| PROJECT_MEMORY.md uses generic role names | "Samaya Procurement team" | resource_management_plan.md names "Hani Alghamdi" |

## New Stakeholders / Roles Since Approval

| Stakeholder | Status | Impact on Plan |
|-------------|--------|----------------|
| **AD Engineering** (MEP Designer) | Appointed Jun 21, kick-off Jun 25 | Add to register as T1/T2 Specialist. Define engagement cadence for MEP design reviews. |
| **Muhammad Fida** (Sustainability Specialist) | CV approved Jun 24, PO issued SAR 12k/mo | Add to register as **Sustainability Specialist** (not Manager — per Adel Darwish instruction). Define reporting line (to PM). |
| **Rawasin** (AV/IT — sister company) | Contract EXECUTED | Add as T1 Specialist. Define interface with T2-15 ICT/Security System Integrator. |
| **Studio ZNA** (Lighting Designer) | Fee £40,527 approved, contract pending | Add as T2 Specialist. Define engagement for lighting design coordination. |
| **Eng. Waris Sultan** (Project Director) | Replaced Ahmed Albahrawi (Jun 2026). Exhibitions PD from 13-Jun. | Update org chart. Replace Albahrawi in RACI. Update role description. Note: Waris is project-level PD; Adel Darwish is Samaya-level Projects Director. |
| **Interactive Specialist** | 🔴 CRITICAL GAP — Lumotion declined, no replacement | Add placeholder with TBC status. Note recruitment in progress per Adel Darwish (Jul 1). |

## Other Personnel Updates

| Role | Previous (in plan) | Updated | Source |
|------|-------------------|---------|--------|
| QA/QC Manager | Abdelmohaimen Medhat | **Vacant (Samir acting)** | Medhat left 15-Jun. specialist_register.md |
| Procurement Manager | "Samaya Procurement team" | **Hani Alghamdi** | resource_management_plan.md |
| IT/Data Authority Liaison | T3-09 generic | **Eng. Salah Eldin** | Rev 03 HTML T3-09 row |

## New Engagement Requirements

| Requirement | Source | Impact on Plan |
|-------------|--------|----------------|
| PMC weekly status presentations (SPI/CPI, manpower histogram, register statuses, week-over-week comparison) | PMC mandate (PROJECT_MEMORY #8) | Add to §8 Communication Plan — new weekly deliverable with specific content requirements |
| CG new numbering system (by discipline: AR-XXXX, MEP-XXXX, ST-XXXX) | Sundus Alfeer directive 4-Jun | Update §1.4 document control references |
| IT Engineer CVs requested for review and interview | Adel Darwish 2-Jul | T1-07 IT/Security Specialist recruitment in progress — update role status |

## Residual Audit Gaps (from Rev 03 PMBOK Audit)

| Gap | Severity | Status | Note |
|-----|----------|--------|------|
| G-01: Stakeholder Value-Proposition Map | Medium | **Closed in Rev 04** | Added Tier-1 stakeholder value map table |
| G-02: Conflict Mediation Protocol | Medium | Open | Add pre-escalation mediation protocol for inter-organisational disputes |
| G-03: Stakeholder Management Software Governance | Low | **Closed in Rev 04** | CDE Aconex documented as system-of-record |
| G-04: Emotional Intelligence / Communication Profiles | Low | Open | Add one-paragraph communication-style notes for Tier-1 stakeholders |
| G-05: Value Realization Tracking | Medium | Open | Link objectives to KPIs in value-realization dashboard |

## Verdict

**Needs Minor Update** — 6 new stakeholders/roles and 2 new engagement requirements since approval. The plan's structure is sound (9.0/10 PMBOK 6) but the register and org chart are stale. A Rev.04 update was warranted.

## Recommended Actions (Priority Order)

1. **Update Stakeholder Register** — add AD Engineering, Fida (as Sustainability Specialist), Rawasin, Studio ZNA, Waris Sultan. Remove Ahmed Albahrawi, ITC (on hold), Medhat (vacant).
2. **Update Org Chart** — reflect Waris Sultan as PD, AD Engineering as MEP Designer, Rawasin as AV/IT sister company, Hani Alghamdi as Procurement Manager.
3. **Add PMC Weekly Reporting** to §8 Communication Plan.
4. **Add Interactive Specialist placeholder** — note as TBC with recruitment in progress.
5. **Close G-01 (Value Map)** — low effort, quick win for next revision.
6. **Update Document Control** — reflect new CG numbering directive.

---

## Revision Production (Rev N+1) — Worked Example

After the audit, the Rev 04 was produced with the following workflow:

### Step 1: Delegate HTML Build to Sub-agent

The sub-agent received:
- Full audit findings (6 new stakeholders, 2 new requirements, 5 residual gaps)
- Path to the Rev 03 HTML source file
- Instructions to: update register, org chart, communication plan, interface matrix, KPIs, document control, and close G-01 and G-03

### Step 2: Update Supporting Files in Parallel

While the sub-agent built the HTML, these files were updated:

| File | Change |
|------|--------|
| `CG_STATUS.md` | Status: Code C → ✅ Approved. Added Rev 04 note. |
| `PROJECT_MEMORY.md` | Code C item #4: "awaiting CG verdict" → "✅ Approved" |
| `PMBOK_Structure_Audit.md` | Updated to Rev 04. G-01 and G-03 marked Closed. |
| `Rev04_Change_Log.md` | Created with full change log (new file) |

### Step 3: Verify Sub-agent Output Against Repo Sources

**CRITICAL: The sub-agent may get personnel names wrong.** After the sub-agent produces the Rev N+1 HTML, verify every name against the repo sources listed above. In this session, the sub-agent produced these errors that had to be corrected:

| Error in Sub-agent Output | Correct Value | Source |
|--------------------------|---------------|--------|
| "Adel Darwish" as Project Director | **Eng. Waris Sultan** | specialist_register.md |
| "Sustainability Manager" | **Sustainability Specialist** | Review_Email_to_Fida.md |
| "Abdelmohaimen Medhat" as QA/QC Manager | **Vacant (Samir acting)** | specialist_register.md + resource_management_plan.md |
| "Samaya Procurement team" | **Hani Alghamdi** | resource_management_plan.md |

### Step 4: Changes Applied to Rev 04 HTML

| Change | Detail |
|--------|--------|
| Document Control | Rev 03 → 04, date updated, revision history row added |
| New Stakeholders | AD Engineering (T1), Muhammad Fida (T1 Sustainability Specialist), Rawasin (T1), Studio ZNA (T2), Interactive Specialist (T2 TBC) |
| Updated Stakeholders | Waris Sultan replaces Albahrawi (PD), AD Engineering replaces ITC (MEP Designer), Hani Alghamdi named (Procurement), QA/QC marked Vacant |
| Org Chart | Updated with all new roles |
| Communication Plan | Added PMC weekly status presentation |
| Interface Matrix | Added I-15 (MEP coordination) and I-16 (AV/IT ↔ ICT/Security) |
| KPIs | Added K-11 (PMC weekly report on-time rate) |
| G-01 Closed | Added Tier-1 stakeholder value map table |
| G-03 Closed | CDE Aconex documented as system-of-record |
| Stakeholder Count | 55 → 61 roles |

### Pitfalls Encountered

- **Sub-agent takes time** — the HTML is 2456 lines. Update supporting files in parallel while waiting.
- **Sub-agent gets personnel wrong** — always verify names against specialist_register.md and resource_management_plan.md. The sub-agent doesn't have access to these unless you pass them in context.
- **CG_STATUS.md and PROJECT_MEMORY.md must agree** — if one says Code C and the other says Approved, that's a contradiction. Both were updated in this session.
- **Doc code changed between submission rounds** — PL-0020 (initial) → ZD-0020 (approved). Both variants exist in the archive. The audit must check both.
- **"Sustainability Manager" vs "Sustainability Specialist"** — Adel Darwish explicitly instructed this change. The PROJECT_MEMORY.md still says "Sustainability Manager" — don't trust it. Check Review_Email_to_Fida.md.
- **Project Director vs Projects Director** — Waris Sultan is project-level PD (Exhibitions). Adel Darwish is Samaya-level Projects Director. They are different roles. The plan should show Waris as PD.
