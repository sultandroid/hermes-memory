---
name: document-gap-analysis
description: "Compare two related documents (accepted SOT vs consultant submission, old rev vs new rev, plan vs requirements) and produce a structured comparison table identifying structural, framing, content, and contradiction differences. Covers sustainability plans, management plans, technical reports, and any paired documents where one is the authoritative baseline."
version: 1.0.0
author: Hermes Agent
platforms: [macos, linux]
metadata:
  hermes:
    tags: [document-comparison, gap-analysis, SOT, baseline, merge-recommendation]
    examples: ["smp-vs-revc05", "plan-vs-requirements"]
---

# Document Gap Analysis

Compare two related documents — an accepted Single Source of Truth (SOT) vs a consultant/contractor submission, or an old revision vs a new revision — and produce a structured comparison table with merge recommendations.

## When to Use

- A consultant submits a document (e.g., Sustainability Strategy RevC05) and you need to compare it against the accepted SOT (e.g., the repo SMP)
- A new revision arrives and you need to identify what changed vs the approved baseline
- A plan document needs to be audited against contractual requirements (ER, SoW)
- You need to decide what content from a submission should be merged into the SOT

## Comparison Dimensions

Always assess these 6 dimensions:

### 1. Structure / Section Mapping

Compare the table of contents and section organization:

| Dimension | What to check |
|-----------|---------------|
| Section count | Does one document have sections the other lacks? |
| Organization | Flat list vs multi-part structure? |
| Navigation | Table of contents, page numbers, cross-references? |
| Document control | Cover page, revision log, parties table, authority basis? |

**Output:** A section-by-section mapping table with verdict per section (Keep SOT / Keep Submission / Merge).

### 2. Framing / Strategic Approach

Compare the fundamental framing of the document:

| Aspect | What to check |
|--------|---------------|
| Primary framing | Code-compliance vs rating-system vs TBL vs other? |
| Certification stance | Hard commitment vs aspirational vs "subject to review"? |
| Lifecycle scope | Design-only vs construction-only vs full D&B? |
| Authority basis | Which contractual clauses are cited as the primary hook? |

**Output:** A framing comparison table noting contradictions and alignment.

### 3. Content Depth

Compare how deeply each document covers shared topics:

| Topic | SOT depth | Submission depth | Verdict |
|-------|-----------|-----------------|---------|
| Energy | Brief mention | Detailed: baseline, modelling, equipment thresholds | Submission has superior depth |
| Materials | Generic criteria | Certification workflow, emission thresholds, banned substances | Merge |
| ... | ... | ... | ... |

**Output:** A content depth table with verdict per topic.

### 4. Roles & Responsibilities

Compare who is accountable for what:

| Role | SOT | Submission | Verdict |
|------|-----|------------|---------|
| Sustainability Manager | Generic | Named person with credentials | Merge |
| RACI matrix | Not present | 8 parties × 8 categories | Merge |
| Subcontractor accountability | Not addressed | Per-sub credit ownership | Merge |

**Output:** A roles comparison table.

### 5. Deliverables / Milestones Schedule

Compare how deliverables and timelines are structured:

| Aspect | SOT | Submission | Verdict |
|--------|-----|------------|---------|
| Basis | Week-based | Day-based | Different but compatible |
| Design deliverables | SAR-02 to SAR-07 | M1-M3 with assessor gates | Merge |
| Reporting | Monthly CSR + quarterly | R-01 to R-07 with authors/recipients | Merge |

**Output:** A schedule comparison table.

### 6. Contradictions & Gaps

Identify explicit contradictions and gaps in one document vs the other:

| Issue | SOT says | Submission says | Resolution |
|-------|----------|-----------------|------------|
| Waste target | ≥ 60% | ≥ 75% | Must align |
| Oddy aging | 14 days | 49 days | Must align |
| Subcontractor matrix | Not addressed | Full matrix | Gap in SOT |

**Output:** A contradictions table with recommended resolution.

## Methodology

### Step 1: Read Both Documents Fully

Read the SOT first (it's the authoritative baseline), then the submission. For large documents, read the TOC first to understand structure, then read each section.

```python
# Pattern for reading large documents
read_file(path="sot.md")                    # Full SOT
read_file(path="submission.html", limit=200)  # Submission in chunks
```

### Step 2: Build the Section Mapping Table

Create a table mapping each SOT section to its submission counterpart:

| Section | SOT | Submission | Verdict |
|---------|-----|------------|---------|
| Executive Summary | §1 — Code-compliance framing | §3 — D&B mandate, 5 Must-Knows | Merge |
| ... | ... | ... | ... |

Verdict options:
- **Keep SOT** — SOT is superior or is the agreed direction
- **Keep Submission** — Submission is superior
- **Merge** — Both have value, combine
- **Contradiction** — Values differ, needs resolution

### Step 3: Identify Framing Differences

Look for fundamental differences in:
- **Primary framing** — e.g., "code-compliance-based" vs "Mostadam-anchored"
- **Certification stance** — e.g., "not a contractual performance bond" vs "tracking points"
- **Lifecycle scope** — e.g., implicit in phase table vs explicitly stated
- **Target numbers** — e.g., waste diversion 60% vs 75%

### Step 4: Assess Content Depth Per Topic

For each shared topic, assess:
- **SOT depth** — How many paragraphs/tables? How specific?
- **Submission depth** — Same assessment
- **Verdict** — Which is more actionable? Which has more technical detail?

### Step 5: Identify Gaps

A gap is a topic covered in one document but completely absent in the other:

| Gap | Present in | Absent in | Impact |
|-----|-----------|-----------|--------|
| Subcontractor obligations | Submission | SOT | Critical for execution |
| BIM LOD 4 review | Submission | SOT | Valuable for quality |
| Existing MEP baseline | Submission | SOT | Critical for refurbishment |

### Step 6: Produce Summary Verdict

| Category | Count |
|----------|-------|
| Keep SOT | N sections |
| Keep Submission | N sections |
| Merge | N sections |
| Contradictions to resolve | N |
| Gaps in SOT that submission fills | N |

**Bottom line:** One-paragraph recommendation on what to do — e.g., "Keep the SOT's strategic framing but merge the submission's operational detail. Resolve the two contradictions before finalizing."

## Pitfalls

1. **Don't assume the SOT is complete.** The submission may contain critical operational detail the SOT lacks (subcontractor matrices, procurement specs, BIM integration).
2. **Don't assume the submission is better.** The SOT may have the correct strategic framing that the submission gets wrong (e.g., code-compliance vs rating-chasing).
3. **Flag contradictions explicitly.** Don't silently pick one value — show both and recommend a resolution.
4. **Don't merge everything.** Some content belongs in the submission only (e.g., revision history, cover page branding). The SOT should only absorb content that adds operational value.
5. **Check document dates.** The newer document may supersede the older one, or the SOT may have been updated after the submission was written.
6. **Check document purpose.** One may be a strategic plan, the other an operational implementation document. They may serve different purposes and shouldn't be fully merged.
7. **Large HTML files may exceed read_file limits.** Read in chunks (200-300 lines at a time) using offset/limit. The submission may be 2-5× the size of the SOT.
8. **Don't just compare TOCs.** The same section title may cover very different content. Read the actual text.
9. **Watch for renamed sections.** The submission may cover the same topic under a different section number or name.
10. **The submission may have content the SOT doesn't need.** E.g., a 25-page HTML document may have elaborate cover pages, SVG graphics, and revision history that don't belong in a markdown SOT.

## Reference Files

- `references/smp-vs-revc05-comparison.md` — Worked example: Aseer Museum SMP (repo SOT) vs RevC05 HTML (Fida submission), 6-dimension comparison with 14-section mapping, framing analysis, content depth assessment, and merge recommendations.
