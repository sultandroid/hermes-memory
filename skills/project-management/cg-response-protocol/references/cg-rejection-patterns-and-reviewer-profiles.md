# CG Rejection Pattern Register & Reviewer Profiles — Methodology

> How to build a consolidated CG rejection pattern register and per-reviewer profiles from scattered project registers and CG response documents.

## Trigger

Use this when the user asks to:
- "Build a CG rejection pattern register"
- "Analyse CG rejection trends"
- "Create reviewer profiles"
- "Forecast CG response for upcoming submittals"
- "Identify recurring rejection reasons"

## Data Sources to Mine

| Source | What It Contains | Where to Find It |
|--------|-----------------|------------------|
| **Submittal Register** | All submittals with CG response codes (A/B/C/D), dates, reviewer names | `01_Registers/submittal_register.md` |
| **Material Submittal Register** | MA-specific rejections with verbatim CG comments | `01_Registers/material_submittal_register.md` |
| **NCR Register** | Non-conformance reports issued by CG | `01_Registers/ncr_register.md` |
| **SI Register** | Site instructions — shows CG enforcement patterns | `01_Registers/si_register.md` |
| **Comment Register** | Design comment disposition with reviewer attribution | `Technical_Office/comment_register.md` |
| **Deliverables Register** | Phase/discipline breakdown with CG status codes | `Technical_Office/deliverables_register.md` |
| **CG_STATUS files** | Per-plan CG response details with named reviewers | `03_Plans/*/CG_STATUS.md` |
| **CR Sheet files** | Detailed CG comment-by-comment analysis | `03_Plans/*/cr_sheet_*.md` |
| **Reply Analysis files** | Deep-dive on specific CG responses | `03_Plans/*/CG_RE_*.md` |
| **PROJECT_MEMORY** | Organisational chart with CG team members | `99_Archive/00_Project_Overview/PROJECT_MEMORY.md` |
| **Email logs** | CG email addresses, correspondence volume | `99_Archive/05_Quality_Management/QA_QC_Plans/CG_STATUS.md` |

## Workflow

### Phase 1: Extract All C/D Submittals

1. Read the submittal register — extract every row with Code C (Revise & Resubmit) or Code D (Disapproved)
2. For each C/D submittal, capture:
   - Ref, Subject, Discipline, Date, CG Reviewer(s), Code
   - Verbatim or near-verbatim CG comments (from the register's notes column)
3. Group by discipline (IFC Drawings, Prequalifications, Material Submittals, Design Documents, HSE Plans)
4. Add NCRs as a separate section — they are enforcement actions, not submittal reviews

### Phase 2: Identify Recurring Rejection Patterns

1. Read through all verbatim CG comments
2. Group similar comments into categories (e.g., "missing supporting documentation", "incomplete submission", "non-compliance with specs")
3. Count occurrences per category
4. Rank by frequency
5. For each pattern, note:
   - Which disciplines it affects
   - Severity (how hard to fix)
   - Whether it's a documentation gap, a technical gap, or a process gap

### Phase 3: Calculate Rejection Rates

1. For each discipline: count total submittals, Code C count, Code D count
2. Calculate C+D rate = (C + D) / Total
3. Note any discipline with 100% rate (e.g., IFC Drawings) — these are systemic problems
4. Calculate overall project C+D rate

### Phase 4: Analyse Cycle Times

1. For each submittal with known dates: calculate CG review time (response date - submission date)
2. Group by code type (B vs C vs D)
3. Calculate average review time per code type
4. Identify outliers (fastest, slowest)
5. Track submittals that reached Deemed Approval (14+ days silent per ER Section 2.4.A)
6. Track longest-open C/D submittals

### Phase 5: Build Reviewer Profiles

1. Collect every named CG reviewer from all registers and CG response documents
2. For each reviewer, extract:
   - **Role** — from email signatures, signatory blocks, or organisational chart
   - **Known submittals reviewed** — every submittal where their name appears
   - **Tendencies** — what they focus on, what they reject, what they approve
   - **Common conditions** — recurring requirements they impose on approvals
   - **Review speed** — calculate from submission and response dates
3. For reviewers with no confirmed submittals (e.g., Ahmed Yehia), mark as "Unknown — monitor"
4. Build a comparison matrix: reviewer × strictness × speed × focus areas × typical outcome

### Phase 6: Forecast Future CG Responses

1. List all submittals currently under CG review (Submitted status, no response yet)
2. For each, predict the code based on:
   - Historical pattern for similar submittals (same discipline, same reviewer)
   - Current known gaps (missing data, pending tests, unresolved issues)
   - Whether the submittal is NRS-authored (lower risk) or Samaya-prepared (higher risk)
3. Categorise as High Risk (predicted C/D), Medium Risk, or Low Risk (predicted B/DA)

### Phase 7: Write Recommendations

Structure recommendations in three time horizons:

| Horizon | Scope | Examples |
|---------|-------|---------|
| **Immediate (7 days)** | Fixes that can be done now | Separate electrical data from HSE plans, pre-clear structural DD, bundle NRS review reports |
| **Medium-term (30 days)** | Process improvements | Create CG submission checklist, use DA rule strategically, pre-position FLS endorsement |
| **Long-term (60 days)** | Systemic changes | Reduce C/D rate from 31% to 15%, address IFC quality issue, build reviewer preference database |

## Output Structure

### File 1: `cg_rejection_patterns.md`

```
---
last_updated: YYYY-MM-DD
owner_agent: <agent>
status: active
source: <list of source files>
---

# CG Rejection Pattern Register — [Project Name]

## 1. Consolidated Rejection Table
  - 1.1 IFC Drawings
  - 1.2 Prequalification Submittals
  - 1.3 Material Submittals
  - 1.4 Design Documents
  - 1.5 NCRs

## 2. Pattern Analysis
  - 2.1 Recurring Rejection Reasons (ranked by frequency)
  - 2.2 Rejection Rate by Discipline
  - 2.3 Cycle Time Analysis
  - 2.4 Reviewer Tendencies

## 3. Forecast
  - 3.1 Currently Under CG Review (predictions)
  - 3.2 High-Risk Submittals
  - 3.3 Low-Risk Submittals

## 4. Recommendations
  - 4.1 Immediate Actions (7 days)
  - 4.2 Medium-Term Strategy (30 days)
  - 4.3 Long-Term Strategy (60 days)
  - 4.4 Risk Register Updates
```

### File 2: `cg_reviewer_profiles.md`

```
---
last_updated: YYYY-MM-DD
owner_agent: <agent>
status: active
source: <list of source files>
---

# CG Reviewer Profiles — [Project Name]

## [Reviewer Name]
### Role
### Known Submittals Reviewed
### Tendencies
### Common Conditions
### Review Speed
### Submission Strategy

## Reviewer Comparison Matrix

## Key Takeaways
```

## Pitfalls

- **Not all CG responses name the reviewer.** About 40% of C/D submittals in the Aseer Museum registers are marked "CG (general)" with no named reviewer. These cannot be attributed. Note this limitation explicitly.
- **Reviewer assignment is not predictable.** CG does not publish reviewer assignments in advance. Prepare every submission to the highest standard regardless of who may review it.
- **Cycle time calculation requires both dates.** If the register only has a submission date or only a response date, you cannot calculate review time. Note missing dates.
- **Deemed Approval (DA) submittals have no reviewer attribution.** CG was silent — no reviewer name is available. These are excluded from reviewer profiles.
- **Email addresses are not reviewer names.** CG_STATUS files often list email addresses (e.g., melbaz@cg.com.sa) but the actual reviewer name on the submittal response may differ. Cross-reference against signatory blocks on CG response PDFs.
- **One reviewer may have multiple roles.** Mohammad Elbaz is both CG PM (signs final approvals) and a detailed reviewer (comments on org charts, team structure). Distinguish between his signatory role and his review role.
- **Review speed varies by submittal complexity.** A fast reviewer on a simple prequalification may be slow on a complex design plan. Note the submittal type alongside the speed.
- **Forecasts are probabilistic, not certain.** Label predictions clearly as "High Risk", "Medium Risk", "Low Risk" — not as definitive outcomes.

## Aseer Museum Reference

A worked example from 2026-07-20 lives at:
`Technical_Office/CG_Analysis/cg_rejection_patterns.md`
`Technical_Office/CG_Analysis/cg_reviewer_profiles.md`

Key findings from that analysis:
- 217 total submittals, 31% C+D rate
- IFC Drawings: 100% C/D rate (systemic design quality issue)
- 10 recurring rejection patterns identified
- 11 CG reviewers profiled (5 named + 6 additional)
- 18+ submittals forecast with risk ratings
- 12 recommendations across 3 time horizons
