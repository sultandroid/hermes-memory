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

## Core Principle: Two Separate Streams

CG comments come in two distinct types. **Never merge them into one response.**

| Stream | Source | Response Format | Audience |
|--------|--------|-----------------|----------|
| **Submission Plan Comments** | CG review of submission plan/register (e.g. Mohammad Elbaz) | **CR Sheet** (Excel) - sent to CG for agreement | CG + internal |
| **Detailed Technical Review** | CG review of technical deliverables (e.g. Abdrabo Shahin, Code C) | **Consultant Comment Register** (Excel) - internal tracking | Internal only until resubmission |

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

- "This was completed at Stage 3. NRS draft (XXXX) for reference. Included in submission plan and drawing register." - for items already done
- "This will be in the Life Safety registers and submittals (Namaa), not in the current architectural package." - for scope handoffs
- "Bespoke setwork furniture shown on GA with setwork codes. Remaining FF&E to be coordinated from 50% to 90% to IFC." - for phased items
- User-verified FF&E response: "Noted. Will add to submission plan and drawing register. Already in GA drawings, will split into separate drawings." — Confirms: (1) setwork already shown, (2) FF&E is a separate phased track, (3) supplier appointment is the blocker, (4) actions = add to submission plan + drawing register + split GA drawings
- FF&E scope clarification: "Bespoke setwork furniture is shown on the GA drawings with setwork codes. Remaining FF&E items will be coordinated and included in subsequent stages from 50% to 90% to IFC. FF&E supplier to be appointed." — CG comment. Response: "Noted. Will add to submission plan and drawing register. Already in GA drawings, will split into separate drawings."
- "Noted." - for accepted process comments
- "All applicable loads in BOD per SBC. Showcase weights from manufacturer. Artwork weights from curator." - for technical clarifications

## Multi-Round CRS Disposition Matrix Pattern

When CG issues multiple rounds of comments on the same document (e.g., R1 9-Mar, R2 2-Jun, R3 18-Jun), use a **single consolidated disposition matrix** with round-separator rows:

### Structure

```
| # | Round | CG Comment | Disposition | Ref | Status | Route/Scope |
|---|---|---|---|---|---|---|
| cat-row | Round 1 — CG comments (9-Mar-26) — closed in Rev 1/2 |
| CG-01 | R1·9-Mar | [comment] | [response] | §X | CLOSED | SMP-scope |
| cat-row | Round 2 — CG CRS (2-Jun-26, Code C) — addressed in Rev 3 |
| CRS-01 | R2·2-Jun | [comment] | [response] | T1-07 | CLOSED | SMP-scope |
| cat-row | Round 3 — CG CRS (18-Jun-26, Code C) — addressed in Rev 4 |
| CRS-18 | R3·18-Jun | [comment] | [response] | CRS | CLOSED | Procedural |
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
R1: CG-01 → CLOSED
R2: CG-01 → CLOSED (carried forward), CRS-07 → RE-OPENED (CV not yet submitted)
R3: CRS-18 → CLOSED (CRS completed, QA performed)
```

### Caveman Style for C:Resubmit Reasons

When adding CG resubmit reasons to remarks, write short direct sentences:
- "CG want: loading schedule, masonry weights, concrete cover, wind/seismic refs. All in BOD per SBC. Need to clarify and resubmit."
- "CG want: loading notation schedule, load combo names. Loading tables in BOD per SBC. Need to clarify and resubmit."
- "CG want: audit report for previous design stage. Under preparation. Will include in next package."

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
1. State the numbers: "X drawings → B, Y drawings → C, Z drawings → not stamped"
2. State the contradiction: "Overall C seems incorrect given X are B"
3. Name specific drawings with contradictory stamps
4. Ask 2 clear questions: (a) should overall be B? (b) confirm status for specific drawings

**Template:**
```
Subject: Clarification on Overall Status — Submittal [NUMBER]

Dear Eng. [Name],

We received the review for Submittal [NUMBER]. The overall status is C, but the breakdown shows:

[X] drawings → B
[Y] drawings → C
[Z] drawings → not stamped

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

## Status Definitions

| Status | Meaning | Color |
|--------|---------|-------|
| Closed | Resolved, CG position agreed | Green |
| Open | Action required, pending | Red |
| Noted | Acknowledged, no action needed | Blue |
| C:Resubmit | CG returned with comments, blocked until resubmission | Yellow + "BLOCKED" prefix |

## Pitfalls

- **Never add unapproved names to documents.** If a person's name hasn't been formally approved by CG/MoC (via CV submission, KPR update, or formal appointment), list the role only with a note: "Per live KPR" or "TBC — appointment pending." Adding unapproved names creates liability — CG will hold Samaya to that person's qualifications even if they were never formally accepted. The user explicitly corrected: "dont add names are not approved."
- **Never merge submission plan comments with detailed technical reviews** — they are two separate streams with different audiences and response formats.
- **cat-row separators** must use `.cat-row td` class (dark background, white text), not blank rows. Blank rows break table continuity.
- **Status badges** must be consistent: CLOSED (green), SUBMITTAL-PENDING (amber), IN-PROGRESS (blue), RE-OPENED (red). Don't invent new badge types mid-document.
- **Round column** must include both date and round number (e.g., "R2 · 2-Jun") for traceability across revisions.

## File Organization

```
02_CG_Responses/
  ├── Architecture/          # Arch-specific CG responses
  ├── Structure/             # Structural CG responses (BOD, loading, etc.)
  └── YYYY-MM-DD_Description/  # Dated response packages
        ├── 01_CR_Sheet/
        ├── 02_NRS_Draft_Drawings/   # If applicable
        ├── 03_Registers/            # Updated submission plans
        └── 04_Correspondence/       # CG emails
```

## Project Repo Convention

The project repo (`aseer-museum-pm`) is **status-only**:
- Only markdown files (`.md`) - no binaries
- No PDFs, no xlsx, no docx, no dwg
- No images, no archives
- `.gitignore` blocks all binary formats
- Push only status updates, decisions, action items, and register summaries
