---
name: document-gap-analysis
description: "Compare two related documents (accepted SOT vs consultant submission, old rev vs new rev, plan vs requirements, summary vs source references) and produce a structured comparison, annotation, or audit."
version: 1.1.0
author: Hermes Agent
platforms: [macos, linux]
metadata:
  hermes:
    tags: [document-comparison, gap-analysis, SOT, baseline, merge-recommendation, source-audit]
    examples: [smp-vs-revc05, plan-vs-requirements, summary-vs-sources]
---

# Document Gap Analysis

Compare two related documents — an accepted Single Source of Truth (SOT) vs a consultant/contractor submission, an old revision vs a new revision, or a summary document against its cited source references — and produce a structured comparison, annotation, or audit report.

## When to Use

- A consultant submits a document (e.g., Sustainability Strategy RevC05) and you need to compare it against the accepted SOT (e.g., the repo SMP)
- A new revision arrives and you need to identify what changed vs the approved baseline
- A plan document needs to be audited against contractual requirements (ER, SoW)
- You need to decide what content from a submission should be merged into the SOT
- A summary document references source documents and needs verification of each claim
- You are adding source-reference annotations to a document and need to verify accuracy first

## Comparison Dimensions

Always assess these 6 dimensions for standard SOT-vs-submission comparisons:

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

---

## Source-Reference Audit Mode

When a document cites source references (e.g., "per PEP section 19" or "per BEP Rev 01") and you need to verify each claim against the actual source, use this workflow.

### Why This Matters

Citing a wrong section, a non-existent source, or inaccurate content destroys credibility. Every reference annotation must be verified against the actual source document before it's added.

### Workflow

#### Step 1: Locate Source Documents

Find the actual source files — not just reference notes or summaries. Search the project folder tree:

```
search_files(pattern="*PL-0015*", target="files")
search_files(pattern="*PEP*", target="files")
```

For DMP/BEP documents, check adjacent folders (02.1_DMP, 02.2_BEP_MIDP_TIDP). Source files may be in PDF, HTML, DOCX, or MD format.

**Use formal reference MD files when available.** The repo stores source documents in both HTML (generated output) and MD (structured reference). Prefer the `.md` files under `03_Supplementary/` or `reference/` folders — they contain the same content in a grep-parseable format. Raw HTML files are harder to search and may embed styling that obscures content.

**Check document approval status before citing.** A document may be "For CG Approval" (not yet approved), "Code B" (approved with comments), or "Code A" (fully approved). Read the frontmatter metadata:
- PEP Rev 04: status "For CG Approval" — cite as "(submitted, under CG review)"
- BEP Rev 01: Code B (approved with comments) — can cite as approved
- DMP, contract docs: check their own metadata

Only cite unapproved documents as submitted/under-review — never as approved sources.

#### Step 2: Extract Source Content

Read the source documents to find the specific sections cited:

- For HTML: use `search_files` (grep) to find section headings, then `read_file` to extract surrounding context
- For DOCX: use `python-docx` to iterate paragraphs and tables
- For PDF: convert to text first or use `read_file` which auto-extracts

Key data to extract: names, numbers, durations, codes, thresholds, and the exact wording of the cited claim.

#### Step 3: Cross-Check Each Claim

For each claim in the target document, determine:

| Verdict | Meaning |
|---------|---------|
| MATCH | Claim accurately reflects the source |
| MISMATCH | Claim differs from source (explain how — different number, name, duration, etc.) |
| NOT_FOUND | Claim does not exist anywhere in the source document |
| WRONG_SECTION | Claim exists but in a different section than cited |
| PARTIAL | Core concept matches but details differ |

#### Step 4: Fix Annotations

Based on audit findings, fix each reference annotation:

1. **Correct section references** — point to the actual section that contains the content
2. **Remove wrong source attributions** — if a claim references DMP but the DMP doesn't contain it, either find the real source or mark as project-developed
3. **Add caveats** — where the document's claim differs from the source, note it in the annotation
4. **Quote the source** — when possible, include the exact wording from the source in quotation marks

#### Step 5: Handle Multiple Sources

Some claims may draw from multiple documents (e.g., CDE procedures come from PEP not BEP, but BEP defines ISO 19650 codes). Attribute each part to its correct source:

```
Ref: PEP sec 18.1 (Aconex registers). BEP sec 6.3-6.4 (ISO 19650 status codes).
```

### Annotation Style Guide

When adding reference annotations to a document, follow these rules:

**Format:**
- Use `Ref:` prefix
- Use plain language — no symbols: no §, —, ·, →, •, ✓, ✗
- Write "sec" not "§", "section" not "§"
- Parenthetical notes for caveats: `(project-developed, not in source)`

**Content:**
- Include source document code and name: `PL-0015 Rev 04 (PEP)`
- Include the specific section: `sec 17.1`
- Quote the source text directly when possible: `PEP states: "Drawing Register lists ~567 rows..."`
- Note where the document's claim differs from the source
- Mark content that is not found in any source as project-developed

**Length:**
- Keep annotations short — one to three lines
- Use natural language like an engineer's inline note
- Don't over-explain or add AI-sounding caveats

**Styling (DOCX):**
- Halftone gray: RGB(0x99, 0x99, 0x99)
- Font size: 7.5pt
- Italic
- Place directly below the section heading

### Example Annotations

```
Ref: PL-0015 Rev 04 (PEP) sec 4.1 (gates) · sec 19.1 (turnaround) · RIBA Plan of Work 2020.
G0-G1 done pre-contract; scope starts at G2 (RIBA 4).
```

```
Ref: PL-0015 Rev 04 (PEP) sec 20. PEP states: "Drawing Register lists ~567 rows but only ~158 are
at Rev A status — large reconciliation gap." Numbers approximate per PEP.
```

```
Ref: PL-0021 Rev 01 (BEP) sec 7.4.2 (BEP uses 4 levels: Critical 24h / High 3WD / Medium 1WK / Low;
Summary has 3 levels).
```

---

## Methodology

### Standard Mode: SOT vs Submission

#### Step 1: Read Both Documents Fully

Read the SOT first (it's the authoritative baseline), then the submission. For large documents, read the TOC first to understand structure, then read each section.

```
# Pattern for reading large documents
read_file(path="sot.md")                    # Full SOT
read_file(path="submission.html", limit=200)  # Submission in chunks
```

#### Step 2: Build the Section Mapping Table

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

#### Step 3: Identify Framing Differences

Look for fundamental differences in:
- **Primary framing** — e.g., "code-compliance-based" vs "Mostadam-anchored"
- **Certification stance** — e.g., "not a contractual performance bond" vs "tracking points"
- **Lifecycle scope** — e.g., implicit in phase table vs explicitly stated
- **Target numbers** — e.g., waste diversion 60% vs 75%

#### Step 4: Assess Content Depth Per Topic

For each shared topic, assess:
- **SOT depth** — How many paragraphs/tables? How specific?
- **Submission depth** — Same assessment
- **Verdict** — Which is more actionable? Which has more technical detail?

#### Step 5: Identify Gaps

A gap is a topic covered in one document but completely absent in the other:

| Gap | Present in | Absent in | Impact |
|-----|-----------|-----------|--------|
| Subcontractor obligations | Submission | SOT | Critical for execution |
| BIM LOD 4 review | Submission | SOT | Valuable for quality |
| Existing MEP baseline | Submission | SOT | Critical for refurbishment |

#### Step 6: Produce Summary Verdict

| Category | Count |
|----------|-------|
| Keep SOT | N sections |
| Keep Submission | N sections |
| Merge | N sections |
| Contradictions to resolve | N |
| Gaps in SOT that submission fills | N |

**Bottom line:** One-paragraph recommendation on what to do.

## Pitfalls

1. **Don't assume the SOT is complete.** The submission may contain critical operational detail the SOT lacks.
2. **Don't assume the submission is better.** The SOT may have the correct strategic framing that the submission gets wrong.
3. **Flag contradictions explicitly.** Don't silently pick one value — show both and recommend a resolution.
4. **Don't merge everything.** Some content belongs in the submission only.
5. **Check document dates.** The newer document may supersede the older one.
6. **Check document purpose.** One may be a strategic plan, the other an operational implementation document.
7. **Large HTML files may exceed read_file limits.** Read in chunks (200-300 lines at a time).
8. **Don't just compare TOCs.** The same section title may cover very different content.
9. **Watch for renamed sections.** The submission may cover the same topic under a different section number.
10. **The submission may have content the SOT doesn't need.** E.g., elaborate cover pages, SVG graphics.
11. **Always verify source documents before citing them.** Never add a reference annotation without reading the actual source text first. Session 2026-07-25 caught systematic section-reference errors across 3 source documents because annotations were added from memory, not from source verification.
12. **Don't trust section number mappings.** The source document's section numbering may differ from what the summary claims (e.g., BEP §3 in summary was actually BEP §2.1). Always extract the actual section headings from the source.
13. **Check if the source even mentions the claimed content.** The audit found entire concepts attributed to DMP (ICE wheel, interface register, turnaround times) that simply don't exist in that document.
15. **Check document approval status before citing.** A document marked "For CG Approval" or "Draft" is not an approved source. Read the frontmatter metadata. Cite unapproved documents as "(submitted, under CG review)" — never as authoritative references. The user explicitly corrected this in session 2026-07-25: PEP Rev 04 had status "For CG Approval" but was cited as a source without qualification.

16. **Use formal MD files from the repo, not raw HTML.** The repo stores structured `.md` reference files under `03_Supplementary/` and `reference/`. These are easier to search and parse than raw HTML files. Raw HTML files may embed content in SVG, CSS, or inline elements that grep/search can't find. Always check for the MD equivalent first.

## Reference Files

- `references/smp-vs-revc05-comparison.md` — Worked example: Aseer Museum SMP (repo SOT) vs RevC05 HTML (Fida submission), 6-dimension comparison with 14-section mapping, framing analysis, content depth assessment, and merge recommendations.
- `references/source-reference-audit.md` — Worked example: auditing a summary DOCX against PEP Rev 04, DMP Rev C03, and BEP Rev 01 source documents. Covers systematic section-reference errors, missing content, and correction workflow.
