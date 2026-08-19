---
name: cg-response-protocol
description: "Protocol for handling CG (Consultant) comment responses on submittals. Two-stream separation: submission plan comments vs detailed technical reviews."
tags:
  - cg
  - consultant
  - response
  - cr-sheet
  - submittal
---

# CG Response Protocol

## CRS Creation Workflow (MANDATORY — Follow in Order)

When the user says "create CRS" or "make a CRS sheet":

1. **Fetch the blank template immediately** from `https://samaya-factory.com/templates/crs/CRS_TEMPLATE_BLANK.xlsx` — do NOT ask which template, do NOT describe the format, do NOT ask for confirmation
2. **Save as** `CRS_[DocRef]_Rev[XX].xlsx` in `02_CG_Responses/`
3. **Fill header block** (rows 1-7): PROJECT NAME, CRS NUMBER, DOCUMENT No., DOCUMENT TITLE, DISCIPLINE, DATE, Rev
4. **Fill data rows** (row 11+): No., Initial, Sheet/Ref, Code, Reviewer Comment, Originator Reply, Reply By, Status
5. **Present to user for review** — do NOT send to CG or specialist without user approval
6. **Do NOT get sidetracked** by other tasks (risk register updates, merge conflicts, template hosting) before completing the CRS — the CRS is the primary deliverable

### CRS Template Location

The approved blank CRS template and all other Samaya templates are at:

> **https://samaya-factory.com/templates/**

| Template | URL |
|----------|-----|
| CRS blank | `/templates/crs/CRS_TEMPLATE_BLANK.xlsx` |
| DOCX (Samaya branded) | `/templates/docx/Samaya_Corporate_System_Template.docx` |
| RFI/TQ letter | `/templates/rfi/RFI_TEMPLATE.html` |
| A4 print layout | `/templates/html/_A4-print-template.html` |
| Weekly progress report | `/templates/reports/_TEMPLATE_Weekly_Progress_Report.xlsx` |
| QA/QC log | `/templates/reports/_TEMPLATE_QAQC_Log.xlsx` |
| Clash report | `/templates/reports/_TEMPLATE_Clash_Report.xlsx` |
| Structural penetration register | `/templates/registers/Structural_Penetration_Register_Template.xlsx` |

OneDrive source of truth: `04_Docs/09_Registers/CRS_Templates/CRS_TEMPLATE_BLANK.xlsx`

### Pitfall — Do Not Sidetrack

When the user asks for a CRS, the CRS is the ONLY deliverable until it is done. Do NOT:
- Update risk registers mid-CRS
- Fix merge conflicts in unrelated files
- Host templates on the server
- Research CG comments from Outlook
- Ask the user to paste comments you could find yourself

Complete the CRS first, then ask "what next?".

## Stage-Boundary Triage — Out-of-Stage CG Comments

CG frequently comments on items that belong to a **different design stage** than the one submitted. This is a distinct pattern from scope creep (which is about wrong discipline) — stage-boundary comments are about wrong **timing**.

### Detection

| Signal | What It Means |
|--------|---------------|
| CG asks for 90% DD details during a 50% DD review | Stage-boundary comment — belongs to next gate |
| CG asks for IFC-level coordination during DD | Stage-boundary comment — premature |
| CG asks for shop drawings during design review | Stage-boundary comment — shop drawings follow design approval |
| CG asks for material samples before design intent is frozen | Stage-boundary comment — samples follow design freeze |

### CRS vs RFI Decision

| Situation | Use | Why |
|-----------|-----|-----|
| CG comments on items clearly belonging to a later stage | **CRS** — state the boundary, defer | We control the position; no need to ask permission |
| CG rejects our stage-boundary position and insists | **RFI** — formalise the dispute | Escalate only after CRS pushback fails |
| CG mixes in-stage and out-of-stage comments in one review | **CRS** — triage each comment separately | Respond to in-stage, note-and-defer out-of-stage |

### CRS Response Language for Stage-Boundary Comments

```
Noted. This item belongs to the [90% DD / IFC / Shop Drawing] stage
and will be addressed in the relevant submission per the DMP stage-gate
sequence. The current submission is [50% DD / Gate 1 DD] and covers
[scope of current stage].
```

No argument, no justification — just state the boundary. CG can disagree, but the burden shifts to them to explain why a later-stage item belongs in the current review.

### Triage Workflow

1. **Read each CG comment** against the DMP stage-gate definition for the current submission
2. **Classify**: In-stage (respond) vs Out-of-stage (note and defer)
3. **For in-stage**: Draft technical response per Stream 2
4. **For out-of-stage**: Use the CRS response language above — do not comply, do not argue
5. **Log recurring pattern**: If the same CG reviewer repeatedly issues out-of-stage comments, add a risk entry (see PRR-COM-10 template below)

### Risk Entry Template

When CG stage misunderstanding is a recurring pattern, add to the risk register:

| Field | Value |
|-------|-------|
| ID | PRR-COM-10 (or next available) |
| Title | CG consistently issues out-of-stage comments on submittals |
| Score | 3x3 = 9 (High) |
| Mitigation | CRS stage-boundary responses; escalate pattern to PM for CG coordination meeting |
| Actions | A1: Add stage-boundary column to CRS template; A2: Triage every CG response; A3: Raise at next CG coordination meeting |

## Core Principle: Two Separate Streams

CG comments come in two distinct types. **Never merge them into one response.**

| Stream | Source | Response Format | Audience |
|--------|--------|-----------------|----------|
| **Submission Plan Comments** | CG review of submission plan/register (e.g. Mohammad Elbaz) | **CR Sheet** (Excel) - sent to CG for agreement | CG + internal |
| **Detailed Technical Review** | CG review of technical deliverables (e.g. Abdrabo Shahin, Code C) | **Consultant Comment Register** (Excel) - internal tracking | Internal only until resubmission |

## Core Principle 2: Plan vs Register Distinction

When CG returns Code C on a **management plan** (RMP, SMP, DMP, HSE Plan, QMP), not all comments are valid. Some ask for operational data that belongs in live registers, not the plan itself. **Before complying, ask: "Is this methodology or data?"**

| If CG asks for... | It belongs in... | Response |
|---|---|---|
| Risk scores, P6 Activity IDs, float values, specific risk entries | **Live register** (PRR, DDR, HSE, AV) | Push back — plan is methodology, register has the data |
| Register snapshots, register structure, register counts | **Plan** (as reference only) | Comply — add note that registers are live documents, attach snapshot |
| Methodology changes (scoring approach, identification techniques, review cadence) | **Plan** | Comply — this is what the plan is for |
| Standardised scoring across all registers | **Neither** — per PMBOK Ch. 11.3, different risk types may use different scales | Push back — document per-register scales clearly, no rescoring needed |

### Why 4 Registers for Aseer Museum

| Register | Who Uses It | Why Separate |
|----------|-------------|-------------|
| **PRR** (Master) | PM + Commercial Manager | Project-level risks — schedule, cost, contracts, design, execution. The whole team sees it. |
| **DDR** (Design) | Technical Office + Design Manager | Design-phase technical risks — 77 detailed items (clash, LOD, coordination). Putting them in PRR would make it 100+ and unmanageable weekly. |
| **HSE Register** | HSE Manager | Safety risks — uses different scale (CxL 5x5) and is legally required to be standalone on site. |
| **AV Register** | AV Lead | AV/Multimedia specialist risks — heat gain, content production, integration risks unrelated to other project risks. |

**Why not fewer?** One register with 178 risks would be unreadable weekly. HSE must be standalone by regulation.

**Why not more?** Procurement and Quality risks are currently under PRR categories (PRC, QLT). If they grow past 20+ each, they can be split. Current 4 registers = balance between detail (each team sees their own) and simplicity (not 10 registers nobody tracks).

## Mandatory: Run the 7 Lenses on Every CG Interaction

This protocol integrates with the **CG Analysis & Lessons Learned System** (`cg-analysis-and-lessons` skill). Every CG response handler MUST run the 7 lenses:

### Pre-Submit Gate (before sending anything to CG)

| Lens | Check |
|------|-------|
| Rejection | Has this submittal type been rejected before? Check `cg_rejection_patterns.md` |
| Condition | Are all previous Code B conditions closed? Check `cg_code_b_conditions.md` |
| Checklist | Run the pre-submission checklist in `cg_forecast_engine.md` Sec 3 |
| Improvement | Is there a lesson from a similar past submittal? Check `lessons_learned_register.md` |

If any check fails -> **do not submit**. Flag the blocker and resolve first.

### Post-Response Capture (when CG replies)

| Lens | Action |
|------|--------|
| Rejection | Code C or D? -> Capture CG comment verbatim -> Log as lesson |
| Condition | Code B with conditions? -> Add to `cg_code_b_conditions.md` |
| Delay | Response took >14 days? -> Flag as DA risk in submittal register |
| NCR | New NCR issued? -> Root cause analysis -> Log as lesson |
| Rework | Does the response require rework? -> Capture the process gap |
| Checklist | Did we miss a checklist item? -> Update the checklist |
| Improvement | Any positive finding? -> Capture for future projects |

### Lessons Learned: Client-Sharable Only

When logging a lesson from a CG interaction, remember the lessons learned register is a **formal project deliverable** shared with the client. Only capture project-relevant lessons — no internal process notes, tool quirks, or session-specific events. See `cg-analysis-and-lessons` skill for the full lessons learned workflow and what to exclude.

## CG Reviewer Behavior Patterns (Quick Reference)

| Reviewer | Type | Strategy |
|----------|------|----------|
| **Mansour Alrezeni** | Code enforcer + bypasses Samaya | Submit only what spec says. Do not propose alternatives or splits — he will reject. Escalate structural decisions to Elbaz. **Known to email sub-consultants (NRS, ZNA) directly, bypassing Samaya's project management role. Flag any direct communication with specialists as a communication plan violation per PL-0018 Sec 12.6 S-1 (direct subcontractor-to-CG communication not permitted).** |
| **Mansour Alrezeni — "Noise Only" Pattern** | Sends reminders that re-state his position without engaging with the contractor's counter-proposal | When Mansour sends a follow-up reminder that ignores your detailed response (Oddy timeline, two-track proposal, supplier evidence), **do not reply.** He is making noise — re-stating his position without addressing your points. The ball is in CG's court. Only reply if he raises a genuinely new request or escalates to Hossam/Elbaz. |
| **Venugopal Poyakkara Veetil — AV Specialist** | Extremely detailed technical reviewer | Reviews AV/IT/ELV submittals. Rejects generic documents that don't demonstrate buildable solutions. Requires: project-specific control architecture with interface matrix, selected switch models with port counts/PoE budgets/fibre topology, exhibit-by-exhibit control with device lists and alarm matrices, supported UPS load calculations with rack-by-rack schedules. Will reject documents that are "operational concepts" rather than approved submissions. Requires signed/stamped documents from AV Specialist Contractor. |
| **Eng. Gaby Khoury — Showcases** | Drawing completeness + material submittal reviewer | Reviews showcase/architectural DD submittals. Requires: all details incorporated, mechanism illustrations with operation/access, access panel dimensions on plans+elevations, additional plan/section/detail drawings, electrical/AV outlet locations, interface details with adjacent finishes, structural design calculations. On **showcase material submittals** he issues a standard 8-comment set (gasket, Corian 400-grit + seamless corner, patinated-brass alternative pending Oddy, low-iron 11.5mm mitred UV-bonded glass, structural steel details, mechanism details, Abloy lock count, low-UV/low-heat lighting) + off-site fabrication rule. Route to Glasbau Hahn. See `references/gaby-khoury-showcase-material-submittal.md`. |
| **Mohamed Magdy — Mechanical** | Code compliance + ergonomics | Reviews mechanical/plumbing submittals. Checks SBC code references for discrepancies, ergonomic standards (sink-to-wall distances), and completeness of assessment report comments. |
| **CG (general)** | Conflates deliverables | When CG returns Code C with cross-discipline comments, check if comments are in-scope before accepting them all |
| **CG (general)** | Unaware of NRS-MoC deliverables | Before responding to design-stage requests, verify if already delivered under original design contract |

See `cg-analysis-and-lessons` skill for full reviewer profiles, forecast engine, and lessons learned register.

## Stream 1: Submission Plan CR Sheet

- Covers comments about **what to submit, when, and by whom**
- Format: Excel with columns: CR, CG Comment, CG Reference, Response, Position, Status, Open/Closed, Action Required, Supporting Documents
- CR numbering: sequential (CR-01, CR-02...) or prefixed by discipline (ARC-01, STR-01...)
- Responses are from **Samaya's perspective** - never mention sub-consultant scope splits to CG
- Sent to CG for agreement on positions
- Closed items: Stage 3 completed, draft in submission plan
- Open items: FF&E supplier, Life Safety by Namaa, pending tests

## Stream 2: Detailed Technical Review Register

- Covers comments about **technical content** of submitted deliverables (BOD, calculations, drawings)
- Usually Code C (Revise & Resubmit) or Code B (Approved with Comments)
- Format: Excel with columns: Comment No., Consultant Comment, Contractor Response, Status, Reference Document, Action By, Target Date
- **Not sent to CG** - internal tracking for the resubmission workstream
- Each comment gets a contractor response explaining the position
- Status: Open / Closed / Noted

## CR Sheet Response Framing

- **Quotes must be verbatim** - when quoting CG comments, ER/SoW text, or contract clauses, copy the original text exactly as written. Do NOT paraphrase, rephrase, or "clean up" the quote. The user explicitly said: "when qoute write the orginal text as it dont rewrite."
- **No `Sec` symbol** — never use `Sec`. Use `Sec` instead (e.g., `ER Sec 3.7.XIII` not `ER Sec 3.7.XIII`). The user has repeatedly corrected this across multiple sessions.
- **No AI symbols** — no arrows (`->`, `<-`), bullets (`*`, `-`), em dashes (`--`), en dashes (`-`), middle dots (`-`), or any decorative Unicode symbols. Plain ASCII only.
- **Plain engineer English ("hummadize")** — short, direct sentences. No fluff, no AI cliches, no "seamlessly", "robust", "holistic", "leverage", "streamline", "facilitate". Write like an engineer writing to another engineer.
- **NRS is Samaya's sub-consultant** — never frame NRS as separate or independent. Samaya directs NRS. Say "We direct NRS to..." not "NRS will..." or "NRS is responsible for...". Samaya is the D&B contractor; NRS works under Samaya's umbrella.
- "This was completed at Stage 3. NRS draft (XXXX) for reference. Included in submission plan and drawing register." - for items already done
- "This will be in the Life Safety registers and submittals (Namaa), not in the current architectural package." - for scope handoffs
- "Bespoke setwork furniture shown on GA with setwork codes. Remaining FF&E to be coordinated from 50% to 90% to IFC." - for phased items
- User-verified FF&E response: "Noted. Will add to submission plan and drawing register. Already in GA drawings, will split into separate drawings." — Confirms: (1) setwork already shown, (2) FF&E is a separate phased track, (3) supplier appointment is the blocker, (4) actions = add to submission plan + drawing register + split GA drawings
- "Noted." - for accepted process comments
- "All applicable loads in BOD per SBC. Showcase weights from manufacturer. Artwork weights from curator." - for technical clarifications

## Multi-Round CRS Disposition Matrix Pattern

When CG issues multiple rounds of comments on the same document (e.g., R1 9-Mar, R2 2-Jun, R3 18-Jun), use a **single consolidated disposition matrix** with round-separator rows:

### Structure

```
| # | Round | CG Comment | Disposition | Ref | Status | Route/Scope |
|---|---|---|---|---|---|---|
| cat-row | Round 1 — CG comments (9-Mar-26) — closed in Rev 1/2 |
| CG-01 | R1.9-Mar | [comment] | [response] | Sec X | CLOSED | SMP-scope |
| cat-row | Round 2 — CG CRS (2-Jun-26, Code C) — addressed in Rev 3 |
| CRS-01 | R2.2-Jun | [comment] | [response] | T1-07 | CLOSED | SMP-scope |
| cat-row | Round 3 — CG CRS (18-Jun-26, Code C) — addressed in Rev 4 |
| CRS-18 | R3.18-Jun | [comment] | [response] | CRS | CLOSED | Procedural |
```

### Rules
- **cat-row** (`.cat-row td` with dark background) separates rounds — never use blank rows
- **Round column** shows date + round number for traceability
- **Status badges**: `CLOSED` (green), `SUBMITTAL-PENDING` (amber), `IN-PROGRESS` (blue), `RE-OPENED` (red)
- **Ref column** links to the document section or role ID that addresses the comment
- **Route/Scope** column shows whether the fix is in-scope or requires external action (PQD Register, DS, etc.)
- Each round gets its own cat-row header, even if only 1-2 comments remain open
- Comments that span multiple rounds (e.g., CG-03 re-opened in R2) get a `RE-OPENED` badge with explanation

### Status Progression
```
R1: CG-01 -> CLOSED
R2: CG-01 -> CLOSED (carried forward), CRS-07 -> RE-OPENED (CV not yet submitted)
R3: CRS-18 -> CLOSED (CRS completed, QA performed)
```

### Caveman Style for C:Resubmit Reasons

When adding CG resubmit reasons to remarks, write short direct sentences:
- "CG want: loading schedule, masonry weights, concrete cover, wind/seismic refs. All in BOD per SBC. Need to clarify and resubmit."
- "CG want: loading notation schedule, load combo names. Loading tables in BOD per SBC. Need to clarify and resubmit."
- "CG want: audit report for previous design stage. Under preparation. Will include in next package."

### Multi-Round Code C Pattern — Rev.01 Still C, All Comments Open

When a Rev.01 resubmission gets **Code C again** with all comments still marked Open by CG:

**Worked example — PEP ZD-0086 (Jul 2026):**
- Rev.00 submitted 16 Jul -> Code C 22 Jul (15 comments, all Open)
- Samir circulated CG comments 22 Jul, asked team to respond
- Samir sent Rev.01 to Waris 25 Jul: *"Please Review and if it's Confirmed from your side, please let's Submit it"*
- Rev.01 submitted 26 Jul -> Code C again 27 Jul (same 15 comments, all still Open)
- CG note: *"The CRS reply"* — meaning the CRS was not fully resolved
- Root cause: 1-day internal review, no formal sign-off gate, responses were explanations not evidence
- See `01_Registers/lessons_learned_register.md` LL-013 and `03_Plans/11_Quality/lessons_learned_register.md` LL-017

#### Red Flag: PM Says "Please Review and Confirm"

When the PM/Construction Manager sends an email saying *"Please Review and if it's Confirmed from your side, please let's Submit it"* — this is a **red flag** that the CRS was not fully resolved before resubmission. The "please review" language means the team hasn't confirmed all responses yet.

| Signal | What It Means | Action |
|--------|---------------|--------|
| PM asks team to "review and confirm" before submission | CRS responses are not yet finalised internally | **Do not submit.** Hold until all CRS items are closed or explicitly deferred with a cover-note commitment. |
| PM says "finalize it TODAY so we can resubmit by end of day" | Resubmission is being rushed to meet an internal deadline | Flag to the user: the resubmission is going out before the CRS is fully resolved. CG will return Code C again. |
| Rev.01 submitted without all CRS items closed | CG returns Code C with all comments still Open | **Root cause confirmed.** The resubmission was premature. The team submitted explanations instead of physical evidence. |

**Root cause of 2nd Code C:** The Rev.01 was submitted before the CRS was fully resolved. CG did not accept any of the contractor's responses because they were explanations, not physical evidence. Every comment that was Open in Rev.00 remained Open in Rev.01.

**Prevention:** Before any resubmission, run a CRS closure check:
1. Are all CG comments from the previous round addressed with a response?
2. Are the responses **physical evidence** (test reports, approved drawings, completed studies) — not explanations or references to existing documents?
3. If any item is still "under preparation" or "being arranged", defer it explicitly in a cover note — do not submit hoping CG will accept partial responses.

### Pattern Recognition

| Round | Submittal | CG Response | Comments Status |
|-------|-----------|-------------|-----------------|
| Rev.00 | First submission | Code C | 15 comments, all Open |
| Rev.01 | Resubmission | **Code C (2nd time)** | Same 15 comments, **all still Open** |

### What This Means

- CG did **not** accept any of the contractor's responses from the CRS
- Every comment that was Open in Rev.00 is still Open in Rev.01
- The contractor's responses (explanations, references to SBC clauses, coordination meeting agreements) were **insufficient** to close any item
- CG wants **physical evidence** (test results, reports, approved drawings), not explanations

### Common Root Causes

| Comment Type | Why Still Open | What CG Actually Wants |
|-------------|----------------|----------------------|
| Team approval | CVs submitted but not formally approved | Appointment letters + MoC acceptance |
| Testing (core, rebar scan) | "Under preparation" response | Completed test reports with results |
| Geotechnical | "Being arranged" response | Borehole logs + lab test results |
| Loading notation | "Already in BOD per SBC" response | Load pattern/case/combination schedule matching analysis software |
| Seismic study | "Need architect to confirm occupancy" response | Full SBC 301 study with occupancy classification, risk category, occupant load calc |
| Architectural/MEP changes | "Will be in next stage" response | Current loading plans must reflect ALL known changes, not defer them |

### Action Plan

1. **Stop resubmitting explanations.** CG has rejected the explanation approach twice.
2. **Complete the physical evidence** — core testing, rebar scan, geotechnical investigation must be done before Rev.02
3. **For loading/seismic comments** — produce the exact schedule/study CG described, not a reference to existing BOD content
4. **For team approval** — formalize the appointment and get MoC sign-off
5. **Update the risk register** — this is now a High/Critical risk, not a routine resubmission

### CRS Disposition for Multi-Round

Use the consolidated disposition matrix pattern (see above) with a clear note:

```
| cat-row | Round 1 — CG comments (5-Jul-26) — Rev.00 Code C — all Open |
| cat-row | Round 2 — CG comments (18-Jul-26) — Rev.01 Code C — all still Open |
```

Add a summary row at the top:

```
| SUMMARY | 2 rounds | 15 comments | 0 closed | All require physical evidence, not explanations |
```

## Interpreting Mixed-Status CG Responses

CG often returns a submittal with **different statuses at different levels**. Do not conflate them.

| Level | What it means | Example |
|-------|---------------|---------|
| **Submittal-level status** | Overall CG verdict on the package as a whole | "C" (Revise & Resubmit) |
| **Item-level status** | Per-drawing/per-document status from the register | B, C, Not Stamped |
| **Excluded items** | Packages CG explicitly deferred to a later review cycle | "Setwork Details excluded pending Look and Feel review" |

**Critical pattern — "C overall but mostly B":**
- CG may stamp the submittal C overall while approving most individual drawings as B
- The C is driven by a small number of items that need revision, not the whole set
- **Do not treat the overall C as a blanket rejection** — check the per-item breakdown
- **Action:** query CG if the overall C seems disproportionate to the per-item breakdown

**"Not Stamped" items:**
- Drawings submitted but CG did not review or stamp
- These have **no status at all** — not approved, not rejected, not reviewed
- Common reasons: CG ran out of time, CG focused on specific sections, CG waiting on dependencies
- Action: flag as "Not Reviewed" in tracking, do not assume approval or rejection

**Excluded/deferred packages:**
- CG explicitly carves out certain drawing groups from the current review cycle
- These get a separate review at a later date
- Action: track separately, do not include in current resubmission unless CG asks

**Contradictory stamps — "C" with "Approved As Submitted" text:**
- CG sometimes stamps C on a drawing that also carries "Approved As Submitted" text
- This is an internal inconsistency — the stamp and the text disagree
- **Action:** flag both drawings by number in the query email. Ask CG to confirm the correct status. Do not guess which one is right.

**C-stamped drawings with no comments:**
- CG may issue a C stamp on a drawing with no review notes, no markup, no comments
- The drawing number and "C" are the only marks
- **Action:** ask CG explicitly for the review notes. Without comments, the resubmission has no direction.

**Practical analysis — what was actually actioned:**
```
Total submitted = A
Actioned (B + C) = B
Not reviewed (Not Stamped + Excluded) = A - B
Effective review rate = B / A
```
- If review rate is low (<50%), the CG did not complete their review
- Flag this in status reports: "CG reviewed only X% of submitted drawings"
- The resubmission scope is only the C-rated items + any CG comments on B-rated items
- Not Stamped items stay as-is unless CG specifically asks for changes

## Querying CG About Status Inconsistencies

When the overall submittal status contradicts the per-item breakdown, send a short email to CG:

**When to query:**
- Overall C but majority of actioned drawings are B
- C-stamped drawings with "Approved As Submitted" text
- C-stamped drawings with zero comments
- 121+ drawings not stamped (CG didn't review most of what they received)

**Email structure (keep it short, 2 questions max):**
1. State the numbers: "X drawings -> B, Y drawings -> C, Z drawings -> not stamped"
2. State the contradiction: "Overall C seems incorrect given X are B"
3. Name specific drawings with contradictory stamps
4. Ask 2 clear questions: (a) should overall be B? (b) confirm status for specific drawings

**Template:**
```
Subject: Clarification on Overall Status — Submittal [NUMBER]

Dear Eng. [Name],

We received the review for Submittal [NUMBER]. The overall status is C, but the breakdown shows:

[X] drawings -> B
[Y] drawings -> C
[Z] drawings -> not stamped

With [X] drawings approved as noted and only [Y] marked C, the overall C seems incorrect. Also, [N] drawings ([NUMBERS]) have "Approved As Submitted" on them but received a C stamp with no comments — we cannot identify what needs revision.

Please clarify:
1. Should the overall status be B instead of C?
2. For drawings [NUMBERS], can you confirm the correct status?

Regards,
Eng. Mohamed Sultan
```

## Caveman Style for C:Resubmit Reasons

When adding CG resubmit reasons to remarks, write short direct sentences:
- "CG want: loading schedule, masonry weights, concrete cover, wind/seismic refs. All in BOD per SBC. Need to clarify and resubmit."
- "CG want: loading notation schedule, load combo names. Loading tables in BOD per SBC. Need to clarify and resubmit."
- "CG want: audit report for previous design stage. Under preparation. Will include in next package."

## Deemed Approval — CG Silence = Approval

When CG does **not respond** to a submittal within the contractual review period (typically 14-21 working days per DMP/SoW), the submittal is **deemed approved** per standard construction practice.

### When to Apply

| Condition | Action |
|-----------|--------|
| CG silent for > contractual review period | Mark as **Deemed Approved** in the register |
| CG silent for > 30 days with no acknowledgment | Flag in status report — unreasonable delay |
| CG silent for > 60 days (as in this session) | **Confirmed deemed approved** — proceed as if Code A |
| CG eventually responds after deemed approval date | Log the response but do not retroactively change status unless CG explicitly overrides |

### Register Entry

Update the submittal register with:

| Field | Value |
|-------|-------|
| Status | **Deemed Approved** (not "Pending") |
| Date Approved | Last day of contractual review period (or date you declared it) |
| Remarks | "CG did not respond within [N] days. Deemed approved per [DMP/SoW clause if available]." |

### Email Record

Keep the email thread showing:
1. Date of submission (e.g., 21 May 2026)
2. Date range with no CG response (e.g., 21 May -> 20 Jul = 60 days)
3. Your declaration of deemed approval

### Risk

- CG may later claim they were still reviewing — document your declaration date clearly
- For **critical-path items** (shop drawings, long-lead materials), send a follow-up email before declaring deemed approval: "We have not received a response within the review period. Please advise if you require more time, otherwise we will proceed per the deemed approval provision."
- For **non-critical items** (management plans, informational submittals, CV packs), deemed approval is safer to declare without follow-up

## Status Definitions

| Status | Meaning | Color |
|--------|---------|-------|
| Closed | Resolved, CG position agreed | Green |
| Open | Action required, pending | Red |
| Noted | Acknowledged, no action needed | Blue |
| C:Resubmit | CG returned with comments, blocked until resubmission | Yellow + "BLOCKED" prefix |
| Deemed Approved | CG did not respond within review period | Green (same as Approved) |

### CRS Triage — Filtering Comments Before Forwarding to Designer

### Recurring Pattern: Resubmitting Without Closing CRS Comments

This is a documented recurring issue on this project. Instances:
- Structural DD (1C0-1G-0001) — Code C twice, 15 comments all Open both rounds
- PEP (ZD-0086) — Code C twice, 26 comments all Open both rounds
- DMP — Code D then C, comments partially addressed

Root cause in every case: the CRS Originator Reply column was left empty or contained explanations instead of physical evidence. CG returned Rev.01 with all comments still Open. The CG's note "The CRS reply is missing from SAMAYA side" confirms the pattern.

**Prevention — CRS closure check before any resubmission:**
1. Every CG comment MUST have a response in the Originator Reply column
2. Responses MUST be physical evidence (test reports, approved drawings, completed studies) — not explanations, references, or "under preparation"
3. Any item still pending must be explicitly deferred in a cover note with a commitment date
4. Internal QA review must be completed and signed off before submission

**Red flag:** When the PM says "Please review and confirm" before submitting — it means CRS responses are not yet finalised. Hold submission until all items are confirmed.

When you receive a CG CRS (Comments Resolution Sheet) for a submittal, **do not forward the raw CRS to the designer.** Filter comments by responsible party first.

### Triage Categories

| Category | Who handles | Examples from this session |
|----------|-------------|---------------------------|
| **Design scope** | Forward to designer (NRS) | Showcase design comments (#9-10, #67-82), sections missing dimensions (#140-143), floor/ceiling scoping (#19-20), title block/QA notes (#3-4, #8) |
| **Samaya/contractor gap** | We respond to CG directly | Cloud survey pending (#1), demolition methodology (#11-12), mock-ups/material samples/BIM coordination (#5-7) |
| **CG process issue** | We query CG | Overall C status when 88 drawings are B and only 29 are C — disproportionate verdict |

### Triage Rules

- **Cloud survey / survey-related comments** are Samaya's responsibility, not the designer's. Acknowledge as pending in your response to CG. Do not forward to NRS.
- **Title blocks, QA notes, sheet layout standards** ARE on the designer (they produce the drawings). Forward these to NRS.
- **Doors/stairs shop drawings** (#13) are contractor action — the designer provides design intent, contractor produces shop drawings.
- **Setwork details and graphic housing** (items #83-99) are specialist sub scope, not NRS — handle separately.
- **B-status per-drawing comments** ("See General Comments") are typically contractor action unless the general comment itself is design-related.
- **Verify which floor(s) the CRS covers** by checking drawing number prefixes (BF=Basement Floor, LG=Lower Ground, GF=Ground Floor). The document title may say one floor only. Do not assume multi-floor coverage.
- **Demolition comments** (#11-12, #15-16) are contractor action — demolition methodology, ceiling removal clarification. Do not forward to NRS.
- **Sections missing dimensions/room names** (#140-143) ARE on the designer — they produce the section drawings. Forward to NRS.
- **Floor/ceiling scoping comments** (#19-20) about space labeling (FFL/CIL), finishes schedule format, expansion joint treatment ARE on the designer. Forward to NRS.
- **Do NOT lump Samaya gaps into a vague "etc." in the forwarding email** — be specific about what Samaya handles (cloud survey pending, demolition methodology, mock-ups, material samples, BIM coordination) so the designer knows exactly what is not their problem.
- **When the user corrects your triage** (e.g. "title blocks is on jim"), fix the email immediately — do not argue. The user knows who produces what.

### Forwarding Email Template

```
Subject: NRS Input Required — [CRS NUMBER] ([Floor])

Dear Jim,

CG returned the CRS for the [Floor] [Discipline] DD submittal (overall C). We are preparing our response and will address the items on our side ([list Samaya gaps]) directly with CG.

The following items need NRS design input:

[Section heading]:
- #[N] — [brief description]
- #[N] — [brief description]

Please review and advise so we can prepare the resubmission.

Regards,
Mohamed Sultan
```

### CRS Email to NRS — What NOT to Include

- Do NOT list contractor-side items (cloud survey, mock-ups, material samples, BIM coordination, demolition methodology) as NRS action items
- Do NOT ask NRS to fix things that are Samaya's responsibility
- Do NOT include the full raw CRS — only the filtered NRS-relevant items
- Do NOT use the CRS email to also discuss unrelated topics (visuals, invoices, etc.) — keep it focused

## Design Study Folder Structure

When NRS submits a design study in response to CG/Ministry requests, file it under a dedicated `12_Design_Studies/` folder:

```
Aseer-Museum/
+-- 12_Design_Studies/
|   +-- 01_Object_List/          (object schedule files)
|   +-- 02_New_Study/            (future studies)
|   +-- 03_Study_01/
|       +-- MOC-ASE-AR-ARC-GEN-DDD-DS01-00_DRAFT.pdf   (NRS study PDF)
|       +-- G12_Structural_Assessment_Template.docx     (team templates)
|       +-- G12_Logistics_Method_Statement_Template.docx
```

The study PDF is extracted from Outlook via AppleScript. Team action templates (structural assessment, logistics method statement) are generated as Samaya-branded DOCX and placed alongside the study.

## Pitfalls

- **Plan vs Register distinction** — When CG returns Code C on a management plan (RMP, SMP, DMP, etc.), not all comments are valid. Some ask for operational data that belongs in live registers, not the plan itself. Before complying, ask: "Is this methodology or data?" If data (risk scores, P6 IDs, specific risk entries, register snapshots), push back — the plan is methodology, the register has the data. The user explicitly confirmed this position after initially agreeing to comply. See `references/rmp-cg-response-patterns.md` for the full worked example.
- **Defend original design decisions** — When you validated the user's approach (e.g., different scoring scales per register is fine per PMBOK), and CG challenges it, defend the original design. Don't flip positions and immediately change the plan. The user will correct you. The correct response: acknowledge CG's preference, explain the PMBOK basis, offer to document more clearly (not change), no rescoring.
- **No placeholders in formal submissions** — Never submit a plan with "To be recalculated", "To be confirmed", or any other placeholder text. CG will flag it as incomplete. Either include real data or remove the section entirely with a clear statement that it will be completed when inputs are available. The user explicitly corrected this: "ليه حطيتهم من الأول" — placeholders are worse than omitting the section.
- **Never add unapproved names to documents.** If a person's name hasn't been formally approved by CG/MoC (via CV submission, KPR update, or formal appointment), list the role only with a note: "Per live KPR" or "TBC — appointment pending." Adding unapproved names creates liability — CG will hold Samaya to that person's qualifications even if they were never formally accepted. The user explicitly corrected: "dont add names are not approved."
- **Never merge submission plan comments with detailed technical reviews** — they are two separate streams with different audiences and response formats.
- **cat-row separators** must use `.cat-row td` class (dark background, white text), not blank rows. Blank rows break table continuity.
- **Status badges** must be consistent: CLOSED (green), SUBMITTAL-PENDING (amber), IN-PROGRESS (blue), RE-OPENED (red). Don't invent new badge types mid-document.
- **Round column** must include both date and round number (e.g., "R2 . 2-Jun") for traceability across revisions.
- **Verify which floor the CRS covers** — CG often reviews one floor at a time. Check drawing number prefixes (BF=Basement Floor, LG=Lower Ground, GF=Ground Floor) in the CRS drawing references. The document title may say "Basement Floor" only. Do not assume a CRS covers multiple floors unless explicitly stated. When forwarding to the designer, name the correct floor in the subject line.

### CRS From a Specialist's "Audit Response" Workbook (Rawasin / AV-style)

When the CRS input is a specialist's own response workbook (e.g. Rawasin's `Audit Response.xlsx` for AV Package Part II), NOT a CG CRS form, build the Samaya CRS from it. Source layout:

- Two sheets: `1st Submital responce` and `2nd Submital responce.` (note trailing dot + space in sheet name — read by exact title).
- Each comment is **two stacked rows**: CG comment (verbatim) in the first B-cell, then the specialist's reply in the next B-cell. The No. appears only on the first row. Iterate row-by-row collecting pairs — do not assume one comment per row.
- The specialist's reply is the **Originator Reply**; keep the specialist's substance (Samaya may reframe wording). Never put Samaya-internal commentary (cost, schedule risk) in the reply column.
- Assign the CRS doc ref from the underlying submittal (e.g. AV Part II = MOC-MUS-ASE-1E0-1G-0002). Confirm the ref + prior CG code from the submittal register (this package was Code D then Code C).
- **Pre-submission status convention:** mark items `Open` (red) that still need resolution before CG submission, `Closed` (green) only for genuinely complete ones. The CRS is presented to the user for review and is NOT submission-ready until the Open blockers are cleared. Do not send to CG/specialist without user approval (user review gate).
- Committing `.xlsx` to the `aseer-museum-pm` repo requires `git add -f` (the repo `.gitignore` blocks binary xlsx); the post-commit webapp-regen hook dirties `06_Risk_System/webapp/` — `git checkout --` those before pushing.

### CG-Proposed Material Change — Control Lever (user strategy, Aseer flooring 2026-08)

When CG (or a CG reviewer) proposes substituting a specified material/finish, treat it as a **control lever, not a commitment**:

- Samaya (the D&B contractor) is NOT obliged to implement a CG-proposed substitution — CG proposals are suggestions/flags, not decisions (consistent with the NRS patinated-brass rule).
- Route the proposal to the design authority (NRS/Jim) for a technical opinion — that opinion becomes Samaya's reference point.
- Design authority rejects → Samaya closes it citing the technical reference.
- Design authority approves → Samaya can STILL reject from its own side for schedule/scope reasons. The opinion is ammunition, not a mandate.
- **Precedent risk:** each approved substitution opens the door to many more, and every change costs time + sample approval + schedule pressure (already tight). Treat a single material change as a gateway to be controlled, not rubber-stamped.
- User prefers **local suppliers** (e.g. Sheed, sheedsa.com) over imports for substitutes — reduces import lead time/approval friction.

### Supplier Technical Rebuttal — When CG Demands Alternatives

When CG rejects a material submittal (Code C) and demands "3 alternative suppliers" but the supplier has already provided a technical rebuttal:

#### Check Outlook first

The supplier's reply often sits in an Outlook folder (not the project submittal folder). Search by:
- Submittal ref (MA-NNNN) in subject
- Supplier PM's email address
- Date range around the CG rejection date

**SQLite query pattern:**
```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_NormalizedSubject, substr(m.Message_Preview, 1, 500)
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_NormalizedSubject LIKE '%MA-0006%'
   OR m.Message_NormalizedSubject LIKE '%Glasbau%'
ORDER BY m.Message_TimeReceived DESC;
```

#### Extract attachments

Use AppleScript `osascript` to extract the supplier's reply sheet + manufacturer datasheet from the email. These are the two key documents.

#### Build the argument

1. The "3 suppliers" demand was based on the initial non-compliant submission
2. The supplier has now proven technical compliance (datasheet + comments reply)
3. Request CG to accept single supplier with technical justification
4. If CG insists, then source 3 alternatives — but the supplier's existing reply is the strongest negotiating position

#### Email evidence in CR Sheets — reference only, no .txt files

When citing email correspondence in a CR Sheet:
- **Do NOT include .txt files** of email threads in the support folder
- **Do NOT include raw email text** in the CR Sheet body
- **Reference by date and sender only** — e.g. "Glasbau Hahn reply 29-Apr-2026", "NRS Jim Richards 19-Jun-2026"
- If a printed PDF of the email exists (e.g. from Outlook print-to-PDF), include that in the support folder instead
- The CR Sheet is a formal document — email body text is not appropriate content

#### Resubmission support folder

Build a structured folder at the subcontractor's submittal directory:

```
MA-NNNN_Rev01_Support/
+-- 01_CG_Rejection_Code_C/
+-- 02_Supplier_Technical_Reply/
+-- 03_Manufacturer_Datasheet/
+-- 04_Supporting_Data_Sheets/     (flat — no subdirs)
+-- 05_PQ_Approval/
+-- 06_Sample_Board/
+-- 07_Related_Submittal_Support/
+-- 08_Email_Thread/               (outside support folder — for CG)
+-- 09_Resubmission_Checklist/     (outside support folder — for CG)
```

### CR Sheet structure for material resubmission

| # | CG Comment | Reference | Response | Supporting Doc | Status | Remarks |
|---|-----------|-----------|----------|---------------|--------|---------|
| 1 | Materials don't comply | Rejection letter | Supplier reply + data sheets | 02_Supplier_Reply/ + 04_Data_Sheets/ | CLOSED | All materials match finishes schedule |
| 2 | AR glass non-compliant | Rejection letter | Manufacturer datasheet proves spec | 03_Manufacturer_Datasheet/ | CLOSED | Tvis > 97%, Rvis < 1% |
| 3 | Comply with SI-007 | Rejection letter | NRS approved drawings | 08_Email_Thread/ | CLOSED | SI closed |
| 4 | Brass patinated | Rejection letter | Separate submittal | 07_Related_Submittal_Support/ | PARTIAL | Look & feel request sent to CG |
| 5 | 3 alternative suppliers | Rejection action | Request single-source acceptance | 02_Supplier_Reply/ + 05_PQ_Approval/ | OPEN | Awaiting CG decision |

**Real-world CR sheets are longer than 5 items.** PQ (prequalification) conditions carry forward as additional CR rows — they were never closed by the original Rev.00 MA submission. For the full 10-row MA-0006 Rev.01 pattern (with PQ-0063 conditions 1/2/5/6) and the canonical file locations, see `references/ma-0006-showcase-resubmission-case.md` sections "Full 10-Comment CR Sheet Structure", "Canonical File Locations", and "Rev.01 Status".

### Look & Feel Approval Strategy

When supplier test reports/certifications take time (supplier lead time), but the visual sample is ready:

1. **Request CG to approve LOOK AND FEEL now** — visual appearance, colour, texture
2. Test reports & certifications to follow once received from supplier
3. Alternative samples from local suppliers in parallel
4. Submit outstanding docs as Rev.01 addendum within 30 days

### Separate Submittal Principle

**Do not block one submittal because a related submittal is pending.** Example:
- MA-0006 (showcase materials: glass, silicone, fabric, Corian, lighting, powder coating) — independent of brass
- MA-0007 (patinated brass) — separate submittal, separate rejection
- MA-0006 Rev.01 can proceed without MA-0007 approval

### Track A/B Separation — When CG Blocks Over a Finish Material

When CG rejects a submittal (Code C) specifically over a **finish material** issue (e.g., patinated brass), and the supplier confirms the material is single-source or high-risk, **split the response into two independent tracks**:

| Track | What | CG Action Needed | Critical Path |
|-------|------|-----------------|---------------|
| **A — Shop Drawings / Fabrication** | Showcase construction, dimensions, integration points, production drawings | Approve independently — finish material does NOT affect fabrication | Production lead time — this is the time-critical path |
| **B — Finish Material (MA-0007)** | Patinated brass sample, Oddy testing, certifications, alternative suppliers | Approve look & feel now; test reports to follow | End of August (Oddy results) |

**When to use this pattern:**
- CG rejects a submittal over a finish material that is a **small fraction** of the overall scope
- The supplier confirms the finish does **not affect** fabrication/production
- The finish material has **long-lead testing** (Oddy, fire, VOC) that will take weeks
- The shop drawings are **otherwise ready** for approval

**Email framing for Track A/B:**

```
We have split the approval process into two independent tracks:

Track A — Shop Drawings (not affected by finish material):
- [Supplier] has confirmed the [finish] is a surface finish only and does not affect fabrication.
- We request CG to proceed with shop drawing approval independently — this is the critical path for production lead time.

Track B — Finish Material (MA-0007):
- Oddy testing in progress — results expected [date].
- In parallel, developing [alternative] from local suppliers as lower-risk substitute — sample within 30 days.
- This can serve as the alternative manufacturer option you requested.
```

**When the supplier advises AGAINST their own material (GBH Letter 002 pattern):**

If the supplier's formal letter states they do NOT recommend the specified material:
1. This strengthens the Track A/B argument — the supplier themselves says the finish shouldn't block fabrication
2. Use the supplier's own words as evidence: "GBH has requested that patinated brass approval NOT hold shop drawing approval"
3. The supplier's technical objections (single-source, colour inconsistency, conservation risk) become Samaya's evidence for proposing an alternative
4. Update the CR sheet to reference the supplier's letter as a new supporting document
5. The response shifts from "we're working on it" to "this material is high-risk, we recommend alternative path"

**Handling CG's "2 alternative manufacturers" demand when supplier confirms single-source:**

When CG asks for 2 alternative certified manufacturers but the supplier's letter confirms only 1 supplier exists globally:

- **Frame it as GBH's market finding, not an absolute fact.** Say: "GBH conducted a market search and identified only one supplier capable of producing it to the required museum standards." Not "only one supplier exists globally" — CG may challenge that claim.
- **CG likely wants to see options to choose from, not supply from multiple sources simultaneously.** Frame the response accordingly: "This gives you multiple options to review and select from."
- **Single-source argument for finish consistency:** Patinated brass is specified across multiple project elements (showcases, wayfinding, doors, wall cladding). To guarantee colour and texture consistency, all must come from a single supplier. Different suppliers = visible variations due to the manual patination process.
- Propose alternatives in a DIFFERENT material category (e.g., PVD-coated brass instead of patinated brass)
- Reference the risk register entry (e.g., PRR-PRC-05, Score 12, Critical) to show the risk is already tracked
- Offer: "Samaya will source [alternative material] alternatives from KSA suppliers as a functionally equivalent, lower-risk substitute — samples within 30 days."

**Alternative submittal package scope:** When offering a PVD-coated or other alternative, the full submittal package must include: sample, manufacturer certificates, and test reports — not just a visual sample. State this explicitly in the email: "Full package to be submitted within 30 days including sample, manufacturer certificates, and test reports."

**Do NOT recommend accepting an alternative before it's submitted.** Never say "recommend CG accept X as primary path" when X is still in development. Say "to be submitted for CG review" instead.

**Email composition — which email to reply to and what to attach:**

When CG sends a follow-up email (e.g., Mansour's 13-Jul reminder asking for 2 alternative manufacturers), reply to THAT specific email, not the original rejection. Attachments:

1. **Updated CR Sheet** — reflecting the new information (GBH letter, Track A/B split, alternative proposal)
2. **Supplier's letter** — the document that confirms single-source or advises against the material (e.g., GBH Letter 002)

Do NOT attach the original submittal PDF, sample board photos, or data sheets — those were already submitted. The reply is a status update + proposal, not a full resubmission.

**Email structure for this scenario:**

```
Subject: RE: [Original Subject]

Dear Eng. [Name],

We received [Supplier Letter Ref] from [Supplier] regarding [topic]. Risk [Risk ID] (Score [N], [Rating]) already registered.

On your request for 2 alternative manufacturers:
[Supplier] searched the market and found only one supplier for this finish. We also contacted [country] suppliers — samples with certificates expected within [timeframe]. A [alternative] is also in development (full package within [timeframe]). This gives you options to choose from, while ensuring the final finish is applied consistently from one source across all project elements.

Current samples submitted:
1. [Material A] — [N] effects under [Submittal Ref]. [Status].
2. [Material B] — [description] already submitted.
3. [Material C] — in development, to be submitted for your review within [timeframe].

Request — approve two independent tracks to avoid delay:

Track A — [Submittal Ref] & Shop Drawings: Proceed now. [Finish] is a surface finish only, does not affect fabrication — [Supplier] confirmed.

Track B — [Submittal Ref] ([Finish]): Finalize separately. [Status updates].

Attached: updated CR Sheet and [Supplier Letter].

Kindly confirm.

Best regards,
[Name]
```

**Before composing the email, verify the baseline:** Check what was in the first submission (data sheets, samples, TDS) vs what's new in the resubmission. The first submission may already have all technical data sheets complete — the resubmission is about responding to CG's open conditions, not adding missing TDS. List the baseline clearly so the email doesn't claim to be submitting things that were already submitted.

**CR Sheet conciseness rules:**
- Write short, human English. No long paragraphs. Break into short lines.
- When multiple items reference the same source document (e.g., GBH Letter 002), put the full content in ONE item and have others say "See Item [N] for details." Never repeat the same information.
- Status/remarks columns should be 1-2 sentences max.
- Don't say "recommend" for something not yet submitted. Say "to be submitted for CG review."
- For timing-dependent items (shop drawings, on-site team), state the actual trigger condition, not an arbitrary day count. E.g., "to be submitted in the coordination stage after MEP design freeze" not "14-day extension." "Available after first batch delivery" not "upon Rev.01 approval."
- **No "only one supplier exists globally" as an absolute claim.** Frame as: "GBH conducted a market search and identified only one supplier capable of producing it to the required museum standards." CG may challenge absolute claims.
- **CG's "2 alternative manufacturers" request is about options to choose from, not supply from multiple sources simultaneously.** Frame the response accordingly: "This gives you multiple options to review and select from."
- **Single-source argument for finish consistency:** Patinated brass is specified across multiple project elements (showcases, wayfinding, doors, wall cladding). To guarantee colour and texture consistency, all must come from a single supplier. Different suppliers = visible variations due to the manual patination process.
- **Alternative submittal package scope:** When offering a PVD-coated or other alternative, the full submittal package must include: sample, manufacturer certificates, and test reports — not just a visual sample. State explicitly: "Full package to be submitted within 30 days including sample, manufacturer certificates, and test reports."
- **Email reply target:** Reply to the CG's most recent follow-up email (e.g., Mansour's reminder asking for 2 alternatives), not the original rejection. Attachments: (1) updated CR Sheet, (2) supplier's letter. Do NOT re-attach original submittal PDFs, sample board photos, or data sheets — those were already submitted.
- **Email structure for Track A/B proposal:** Keep it short. State the supplier's finding, list current samples submitted, then the two-track request. End with "Kindly confirm." See the full template in the Track A/B section above.
- **Before composing, verify the baseline:** Check what was in the first submission (data sheets, samples, TDS) vs what's new in the resubmission. The first submission may already have all technical data sheets complete — the resubmission is about responding to CG's open conditions, not adding missing TDS. List the baseline clearly so the email doesn't claim to be submitting things that were already submitted.

See `references/ma-0006-showcase-resubmission-case.md` for the full worked example.
For the AV Package Part II (1E0-1G-0002, Rawasin) CRS specifically, see `references/rawasin-av-crs-workflow.md` — exact doc ref, Adel-bank source path (OneDrive stubs + EDEADLK), the readable `/Volumes/MIcro/Download/AV Package Part II Rev. 001/` package layout, the CG 2nd-submittal verbatim file-name map, and the CDE export pitfall (only first 100 of N results).

## Plan-Level CG Comment Audit Against Contractual Obligations

When CG returns a management plan (SMP, DMP, HSE Plan, QMP) with Code C, audit each comment against the actual ER/SoW/SBC text before drafting responses. This determines which comments are valid, which are already addressed, and what specific action is needed.

See `references/plan-cg-comment-audit.md` for the full workflow: extracting comments, mapping to ER/SoW clauses, checking the submitted document, determining priority, and producing the audit table.
See `references/crs-to-drawing-register.md` for extracting per-drawing review codes from CG CRS Excel files and updating the drawing register with floor-by-floor DD Gate status tables.
See `references/crs-excel-extraction-from-outlook.md` for extracting CRS Excel files from Outlook .olk15MsgAttachment attachments — base64 boundary markers, XLSX parsing from ZIP, and multi-round Code C pattern analysis.
See `references/cg-rejection-patterns-and-reviewer-profiles.md` for the methodology to build a consolidated CG rejection pattern register and per-reviewer profiles from scattered project registers and CG response documents. Covers the 7-phase workflow (extract C/D submittals, identify patterns, calculate rates, analyse cycle times, build profiles, forecast responses, write recommendations) and the canonical output structure for both files.

### Key ER References for Plan Audits

| ER Section | Content | When to cite |
|-----------|---------|-------------|
| Sec 2.4D | Sustainability & Environmental Performance | Material compliance, VOC, Oddy comments |
| Sec 2.7 | General Cleaning — sustainability requirements | Cleaning sustainability comments |
| Sec 3.7.VIII | Client sustainability initiative, energy efficiency | Client initiative, energy efficiency comments |
| Sec 3.7.XIII | Applicable Codes — Mostadam Manual (no cert level) | Mostadam-related comments |
| SoW Sec 1.5 | Oddy testing, British Museum certification | Oddy test comments |
| SoW Sec 2.1 | Exhibition design (RIBA Stage 4) and off-site fabrication | Exhibition sustainability comments |

## Critical Finding Pattern: MOSTADAM Certification Level

The ER lists "Mostadam Manual" as an applicable code but does **not** specify any certification target level (Bronze/Silver/Gold). This is a common source of CG comments. The correct position:

> SMP should be compliance-based, not certification-based: comply with SBC 1001 and Mostadam Manual as referenced in the ER — no commitment to any specific rating level.

Any references in the SMP to a specific Mostadam level should be removed unless contractually required.

### CG Asking for Credit Selection Criteria

If the SMP includes a Yes/No MOSTADAM credit selection table and CG asks for selection criteria/rationale:

| Situation | Response |
|-----------|----------|
| SMP has a Yes/No credit selection table | **Remove the table entirely.** The table implies we are pursuing certification. Since no certification level is contractually required, there are no credits to select. The table invites exactly this question. |
| CG asks for rationale per credit | **Push back.** "The MOSTADAM credit matrix is an informational reference showing the relationship between project scope and MOSTADAM D+C credits. Since no specific certification level is contractually required per ER Sec 3.7.XIII, there are no credits to select or criteria to define. The table is provided for awareness only." |
| CG insists on keeping the table | Add a note: "Credit selection is based on project scope and applicable code requirements per ER Sec 3.7.XIII. No specific certification level is contractually required." |

**Do NOT** add a rationale column or fill rows with justifications — that implies we are pursuing certification, which we are not. The best move is to remove the table so it stops inviting the question.

## CG Scope Creep — Three Patterns to Watch

CG frequently asks the contractor (Samaya) to produce deliverables that belong to the design team (NRS, ZNA, AD Engineering). Three distinct patterns:

| Pattern | Example | RIBA Issue |
|---------|---------|------------|
| **Stage Regression** | CG asks Samaya to present "scenography concepts, narrative, interdisciplinary integration" | Stage 2 (Concept) work requested during Stage 4 (Technical Design) |
| **Full Design Package** | CG demands 10-drawing scenography set (Master Plan, Showcase Details, Lighting, Signage, Multimedia, Circulation, Finishes, Maintenance Access, Environmental Control) | Stage 3 (Spatial Coordination) work — NRS's A2742 contractual deliverable |
| **Role Confusion** | CG uses Material Board review to demand full AV/IT/Lighting engineering schedules (projectors, speakers, CCTV, access control, lighting controls, dimming systems, RCP coordination) | Stage 4 but belongs to designers (NRS/ZNA/AD), not contractor |

### RIBA 2020 Stage Regression Argument

The strongest defense is RIBA 2020 stage classification:

| CG Request | Belongs To | RIBA Stage | Samaya's Stage |
|------------|-----------|-----------|----------------|
| Scenography presentation (concept, narrative, vision) | NRS | Stage 2 — Concept | Stage 4 — Technical Design |
| 10-drawing scenography package (master plan, showcase layout, circulation, signage) | NRS | Stage 3 — Spatial Coordination | Stage 4 — Technical Design |
| AV/IT/Lighting engineering schedules & control drawings | NRS/ZNA/AD | Stage 4 — Technical Design (designers' scope) | Stage 4 — Samaya executes, doesn't author design |

**Key message:** Samaya is the contractor executing the design. The design intent, scenography narrative, and detailed engineering belong to the design team. Requesting Samaya to produce design documents creates a liability gap — we cannot warrant design decisions that belong under the designer's professional seal.

### Consulting NRS on Scope Boundaries — Email Framing

When you need NRS's opinion on whether a CG request is scope creep, **do not** phrase it as "would you handle this directly?" — that sounds like you're asking them to take work off your hands. Instead, **consult them as the design authority**:

**Correct framing:**
- "Is this something NRS should present, or should Samaya prepare it?"
- "Is this within NRS's current design deliverables, or is CG asking for something new?"
- "We see the material board as our scope, but the engineering schedules as design team scope. Your advice on where each sits would help us respond correctly."

**Wrong framing (avoid):**
- "Would you handle this directly?" — sounds like delegating
- "We need NRS to prepare the formal response" — too directive for a consultant
- "CG should receive this directly from NRS" — telling them what to do

### NRS Already Responded But CG Wasn't Satisfied

When NRS has already responded to a CG request (e.g., "this is within our scope") but CG sent a follow-up reminder, the email to NRS should:

1. **Acknowledge the previous response** — "I understand NRS previously responded that these are within your scope"
2. **State the new fact** — "but CG sent a follow-up reminder, so it seems they expect a more concrete response"
3. **Ask for advice** — "Could you advise how we should handle this?"

This avoids blaming NRS for an insufficient response while making it clear the issue isn't resolved.

### Evidence for Scope Creep Claims

When CG rejects a material board (Code C) because specialists demand engineering schedules, the rejection document itself is the evidence. Attach it to the email to NRS:

- The CG response shows AV/IT/Lighting specialists requesting full equipment schedules per gallery
- A Material Board shows finishes, samples, and visible equipment appearance — not engineering design
- Equipment schedules, control drawings, and system coordination are design engineering deliverables

## Scope Creep Protection — CR Sheet with Cost/Schedule Impact

### User Review Gate — Do NOT Send Directly

**The CR sheet is a collaborative document, not a dispatch.** After producing the CR sheet and content changes file:

1. **Present both files to the user** — open them in the editor or show the key decisions
2. **Flag the decisions the user needs to make** — especially push-back items (scope creep) and any comments where the response strategy has options
3. **Wait for user confirmation** before sending to the specialist
4. **Do NOT send the CR sheet to the specialist** without the user reviewing it first

The user explicitly corrected: "I didnt send the CR sheet please open we have to work on it again to send to fida" — meaning the CR sheet is reviewed and potentially modified by the user before it goes out.

When CG returns a plan with Code C, not all comments are equal. Some are valid contractual obligations, others are scope creep. Before sending instructions to the specialist, triage each comment into one of three lanes:

| Lane | Criteria | Action | Example |
|------|----------|--------|---------|
| **Comply** | Contractual obligation, no cost/schedule impact | Add to plan, no pushback | MOSTADAM prerequisites table, cleaning sustainability |
| **Comply (limited)** | Contractual obligation but scope-limited — we define criteria, others implement | Add criteria to plan, state who implements | Sustainability SPECS (we define, NRS implements) |
| **Push back** | Not a contractual obligation, or has cost/schedule impact | Do NOT include. Prepare separate proposal if CG insists | Exhibition sustainability strategy (not in ER/SoW as standalone deliverable) |

### CR Sheet Structure for Fida

When sending instructions to the specialist, structure the CR sheet as:

```
## CG Comment N - [Title]

| Field | Detail |
|-------|--------|
| CG Comment | [exact text] |
| ER/SoW Reference | [clause] |
| Our Obligation | Our responsibility / Push back - [reason] |
| Schedule Impact | None / [duration] |
| Action for Fida | [specific copy-paste instructions] |
| Response to CG | [exact text to use] |
```

**IMPORTANT - Do NOT include Cost Impact column when sending to the specialist.** The user explicitly removed the Cost Impact column from the CR sheet before sending to Fida. The specialist only needs to know: what to do, where to put it, and what to say to CG. Cost information is internal Samaya data.

### User Review Gate - Do NOT Send Directly

**The CR sheet is a collaborative document, not a dispatch.** After producing the CR sheet and content changes file:

1. **Present both files to the user** - open them in the editor or show the key decisions
2. **Flag the decisions the user needs to make** - especially push-back items (scope creep) and any comments where the response strategy has options
3. **Wait for user confirmation** before sending to the specialist
4. **Do NOT send the CR sheet to the specialist** without the user reviewing it first

The user explicitly corrected: "I didnt send the CR sheet please open we have to work on it again to send to fida" - meaning the CR sheet is reviewed and potentially modified by the user before it goes out.

### Middle Ground: Offer a Subsection Instead of a Standalone Document

When CG asks for a new standalone document, offer to add a brief subsection to the existing plan at no cost. This:
- Closes the content gap without creating a new deliverable
- Avoids the cost/schedule impact of a standalone document
- Shows good faith to CG
- Preserves the position that a standalone document is a separate scope

Example: "The SMP already covers material compliance, Oddy testing, VOC limits, and energy efficiency. Exhibition-specific requirements are addressed through the same criteria. A standalone Exhibition Sustainability Strategy is not required by ER/SoW but can be provided as a separate scope if needed."

### Add New Risks to Risk Register

For each push-back item, add a risk to the project risk register:

| Risk ID | Category | Risk Event | P | S | Score | Mitigation |
|---------|----------|-----------|--|---|-------|------------|
| PRR-SMP-001 | COM | CG may insist on exhibition sustainability strategy as condition of SMP approval | 3 | 2 | 6 (Medium) | Prepare position paper showing coverage in existing SMP. If CG insists, submit separate proposal. |
| PRR-SMP-002 | PRC | CG may reject SASO equivalent and demand Energy Star/WaterSense | 2 | 2 | 4 (Medium) | Proactively specify SASO equivalent. If rejected, provide cost comparison and request VO. |

## File Organization

```
02_CG_Responses/
  +-- Architecture/          # Arch-specific CG responses
  +-- Structure/             # Structural CG responses (BOD, loading, etc.)
  +-- YYYY-MM-DD_Description/  # Dated response packages
        +-- 01_CR_Sheet/
        +-- 02_NRS_Draft_Drawings/   # If applicable
        +-- 03_Registers/            # Updated submission plans
        +-- 04_Correspondence/       # CG emails
```

## CG Communication Plan Violation Detection

CG frequently bypasses Samaya and contacts subcontractors/specialists directly. This is a breach of the project communication plan (PL-0018 Rev C02, Sec 12.6 S-1: "All subcontractor correspondence must flow through the Samaya channel — direct subcontractor-to-CG communication is not permitted."). Run this check when the user asks to audit CG communication.

See `references/cg-communication-plan-violation-detection.md` for:
- SQLite queries to detect CG-to-specialist direct emails
- Queries to detect specialist-to-CG direct emails
- Violation severity classification (HIGH/MEDIUM/LOW)
- PL-0018 clause references for each violation type
- Known violations log for Aseer Museum
- Report template with clause citations

### Key patterns to watch

| Pattern | What to check |
|---------|---------------|
| CG emails NRS/ZNA/AD Engineering directly | Query Mansour's To field for @nissenrichards, @studiozna, @adeng |
| Subcontractor emails CG without Samaya managing | Query non-Samaya senders with CG in To but no Samaya in CC |
| CG directs specialist to act | Look for "Dear [specialist], please..." language in CG emails |
| Specialist CC's CG on internal reply | Check if specialist replies to Samaya with CG reviewer in CC |

### When to run

- User says "check mails for communication plan violations"
- User says "Mansour is contacting subcontractors directly"
- Weekly compliance audit
- Before raising a formal complaint about CG conduct

### Pitfall — Samaya team may initiate the bypass

Before blaming CG for direct communication, check who started it. In one case (Jul 2026), Waris CC'd ZNA (Dogan) on his reply to Mansour. Mansour then exploited that opening by putting Dogan in To. The violation report initially blamed Mansour alone — the full thread showed Waris opened the door.

**Always trace the full email thread** (via Conversation_ConversationID) before assigning fault. The first person to include a specialist on a CG thread is the one who breached protocol, even if CG later escalated it.

### Pitfall — reference emails by date+subject, not internal IDs

When writing violation reports, use date and subject line to identify emails — not internal SQLite Record_RecordID numbers. Internal IDs are meaningless to anyone outside the agent session. Recipients need to find the email in their own Outlook. Correct: "9 Jul 2026, subject: A large stone mentioned in Art Commission Schedule". Wrong: "Email ID 48008".

### Email draft templates for raising violations

When a violation is confirmed, three emails are typically needed:

**1. Internal email to Samaya team member (if they initiated):**
```
Subject: Communication Protocol — [Specialist] CC on CG Thread

[Name],

During the email audit for [period], I found that on [date] you [CC'd/emailed] [specialist] on your reply to [CG person] regarding [topic].

Per PL-0018 Sec 12.6 S-1, all specialist correspondence must flow through the Samaya channel. CC'ing a specialist on a CG thread creates a direct line that bypasses Samaya's project management role.

Going forward, please route all specialist communication with CG through Samaya's project management team. If CG needs specialist input, we coordinate it internally and issue the response ourselves.

Regards,
[Name]
```

**2. Email to CG PM (when CG initiated):**
```
Subject: Communication Protocol — Direct Contact with [Specialist]

Dear Eng. [CG PM Name],

During our email review, we observed that Eng. [CG reviewer] has been adding [specialist email] directly to the To line on the [subject] thread — [N] emails to date.

Per the approved Communication & Reporting Plan (PL-0018 Rev C02, Section 12.6), all correspondence with Samaya's sub-consultants must flow through Samaya. [Specialist] is Samaya's [role] and operates under our contract.

Direct CG-to-[specialist] communication:
- Bypasses Samaya's technical review before forwarding
- Creates liability — Samaya cannot warrant design decisions made under direct CG instruction
- Undermines the communication protocol agreed and approved by all parties

We request that all future communication with [specialist] be routed through Samaya's project management team. We will ensure timely forwarding and technical completeness.

Regards,
[Name]
```

**3. Email to subcontractor (when they contacted CG directly):**
```
Subject: Communication Protocol — Direct Contact with CG

[Name],

On [date], you [action] to [CG person] regarding [topic].

Per the project Communication & Reporting Plan (PL-0018 Rev C02, Section 12.6), all subcontractor correspondence with CG must go through Samaya. Direct subcontractor-to-CG communication is not permitted.

Going forward, please route all external communication with CG through our project management team. We will handle the submission and coordination.

Regards,
[Name]
```

### Monitoring setup

Set up a daily cron job that checks CG emails for direct contact with sub-consultants. The script at `scripts/monitor_cg_comm_protocol.sh` (in this skill's directory) runs two checks:
1. CG To field for specialist domains (NRS, ZNA, Rawasin, Glasbau, AD Eng, etc.)
2. Non-Samaya senders emailing CG without Samaya in CC

Schedule: daily at 9 AM via `cronjob action=create schedule="0 9 * * *" script=~/.hermes/skills/project-management/cg-response-protocol/scripts/monitor_cg_comm_protocol.sh`.

**Pre-run script integration:** When this cron fires, the monitor script output feeds into the agent as pre-run context. The agent then runs the SQLite queries independently to verify and produce the final report. If the monitor script returns an empty array `[]`, the agent reports "No violations detected."

## Design Recovery Plan vs Revised Schedule vs EOT — Three Distinct Requests

When CG/PMC/Planning asks for a **recovery plan**, do NOT conflate it with a revised schedule or an EOT. They are different deliverables with different acceptance criteria, and mixing them up causes a Code D rejection.

| Request | What CG wants | Contractual context | Failure mode |
|---------|---------------|---------------------|--------------|
| **Recovery Plan** | How the current delay is recovered **WITHIN the existing contractual completion date** | Must stay inside the original completion date (e.g. 30-Sep-2026) | Code D if forecast finish exceeds the contractual date |
| **Revised Schedule** | Updated dates/interim milestones reflecting current reality | May extend dates, often tied to an EOT claim | Rejected if CG asked for a recovery plan but got a revised schedule ("Not a revised schedule" is CG's explicit pushback) |
| **EOT (Extension of Time)** | Formal claim to move the completion date | Separate contractual process (e.g. LT-0007 for 223 days) | Pending MoC/CG approval; not a substitute for a recovery plan |

### The Contradiction to Handle Explicitly

CG often demands a recovery plan **inside the original deadline** while a separate **EOT request is still pending**. These are in tension: the EOT (if granted) relaxes the deadline, but CG will not wait for its outcome. Handle both in the response:

1. **Recovery plan baseline path** — how to finish design before the contractual date (this is what CG actually wants). Every interim milestone must fit inside the original completion date.
2. **EOT contingency track** — note that the EOT claim (ref, days) is under review and covers any deliverables that legitimately cannot fit, WITHOUT making it part of the primary commitment.

Do not let the recovery plan's forecast finish dates drift past the contractual date — that is the exact reason CG rejects the plan.

### Code D Recovery-Plan Rejection — the verbatim reason
> "The design phase forecast finish dates exceed the contractual completion date. The submitted schedule is therefore disapproved."

A Code D on a recovery plan means a **full re-submission (Rev.01)**, not a revision under the same ref.

### Worked example — ZD-0104 (Aseer, Aug 2026)
- ZD-0104 "Design Phases Recovery Plan" submitted 03-Aug → CG Code D 04-Aug (reason above; the plan had 90% finishing 01-Oct and IFC 100% 14-Oct — both past 30-Sep).
- Separate EOT LT-0007 (223 days, 30-Sep→11-May-2027) was pending with MoC the whole time.
- 18-Aug CG re-requested a recovery plan "Not a revised schedule" → PM asked for an urgent cross-discipline design meeting to finalise it.
- See `references/design-recovery-plan-case-zd-0104.md` for the full thread, the rejected schedule dates per discipline, and the review/response sequence.
See `references/specialist-delay-diagnosis.md` for the pitfalls in answering "which specialist is behind": tracker lead-name ≠ appointed, low-% ≠ technical delay (check contract/PO/appointment), and stale registers vs today's emails (acoustic contract was signed while the register still showed "under review").

### Response playbook
1. **Confirm the deliverable type first** — recovery plan (inside date) vs revised schedule vs EOT. Ask if ambiguous; do not guess.
2. **Urgent cross-discipline meeting** — the plan needs written confirmation of commitment from every designer/specialist (additional resources, overtime) before it goes to CG. Do not submit a plan no specialist has committed to.
3. **Every interim date inside the original completion date.**
4. **Code D on a plan = full Rev.01 re-submission**, not a fresh submittal under the same ref.
5. **Do not submit explanations again** — CG rejected the first plan for date overflow; the fix is a real compressed schedule + confirmed resource commitments, not a re-worded document.

## Proper Submission Sequence for Physical-Work Submittals (IR / Site Tests)

When a submittal involves **physical work on site** (concrete core tests, soil boreholes/geotechnical investigation, rebar scanning, mock-ups), CG enforces a strict 6-step sequence. **An Inspection Request (IR) must be filed AFTER the work is physically done, never before** — filing an IR to request the work, instead of to inspect completed work, earns an automatic Code C.

### CG's 6-step sequence (verbatim from a Code C rejection, Aseer 16-Aug-2026)
| Step | Document | Purpose | Missing = rejection reason |
|------|----------|---------|---------------------------|
| 1 | Third-party testing agency prequalification | Approve the lab credentials | "Done" (first to be cleared) |
| 2 | **Method Statement + drawings showing exact test locations** | How + where the work happens | "Missing" |
| 3 | **SNA (Start New Activity)** | Request site clearance to begin | "Missing" |
| 4 | **Execution** — physically conduct the test/work | The actual site activity | "Missing" |
| 5 | **IR** — submit the Inspection Request | Inspect completed work | "Missing" |
| 6 | **Reporting** — final third-party test report + close-out of comments | Prove results; feed into design | "Missing" |

CG's verbatim framing: *"an IR cannot be issued before the physical work is actually executed."* An IR is an inspection request for work that is **complete**, not a start-activity notice.

### Worked example — IR-0003 Core Test (Aseer, Aug 2026)
- Submitted an IR for concrete core testing **before the coring was performed** → CG Code C 16-Aug-2026.
- The Method Statement (MS-0017 Core Cutting) was only sent **after** the IR was already rejected — wrong order on our side.
- The Location Plan (ZD-0110) separately got Code B — plan accepted, but the test still must happen in sequence.
- **Root cause:** the team treated the IR as a "start the work" request. It is not.

### Rule for drafting site-test submittals
1. **Never file an IR for work not yet executed.** Check the physical status first — if the cores/boreholes haven't been drilled, the correct next document is the MS + SNA, not an IR.
2. **Sequence the submittals**: MS + drawings (step 2) → SNA (step 3) → execution → IR (step 5) → test report (step 6).
3. A **Code C on a site-test IR** usually means "you're out of sequence," not "your test method is wrong." Re-issue in the correct order rather than re-submitting the same IR.
4. The lab payment/advance is an administrative gate that blocks step 4 (execution) — resolve it before promising test dates.

## Warning Letter (LT) Audit — Escalation Chain & Feasibility

When CG issues a formal warning letter (LT-XXX), the audit methodology differs from NCR audit. Warning letters typically come after an SI NCR LT escalation chain and require feasibility assessment, not just procedural checks.

### Trigger

CG issues an LT (Warning Letter). Before responding: trace the full escalation chain, assess procedural validity of each prior step, evaluate feasibility of demands against design readiness, and distinguish procedurally-sound LTs from procedurally-defective ones.

### The 5 LT Checks

| # | Check | What to Look For | Source |
|---|-------|-----------------|--------|
| 1 | **Escalation Chain** | Trace: Was there an SI first? NCR? Letter? Proper C1 channel at each step? | SI register, NCR register, Comm Plan 6.1 |
| 2 | **Procedural History** | Was each prior step (SI, NCR) procedurally sound? If the SI was defective, the whole chain is weak. | Comm Plan 7.1, 7.3 |
| 3 | **DMP / Scope Support** | Does the approved DMP or SOW support CG's position? Some LTs cite legitimate requirements. | DMP (00_Contracts/01_DMP/), SOW |
| 4 | **Design-Readiness Dependency** | Are the demanded actions blocked by design decisions not yet made? | DMP Part 3 (stage gates), submittal register |
| 5 | **Feasibility** | Break down each demand - reasonable lead time? Within team capacity? Already in progress? | Action items, risk register, project status |

### Check 1 - Escalation Chain

Trace the full chain backwards. Example:
```
LT-003 (28-Jul)
  +-- NC-1A0-008 (10-Jun) - failure to respond to SI-008
       +-- SI-008 (09-May) - material approvals required
```

If the chain follows SI NCR LT through proper Aconex channels, the escalation is procedurally valid.

### Check 3 - DMP / Scope Support

Search the approved DMP for clauses that support or contradict CG's position. DMP 8.2 says "no material specified in IFC drawings without Code A approved sample" - this supports CG on material timing. DMP Part 3 stage gates show some materials can't be submitted pre-50% DD.

### Check 4 - Design-Readiness Dependency

Segregate materials into two categories:

| Category | Can Submit Now? | Example |
|----------|----------------|---------|
| Design-ready (already specified) | Yes - no excuse for delay | Finishes from approved schedule |
| Design-pending (awaiting DD decisions) | No - blocked by design gate | Bespoke setwork finishes |

### Check 5 - Feasibility Breakdown

| Demand | Feasibility | Evidence Required |
|--------|-------------|-------------------|
| Submit prequal documents | Depends on material selection | Submittal register |
| Submit tech data sheets | Reasonable for selected materials | Procurement status |
| Physical samples | Some await design decisions | Design stage status |
| Delivery schedule update | Reasonable | Current schedule |
| Recovery Plan | New demand - needs assessment | Programme status |

### Response Strategy

An LT needs a more nuanced response than an NCR:

| Situation | Strategy |
|-----------|----------|
| SI properly issued, NCR valid, LT follows chain | Accept procedural validity, respond with substance (DMP sequencing, design blockers, feasibility) |
| SI had procedural defects (email, wrong tier) | Flag chain weakness but don't rely on it alone - main defence is substance |
| CG mixes legitimate requirements with scope creep | Accept valid items, push back on scope creep separately |

See `references/warning-letter-audit-worked-example.md` for the full LT-003 worked example.

---

## NCR Validity Audit — 5 Checks Against Communication Plan

When CG issues an NCR alleging non-performance, audit it against the Communication Plan (PL-0018) and project procedures before responding.

### Trigger

CG issues an NCR. Before responding: check the Communication Plan, check scope/SOW, check timeline, record the audit. If invalid, escalate — do NOT comply.

### The 5 Checks

| # | Check | What to Look For | Comm Plan Ref |
|---|-------|-----------------|---------------|
| 1 | **Channel** | Was the original instruction sent through Aconex (C1)? If only email (C2), it has no contractual standing | Sec 6.1, Sec 6.3 |
| 2 | **Recipient / Tier** | Contractual matters go to L3 (Project Director), not L2 (Tech Office Manager) | Sec 7.1 |
| 3 | **Scope** | Is the action within contracted scope? Check ER/SoW and risk register for "not in scope" entries | ER/SoW |
| 4 | **Timeline** | Is the deadline reasonable? Compare against Sec 7.1 SLAs (L1=48h, L2=5WD, L3=10WD) | Sec 7.1 |
| 5 | **Response Path** | Did you escalate correctly? Forwarding contractual matters to PD is correct protocol | Sec 7.3 |

### Check 1 — Channel (Sec 6.1, Sec 6.3)

C1 (Aconex) is the system-of-record for formal submittals/NCRs. C2 (Email) is for clarification only with no contractual standing. If the original instruction was direct email only (no Aconex transmittal number) — channel violation.

### Check 2 — Recipient Tier (Sec 7.1)

| Tier | Level | Owner | Scope |
|------|-------|-------|-------|
| L2 | Project Management | Tech Office Mgr | Submittal delays, resource conflicts |
| L3 | Contractual / Commercial | Project Director | VO scope, contractual interpretation |

BOQ/drawing reconciliation is contractual -> belongs at L3 (PD). Per Sec 7.4 Rule 1: no skipped tiers.

### Check 3 — Scope

Search risk register: `grep -i "not in scope|scope creep|BOQ.*reconcil" 01_Registers/risk_register.md`

Common scope-creep NCR patterns:
- BOQ vs Drawings reconciliation (pre-contract QS exercise, not D&B Contractor deliverable)
- Design production (belongs to design team, not contractor)
- Employer document reconciliation

Scope disputed -> forward to PD/PM for CG discussion. Do NOT respond substantively.

### Check 4 — Timeline

Compare NCR deadline against SLA (L1=48h, L2=5WD, L3=10WD). A project-wide BOQ reconciliation in 3 days is unreasonable. Respond with counter-proposal.

### Check 5 — Response Path

Correct L2 response to contractual instruction: (1) do not comply substantively, (2) forward to L3 (PD/PM), (3) log in action items. This is correct escalation, not neglect.

### Rebuttal Evidence Pack

1. Communication Plan excerpts (Sec 6.3, Sec 7.1, Sec 7.3)
2. Risk register entry (e.g., PRR-COM-09 — flagged not in scope)
3. Email audit trail (email-only, wrong recipient)
4. Action items log (instruction logged + escalated)
5. Counter-proposal timeline

### Auditing the PD's NCR Response

After the PD drafts a response, check if procedural violations (channel, recipient, tier, timeline) were included. The PD may choose a substance-only strategy (citing DMP sequencing, contract priority) without mentioning procedural defects. This is a valid strategic choice — substance arguments are harder for CG to rebut since they reference CG-approved documents. But the procedural violations should still be noted as supplementary ammunition.

#### Substance vs Procedure Strategy

| Approach | Best When | Risk |
|----------|-----------|------|
| Substance only | CG-approved document supports your position (DMP Code B, priority clause) | CG can argue facts, but against their own approval |
| Procedure + substance | NCR has clear procedural defects (wrong channel, wrong tier, unreasonable timeline) | Can feel combative -- CG may get defensive |
| Substance first, procedure in reserve | Best for escalation -- use procedure only if CG rejects the substance response | Keeps maximum flexibility for later rounds |

#### Distinguishing Procedurally-Valid LTs from Defective NCRs

When auditing a warning letter (LT) vs an NCR, the key difference is the escalation chain:

| Feature | Procedurally-Valid LT | Defective NCR |
|---------|----------------------|---------------|
| Chain | SI (via Aconex C1) to NCR to LT | Direct email (no C1) to NCR |
| Channel | Aconex at every step | Email only |
| Recipient | Company-level or PD | Wrong tier (individual, L2) |
| Timeline | Follows SLA ladder | Arbitrary deadline |
| Scope basis | DMP/SOW supports requirement | Scope not in contract |

Worked example - LT-003 vs NC-1G0-0019:
- LT-003: SI-008 via Aconex, NC-1A0-008, LT-003 = procedurally valid chain (even if demands are tight)
- NC-1G0-0019: Direct email (no SI), NCR with 3-day deadline = procedurally defective (channel, tier, timeline)

Response strategy differs:
- Valid chain respond with substance (DMP sequencing, design blockers, phased plan)
- Defective chain escalate, contest validity first
- Mixed respond with substance, note defects in reserve

#### User Preference Flag Missing Procedural Violations

When auditing the PD's response, always note which procedural violations (channel, tier, deadline) were not mentioned. The user expects these documented even if the PD chose not to include them. Offer as supplementary rebuttal points.

#### DMP Clause Verification

The approved DMP PDF should be converted to markdown and stored at `00_Contracts/01_DMP/` as a formal read-only reference (`agent_edit: prohibited`, `status: formal_read_only`). If already converted:

1. Read the relevant section from the markdown files — the DMP is split into 5 part files with `00_INDEX.md` as the table of contents
2. Cross-reference with RIBA checklists in the DMP folder — BOQ/cost planning is typically Stage 3, not Stage 4 (Technical Design)
3. Check the SOW — Stage 4 gates (50% to 90% to 100%) are design deliverables, not cost exercises

If not yet converted:

1. Check `08_Document_Index/key_documents.md` for the OneDrive path to the actual PDF
2. Extract text with `pdftotext`, split into section files by the document's actual structure
3. Save under `00_Contracts/{NN}_{Plan_Name}/` with YAML frontmatter: `agent_edit: prohibited`, `status: formal_read_only`, `approval_code: B`
4. The DMP (PL-0029) was converted in Jul 2026 — use `00_Contracts/01_DMP/` as a template for other approved plans

For all plans: verify the PD's claims against the actual approved document. If the claim is consistent with the RIBA framework, SOW, and approved plan records, it is likely correct.

#### User Preference — Flag Missing Procedural Violations

When auditing the PD's response, always note which procedural violations were not mentioned. The user expects procedural defects (channel violation Sec 6.1/Sec 6.3, wrong tier Sec 7.1, unreasonable timeline) to be documented even if the PD chose not to include them. Offer them as supplementary rebuttal points in a brief note.

### Reference Files

- Communication Plan: `03_Plans/03_Communication/communication_plan.md`
- Risk register: `01_Registers/risk_register.md`
- Action items: `00_Status/action_items.md`

## Project Repo Convention

The project repo (`aseer-museum-pm`) is **status-only**:
- Only markdown files (`.md`) - no binaries
- No PDFs, no xlsx, no docx, no dwg
- No images, no archives
- `.gitignore` blocks all binary formats
- Push only status updates, decisions, action items, and register summaries