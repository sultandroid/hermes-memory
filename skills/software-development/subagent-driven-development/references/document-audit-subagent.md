# Document Cross-Reference Audit via Sub-Agent

Audit a large target document (HTML proposal, technical report) against multiple reference documents (SOW, ER, spec sheets, plans) by delegating to a sub-agent with full context.

## When to Use

- User asks to "audit X against Y", "review sections against reference docs", "check proposal against project info"
- Target document is a self-contained file (HTML, MD, PDF)
- Reference documents exist as separate files in the project folder
- Goal is a structured audit report with section-by-section findings, severity ratings, and prioritized fixes

## Workflow

### Step 1: Read the Target Document

Read the full target document to understand its structure (sections, appendices, page count). Note:
- Total sections and their headers
- Any appendices listed in TOC
- Page numbering scheme
- Key claims (numbers, areas, durations, costs)

### Step 2: Gather Context from Memory & History

Before delegating, collect:
- Project facts from memory (client, designer, BoQ, brands, Odoo ID)
- Session history learnings (previous cleanup instructions, resolved issues)
- Any known constraints (e.g., "SOW/ER references were supposed to be cleaned")

### Step 3: Locate Reference Documents

The sub-agent may have filesystem access but the delegate_task parent doesn't. In the context, include:
- Exact file paths to reference documents (use terminal/search to confirm existence first)
- A summary of what each reference doc covers
- If OneDrive paths cause permission issues, note alternative search strategies

### Step 4: Delegate the Audit

Use `delegate_task` with comprehensive context:

```python
delegate_task(
    goal="Audit the [document name] against all project reference documents",
    context=f"""
    TARGET DOCUMENT: /path/to/target.html

    STRUCTURE (from pre-read):
    - Section 1: Company Profile
    - Section 2: Project Understanding
    - Section 3: Scope of Work (WBS, exclusions, gallery breakdown, supporting areas)
    - ... (list all sections and appendices)
    - Total pages: N
    - Appendix E referenced in TOC but NOT in HTML body

    PROJECT FACTS (verify against these):
    - Client: ...
    - Designer: ...
    - BoQ base: $X
    - AV brands: ...
    - Exhibition area: ~Y sqm (from reference)

    REFERENCE DOCUMENTS:
    1) /path/to/ref1.md — covers SOW scope
    2) /path/to/ref2.md — covers ER requirements
    3) etc.

    CONSTRAINTS:
    - All SOW/ER references should have been replaced with "Excluded — client scope"
    - 24-page count must match rendered content
    - etc.

    AUDIT INSTRUCTIONS:
    For EACH section, flag:
    1. Factual discrepancies vs reference docs
    2. Missing content (promised but not delivered)
    3. Inconsistencies within the document
    4. Generic/placeholder content
    5. Completeness gaps (missing appendices, tables)
    6. Brand/AV details that don't match design docs

    OUTPUT FORMAT:
    Write a comprehensive Markdown audit report to /tmp/ or a new .md file with:
    - Section-by-section findings table (Section | Finding | Severity | Recommended Fix)
    - Overall score (1-10)
    - Top 5 priority issues
    - Compliance gaps against ER requirements
    - Brand verification table

    CRITICAL: READ-ONLY task. Do NOT modify the target document.
    """,
    toolsets=['terminal', 'file']
)
```

### Step 5: Present & Save Results

After the sub-agent returns:
1. Read the audit report to summarize key findings
2. Tell the user the full report path
3. Present a compact table of critical/high issues in your response

## Context Construction Rules

### What MUST be in the context:

| Info | Why | Example |
|------|-----|---------|
| Exact file paths | Sub-agent needs to find files | `/full/path/to/proposal.html` |
| Document structure summary | Sub-agent can skip the full pre-read | "12 sections, 5 appendices, 24 pages claimed" |
| Project facts from memory | Sub-agent has no memory access | "Designer: BMA, AV: LOPU/QSC/Crestron" |
| Section-by-section pointers | Helps sub-agent focus its reading | "Section 2 claims ~1,500 m² — verify against SOW" |
| Known constraints | Avoids repeating past mistakes | "SOW/ER cleanup was supposed to be done" |
| READ-ONLY warning | Prevents accidental overwrite | "CRITICAL: Do NOT modify the target document" |

### What to OMIT from context:

- Raw file dumps >200KB (will timeout the sub-agent)
- Full conversation history (sub-agent doesn't need it)
- Previous session compaction notes (not relevant)

## Pitfalls

- **Sub-agent times out on large files** (>150KB HTML, >2500 lines). Pre-read the file yourself and include a structure summary in context instead of making the sub-agent read the whole thing.
- **OneDrive permission errors on terminal search**. Tell the sub-agent to try `read_file` (different permissions) or search for extracts in alternative paths.
- **Sub-agent overwrites the target file**. Always include the READ-ONLY warning. After delegation, verify the source file wasn't modified (`ls -la` to check timestamp/size).
- **Sub-agent fabricates reference content**. If a reference doc can't be found, the sub-agent may invent scope numbers. Tell it to note gaps explicitly rather than guess.
- **Memory not available to sub-agents**. Include all relevant memory facts (project info, user preferences, past corrections) explicitly in the context.
- **Session history not available**. Include key learnings from past sessions (e.g., "SOW references previously cleaned from body but Appendix A still has them").

## Verification

After the sub-agent returns:
- [ ] Check the target file was NOT modified (`ls -la` vs before)
- [ ] Read the audit report — verify it covers all sections
- [ ] Check that severity ratings make sense (Critical vs High vs Medium)
- [ ] Confirm the report was saved to a durable path (not /tmp if it should persist)
- [ ] Check for hallucinated references (claims about documents the sub-agent couldn't actually read)
