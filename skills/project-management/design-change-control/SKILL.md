---
name: design-change-control
title: Design Change Control — Stage Transition Management
description: Manage design changes between approved baseline (Stage 3) and subsequent stages (Stage 4+). When a Stage 4 submission deviates from the approved Stage 3 baseline, produce a Design Change Register (DCR) with formal Backup Reports per change, map to audit/NCR closure items, and submit to CG for approval.
version: 1.0.0
author: Hermes Agent
trigger: user asks about design changes between stages, whether the audit report needs updating from a new submission, or how to document deviations from an approved design baseline
tags: [design-change, stage-gate, design-compliance, dcr, backup-report, aseer]
---

# Design Change Control

## Core Principle

**Stage 3 = approved baseline. Stage 4 = execution design. Any difference = design change, not a refinement.**

The contractor (Samaya) is contractually bound to the approved Stage 3 baseline. Deviations without documented approval create compliance risk at handover.

## When To Use

- User receives a Stage 4/DD submission and asks "do we need to update the Stage 3 audit?"
- User asks "why did this change from what was approved?"
- CG review flags "why change?" on Stage 4 drawings
- User wants to track design deviations systematically

## Key Distinction: Don't Update the Stage 3 Audit

| Wrong | Right |
|-------|-------|
| Update Stage 3 audit report to reflect Stage 4 changes | Keep Stage 3 audit as a historical record of discrepancies found AT THAT STAGE |
| Mark audit items "closed" directly in the audit PDF/xlsx | Create a separate **Audit Closure Tracker** mapping each audit item to its Stage 4 resolution DCR |
| Treat Stage 4 changes as "refinements" that don't need documentation | Treat every Stage 4 deviation from Stage 3 as a formal Design Change |

## Process

### Step 1: Identify All Changes Between Stage 3 and Stage 4

Compare the Stage 4 submission against the Stage 3 approved baseline. For each deviation, capture:

| Field | Source |
|-------|--------|
| What changed | Side-by-side comparison of Stage 3 drawing vs Stage 4 drawing |
| Why it changed | Change trigger (contractor input, specialist review, site condition, client request) |
| Technical justification | The rationale (from the designer/subcontractor) |
| Impact — Cost | Neutral / Minor / Significant |
| Impact — Programme | Neutral / Minor / Critical |
| Impact — Quality/Aesthetic | Visual, functional, or conservation impact |
| Reference photo | Screenshots of Stage 3 vs Stage 4 for visual evidence |

### Step 2: Create Design Change Register (DCR)

Excel register with these columns:

```
DCR ID | Date Raised | Stage 3 Reference (Approved) | Stage 4 Reference (Proposed) | Description of Change | Change Trigger | Justification | Impact — Cost | Impact — Programme | Impact — Quality/Aesthetic | Status | CG Status | Reference Photo
```

**Reference photos:** OCR screenshots to extract text evidence, embed or hyperlink them in the register for traceability.

**Naming:** `DCR-{PROJECT-CODE}-001.xlsx`

### Step 3: Map to Existing Audits / NCRs

Create an **Audit Closure Tracker** sheet in the DCR workbook:

```
Audit Item | Description | NRS Proposal (from Audit) | Stage 4 Status | DCR Reference | Mapped to Showcase Change | Closure Date | Notes
```

Many Stage 3 audit items will be partially or fully addressed by Stage 4 submissions. The tracker makes this visible.

### Step 4: Require Formal Backup Reports per Change

Each DCR entry needs a standalone **Backup Report** from the designer containing:

1. **Visual comparison** — Stage 3 vs Stage 4 marked-up drawing extract (annotated screenshot or CAD overlay)
2. **Technical rationale** — why Stage 3 solution was not feasible (structural, functional, manufacturing, or conservation grounds)
3. **Supporting evidence** — manufacturer data, specialist consultant calculations, test results
4. **Impact assessment** — cost, programme, quality, maintenance implications
5. **Precedent references** — equivalent solutions accepted on other museum projects (optional but strengthens the case)

**Never accept verbal/"email justification" as a Backup Report.** The designer must produce a formal documented submission.

### Step 5: Submit to CG for Formal Approval

- Compile: DCR Excel + all Backup Reports as a consolidated submission
- Reference the original Stage 4 submission code (e.g., MOC-MUS-ASE-1A0-ZD-0066)
- Each DCR item must be explicitly approved (or rejected with revision instructions)
- Stage 4 cannot proceed to IFC until all DCR items are closed

## Common Design Change Types (Aseer Museum Showcase Example)

| DCR Category | Typical Changes | Common CG Pushback |
|---|---|---|
| Material/finish substitution | Fabric change (Kvadrat→Création Baumann), Corian colour changes | "Not per approved design — propose alternative with justification" |
| Dimensional change | Plinth height 200mm→100mm, panel width changes | "Dimensions and proportions do not match approved design" |
| Mechanism change | Hinged→sliding doors, dual opening mechanisms | "Clarify opening mechanism and locking system and their functional/visual impact" |
| System change | New material introduced (Acorian), new fixing method | "Clarify why new material when it was not in original design" |
| Procedural | Numbering system changed between submissions | "Standardize numbering system for all showcases across future submissions" |

## NRS's Incorrect Position (Documented)

When NRS (Nissen Richards Studio) says:
- "These are refinements, not changes" → **Incorrect.** If the Stage 3 drawing shows A and Stage 4 shows B, it's a change regardless of justification.
- "Our drawings should not be issued to the consultant; only Glasbau Hahn shop drawings should be reviewed" → **Incorrect.** The Stage 4 design submission is Samaya's contractual deliverable. NRS drawings ARE the submission. GH shop drawings are downstream.
- "There is no need to provide further 3D drawings" → **Procedurally wrong.** The reviewer (CG) sets the information required for review, not the submitter.

**Correct response:** "These are formal design changes. Issue a Backup Report per change or we cannot proceed to IFC."

## DCR Excel Format

### Sheet 1 — Design Change Register
- Navy (#1E293B) headers with white bold font
- Alternating row shading (#F8FAFC on even rows)
- "Reference Photo" column with clickable hyperlinks to image files
- Freeze panes below header row
- Landscape orientation, fit to width

### Sheet 2 — Audit Closure Tracker
- Maps every Stage 3 audit item (from A2742-10.07-001A or similar) to its Stage 4 resolution
- Columns: Audit Item #, Description, Stage 3 Proposal, Stage 4 Status, DCR Reference, Mapped to Change?, Closure Date, Notes
- Shows which items are closed by Stage 4, partially addressed, or still open

### Sheet 3 — Legend
- Column definitions for DCR register

### Sheet 4 — Reference Photos
- File names with descriptions and hyperlinks

### Sheet 5 — Embedded Images (optional)
- Actual images embedded for visual review within the workbook

## Reference Photos Workflow

When user sends screenshots of Stage 3/Stage 4 drawings:

1. **Copy to permanent directory:** `~/Desktop/DCR_Reference_Photos/`
2. **OCR with tesseract** to extract text evidence: `tesseract /path/to/image.png stdout -l eng`
3. **Name descriptively:** `03_showcase_type2_plinth_change.png` (not `Screenshot_2026-06-23_at_15.51.45.png`)
4. **Describe each image** based on OCR output — what it shows, which stage it's from, what DCR it supports
5. **Embed or hyperlink** in the DCR workbook — clickable "Reference Photo" column with file:// links to open from Excel

## Pitfalls

1. **Don't update the Stage 3 audit report.** The audit is a historical record of discrepancies at THAT stage. Update would retroactively change a closed stage's findings.
2. **Don't accept verbal justifications.** CG requires documented Backup Reports per change. Email threads are not sufficient.
3. **Don't let the designer frame changes as "refinements."** If Stage 3 baseline shows X and Stage 4 shows Y, it's a change — regardless of how minor or well-justified.
4. **Cost impact is not always monetary.** A "neutral cost" change with negative aesthetic impact still needs CG approval.
5. **CG "For Information Only" ≠ approval.** Do not treat FYI as sign-off on the changes. The DCR submission must be explicitly approved (Code A/B) before Stage 4 can proceed.
6. **Image OCR is lossy** — tesseract may miss text in small fonts, tables, or complex layouts. Cross-reference with original PDF where possible.
7. **Don't embed images directly in Excel data rows** — openpyxl places them as floating objects that overlap cells. Use hyperlinks in cells + a dedicated "Embedded Images" sheet instead.

## Related Skills

- `project-register-manager` — openpyxl techniques for creating and styling Excel registers with the same formatting conventions
- `submittal-register-management` — submittal tracking (DCR is a related but distinct register type)
- `project-scope-verification` — when the change triggers a scope question

## Related Reference Files

- `references/aseer-showcase-stage3-to-stage4-dcr-example.md` — Worked example of DCR for Aseer Museum showcase changes
- `references/contractor-correspondence-strategy.md` — How to respond to CG/consultant design changes without accepting liability, including the "draft to PM + ally first" workflow, email templates, and key phrases to use/avoid
