# RFI/TQ Pre-Issue QA Review — Findings Table Template

Use this template for formal QA review of a draft RFI/TQ before Aconex submission. Copy, fill, and save alongside the reviewed document.

## Findings Table Columns

| # | Check Area | Item | Result (Pass/Fail/Flag) | Severity (Blocker/Major/Minor) | Location | Recommended Fix |

## Severity Definitions

| Severity | Criteria | Action |
|----------|----------|--------|
| Blocker | Invented citation, wrong contract reference, wrong entity, wrong critical-path date | Do Not Issue |
| Major | Missing required field (doc ref, deadline), wrong routing, broken critical workflow | Fix before issue |
| Minor | Style variance, missing optional info, incomplete distribution | Patch before issue |

## Verdicts

| Verdict | Criteria |
|---------|----------|
| Issue | All Pass, no Flags |
| Issue-with-corrections | Minors only, fixable |
| Do-not-issue | Blocker(s) present |

## Three Check Domains

### 1. Format & Document Control
- Style guide conformance (fonts, colors, margins, RTL)
- Bilingual rendering (AR RTL primary, EN LTR secondary via bidi classes)
- Logo strip: all 4 parties present, asset paths resolve
- Document-control block: ref, rev, date, status, distribution
- RFI/TQ reference number present and unique (MOC-MUS-ASE-1A0-TQ-XXXX)
- Revision history populated (not empty dashes)
- QC sign-off: Prepared/Reviewed/Approved
- Footer pagination matches actual page count
- Status consistent across status field, revision history, and footer
- TOC entries match actual page content

### 2. Content vs Project Information
- Every contractual citation traces to a real clause in the source document
- Quoted text matches source verbatim — no drift, no invented language
- Dates align with current baseline/EOT programme
- Entity names correct (subcontractor numbers, gallery codes, firm names)
- MoC-supplied / excluded items table matches SOW §2.2
- Question numbering continuous, no gaps or duplicates
- Priority claim supported by dependency argument

### 3. Communication & Stakeholder Plan
- Routing matches Comm Plan (Samaya → CG → PMC → MoC)
- Distribution list matches stakeholder matrix — no missing recipients
- Points of contact: don't ask MoC for info Samaya already has (Stakeholder Register)
- Response deadline stated and tied to critical path
- RFI is logged in register with originator, date, file reference
- WITHOUT PREJUDICE / rights-reservation clause present for scope-boundary RFIs
