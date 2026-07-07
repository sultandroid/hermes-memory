---
name: outgoing-document-qa-review
description: "QA review pipeline for formal outgoing construction documents (RFIs, TQs, formal correspondence) before Aconex issuance. Three-layer check: Format & Document Control → Content vs Source Documents → Stakeholder & Routing alignment. Produces findings table with severity ratings and go/no-go verdict."
version: 1.0.0
author: Samaya Technical Office
tags: [qa-review, rfi, tq, construction-documents, document-control, aconex]
---

# Outgoing Document QA Review

QA review process for formal documents (RFIs, TQs, submittals) issued by the Technical Office to CG/PMC/MoC via Aconex. Use before any controlled document is sent.

## When to Load

- User asks you to "review" an RFI, TQ, or formal letter before issue
- User asks for a QA check or "fit to issue" assessment
- Any formal document destined for Aconex submission

## Required Inputs

Before starting, confirm these are accessible. If any are missing, list them in the output and mark related checks "Unverified":

1. **The document under review** (HTML and/or PDF)
2. **Style guide** (fonts, color tokens, logo assets, layout spec) — typically at `_Style-Guides/`
3. **Contract reference set** — SOW, ER, Briefing Packs, programme/baseline schedule
4. **Communication Plan** — routing path, distribution matrix, response SLAs, named POCs
5. **Stakeholder / contact register** — named individuals for approvals
6. **RFI/SI register** — to confirm the document is logged
7. **Gallery/room/code lists** — for entity-name verification

## Three-Check Framework

### Check 1 — Format & Document Control

- Style-guide conformance: fonts (e.g. Noto Naskh Arabic / Carlito / JetBrains Mono), color tokens, A4 portrait, margins, clean page breaks, footer pagination
- Bilingual rendering: Arabic RTL primary, English LTR secondary, correct bidi on mixed runs
- Logo strip: all 4 parties (Samaya / CG / ACE / MoC) with correct roles; asset paths resolve
- Document-control block: title, project/contract, issuing + receiving party, contractual reference, status, revision history, distribution, QC sign-off (Prepared/Reviewed/Approved), contents/TOC
- RFI/TQ reference number — if blank, note: **DC adds at time of issue** (not a Technical Office gap)
- Status consistency: draft/issued status matches across status field, revision history, and footer

### Check 2 — Content vs Source Documents

**CRITICAL: Verify every contractual citation against the actual source document.** PDF extraction is mandatory — never trust quoted text without verifying.

For each evidence item or clause citation:
1. Locate the source PDF or document
2. Extract the relevant passage with `pdftotext` or `openpyxl`
3. Compare verbatim against what the document quotes
4. **Fabricated citations = Blocker.** If the quoted text does not match the source, flag immediately and replace with verifiable text.

Other content checks:
- Dates align with the live programme / baseline
- Entity names (gallery codes, subcontractor numbers, stakeholder names) are correct
- Excluded-items / MoC-supplied tables match the SOW
- Question numbering is continuous with no gaps or duplicates
- Priority claims are supported by a dependency/programme argument

### Check 3 — Communication & Stakeholder Plan

- Routing matches the Comm Plan (e.g. Samaya → CG → PMC for RFIs)
- Distribution list matches the stakeholder matrix
- Points of contact asked about in the document — flag if Samaya should pre-fill instead of asking
- Response deadline / "required by" date — note if handled via Aconex workflow rather than document body
- WITHOUT PREJUDICE / rights-reservation language — add for scope-boundary or contractual-position documents
- RFI is logged in the register with correct originator, date, and file reference
- **Do NOT invent recipients** — if user says Curator/Scenographer not needed, accept that

## Output Structure

### Findings Table

| # | Check Area | Item | Result | Severity | Location | Recommended Fix |
|---|-----------|------|--------|----------|----------|----------------|

Severity levels: **Blocker** (document must not issue), **Major** (fix before issue), **Minor** (fix preferred, non-blocking), **Flag** (advisory), **Acknowledged** (user-directed won't-fix), **Pass**

### Go/No-Go Verdict

- **ISSUE** — all blockers resolved, remaining items advisory only
- **ISSUE WITH CORRECTIONS** — minors remain, PM accepts risk
- **DO NOT ISSUE** — one or more blockers present

### Unverified References List

List any required source documents that were unavailable, with the checks left "Unverified."

## Common Pitfalls

- **Fabricated evidence quotes** — agents drafting documents often paraphrase or invent clause text. Always verify with `pdftotext` extraction from the actual source PDF. A quote that "sounds right" but doesn't exist in the source is a Blocker.
- **Relative paths for logo assets** — verify with `os.path.abspath()` from the document's directory. The style guide may document a wrong path depth; test actual resolution.
- **RFI/TQ reference numbers** — the Technical Office drafts the content; the Project Document Controller (DC) assigns the formal reference number at issue time. Don't flag missing numbers as a Technical Office gap.
- **Response deadlines in the body vs Aconex** — the formal DS form / Aconex workflow handles the response SLA; the document body may only state priority. Accept this unless the Comm Plan requires explicit deadlines in the document body.
- **Distribution list completeness** — ask about missing recipients (Curator, Scenographer) but accept the user's direction. Not every RFI needs the full stakeholder matrix.
- **WITHOUT PREJUDICE clause** — always add for scope-boundary or contractual-position RFIs. Include contract number reference.
