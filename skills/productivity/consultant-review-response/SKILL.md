---
name: consultant-review-response
description: "Review project plans and programme schedules against contract documents (SOW/ER) and CG comments — compliance review, schedule audit, gap analysis, and resubmission tracking."
version: 1.0.0
author: Hermes Agent
---

# Consultant Review Response

Review consultant/subcontractor responses to CG-approved scopes of work, evaluate fee proposals against CG requirements, and produce compliance gap analyses and negotiation positions — plus create new revisions of project management plan documents (CRP, DMP, BEP, Stakeholder Plan, QMP, HSE Plan) when Consultant/Client review returns Code B (Approved with Comments) or Code C (Revise & Resubmit).

**Subcontractor/Consultant Appointment Review:** See `references/subcontractor-appointment-review.md` for the workflow to evaluate a consultant's fee proposal and reply against CG Code B comments — produces a three-way cross-reference gap matrix and negotiation summary.

**Specialist Deployment Breakdown (NRS vs SAMAYA):** See `references/specialist-deployment-breakdown.md` for mapping SOW §5.5 specialist positions against NRS contractual scope vs SAMAYA subcontractor engagements — formal response template with position-level breakdown and project data source references.

## 0e. Design Schedule Management (absorbed from `design-schedule-management`)

Build realistic design-phase schedules when the contract demands compressed timelines (e.g., SOW/ER requires 3-month design for a museum fit-out). Covers both ideal compression and real-world baseline given staffing/content gaps.

### Core Principles

#### 1. Correct Phase Sequencing — Never Skip These

```
PREQUALIFICATION     → determines who supplies/work — must finish BEFORE 50% design
     ↓
50% DESIGN           → concept design all disciplines + specialized
     ↓
MATERIAL SUBMITTALS  → samples + approvals from prequalified vendors
     ↓
90% DESIGN           → detailed design with APPROVED materials in specs
     ↓
IFC 100%             → final package + BIM federation + approvals
```

**Critical rule**: Material approvals must complete BEFORE 90% design finalizes. Prequalification must complete BEFORE 50% design starts for specialized disciplines.

#### 2. Compression Methods (when contract demands tighter timelines)

| Method | Benefit | Risk |
|--------|---------|------|
| **Parallel disciplines** — ARC, STR, MEP, Specialized simultaneously | Cuts 60-70% off serial timelines | Coordination overload |
| **Fast-track approvals** — 5d→2-3d per item | ~40% schedule reduction | Requires written consultant commitment |
| **Overlapping stage gates** — Assessment/50% overlap | Eliminates dead gaps | Re-work if assessment misses issues |
| **Direct-to-IFC per ER §2.4** — Code-governed items skip 50%/90% gates | Weeks saved per item | CG must pre-approve list |
| **Progressive release** — Fabrication info per discipline, not batched | Early procurement for long-lead items | Partial package tracking complexity |
| **Rolling wave decomposition** — Early IFC for low-coordination packages | Faster procurement start | Requires careful wave planning |

#### 3. Realistic Durations per Design Package (museum fit-out)

| Package | 50% (working days) | 90% (working days) |
|---------|:------------------:|:------------------:|
| Architectural | 12-15 | 10-12 |
| Structural | 8-10 | 8 |
| MEP (Elec + Mech) | 8-10 each | 8-10 each |
| Specialized (AV/Graphics/Lighting/Showcase) | 7-10 each | 7-10 each |
| BIM Federation | — | 10 + 5 clash |

#### 4. Direct-to-IFC Element List Review

ER §2.4 permits skipping 50%/90% for certain elements. Review each proposed element against these classes:

| Class | Definition | Example |
|-------|-----------|---------|
| **A** | Fully defined in Stage 3 design & ER specs | Standard materials, finishes fully specified |
| **B** | Code-governed commodity (SBC/NFPA/ASTM) | Fire sealant, gypsum board, EMT conduit |
| **C** | Like-for-like replacement / validation | FCU replacement with same duty |
| **D** | Auxiliary / BOH areas — outside exhibition intent | BOH doors, plant room finishes |

**Exclusion zones** (must stay in staged route): Gallery finishes, showcases, setworks & scenography, exhibition lighting, AV hardware, graphics & wayfinding, FLS strategy, structural modifications.

**Critical precondition — ER §2.4 requires list approval before IFC submissions.** Sending IFC packages without prior list approval means CG will return Code C.

#### 5. Material Submittal Batching

Batch 100+ items across 5 categories in parallel:
- Week 1: AV data sheets
- Week 2: Structural + Architectural Wave 1 + Electrical + Mechanical
- Week 3: Architectural Wave 2 + approvals start rolling
- Week 4: All approvals complete

Requires **5 concurrent review streams** (one per discipline).

#### 6. Common Pitfalls

- **Material approvals after 90% design** — #1 error. Complete 2 weeks before 90% finalization.
- **Prequalification as afterthought** — Must happen during prelims/assessment.
- **5-day design packages** — Too short for quality. Use 8-12 days for 50%.
- **Sequential disciplines** — ARC then STR then MEP wastes 60% of schedule.
- **Negative float ignored** — Address root cause, not symptom.
- **Direct-to-IFC without prior list approval** — Procedurally invalid. CG will return Code C.
- **Sending IFC before list approved** — The ER clause you rely on requires list approval as a precondition.

### Workflow

### 0a. Pre-Submission Compliance Review (No CG Comments Yet)

When the user asks to review a plan document for CG compliance BEFORE it has ever been submitted — and no CG comments exist for that specific document — use cross-plan CG pattern mining to anticipate what CG will flag.

This applies to plans in the ⚪ "No CG response found" state. The Resource Management Plan, PQP, RACI, Procurement Plan, and Sustainability Plan are all candidates.

### 0b. Programme/Schedule Audit Against SOW + ER

When the user sends a project programme/schedule from the planner and asks "audit against SOW and ER" or "review schedule against scope" — this is a **fundamentally different task** from PM plan compliance review. It uses contract documents (SOW/ER) as reference, not CG comment patterns.

**Trigger phrases:** "audit against sow and er", "review schedule against scope", "check programme against contract", "verify schedule completeness", "راجع الجدول الزمني مع نطاق العمل"

#### Step 1: Identify What the Schedule Actually Covers

**Critical first step — do not assume the schedule covers the full project.** Before any analysis:

- Check the file name for phase indicators: "DESIGN PHASES", "DESIGN PHASE", "CONSTRUCTION", "MASTER PROGRAMME", "SH-006"
- Check the end date against the known contract completion. If the schedule ends months before contract completion, it's likely a phase-specific schedule.
- Look for activity ID prefixes that reveal scope (PE=Preliminaries, AS=Assessment, EN=Engineering/Design, PR=Procurement, CN=Construction)
- The contract completion date is typically beyond the design-only schedule. A programme ending at a design-gate milestone (e.g. 100% IFC) is the design phase, not the full project.

**Pitfall — don't flag duration as unrealistic until you confirm which phase the schedule covers.** A 5-month schedule ending at 100% IFC is normal for design phase. The same duration would be critically unrealistic for a full museum fit-out.

#### Step 2: Locate Contractual Scope Documents

Find the SOW and ER documents. Typical locations for Aseer Museum:

```
Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/
Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/
Docs/01_Contracts_and_ER/01.3_Contractors_SOW/
Docs/01_Contracts_and_ER/01.2_Employer_Requirements/
```

**OneDrive file lock pitfall:** Files under `Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` may return `[Errno 11] Resource deadlock avoided` when not locally synced. **Do not keep retrying the same command.** Instead:
1. Check `Docs/07_Reports/07.5 Audit Report/` for pre-existing Markdown extracts:
   - `EXTRACT_Scope_of_Works.md` (full OCR extract, ~2900 lines)
   - `EXTRACT_Employer_Requirements.md` (full OCR extract)
   - `SUMMARY_Scope_of_Works.md` (condensed version)
2. Also check `Design Files/Package_Part 2/05_AS_Employer's Requirements Documents_250313/` for cached `*.md` files
3. Load `references/aseer-sow-er-scope-reference.md` from this skill for the cached scope checklist

#### Step 3: Extract Key Scope Requirements from SOW/ER

The SOW defines **Seven Parts of Work** (§2.1). Verify each part has schedule coverage:

| Part | Title | What to Check in Schedule |
|------|-------|--------------------------|
| 1 | Technical Design — Exhibition | Design 50%/90%/100% IFC gates, Graphics, AV, Lighting, Showcases, Landscape, Stramp, Terrace, Library |
| 2 | Site Assessment, Surveying & Engineering | Site surveys, cloud survey, structural/MEP/FLS assessments, BIM model |
| 3 | Off-Site Fabrication | Manufacturing activities for all 15 fabrication disciplines (§8) |
| 4 | Enabling Works | Demolition, preparatory works, temporary works |
| 5 | On-Site Fit-Out & Commissioning | Mobilization, installation, testing & commissioning, ITCA |
| 6 | Handover & Training | 17 handover items (§11.3), training plan (§11.7) |
| 7 | Defects | DLP period, snagging access |

For each Part found in schedule → mark as ✅. For each Part missing → **Code C** gap.

Then extract the **mandatory deliverables** that must appear in any schedule, regardless of phase:

| Item | SOW § | Type |
|------|-------|------|
| Design Certification | §6.8 | Gate requirement |
| IFC Document List | §6.9 | Early deliverable |
| ITCA Appointment & Plan | §10.4, ER §2.6 | Before commissioning |
| Mock-ups, Samples & Prototypes | §13.12, §13.27 | Pre-fabrication |
| FAT/SAT | §13.28 | Pre-delivery + post-install |
| Third-Party Certification | §13.29 | Structural, Oddy, environmental |
| Training Plan | §11.7 | Before handover |
| O&M Manuals | §11.5, §11.3(7) | Before practical completion |
| Spares & Attic Stock | §13.2 | 1-year period |
| Dilapidation Survey (pre + post) | §11.1 | On appointment + at handover |
| Interface Responsibility Matrix | §13.30, Appx A | At design commencement |
| Stable Environment verification | §13.3 | Performance gate |
| Sustainability Plan | §13.9 | Ongoing |

#### Step 4: Build a Gap Matrix

| # | Gap | SOW/ER Ref | Severity |
|---|-----|-----------|----------|
| G1 | Description of missing or insufficient scope | §X.X — clause text | **Code C** / High / Medium / Low |

Severity taxonomy (for programme audits, severity = likelihood of CG rejection):

- **Code C** — Entire work part or mandatory deliverable missing (Part 3, Part 6, ITCA, Design Cert, Training Plan)
- **High** — Significant scope element not scheduled or incorrectly sequenced (authority approvals, subcontractor prequal, procurement lead times, Stramp structural design)
- **Medium** — Schedule item exists but duration/sequencing/parallelism is wrong (sequential instead of concurrent as required by §6.1, insufficient review periods)
- **Low** — Missing coordination item, naming inconsistency, or minor deliverable

#### Step 5: Evaluate Schedule Structure

Key structural checks beyond content:

- **Is this design-phase-only?** Check activity IDs and end date. Design phase schedules (EN-prefixed activities ending at IFC) do not need to include fabrication/installation/handover — those belong in the Master Programme.
- **50/90/100% gate structure** — §6.1 requires three sub-stages. Each discipline should have activities at each gate.
- **Review periods — calendar vs working days** — ER §2.4.A/SoW §6.7: 14 **calendar** days for conformance reviews. SoW §6.5: 14 **working** days for stage-end reviews only. **No subsequent approved project document has resolved this conflict.** DMP Rev C03 says "14 calendar days." CRP Rev C02 attempted "Friday excluded" but returned Code C (not approved). PEP Rev03 shows "303 calendar days" but was never formally submitted. For Direct-to-IFC elements (no stage-end review), the 14-calendar-day period applies — SoW §6.5 is scoped to stage-end reviews only, which the Direct-to-IFC mechanism eliminates. If challenged, cite ER §2.4.A as the controlling clause. Full analysis in `references/review-period-conflict.md`.
- **Parallel concurrency** — §6.1 mandates Parts 1, 2, and 4 run concurrently. Check the schedule shows this.
- **Long-lead items** — Showcases (12-16 wks), AV equipment, custom joinery should have early procurement starts.

#### Step 6: Produce Structured Report

Format:

```
## Programme Audit — [Project Name] [Phase Name]

**Source:** [Planner filename]
**Duration:** [Start] → [Finish]
**Scope:** Design Phase Only / Full Project / [Other]
**Contractual basis:** SOW [doc ref] · ER [doc ref]

### ✅ Scope Items Correctly Covered
[Table of adequately scheduled parts/deliverables]

### 🔴 Critical Gaps (Code C — CG would reject)
[#|Gap|SOW/ER Ref|Detail]

### 🟠 High-Severity Gaps
[#|Gap|SOW/ER Ref|Detail]

### 🟡 Medium-Severity Gaps
[#|Gap|SOW/ER Ref|Detail]

### 📋 Recommended Actions
[Ordered list of fixes for the planner, by priority. Include notes for the planner as specific instructions.]

### ⚠️ Note to Planner
[If the programme is under CG review (e.g. returned Code C), state the current approval status and what the planner should prioritize.]
```

**XER/Critical path analysis:** For programmatic extraction of the Primavera P6 network, analysis of the critical path (TF=0), calendar effects, and root-cause quantification of schedule overruns, see `references/xer-schedule-analysis.md` from this skill. Use the Python parsing technique + root-cause framework when the user sends an .xer/.xml export and asks "why does this phase exceed its duration constraint?"

**PDF Gantt chart audit:** When the schedule is a P6 PDF export (not XER/XML) — the common CG submission format — see `references/pdf-gantt-schedule-audit.md` for the methodology: extracting activity data from multi-page Gantt tables, mapping WBS hierarchy, assessing 8 dimensions of schedule health (float distribution, duration realism, sequencing logic, resource concurrency, procurement buffers, overseas supply chain, handover compression, calendar effects), and producing the structured audit report.

**Materials-to-supplier traceability (Stage 3 audit):** When auditing a schedule's procurement phase for completeness of design-named suppliers, see `references/materials-supplier-traceability.md`. Cross-references schedule activities (Specifications & Data Sheet Materials) against Finishes Schedule, Luminaire Spec, AV BOQ, FF&E Schedule, and Materials Register to extract named brands. Produces a traceability matrix Excel with coverage gap analysis. Never rely on the P6 activity names alone — they are generic ("Submit Material for Lighting") while the design docs name 10+ brands under that single line item.

**Full SOW deliverable checklist and specialist subcontractor list available in** `references/aseer-sow-er-scope-reference.md`.

**Producing a formal A4 review report:** After the audit, generate a formal HTML review document (cover page + findings + conclusion) using the template at `references/schedule-review-report-html.md`. **ALWAYS save the report directly to the project folder** (`10_Plans/Schedule_Programme/`) under OneDrive — never to Desktop or /tmp. See the reference file for the HTML structure, severity badge classes, finding table format, and output location rules.

**NRS email drafting — forwarding CG/PMC review comments to design consultant:** See `references/nrs-email-drafting.md` for the informal-collaborative email structure, CC line, common CG comment areas, pre-empting pushback, and attachment verification. This covers the recurring pattern of communicating CG feedback on DD architectural submissions to NRS.

**Design schedule compression strategy (Direct-to-IFC + rolling waves + 10-week template) available in** `references/design-schedule-compression.md`.

**Design schedule compression strategy (Direct-to-IFC + rolling waves + 10-week template) available in** `references/design-schedule-compression.md`.

**Review period conflict analysis (14 calendar vs 14 working days) available in** `references/review-period-conflict.md`.

**Tier table audit (staffing tables × SMP × KPR × CG CRS):** See `references/resource-plan-tier-audit.md` for auditing Tier 2 Discipline Leads & similar staffing tables against Stakeholder Plan T2 codes, KPR approval status, CG comment directives, PMBOK standards, and classification. Includes framing guidelines from the contractor's perspective with client-facing language. Also includes the **KPR-to-HTML cross-reference workflow** for updating plan documents to match the live KPR (reading KPR Excel, classifying approval status, patching HTML, entity name corrections, verification scan).

### 0c. Direct-to-IFC Element List Review

When the user provides a Direct-to-IFC Element List (Excel file listing elements proposed to skip the 50%/90% staged route and proceed straight to IFC) — review against ER §2.4 criteria and SOW scope obligations.

**Trigger phrases:** "direct to ifc", "direct-to-ifc element list", "قائمة عناصر الانتقال المباشر", "ER §2.4 direct"

**Reference mechanism:** ER §2.4 explicitly permits this: *"The Contractor may consider some elements of the design to be able to proceed straight to IFC stage. Any elements considered as such are required to be listed for the PMC and MoC consideration and approval prior to proceeding any further."*

#### Step 1: Verify Justification Classes Against ER §2.4

The list should classify each element using a justification scheme. Standard classes:

| Class | Definition | Example |
|-------|-----------|---------|
| **A** | Fully defined in Pre-Appointment Stage 3 design & ER specs — no residual design decisions | Standard materials, finishes fully specified |
| **B** | Code-governed commodity (SBC/NFPA/ASTM/SASO) — performance-specified, no aesthetic content | Fire sealant, EMT conduit, gypsum board |
| **C** | Like-for-like replacement / validation of existing building systems | FCU replacement with same duty, same-form-factor |
| **D** | Auxiliary / BOH areas — outside exhibition design intent | BOH doors, plant room finishes |

**Check:** Each element should have a valid class (or combination) that justifies direct route. Elements that involve aesthetic review, conservation requirements, or exhibition design intent should NOT be on this list.

#### Step 2: Cross-Reference Against SOW Exclusion Zones

The following SOW items **must remain in staged route** (exhibition design review, conservation, or aesthetic content):

- Gallery finishes (wall/floor/ceilings in exhibition spaces) — SOW §8.4-8.6
- Showcases (conservation display cases) — SOW §8.15
- Setworks, feature walls & scenography — SOW §8.7
- Exhibition lighting & controls — SOW §8.8
- AV hardware layouts & sightline studies — SOW §8.9
- Graphics, wayfinding & artwork — SOW §8.14
- FLS strategy package — SOW §13.6
- Structural modifications (stairs, Stramp structural) — SOW §8.2-8.3
- Premium FF&E & special furniture — SOW §6.22

**Check:** Elements from these categories should be in the exclusions list, NOT the Direct-to-IFC list.

#### Step 3: Identify Missing Candidates

Scan for code-governed or fully-specified elements from the schedule that are NOT on either list but COULD go Direct-to-IFC:

- BMS / Building Management System (ER §3.2, code-governed)
- CCTV & Security System (MOI code-governed — Class B)
- Emergency / exit lighting (NFPA 101/SBC 801 — Class B)
- External signage (Stage 3 defined — Class A/D)
- Landscape / horticulture (non-Stramp areas — Class A)

For each, note the basis and recommend whether to add to the list.

#### Step 4: Verify Exclusion Rationale

For items in the exclusions (staged route) list, check:
- Is the stated reason (aesthetic, conservation, coordination, SOW obligation) valid?
- Does the element truly require staged review, or could it be Direct-to-IFC with certification?
- Is the exclusion consistent with SOW §6.1 (50% gate for exhibition packages)?

#### Step 5: Check Pre-Approval Sequence

**Critical precondition — ER §2.4 requires list approval before IFC submissions.** The mechanism is:

> *"Any elements considered as such are required to be listed for the PMC and MoC consideration and approval prior to proceeding any further."*

The schedule must include:
1. **W1 — Submit element list** for CG/PMC consideration (Day 1)
2. **W1–W2 — CG review period** (14 calendar days per ER §2.4.A)
3. **W2 end — CG approval or rejection** of the list
4. **W3+ — Proceed with IFC submissions** for approved elements

**Failure mode (repeated pattern):** Sending IFC packages without prior list approval means the submission is procedurally invalid — CG will return it Code C without reviewing content, citing the ER clause you relied on.

**Pitfall:** If CG rejects >5 elements from the list, the schedule compression is undermined. Add a fallback clause: if >5 elements are moved back to staged route, the Contractor reserves the right to re-baseline the schedule and claim EOT.

#### Step 6: Consider Rolling Wave Decomposition

For the staged route (exhibition packages retained at 50% → IFC), a single handover at W7-8 is often unrealistic. Decompose into two waves:

| Wave | Packages | IFC Target | Benefit |
|------|----------|-----------|---------|
| **Early** | Graphics, Lighting, FF&E, Acoustics, CITC | W6 | Lower coordination dependency, faster to close |
| **Late** | Showcases, Scenography, AV, Gallery Finishes | W7-8 | Need more coordination, mock-ups, CG material board |

**Check pattern:** If the proposed schedule shows all 11 packages completing 50% → IFC simultaneously, flag it and suggest rolling waves with overlapping review periods. The final NOC stays at W10, but the intermediate IFC releases allow procurement to start earlier.

#### Step 7: Map External Dependencies

Exhibition packages often depend on external tracks outside the Contractor's control. Map these clearly:

| Package | External Dependency | Type | Risk |
|---------|-------------------|------|------|
| Gallery finishes (E-01) | SI-CG-ASEER-007 Material Board sequence | CG-directed | ⚠️ Schedule blocker if unresolved |
| Showcases (E-02) | Glasbau Hahn specialist shop drawings | Subcontractor | Medium — separate track |
| AV (E-05) | MoC software/content delivery (IRM 2.13) | MoC-supplied | Medium — coordination risk |
| FLS Strategy (E-10) | Civil Defense approval | Authority | Medium — lead time |
| Stramp (E-08) | Municipality + Civil Defense permits | Authority | High — combined approvals |

**Recommendation:** Show these as parallel external tracks in the Gantt, NOT as internal activities. Mark them with a trigger flag (e.g., "EOT trigger if >14 days overdue").

#### Step 8: Verify the List Counts

The letter accompanying the list typically states "X elements direct, Y packages retained in staged route." Verify:
- Count matches actual rows in both sheets
- No elements appear on BOTH lists (contradiction)
- No critical element appears on NEITHER list (gap)

### 0d. Transmittal Letter Review

When the user drafts a letter of transmittal (e.g., for submitting a programme + Direct-to-IFC list to PMC/MoC) — verify contractual accuracy of all claims, completeness, and protective language.

**Trigger phrases:** "transmittal letter", "خطاب إحالة", "letter of transmittal", "submission letter"

#### Step 1: Verify Every Contractual Citation

For each clause cited in the letter, verify against the actual contract text (use EXTRACT_*.md files or reference cache):

| Claim in Letter | Contract Source | Verification |
|----------------|----------------|-------------|
| "Combined single design phase" | ER §2.4 | ✅ *"design phase for this D&B contract shall be combined into a single Design Development & Construction Documentation phase"* |
| "14 calendar day review period" | ER §2.4.A, SoW §6.7 | ✅ *"The review period, where applicable, shall be 14 calendar days, unless otherwise specified"* |
| "Reviews for conformance + aesthetics only" | ER §2.4, SoW §6.6 | ✅ *"Reviews by the PMC are only for contractual conformance with the ERs. These reviews do not constitute any form of technical review"* |
| "Material submittals within IFC packages" | ER §2.4.D | ✅ *"The product / material submittal shall be included in the overall Works package IFC documentation submission, and shall not be submitted independently"* |
| "Certification wording per ER §2.4.B" | ER §2.4.B | ✅ Eight-line certification wording template provided |

**Cross-reference conflict — SoW §6.5 (14 working days) vs ER §2.4.A (14 calendar days):** If the letter relies on 14 calendar days, note that SoW §6.5 says "14 working days for stage-end reviews." For Direct-to-IFC elements that bypass stage-end reviews, this conflict is moot. But flag it explicitly in the Schedule Basis document so the PMC can't ambush you later.

#### Step 2: Check Completion Date

Verify the stated contractual completion date against the known contract document (check memory, CONTRACT_REFERENCE.md, or the actual contract). If unverifiable (OneDrive lock), flag it.

#### Step 3: Verify Protective Language

Check for these protective elements in any submission letter:

| Element | Purpose | Status |
|---------|---------|--------|
| **WITHOUT PREJUDICE, WITHOUT WAIVER** | Protects all rights — prevents estoppel | Essential |
| **Article 17 (new instructions) reference** | Any direction changing agreed basis = compensation event | Recommended |
| **Government Tenders & Procurement Law** | KSA statutory framework override | Recommended for KSA contracts |
| **SI-CG-ASEER-007 position reservation** | If there's a standing dispute over SI-007 scope | Recommended |
| **EOT + compensation rights reservation** | Prevents waiver of time/cost claims | Essential |
| **Long-lead item advise (SoW §6.2)** | Discharges contractor's duty to warn | Required |

#### Step 4: Check for Internal/Confidential Content

The letter and attachments may contain internal sheets (EOT Trigger Register, QA Gate checks) that must be removed before submission. Verify the accompanying files are submission-clean.

#### Step 5: Produce Structured Feedback

Format:

```
## Transmittal Letter Review

| # | Item | Verdict | Reference |
|---|------|---------|-----------|
| 1 | Combined design phase claim | ✅ Verified | ER §2.4 |
| 2 | 14-day review period | ✅ Verified (note: SoW §6.5 conflict) | ER §2.4.A, SoW §6.7 |

### ⚠️ Items to Address Before Submission
[Ordered list of corrections or additions]

### 📋 Attachments Check
[ ] Internal sheets removed
[ ] File names match letter
[ ] Revision numbers consistent
```

#### Step 1: Confirm No Existing CG Comments

- Read the plan's `02_CG_Responses/CG_STATUS.md`
- Also check `CG_Response_Register.md` at the parent `02_Plans_and_Procedures/` level
- If no CG comments exist for that specific doc code, proceed with pattern mining

#### Step 2: Mine CG Patterns from ALL Other Project Plans

Collect CG comments from plans that HAVE received CG review. Key plans to check:

| Plan | Likely CG Code | Comments to mine |
|------|---------------|------------------|
| DMP (PL-0029) | Code C | Legends/glossary, repeated content, missing QC loop, schedule alignment |
| HSE Plan (PL-0010) | Code B/C | Named personnel required, ratios (1:50), periodic review, "Live Document" clause, training |
| Communication Plan (PL-0018) | Code C | Compliance statement, escalation matrix, stakeholder completeness, living document mechanism, phase transitions |
| Master Programme (SH-006) | Code B | Float management, scope completeness, activity sequencing, duration justification |

Read each plan's CG response files (PDFs + summary markdowns) from their `02_CG_Responses/` folders.

#### Step 3: Cross-Reference the Plan Against CG Patterns

Build a matrix with these columns:

| # | Gap Found | CG Source | Severity |
|---|-----------|-----------|----------|
| G1 | Description of missing content | Which plan/comment it derives from | **Code C** / High / Medium / Low |

Severity taxonomy:
- **Code C** — Missing content that CG has previously rejected other plans for (living document clause, compliance statement, escalation matrix)
- **High** — Gap CG would flag as a formal comment (blank key personnel names, missing phase transition mechanism)
- **Medium** — Gap CG would note but may not block approval (missing SCE registry, acting PD without timeline)
- **Low** — Minor completeness issue CG may mention (missing glossary, unsigned fields)

#### Step 4: Check Against Project's Own 07_Guidelines (PMBOK Compliance Review)

When the project's plan folder has a `07_Guidelines/` directory containing PMBOK-aligned guideline files (numbered 01-08), these define the PMBOK framework the project is meant to follow.

**Always check `reference/PMBOK_Complete_Reference.md`** under the parent `02_Plans_and_Procedures/reference/` folder — it contains the full PMBOK 6th Ed. process matrix and 7th Ed. principles/domains.

1. **Read all 8 guideline files** — they map to PMBOK 6th Ed. knowledge areas:
   | # | Guideline | PMBOK Process |
   |---|-----------|--------------|
   | 01 | Resource Identification | 9.1 Plan Resource Mgmt (RBS) |
   | 02 | Resource Acquisition | 9.3 Acquire Resources |
   | 03 | Roles & Responsibilities | 9.1 (RACI/RAM) |
   | 04 | Project Organization Charts | 9.1 (Org structure) |
   | 05 | Team Resource Management | 9.4 Develop Team + 9.5 Manage Team |
   | 06 | Physical Resource Management | 9.3 Acquire Resources |
   | 07 | Resource Control | 9.6 Control Resources |
   | 08 | Resource Release Criteria | 9.6 (Demobilization) |

2. **Identify the relevant PMBOK process area** (e.g., PMBOK 6th Ed. §9.1-9.6 for Resource Management). Use the PMBOK_Complete_Reference.md for process definitions.

3. **Build a PMBOK compliance matrix** with these columns:

   | PMBOK Element | 07_Guideline | In Plan? | Note |
   |---|---|---|---|
   | RBS (Resource Breakdown Structure) | 01_Resource_Identification | ❌ Missing | Most fundamental PMBOK output |
   | RACI / RAM | 03_Roles_Responsibilities | ❌ Missing | Separate 02.9_RACI exists but plan doesn't reference |
   | Authority levels | 03_Roles_Responsibilities | ❌ Missing | L1-L4 delegation not defined |
   | Training plan | 05_Team_Resource_Management | ❌ Missing | Guideline requires it |
   | Team charter / ground rules | 05_Team_Resource_Management | ❌ Missing | Per PMBOK 9.4 |
   | Conflict resolution | 05_Team_Resource_Management | ❌ Missing | Per PMBOK 9.5 |
   | Physical resource mgmt | 06_Physical_Resource_Management | ❌ Missing | Equipment/materials tracking |
   | Resource control process | 07_Resource_Control | ❌ Missing | Plan vs actual, variance analysis |
   | Change control for resources | 07_Resource_Control | ❌ Missing | Per PMBOK 9.6 |
   | Demobilization procedure | 08_Resource_Release | ❌ Partial | Timeline only, no formal release procedure |

4. **Separate into categories:**
   - 🟢 **Well-aligned** (keep, no change needed)
   - 🔴 **Priority gaps** (fix before submission)

5. **Cross-reference companion documents** the plan should cite:
   - Key Personnel Register (KP-0001)
   - Master Programme (SH-006) — state alignment and whether it's under resubmission
   - RACI (separate doc at 02.9_RACI)
   - Companion plans (BEP, DMP, PEP, HSE Plan)
   - Contract / SoW / Employer's Requirements

6. **Add CG "Living Document" checklist** — CG requires all plans to include:
   - [ ] Periodic review clause (quarterly, aligned to gates)
   - [ ] Trigger-based revision clause (rule changes, major incidents, management changes)
   - [ ] Phase transition mechanism (P3→P4 design→construction, P4→P5 construction→T&C)
   - [ ] CDE re-submission requirement (all revisions via Aconex)
   - [ ] Compliance declaration (addresses cross-cutting CG directives from DMP, Comm Plan, Master Programme)

7. **Produce recommendations** ordered by priority, each with a specific fix action.

8. **Run a reverse section inventory** — After checking which PMBOK elements are missing from the plan, do the complementary check: read every existing section of the plan and assess whether each is PMBOK-standard, operationally justified (non-standard but worth keeping), or potentially removable. For each section, record:

   | Section | PMBOK Standard? | Justification | Verdict |
   |---------|----------------|---------------|---------|
   | §1 Document Control | ❌ Not PMBOK | Contract transmittal protocol — every submission needs this | 🟢 Keep — admin requirement, no reviewer flags it |
   | §6.2 Office/IT Setup | ⚠️ Operational detail | Shows site readiness, CG appreciates logistical planning | 🟢 Keep — trimmable if page count is a concern |
   | §8.2 Resource KPIs | ⚠️ Expanded detail | Useful site management table, demonstrates measurement discipline | 🟢 Keep |
   | §8.3 Risk Register | ⚠️ Risk is own KA | Resource-specific subset of formal risk register, shows integration | 🟢 Keep |
   | §10 Plan Governance | ❌ Not PMBOK | Compliance declaration directly addresses CG directives from DMP+CMP | 🟡 Keep if you want — shows rigor but escalations belong in Comm Plan |

   Verdict categories:
   - 🟢 **Keep** — required by project protocol (sign-off blocks, revision history, distribution list)
   - 🟢 **Keep** — operational readiness detail that CG values (office setup, training matrix, KPI tables)
   - 🟡 **Keep if needed** — shows rigor but could be absorbed into other sections or trimmed to save pages
   - ❌ **Remove** — genuinely unnecessary, duplicate, or cross-referenced elsewhere

   This prevents the common error of recommending removal of operationally useful content just because it's "not PMBOK." CG reviewers read for practical readiness alongside framework compliance.

#### Step 4a: Generate Updated Revision to Close Gaps

After the compliance review, when the user directs you to produce the updated revision:

1. **Clone the previous revision** — copy the HTML (or Word) as the starting point
2. **Update metadata**: revision number (e.g. C01→C02), date, revision log entry describing what changed
3. **Fill sign-off names** — Prepared/Checked/Reviewed/Approved/Issued (from project team data)
4. **Add new sections** following the existing document structure — keep all existing content intact, only add:
   - **RBS table** (if missing) — hierarchical resource decomposition by category (human/equipment/materials/facilities/services)
   - **Physical resource management** section — equipment/plant/material management process, inspection, storage, maintenance, sustainability, responsible parties table
   - **Training & competency development** — training matrix (induction, BIM, safety, quality, specialist) + competency management
   - **Team charter & performance** — Tuckman stages, daily/weekly/monthly reviews, conflict resolution escalation, health/welfare
   - **Resource control section** — plan vs actual comparison, variance analysis, corrective actions, monitoring tools (histograms/S-curves/EVM), resource reporting schedule, change control
   - **Plan governance section** — living document clause, phase transition mechanism, compliance declaration, escalation matrix (L1-L4), companion documents list
   - **Glossary expansion** — add any missing abbreviations (CDE, AFC, NOC, NTP, LOA, FAT, SAT, ACC, BCF, etc.)
5. **Update footers** on every page — revision number and page count
6. **Cross-reference companion documents** explicitly (RACI, KPR, Master Programme, BEP, DMP, HSE Plan)
7. **Verify** — check no stale revision identifiers remain, count pages, verify section order

#### Step 4b: CG-Ready Framing & Language Strategy (After Gaps Identified)

After identifying compliance gaps (Step 4a) but before finalizing the revision — apply framing strategy. This is about *how you present* the content to minimize CG scrutiny, not *what content* to include.

**Core principle:** CG reviewers scan for risk signals. Remove the loaded labels, keep the operational truth.

**Framing checklist for every plan revision bound for CG:**

| Original Language | Reframe As | Why |
|------------------|-----------|-----|
| "Outsourced" / "Subcontracted" | "Specialist" / "Augmented team" / "Independent specialist" | "Outsourced" signals instability; specialist = expertise |
| "Remote" / "Remote-managed" / "Remote-based" | Omit the pill classification entirely, or use "Specialist" badge. In prose: "Dubai-based" / "International specialists" | "Remote" is a risk flag — CG wonders about availability. Location-based or role-based framing is neutral |
| "Overseas-based" | "International specialists" or omit base and state F2F commitment | "Overseas" sounds distant; "International" sounds normal for a project of this scale |
| "F2F on request" | "F2F presence at [gate/milestone]" or "monthly site presence" | "On request" implies ad-hoc/unreliable; scheduled presence signals planning |
| "Remote-only" (in risk register) | "International team continuity" (normal resource chain risk) | Calling out "remote-only" as a vulnerability in the risk register is self-inflicted |
| "F2F visits" | "Site presence for design review gates" | "Visits" sounds temporary; "presence" sounds committed |
| "Full-time digital presence" <new> | Use when the person isn't site-based but is fully committed | Reassures CG the role isn't part-time despite being remote |

**Deputy/coverage strategy:** When a key role isn't on-site (e.g., BIM Manager is Dubai-based), identify and highlight the on-site deputy:

- Add a line in the org chart box: "BIM Deputy (on-site): [Name] · Role · Location"
- This turns a vulnerability ("manager not here") into a strength ("dual coverage — strategic oversight + local execution")
- Only do this when the deputy is genuinely qualified and already part of the team — never fabricate a deputy

**Pill/classification rebranding:** If the plan uses colored badges to classify staff:

- Keep "FT" (full-time) — this is positive, shows commitment
- Never use "Remote" as a badge class — use "Specialist", "Augmented", or omit the badge
- Keep "Stage" (stage-specific) — this is neutral/expected
- Update the legend accordingly

**Location Matrix wording:** For roles not based on-site/in-HO:

- Focus the description on *when they are present* (gates, reviews, milestones) rather than *where they sit* most days
- Use "X-based" instead of "remote": "Dubai-based", "London-based" — same location, different connotation
- For sustainability / specialist roles: "Independent specialist · periodic review · F2F on request" vs "Outsourced · remote review"

**Don't overstate site presence:** If a role is primarily remote with occasional site visits, keep the Location Matrix icon as ○ (visits), not ● (primary base). The user corrected: overstating site presence undermines credibility — CG may verify. Instead, strengthen the deputy/coverage argument.

**Risk register — self-inflicted wounds:** Review each risk description for language that calls out a structural vulnerability in your own staffing model:

- ❌ "Overseas BIM team continuity (remote-only engagement)"
- ✅ "International BIM team continuity"
- The risk still exists — the mitigation stays the same — but the label doesn't hand CG an objection on a plate

**Page-foot / header titles:** Keep revision identifier and "CG REVIEW" / "CG RESUBMISSION" labels accurate. Never change these as part of framing — they are submission metadata, not editorial choices.

#### Step 5: Cross-Reference Companion Documents

Check whether the plan properly references other project documents that CG considers part of the project baseline:
- **Key Personnel Register** (KP-0001) — does the plan reference it?
- **Master Programme** (SH-006) — is alignment stated?
- **RACI** (if separate from this plan)
- **BEP, DMP, PEP, HSE Plan** — companion plan references
- **Contract / SoW / ER** — authority basis

#### Step 6: Produce Structured Report

Structure the output as:

```
## CG Compliance Review — [Plan Name] RevCXX

**Document ref:** [MOC-ASEER-...]
**Status:** DRAFT (no CG submission yet)

### ✅ What's Already Addressed Well
[Table of adequate sections]

### 🔴 Gaps Likely to Attract CG Comments
[#|Gap|CG Source|Severity table]

### ⚠️ CG "Living Document" Checklist
[-] Periodic review clause
[-] Trigger-based revision clause
[-] Phase transition mechanism
[-] CDE re-submission requirement

### 📋 Section Inventory Summary
[Table: Section | PMBOK Standard? | Verdict — every section accounted for, with justification for non-standard content]

### 📋 Recommendations Before CG Submission
[Ordered list of fixes]
```

#### Common CG Recurring Gaps (Cross-Plan Patterns)

These are gaps CG has flagged across MULTIPLE plans — they will look for them in every new submission:

| Pattern | Originated In | What CG Expects |
|---------|-------------|-----------------|
| **Living Document clause** | HSE #4-6, CommPlan #8 | Periodic review, trigger-based revision, phase transition mechanism |
| **Compliance statement** | CommPlan #1 | Formal statement addressing all prior CG directives from cross-cutting plans |
| **Named personnel** | HSE #3 | All key roles filled with named persons, not blanks |
| **Escalation matrix** | CommPlan #5 | Clear escalation ladder for disputes/issues |
| **Glossary/legends** | DMP #1 | All abbreviations and symbols defined |
| **Phase transitions** | CommPlan #8, HSE | How the plan adapts at each project phase boundary |
| **QC/Review loop** | DMP #4 | Explicit quality control illustration in process flows |
| **Authority compliance** | HSE #1, DMP | SCE/MoMRAH registration, KSA regulatory references |

### 0g. CG Comment Contractual Validity Audit

When the user asks you to audit whether CG comments are themselves valid against the contract documents (SOW/ER/Contract/NRS SOW), not just whether the contractor's submissions comply with the CG comments.

**This is a fundamentally different direction from the compliance review (§0a).** The compliance review asks "does our register satisfy CG comments?" The validity audit asks "do the CG comments have a contractual basis?"

**Trigger phrases:** "audit cg comments against contract", "are cg comments valid", "cg comments vs sow and er", "did cg overstep", "check if cg comment is in scope", "مطابقة تعليقات الاستشاري مع العقد"

### Pre-Step: Check Session History Before Re-Analyzing

Before starting a fresh audit of CG comments against contract, **search session history** for prior analysis of the same comments. If the same CG comment was already analyzed in a previous session (e.g., "Concrete core testing — S2"), do not re-derive the verdict from scratch. Load the prior conclusion and only update if new information has emerged.

**Pitfall — re-analyzing closed items wastes time and may produce contradictory positions.** The user will correct you if you flag something as "borderline" that was already resolved as "within scope."

### Pre-Step: Proactively Search Contract Documents

When the user asks "audit CG comments against contract" or "check if CG comment is in scope," **do not ask the user to provide the contract documents.** Proactively search for and read:

1. `CONTRACT_REFERENCE.md` — pre-compiled summary of contract terms, payment schedule, legal caps
2. SoW (Scope of Work) — 72-page PDF in `Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/`
3. ER (Employer's Requirements) — 170-page PDF in `Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/`
4. NRS SOW — Excel matrix in `Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW_OPTION_01_updated.xlsx`
5. Pre-existing Markdown extracts in `Docs/07_Reports/07.5 Audit Report/` or `23_Scripts/notes/`

If OneDrive lock prevents direct PDF reading, check for cached extracts before reporting failure.

### Step 1: Classify Each CG Comment by Source Type

| Source Type | Authority | Example CG Comment |
|-------------|-----------|-------------------|
| **Contract Scope** — explicitly listed in SOW, ER, Annexes | Highest — mandatory | "Add scenography drawings" (SoW p.40 lists Scenography) |
| **Code Compliance** — required by SBC, NFPA, Civil Defense, MOI | Mandatory — not negotiable | "Universal Access Drawings" (SBC 201) |
| **Due Diligence** — SoW/ER general clause ("Contractor shall investigate") | Ambiguous — scope depends on interpretation | "Concrete core testing" (SoW p.66 due diligence clause) |
| **Procedural/Process** — CG's preferred format or method | Low — CG can request but not add scope | "Separate Rigging Register" (format preference) |
| **New Gate** — sequence or dependency not in contract | Invalid without formal change | "Arch approval first → Structural submission" |
| **Misdirected** — scope belongs to another party (NRS, MoC) | Pushback | "Furniture layouts" if NRS is contracted for interior design |

### Step 2: Verify Against Contract Source Documents

Check these contractual sources IN ORDER:

| Source | What It Contains | File Location Pattern |
|--------|-----------------|----------------------|
| **SoW (Scope of Work)** | 7 Parts of Work, specific deliverables, specialties list | `Contracts/01_Main_Contract/Contractors Scope of Works Document - Technical_250313/` |
| **ER (Employer's Requirements)** | Design control, review periods, codes, standards | `Contracts/01_Main_Contract/Contractors Employers Requirements - Engineering_250313/` |
| **NRS SOW (Design Consultant)** | Who does what — SAMAYA vs NRS scope split | `Contracts/02_NRS_Contract/01_Signed_Agreements/Nissen SOW_OPTION_01_updated.xlsx` |
| **Contract Reference** | Payment milestones, legal caps, document hierarchy | `Contracts/01_Main_Contract/CONTRACT_REFERENCE.md` — pre-compiled summary |
| **Annex 4 (Payment Schedule)** | 15 deliverable bundles proving scope items | Inside main contract PDF |
| **Appendix B (SOW)** | Contractor Specialist Packages vs Specialists/Consultants | Inside SoW PDF |

**OneDrive lock pitfall:** Files under `Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` may be unavailable. Check `Docs/07_Reports/07.5 Audit Report/` for pre-existing Markdown extracts (`EXTRACT_Scope_of_Works.md`, `EXTRACT_Employer_Requirements.md`). Also check `23_Scripts/notes/contracts_sow_summary.md` and `references/aseer-sow-er-scope-reference.md` from this skill.

### Step 3: Produce 5-Tier Verdict per Comment

| Verdict | Meaning | SAMAYA Action |
|---------|---------|---------------|
| ✅ **Valid** — in contract scope | SOW/ER/NRS SOW explicitly lists this deliverable | Comply — add to register/plan |
| ✅ **Valid by Code** — required by regulation | SBC, NFPA, Civil Defense code mandates it | Comply — code compliance is non-negotiable |
| ⚠️ **Borderline** — due diligence or general clause | SoW/ER has a general clause that could cover this | Clarify with CG — may be VO if material cost |
| ❌ **Invalid** — new gate, no contract basis | Not in SOW, ER, or any contract annex | Formally notify — schedule impact notification under Art. 14 |
| ❌ **Misdirected** — belongs to another party | NRS or MoC scope, not SAMAYA's | Pushback — redirect to correct party |

### Step 4: Check for Circular Requirements

**Critical pattern — CG comment "Dates match approved schedule" (#7):** If the approved schedule only covers a subset of project scope (e.g., AV-only program covering 86 days), the CG cannot demand dates for Architecture/Structural scope from a program that doesn't exist for those disciplines. This is a **circular requirement** — the program must be revised first before dates can be set.

**Response:** Flag this as a program revision requirement, not a register compliance issue. The CG comment is technically invalid until a comprehensive program is issued.

### Step 5: Check for Sequence Gates Not in Contract

**Critical pattern — CG comment "Arch approval → Structural submission" (#5):** If the contract has no clause prescribing design sequence between disciplines, the CG is adding a new procedural gate. This is a **program impact** — it creates a dependency that can extend the schedule.

**Response:** Formally notify the CG of the schedule impact. If the gate is imposed without a Change Order, reserve the right to claim EOT under Art. 14.

### Step 6: Structure the Report

```
## CG Comment Contractual Validity Audit

**Source of CG Comments:** [document name]
**Contractual Basis:** SoW [ref] · ER [ref] · NRS SOW [ref] · Contract Annex [ref]

### ✅ Valid (in contract scope)
[# | Comment | Contract Source | Action]

### ✅ Valid by Code (regulatory)
[# | Comment | Code Reference | Action]

### ⚠️ Borderline / Needs Clarification
[# | Comment | Clause | Clarification Needed]

### ❌ Invalid — No Contract Basis
[# | Comment | Why | SAMAYA Position]

### ❌ Misdirected — Wrong Party
[# | Comment | Correct Party | Action]

### 🔴 Circular Requirements
[# | Comment | Why Circular | Program Revision Needed]

### Summary — Recommended SAMAYA Response
[Comply items | Clarify items | Pushback items | Formal notification items]
```

### Pitfalls

- **Don't assume CG is always right or always wrong** — each comment must be individually verified. CG mixes valid code requirements (accessibility, evacuation) with scope creep (testing, geotech) and procedural gaps (program dates).
- **Don't confuse "not in contract" with "invalid"** — Code compliance (SBC, NFPA) is mandatory regardless of whether the SOW/ER explicitly lists it. These are "Valid by Code" not "Invalid."
- **Don't overlook the NRS SOW** — the NRS scope matrix determines who does what. Scenography may be in SAMAYA's SOW scope (SoW p.40, NRS matrix row 44) even though NRS is the lead designer. Always verify both documents.
- **"Due Diligence" is not a blank check** — SoW p.66 says "Contractor shall conduct thorough investigations of all existing structures." This covers visual inspection and document review, not necessarily destructive testing (core sampling). CG may argue it does; SAMAYA may argue it doesn't. This is a negotiation point, not a compliance item.
- **Schedule sequence is not in the contract** — The contract defines scope milestones (Annex 4 payment bundles), not the order in which disciplines approve each other. Arch→Struct sequence is a CG preference, not a contract requirement.
- **Programme dates comment is circular if the program is incomplete** — You cannot comply with a schedule that doesn't cover the scope. Demand a program revision first.

### Reference Files

- `references/cg-comment-contractual-validity.md` — session-specific examples of applying the 5-tier verdict to structural, architecture, and AV CG comments

---

## 0e. Management Review Comment Audit

When the user receives internal senior management review comments on a plan document (Project Director, GM, Group-level) — before or concurrent with CG submission — and needs each comment audited against the current plan revision.

**Trigger phrases:** "PD comments on [plan]", "director reviewed [plan]", "management review feedback", "internal review comments on [plan]", "revised comments from the projects director", "PD recommendation"

**This is distinct from CG comment disposition (§1):** Internal management comments are typically broader/mandatory (fill positions, add matrices, expand sections) rather than specific compliance/technical issues. The output is a readiness assessment, not a disposition table.

#### Step 1: Read the Review Comments

Extract every distinct item from the management review. Classify each as:

| Type | Example | Meaning |
|------|---------|---------|
| **Personnel Fill** | "Fill QA/QC Manager position" | Role exists but vacant — needs appointment |
| **New Role** | "Add Accessibility Consultant" | Role entirely absent from plan |
| **New Section/Matrix** | "Add RACI Matrix" | Complete structural addition needed |
| **Expand Existing** | "Add Detailed Manpower Histogram" | Content exists but is too high-level |
| **Process/Protocol** | "Add Succession Matrix" | Procedure exists but formal matrix missing |

#### Step 2: Read the Current Plan

Read the full plan document (HTML or Word) to understand current section structure. Search for mentions of each item from the review comments.

#### Step 2a: Verify Each "New Role" Request Against Contract Scope

When the PD asks to add a role that isn't in the current plan, **do not automatically accept or reject** — verify whether the role is contractually required first.

Check these sources in order:
1. **SoW §5.4 (Design Team Profile)** — lists mandatory specialists (Accessibility Consultant, Acoustics/Humidity Specialist)
2. **SoW §5.5 (Staffing)** — minimum required roles (AV, Interactives, Setworks, Models, Graphics, Lighting, Showcase, MEP, BIM, T&C, FLS, Café Shade, Landscaping, Structural Engineer)
3. **Appendix B** — two columns: Contractor Specialist Packages (left) vs Specialists/Consultants (right)
4. **Stakeholder Plan CG Comments** — CRS items often flag missing roles (IT/Security T1, Interior Designer, MEP Designer, Org Chart)
5. **DMP/CommPlan CG comments** — cross-cutting directives (Living Document, Compliance Declaration, Escalation Matrix)

For each role the PD wants added, determine:

| Finding | Verdict |
|---------|---------|
| Required by SoW §5.4/§5.5 or Appendix B | ✅ Accept — contractual requirement we missed |
| Required by CG comments on companion plans | ✅ Accept — CG will flag this if absent |
| PD's personal preference, not contractually required | 🟡 Evaluate — may be useful but not mandatory |
| Already covered by another role or plan | 🔵 Push back — reference existing coverage |
| Belongs in a different plan, not this one | 🔵 Redirect — Construction Org Chart → Mobilization Plan, Exhibition Matrix → Subcontractor Register |

**Pitfall — Don't assume PD knows the contract better than we do:** PD may request things that are already covered under a different name or mechanism, or may request things that have no contractual basis. Always verify against SoW/ER/Appendix B before accepting or rejecting.

#### Step 2b: AI Fingerprint Detection in Review Comments (Optional)

When the PD's comment has an unusual format (emojis, mechanical parallelism, template sentences), it may be AI-formatted. Detect and note:

| Signal | Likelihood | Example |
|--------|------------|---------|
| ✅ emoji before every list item | 🔴 Very high | `✅ Fill QA/QC Manager` x10 — ChatGPT's default list format |
| All items follow identical grammar (Verb + Noun Phrase) | 🟠 High | `Fill X`, `Nominate Y`, `Add Z` — uniform parallelism |
| Template opening sentence | 🟠 High | `I have reviewed [X], and it can be submitted to [Y] if an urgency however I have the following recommendation...` — formulaic AI structure |
| Covers all standard PMBOK areas at once | 🟡 Medium | RACI, histogram, succession, org chart, 3 specialist roles all in one pass — enumeration pattern |
| Non-standard grammar alongside polished formatting | 🟡 Medium | `if an urgency`, `recommendation that be incorporated` — AI hallucinating ESL voice |

**How to use this:** Don't dismiss the comments because they look AI-generated — the substance may still be valid. But flag AI formatting to the user so they know the PD likely used a tool, not deep reading. The real value is in the **contract verification step (2a)** — AI-generated comments often miss project-specific contractual requirements and over-apply generic PMBOK templates.

#### Step 3: Map Each Comment to Current State

For each review item, produce:

| Column | Description |
|--------|-------------|
| **Item #** | Numbered from PD's list |
| **PD Recommendation** | Exact wording from reviewer |
| **Rev CXX Status** | What the current plan says about this |
| **Gap** | Description of what's missing or insufficient |
| **Severity** | 🔴 Must act (absent or unfilled) / 🟡 Partial / 🟢 Already covered |

Typical gap categories:
- **🔴 Absent** — role, matrix, or section doesn't exist anywhere in the plan
- **🔴 Vacant** — role exists but no person appointed (plan says "Vacant", "TBC", "hiring")
- **🟡 Partial** — exists but too high-level (e.g. aggregate curve vs detailed histogram; process description vs formal matrix)
- **🟢 Covered** — adequately addressed

#### Step 4: Structure the Audit Report

```
## Management Review Audit — [Plan Name] Rev CXX

### [Item 1–N individual rows]

| # | PD Recommendation | Rev C00 Status | Gap | Severity |

### Summary

| Severity | Count | Items |
|----------|-------|-------|
| 🔴 Absent/Missing | N | ... |
| 🔴 Must appoint | N | ... |
| 🟡 Expand | N | ... |
| 🟢 Covered | N | ... |

### Recommended Actions
[Ordered by priority — appointments first, then new sections, then expansions]
```

#### Step 5: Classify Each Comment by Responsibility

Before finalizing the audit, split each item into:

| Owner | Items | What We Do |
|-------|-------|------------|
| **Plan Team (us)** | New sections, matrices, expanded content, missing role definitions | Add to plan document |
| **PD/HR (them)** | Named personnel, filling vacancies, hiring specialists | Flag vacancy in plan — appointment is their action |

**Critical rule — plan defines roles, not persons.** When a PD says "Fill QA/QC Manager" or "Nominate T&C Manager" and the plan already shows these as "Vacant" / "TBC," the plan is correct. The gap is in hiring, not documentation. Classify these as **PD/HR responsibility items**, not plan content gaps. The plan cannot name people who haven't been appointed.

#### Step 6: Include Next-Step Context

State whether the current revision can still go to CG as-is (per conditional approval) and what the management review expects in the next revision. Note any revision numbering discrepancies found (e.g., CG_STATUS.md says C03 but files on disk show C00).

**Pitfall — Don't confuse management review with CG disposition:** Internal PD comments are directives (do this by Rev 01), not review outcomes (Code B/C). The response is a coverage audit + action plan, not a comment disposition table. Never wrap management comments into a CG-style disposition table — they are pre-submission instructions, not post-review findings.

**Pitfall — Don't report vacant positions as plan gaps:** A plan that shows a role as "Vacant" or "TBC" has done its job — it identified the gap. Appending "Must appoint" as a plan corrective action is wrong. Move these items to a separate PD/HR action column in the audit summary. Only plan-missing content (absent roles, missing matrices, insufficient detail) belongs as plan document gaps.

**Pitfall — Don't accept all PD asks at face value:** PD may request items that are (a) already covered, (b) not contractually required, or (c) belong in a different plan. Always verify against SoW §5.4, Appendix B, and companion plan CG comments before deciding what to add. A PD asking for an org chart for construction phase may need the Construction Mobilization Plan, not the RMP.

### 0h. Sustainability Plan / SMP Review

When the user receives a Sustainability Management Plan (SMP) or scope reduction register from a sustainability consultant and asks you to review it against project requirements — including cross-referencing internal PD comments that may contradict CG directives.

**Trigger phrases:** "review sustainability plan", "audit SMP against contract", "check sustainability scope", "review against project requirements", "sustainability manager scope"

#### Step 1: Identify the Document's True Nature

Not every document titled "Sustainability Management Plan" is actually a plan. Check:

| Document Type | What It Contains | Red Flags |
|---------------|------------------|-----------|
| **Actual SMP** | Strategy, compliance framework, deliverables schedule, R&R, reporting cadence | None — this is what CG expects |
| **Scope Reduction Register** | Proposes deleting sections, eliminating roles, reassigning duties to existing teams | 🔴 **Self-negating** — if the consultant wrote it, they're arguing their own role shouldn't exist |
| **Invoice** | Payment request attached alongside the plan | 🔴 **Premature** — invoice before plan approval is a red flag. Payment should be tied to approval gates, not submission |

**Critical check:** If the consultant sends BOTH a plan and a scope reduction register simultaneously, the documents contradict each other. The reduction register undermines the plan's credibility.

**🚨 Self-Contradictory Submission Pattern:** When a consultant sends two documents in the same email — an SMP establishing their role AND a scope reduction register proposing to delete that role — this is internally inconsistent. The reduction register argues the role shouldn't exist while the SMP assumes it does. Flag this explicitly: the consultant cannot have both positions. The reduction register is likely a cost-reduction exercise, not a genuine plan improvement document.

**🚨 SMP Not Available Locally:** The actual SMP is often an email attachment that never gets saved to the project filesystem. The only document available locally may be the scope reduction register or the CG/PD email thread. When the user says "review the SMP" and only a reduction register or email PDF is in Downloads, state clearly: "The actual SMP is not available locally — only [X] was found. The SMP was an email attachment that needs to be saved to the project folder first." Do not fabricate an SMP review from the reduction register alone.

#### Step 2: Map Against CG's Explicit Directives

CG's approval of the Sustainability Manager typically comes with conditions. Extract these from the CG approval email and build a compliance matrix:

| CG Condition | SMP Says | Verdict |
|-------------|----------|---------|
| Submit detailed R&R for Sustainability Manager | [check] | ✅ / ❌ |
| Coordinate with Lead Designer (NRS) | [check] | ✅ / ❌ |
| Submit comprehensive plan within 1 week | [check] | ✅ / ❌ |
| Adhere to Mostadam + SBC 1001 | [check] | ✅ / ❌ |

**If the scope reduction register proposes deleting the role CG just approved** → flag as a direct contradiction. The CG approval email is the authoritative document — the reduction register cannot override it.

#### Step 3: Audit Each Reduction Item Against Contract

For each item in a scope reduction register, produce a 3-way verdict:

| Verdict | Meaning | Example |
|---------|---------|---------|
| ✅ **Valid reduction** — item genuinely duplicates existing plans (HSE, QA/QC) | Accept — merge into existing processes | Waste management → HSE Plan already covers this |
| ⚠️ **Partial** — item can be reduced but not eliminated | Accept reduction, reject deletion | Reporting frequency: daily→monthly is fine, but monthly reports are required by SoW §13.9 |
| 🔴 **Reject** — item is contractually required or CG-mandated | Keep as-is | Sustainability Manager role — CG just approved it |

**Contractual basis for sustainability requirements:**
- **SoW §13.9** — Sustainability management plan and monthly reporting
- **ER §3.7.XIII** — Mostadam Manual + SBC 1001 as applicable codes
- **ER §2.7** — Sustainability integrated into design and operation
- **Contract Article 7** — Environmental protection (waste, IAQ, site management)
- **CG approval email** — Explicit conditions for the role

#### Step 4: Handle Internal PD Comments That Conflict with CG

When the Project Director's comments contradict CG's explicit directives, do NOT automatically side with either. Produce a **conflict resolution table**:

| Topic | PD Says | CG Says | Recommended Path |
|-------|---------|---------|-----------------|
| Role title | "Sustainability Specialist" not "Manager" | Approved as "Sustainability Manager" | **Keep CG's title** — changing it requires re-approval |
| Role type | Part-time/advisory, no full-time | Full R&R required | **Part-time is fine** — R&R can reflect as-needed engagement |
| Design phase | Minimal — avoid design changes | Coordinate with NRS on deliverables | **Light touch** — NRS coordination yes, but no design rework |
| Reporting | Monthly/weekly only | Monthly progress report per SoW §13.9 | **Monthly** — aligns with both |
| Document title | "Project Sustainability Strategy" | "Sustainability Plan & Strategy" | **Use ER's terminology** — "Project Sustainability Strategy" per ER §3.7.XIII |
| Cost impact | State no cost/time impact | Not addressed | **Include the protection statement** PD wants |
| HSE overlap | Remove duplication | Not addressed | **Reference HSE Plan**, don't duplicate |

**Framing for the PD reply:**
- Agree on valid points (cost protection, HSE de-duplication, monthly reporting, execution-phase focus)
- Explain why CG-mandated items must stay (title, NRS coordination, Mostadam compliance)
- Propose a middle ground that satisfies both

#### Step 5: Add the Contractual Protection Statement

CG's approval email and the SMP itself create a risk that sustainability requirements could be interpreted as scope/cost additions. Add this statement to the strategy:

> *"No sustainability-specific guidelines or initial design criteria were provided with the tender documents. The design criteria and material initial selection were already defined in RIBA Stage 3. Therefore, no cost or time impact shall arise due to sustainability requirements that may affect the project's already-defined cost and time baseline."*

This protects against CG later claiming that sustainability requirements justify scope changes.

#### Step 6: Check for Invoice-Before-Approval Pattern

If the consultant attached an invoice for payment alongside the unapproved plan:

| Issue | Why It's a Problem | Action |
|-------|-------------------|--------|
| 50% payment requested before plan review | Payment should be tied to approval milestones, not submission | Withdraw invoice until SMP is approved |
| "As agreed" without written evidence | No documented payment terms in project files | Request written payment terms before processing |
| Remaining 50% on "final approval" | Ambiguous — who approves? CG or Samaya? | Define approval gate clearly |

**Response:** Instruct the consultant to withdraw the invoice until the SMP is formally approved by CG. Payment milestones should follow the DMP gate structure (50%/90%/100% IFC), not submission.

#### Step 7: Produce Structured Audit Report

```markdown
## Sustainability Plan / SMP Review

**Documents reviewed:**
- SMP / Scope Reduction Register: [filename]
- CG Approval Email: [date]
- PD Comments: [filename]
- Contractual basis: SoW §13.9 · ER §3.7.XIII · ER §2.7 · Contract Art. 7

### 🔴 Critical Issues (Block Submission)
[# | Issue | Source | Why Critical]

### 🟠 High-Severity Issues
[# | Issue | Source | Recommended Action]

### 🟡 Medium / Low Issues
[# | Issue | Source | Recommended Action]

### ✅ Valid Reductions (Accept)
[# | Item | Why Valid]

### ⚠️ PD-CG Conflict Resolution
[Topic | PD Position | CG Position | Recommended Path]

### 📋 Recommended Actions
[Ordered list — what to tell the consultant, what to tell PD, what to submit to CG]
```

#### Pitfalls

1. **Don't assume a "Sustainability Management Plan" is actually a plan** — It may be a scope reduction register. Read the content, not the title.
2. **Don't ignore the invoice** — A consultant sending an invoice before plan approval is a red flag. Flag it explicitly.
3. **Don't side with PD over CG (or vice versa)** — Produce a conflict resolution table that respects both positions. Agree on valid PD points, explain why CG-mandated items must stay.
4. **Don't forget the contractual protection statement** — The "no cost/time impact from sustainability" statement protects against future scope creep claims.
5. **Don't miss the 1-week CG deadline** — If the deadline has passed, flag the urgency. The plan needs to be submitted ASAP.
6. **Self-negating documents** — If the consultant's scope reduction register proposes eliminating the role CG just approved, this undermines the consultant's credibility. Flag it.
7. **Mostadam certification vs compliance** — ER §3.7.XIII lists Mostadam Manual as an applicable code. This means Mostadam compliance (following the manual's criteria) is required, but certification (scoring/rating) is not unless explicitly stated. The strategy should be framed as code-compliance, not certification-chasing.

### 0f. Incoming CG Email — Communication Protocol Verification

When CG sends a request or instruction directly to a specific role (e.g., Technical Office Manager, Engineer), **do not assume the routing is correct**. CG often sends informal coordination emails that bypass the formal Communication Matrix. Before actioning:

1. **Identify the deliverable type** — what is CG asking for? (schedule, plan submission, prequal, RFI, NCR response, material submittal)

2. **Verify recipients via SQLite before any analysis** — the `Message_Preview` column does NOT show To/CC headers. Never infer who was included from the preview. Query:
   ```sql
   SELECT m.Message_ToRecipientAddressList as to_list,
          m.Message_CCRecipientAddressList as cc_list
   FROM Mail m WHERE m.Record_RecordID = <ID>;
   ```
   **Pitfall: Preview does not contain headers.** Getting recipients wrong undermines the entire analysis. Always check the DB.

3. **Cross-reference the approved Communication Plan's Communication Matrix**:
   | Matrix Field | Check |
   |-------------|-------|
   | **From** | Who should originate the response per the matrix? (Contractor → CG, Engineer → CG, etc.) |
   | **To** | Who is the correct addressee? (CG, ACE, PMC, MOC?) |
   | **Action** | Is this for Review, Reply, Approval, or Info? |
   | **Reply Time** | Is the requested turnaround within contractual limits? |

3. **Check Communication Rules** (from the approved Plan):
   - **Rule 4/5**: Engineering submittals → addressed to **Project Directors**, with other key personnel in CC
   - **Rule 7**: Emails missing key personnel are not considered officially received
   - **Rule 11**: All submittals must be **stamped and signed by the Contractor's Project Manager**
   - **Rule 13**: Separate email per topic

4. **Categorize the email**:
   - **Informal coordination** — CG sent directly to you for pre-submission alignment. OK to respond informally, but formal submission still routes through PM.
   - **Formal request** — CG expects a formal response. Requires PM stamp/signature per Rule 11.
   - **Misrouted** — CG addressed the wrong person. Respond stating the correct channel per the Communication Plan.

5. **Outcome**:
   - If the request should come from the **Contractor's Project Manager** per the matrix, advise: "This is informal coordination to me as TO Manager — the formal response must be signed by the PM and submitted per the Communication Plan."
   - Draft the PM's response for their sign-off rather than responding directly.
   - Ensure all key personnel (CG Project Director, ACE PM, MOC PM) are CC'd per Rule 4.

**Example** (Aseer Museum, PL-0018 Rev.02 Communication Matrix):
> CG sent "Deliverables Submission Schedule" request directly to Technical Office Manager. Matrix Item 19 (Time baseline) shows From=Contractor, To=CG, Action=Approval. Per Rule 5+11, the formal response must come from the Contractor's Project Manager, not the TO Manager directly.

**See also:** `references/aseer-communication-matrix.md` for Aseer Museum PL-0018 Rev.02 matrix items and rules.

### 0. Monitor CG Response Status (Pre-Response Phase)

Before a CG response arrives, when the user asks "check CG response" or "check status":

1. **Read CG_STATUS.md** (per-plan summary in `02_CG_Responses/`)
2. **Cross-reference CG_Response_Register.md** (master register at `Docs/02_Plans_and_Procedures/CG_Response_Register.md`)
3. **CHECK OUTLOOK EMAIL DIRECTLY** — do NOT rely solely on status files. They may be stale (last updated date in file header). Use:
   - **Email archive register** (`Register_ASEER_Professional.csv` in `Docs/Email Archive/مشروع متحف عسير الإقليمي/`) — definitive record of submission/reply emails with doc codes and statuses
   - **Live Outlook scan** via AppleScript or body search for the document code (e.g. `PL-0020`, `Stakeholder Management Plan`). See `outlook-email` skill's `references/cg-email-triage.md` for the canonical SQL query and triage pattern (filtering by @cg.com.sa domain, identifying A/B/C/D/NCR codes from previews, extraction).
   - Pattern: Hesham sends submission → CG (Mohammad Elbaz) replies. If no reply email from CG exists, status is genuinely pending.
4. **If no response found**: report as "⏳ Submitted — Awaiting CG Response", note the submission date and conduit (e.g. Hesham Abdelhameed)

The user corrected: *"check outlook mail you will find"* — status files are useful summaries but Outlook email is the authoritative source for whether a CG reply has been received.

### 1. Analyze Review Comments

- Read the CG reply document (PDF/letter) and extract all comments
- Classify each comment:
  - **Structural** — requires changing document content (workflows, sequences, matrices)
  - **Administrative** — requires adding metadata, references, or compliance statements
  - **Clarification** — requires adding explanation or cross-references to existing content
- Identify which comments are already addressed by the current document version

### 2. Create New Revision

- Clone the previous revision file (e.g., `RevC01 → RevC02`)
- Update throughout:
  - Document title and header revision identifiers
  - All page headers (`CRP Rev CXX`, `DMP Rev CXX`, etc.)
  - All page footers (doc number + revision)
  - Cover page title, date, and revision badge
  - Revision history table — add new row, mark previous row with its review outcome (Code B/C)
  - TOC snapshot revision badge and date
  - Disposition chip in section headers

### 3. Add Comment Disposition Table

Insert a new section (typically §1.5 after Related Documents) on Page 03 / Document Control:

```
§1.5 CG Comment Disposition — response to CG review of [Doc Ref] ([Date])

| #  | CG Comment          | Resolution & Section Reference |
|----|---------------------|-------------------------------|
| 1  | Brief comment title | §X.X — how it was addressed   |
```

- Each row maps one CG comment to the specific section(s) that resolve it
- Add a compliance strip stating: the review outcome, date, reviewer, and that this revision addresses all comments for Code A/B resubmission

### 4. Address Structural Comments

For each comment requiring content changes:

| Comment Type | Common Edits |
|-------------|--------------|
| **Workflow sequence** | Reorder flow-row nodes in §7.x submission/submittal workflows |
| **Distribution chain** | Update recipient fields in report/matrix tables to show sequential flow (→ arrows) instead of parallel lists |
| **Missing matrix/table** | Add the required table (escalation ladder, stakeholder register, distribution matrix) |
| **Responsibility clarification** | Update RACI roles, add contractual responsibility statements |
| **Living document mechanism** | Reference existing PDCA/KPI review sections, add phase-transition language |

### 5. Update Status Tracking

- Update `CG_STATUS.md` — mark previous submission as addressed, add new submission row with ⏳ status
- Create `CRP_RevCXX_STATUS.md` (or equivalent) documenting:
  - What changed from previous rev
  - How each CG comment was addressed
  - Date and status of resubmission

### 6. File Naming Convention

```
Rev CXX:  Aseer_[PlanName]_RevCXX_Comprehensive.html
Status:   CRP_RevCXX_STATUS.md (in 03_Supplementary/)
CG Track: CG_STATUS.md (in 02_CG_Responses/)
```

---

### Variant B: Personnel / CV Submittal Rejections (Design Team Approval)

When CG rejects a personnel submittal (e.g., MEP design team CVs) with Code D (Rejected) or Code C (Revise & Resubmit), the response differs fundamentally from plan document revisions.

> For exact clause text and document locations, load `references/contract-clause-mapping.md` from this skill.

#### 1. Identify the Contract Basis

The CG rejection will cite specific contract clauses. Map them to actual contract documents:

| CG Reference | Likely Source | What It Says |
|-------------|---------------|-------------|
| **Technical Proposal Section, Page N** | Main Contract, Appendix 3 (Contractor's submitted Technical Proposal) | Samaya's own bid commitments — CG holds you to what you proposed. Check your submitted methodology. |
| **SOW Appendix, Page N** | `Contractors Scope of Works Document` | Contains Definitions (Designer, Sub-Consultant, Contractor) and Staffing requirements |
| **ER Appendix, Page N** | `Employer's Requirements` | Contains Design Control and Certification requirements |

#### 2. Find the Designer Definition (SOW, Definitions section)

The key clause is the **Designer** definition — establishes the two valid paths:

> "Designer means the Contractor or the entity sub-contracted by the Contractor who is responsible for design and documentation of the Works. **The Designer can either be an externally appointed design consultancy and/or an inhouse design and engineering team** having appropriate and approved qualifications, experience and Authority registration in the disciplines relevant to the Works."

**Two paths** (the "and/or" means you can use either or both):

| Path | Structure | Documentation Required |
|------|-----------|----------------------|
| **Path A — Inhouse team** | Engineers are Samaya employees | Employment contracts, GPOWI, social insurance, SCE classification, company ID |
| **Path B — External consultancy** | Registered firm engaged as subconsultant | CR, SCE firm classification, PII insurance, VAT cert, commercial registration |
| **Hybrid (A+B)** | Samaya inhouse + one or more subconsultants | Both sets of docs |

#### 3. Extract Documentation Gaps

CG rejection tables typically flag per-engineer deficiencies. Build a gap matrix:

| Engineer | Position | CG Rejection Reason | Missing Document |
|----------|----------|---------------------|-----------------|
| Name | Role X Lead | Comment Y | SCE cert / COC / Employment proof / Experience insufficient |

Common missing docs checklist:
- **SCE classification certificate** (individual engineer) — required by ER Section 2.4 "registered engineers"
- **COC (Certificate of Completion)** for similar KSA projects showing engineer's role
- **Employment proof** (contract, GPOWI, insurance) — required for Path A (inhouse)
- **Detailed CV** with project history showing specific responsibilities
- **CR (Commercial Registration)** — required for Path B (firm)
- **PII (Professional Indemnity Insurance)** — required for Path B firms
- **Experience** — SOW Section 5.5 requires "appropriately qualified, skilled and experienced." Junior engineers (<5yr) often rejected.

#### 4. Determine Response Strategy

Based on the gap matrix and chosen path:

| Situation | Recommended Move |
|-----------|-----------------|
| Engineers are Samaya employees but not documented | Submit employment contracts + GPOWI + SCE certs. Keep Path A. |
| Engineers are external freelancers | Register them as a consultancy (CR+SCE) for Path B, OR hire as Samaya employees for Path A — no middle ground. |
| Engineers are from a registered firm | Submit firm's CR, SCE class, PII, and the engineer's SCE cert + COC under the firm's letterhead. |
| Junior engineers with insufficient experience | Replace with senior engineers (>=7yr MEP design). SOW Section 5.5 is explicit about qualification. |
| CG cites Technical Proposal commitment | Read Samaya's submitted bid (Appendix 3 in contract) to see the exact commitment. You may need to align with what you promised. |

#### 5. Reference Contract Clauses in Your Response

For the resubmission cover letter, cite:
- **SOW Section 1.4** — Designer definition (establishes Path A and Path B)
- **SOW Section 5.4** — "The Contractor must submit profiles of the proposed design team members for approval"
- **SOW Section 5.5** — "MEP Specialist" listed as required role; "appropriately qualified, skilled and experienced"
- **SOW Section 6.21** — Sub-Contractors / Sub-Consultants (Path B mechanism)
- **ER Section 2.4** — "All design must be carried out by suitably qualified, experienced and registered engineers"
- **Main Contract Article 13** — Subcontracting provisions (up to 30% without special approval)
- **SOW Section 7.3** — Engineering design must be by "local registered / licensed engineers"

#### 6. Sample Response Structure

```
Subject: Resubmission — MOC-MUS-ASE-1K0-ZD-0050 (Rev.01) MEP Design Team CVs

CG Comments addressed:

1. Comment 01 (Design Firm Engagement):
   The Contractor elects Path [A/B/Hybrid] per the Designer definition
   in SOW Section 1.4. Attached: [proof of employment OR firm registration].

2. Comment 02 (Employment Verification):
   Attached: Employment contracts, GPOWI, SCE certificates for all
   proposed engineers demonstrating they are [Samaya staff / part of
   [Firm Name] / both].

3. Comment 03 (Qualifications):
   All CVs updated with:
   - SCE classification certificates (individual)
   - COCs of similar KSA projects with named role
   - Detailed project histories
   [Replaced] Engineer X (1yr exp) with Engineer Y (8yr exp).
```

#### 7. Status Tracking

- Create a tracker per submission ref (e.g., `MOC-MUS-ASE-1K0-ZD-0050_STATUS.md`)
- Document: what was submitted, what CG rejected, which docs were missing, what was replaced
- Update the master submittal register if one exists

### Role-Based Plans vs Name-Based Registers

**Principle:** Project management plans define **roles, responsibilities, reporting lines, and interfaces** — not individual names. Names change (departures, replacements) and embedding them in plans requires a new revision every time. The live **Key Personnel Register (KPR)** is the authoritative source for current names.

**Implementation in plan revisions:**

- Reference the role, not the name: `T1-01 · Project Director · Responsible for overall project delivery`
- Add a compliance note: *"Current personnel names and approval status maintained in live Key Personnel Register (KPR) [Ref]"*
- In QC sign-off blocks: use "Per live KPR" instead of individual names
- Only deviate for statutory roles (SEC, Municipality, CITC, MOI) — those are role-based by nature, not Samaya hires
- Never populate a name in KPR or plan without email evidence confirming appointment

### Designer vs Contractor/Installer Classification

When reviewing specialist roles against Appendix B / Contract Scope of Works, distinguish:

- **Designer (Specialist)** — individual consultant or firm doing design/consultancy (ZNA Lighting design, AD Engineering MEP design, Nama FLS design)
- **Contractor/Installer (Package)** — company contracted for supply, fabrication, installation (Rawasen AV supply/install, Glasbau Hahn showcase supply/install)

Some items are **combined** (one entity does both): Samaya Graphit (Graphics: design + production + install). Some items need **both**: M&E (AD Engineering design + M&E Contractor installation package).

### CG Comment Status Terminology

- **COVERED** — addressed in this revision but CG has NOT yet reviewed it (badge-low)
- **CLOSED** — CG explicitly confirmed the resolution in a prior review round (badge-pass)
- **SUBMITTAL-PENDING** — depends on external submittal not yet approved (badge-high)
- **IN-PROGRESS** — action underway, not yet complete (badge-low)
- **RE-OPENED** — CG withdrew closure because supporting documents not provided (badge-critical)

Rule: Never mark an SMP-scope item CLOSED unless CG has explicitly reviewed and accepted it.

### CG Disposition Table Column Widths (A4 print)

CG Comment column must be widest (~264px), Disposition column ~120px, Ref ~50px, Status ~72px, Route/Scope ~100px.

### CG Comment Text Preservation

Never rewrite, summarize, or rephrase CG comment text in the disposition matrix. Preserve exact wording. Only the Disposition/Action column is ours to update.

### Revision History — Formal Submissions Only

CG-facing revision history should contain only formally submitted versions. Do NOT include internal drafting iterations or QC-only passes.

### CG Document Number Pattern

Use the CG-facing formal document number from response PDFs (MOC-MUS-ASE-1K0-PL-0020), not internal project codes (MOC-ASEER-SIC-1K0-PL-0020).

---

## §4b — CG-Ready Language & Framing Strategy (absorbed from cg-approval-packaging)

### Red Flag Search Patterns

When reframing a document for CG approval, search for these loaded labels and replace them:

| Red Flag | Replace With |
|----------|-------------|
| `outsourced / remote-managed` | Remove standalone box; merge into org tiers |
| `remote` (pill badge) | `specialist` or `augmented` |
| `F2F on request` | `monthly site presence` or `F2F at design review gates` |
| `remote-only engagement` (risk register) | `specialist availability constraints` |
| `Overseas-based · remote` | Remove "Overseas" and city names — use role description only |

### KPR Cross-Reference — Personnel Name Verification

Before submitting ANY document that names personnel (org chart, resource plan, stakeholder plan, responsibility matrix), every name must be verified against the KPR Excel file. This is a mandatory gate:

| KPR Status | Action |
|-----------|--------|
| `Approved` / `Code A` / `Code B` | Keep the name. Use the KPR's entity name. |
| `Pending` / `Under Review` | Keep the name — the person IS on board. Do NOT blank the name. |
| `Code C` / `Revise and Resubmit` | Keep the name — show "submission in progress". |
| `Vacant` / `TBC` / not in KPR | Show `—` or "Vacant". Do not guess. |

### Exhibit Approval Status Display Rules

| Situation | Display |
|-----------|---------|
| Firm assigned, pending CG approval | `Firm — pending approval` |
| Firm assigned, CG approved | `Approved` (no firm name repeated) |
| Firm assigned, Code B | `Code B approved [date]` |
| No firm assigned (TBC) | `TBC` — no qualifying commentary |

### Reference Files

See `references/aseer-resource-plan-changes.md` and `references/aseer-resource-plan-c00-kpr-sync.md` for before/after examples of CG-ready reframing.

### §0g — Deliverable Submission Schedule Review Response

When Samaya/CG/PMC returns review comments on a **Deliverable Submission Schedule (Excel)**, produce a revised schedule addressing every comment. Workflow: extract PDF comments → map to schedule changes → build revised Excel with openpyxl → apply color conventions (yellow=new, orange=architectural). See `references/deliverable-schedule-review-response.md` for full workflow, Python patterns, and pitfalls.

---

## §0g — Outgoing Document QA Review (absorbed from outgoing-document-qa-review)

Before any formal document (RFI, TQ, submittal) is issued to CG/PMC/MoC via Aconex, run this three-layer QA check:

### Required Inputs
1. The document under review (HTML and/or PDF)
2. Style guide at `_Style-Guides/`
3. Contract reference set (SOW, ER, programme)
4. Communication Plan (routing, distribution, SLAs)
5. Stakeholder / contact register
6. RFI/SI register (confirm document is logged)
7. Gallery/room/code lists for entity-name verification

### Check 1 — Format & Document Control
- Style-guide conformance: fonts, color tokens, A4 portrait, margins
- Bilingual rendering: Arabic RTL primary, English LTR secondary
- Logo strip: all 4 parties (Samaya / CG / ACE / MoC)
- Document-control block: title, project/contract, issuing party, recipient, revision history, distribution
- RFI/TQ reference number — if blank, note: **DC adds at time of issue**

### Check 2 — Content vs Source Documents
**CRITICAL: Verify every contractual citation against the actual source document.** PDF extraction is mandatory — never trust quoted text without verifying. Fabricated citations = Blocker.

### Check 3 — Communication & Stakeholder Plan
- Routing matches the Comm Plan
- Distribution list matches the stakeholder matrix
- WITHOUT PREJUDICE clause for scope-boundary or contractual-position documents

### Output: Findings Table + Go/No-Go Verdict
| Severity Levels | Meaning |
|----------------|---------|
| **Blocker** | Document must not issue |
| **Major** | Fix before issue |
| **Minor** | Fix preferred, non-blocking |
| **Flag** | Advisory only |

Verdict: **ISSUE** / **ISSUE WITH CORRECTIONS** / **DO NOT ISSUE**

### Common Pitfalls
- Fabricated evidence quotes — always verify via pdftotext
- RFI/TQ reference numbers are assigned by DC, not TO
- Response deadlines may be in Aconex workflow, not document body

---

## §0b(vi) — Schedule & Materials Supplier Traceability (absorbed from schedule-materials-audit)

When auditing a contractor's Primavera P6 schedule against design documents to build a materials/supplier traceability matrix:

### Workflow

1. **Schedule Ingestion** — pdftotext the P6 export, map WBS structure (Milestones → Prelims → Assessment → Design 50%/90%/100% → Procurement → Construction → T&C)

2. **Design Document Discovery** — search these locations for supplier data:
   - Finishes Schedule → supplier name in column 6
   - Luminaire Specification → MANUFACTURER block
   - AV BOQ → make/model per item
   - FF&E Schedule → supplier URL/name
   - Showcase Schedule → glass spec, lock type

3. **Cross-Reference** — map each schedule activity material description to the design document entry. Extract supplier/brand from the relevant column.

4. **Build Traceability Matrix (Excel)** — columns: Activity ID, Material/Product, Design Spec Ref, Supplier/Brand, Source Document, Submittal Start/End, Float, Critical

5. **Report Findings by Severity:**

| Severity | Criteria |
|----------|----------|
| **HIGH** | Items on critical path with TBC supplier; design-named brand not reflected in schedule |
| **MEDIUM** | Missing coordination milestones; isolated parallel workstreams |
| **LOW** | Missing milestone dates; documentation gaps |

### Pitfalls
- Scanned PDFs (vendor proposals) need PyMuPDF + tesseract OCR
- Schedule activity names may not match design spec codes — map by description
- A single "Lighting" schedule activity may cover 7+ sub-categories from different manufacturers
- The design source (Finishes Schedule) is authoritative for finish material suppliers

### Reference Files
- `references/aseer-design-document-inventory.md` — complete directory map of Aseer design documents with confirmed brand mappings

---

## Consultant Offer Evaluation — Payment Milestones & PDF Annotation

When a consultant submits a final fee proposal, evaluate it against the RACI matrix and produce an annotated PDF with a summary verdict cover page. See `samaya-technical-office/references/consultant-offer-evaluation-payment-milestones.md` for:

- **Payment milestone pattern** — design contracts use DMP gates (50%/90%/100% IFC), not Concept/Schematic/Detail. Down payment 15% max, 60% tied to design progress, 25% held for IFC approval.
- **PDF annotation workflow** — highlight issues directly on original pages (red=critical, yellow=needs attention, green=acceptable), add text notes, prepend cover page with summary verdict table.
- **Email drafting rules** — no icons/emoji, concise paragraph summaries per party, direct language about lazy offers.

---

## Pitfalls

- **Table width overflow in A4 HTML plans** — tables with `width:100%` but no `table-layout:fixed` cause browsers to auto-size columns by content, ignoring `th` width percentages. This produces inconsistent column widths across tables and overflow on A4 pages. Fix: add `table-layout:fixed` to the global `table` CSS rule, plus `word-wrap:break-word; overflow-wrap:break-word` to `td` and `th`. Then ensure every `<th>` has an explicit width (percentages, not pixels — pixel widths don't scale for A4 print). Convert any `width:60px` / `width:22px` to percentages (`8%` / `4%`).
- **Don't assume a schedule covers the full project** — always check filename and end-date against contract completion before assessing duration. A 5-month programme ending at 100% IFC is the design phase, not the full project. The user will correct you if you flag it as unrealistic without checking.
- **Don't assume a project document is approved just because a reference file exists on disk** — PEP Rev03 has "Contract Duration: 303 calendar days" but was never formally submitted to CG. CRP Rev C02 attempted "Friday excluded" but returned Code C. Always check `CG_STATUS.md`, submission dates, and email archive before citing a document as an approved contractual position.
- **Don't retry the same PDF extraction command 5+ times against OneDrive-locked files** — `[Errno 11] Resource deadlock avoided` means the file hasn't synced locally. Check for pre-existing Markdown extracts in `Docs/07_Reports/07.5 Audit Report/` instead. If neither works, tell the user the file is unavailable due to OneDrive sync, not because of a tool failure.
- **Programme audits use SOW+ER as reference, not CG comment patterns** — never confuse a schedule audit (§0b) with a plan compliance review (§0a). Different documents, different severity taxonomies, different outputs.
**Pitfall — Don't rely on CG_STATUS.md alone** — the status file may be days old. Always verify submission/reply status by checking Outlook email directly: search the email archive register CSV or run a live Outlook body search for the document code. The `outlook-email` skill's `references/cg-email-triage.md` has canonical SQL for this.
- **Don't miss the revision history** — document control audit trail requires every revision to be traceable. Old rows keep their status (Code C, Code B, etc.), new row is always "REVIEW"
- **Don't overflow pages** — adding a disposition table with 8 rows may push content past page bottom. Check rendered page fit; if needed, add page breaks or split into a supplementary page
- **Don't forget to mark previous rev status** — when a plan gets Code C, update the previous revision's status badge from "REVIEW" to "CODE C" so the history is accurate
- **Don't skip the compliance statement** — CG reviewers look for an explicit statement that all comments have been addressed. Add it below the disposition table
- **Preserve original layout** — use targeted patch() edits, never regenerate the full HTML. The user has corrected: "why you change the design/workflow"
- **Cover page "Issued for CG Review" label** — keep this on resubmissions unless explicitly directed otherwise
- **OneDrive file lock (macOS)** — files under `Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` may throw `[Errno 11] Resource deadlock avoided` when not synced locally (`isDownloaded = 0`). Check for pre-existing Markdown extracts in `Docs/07_Reports/07.5 Audit Report/EXTRACT_*.md` before attempting direct PDF extraction. See `references/aseer-sow-er-scope-reference.md` for cached SOW/ER scope data.
- **Programme audits require SOW+ER, not CG pattern mining** — never treat a schedule review as a PM plan compliance check. They use different reference documents (contract scope vs CG comments) and different severity taxonomies. Use §0b for programme audits, §0a for plan reviews.

## Verification

- [ ] All "Rev C01" references replaced with "Rev C02" (or appropriate new revision)
- [ ] Zero stale revision identifiers in headers, footers, cover, TOC
- [ ] Revision history shows new row with accurate description of changes
- [ ] CG Comment Disposition table maps every comment to a specific section
- [ ] Structural changes applied to the referenced sections
- [ ] Status tracking files updated
- [ ] HTML file renders without layout breakage
