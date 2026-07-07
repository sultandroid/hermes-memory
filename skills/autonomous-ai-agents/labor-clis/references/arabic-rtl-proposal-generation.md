# Arabic RTL Technical Proposal Generation

Pattern for generating large Arabic RTL technical proposal HTML documents via `delegate_task`. Proven on the RCRC Experience Exhibition tender (35 sections, 215 KB, 36 A4 pages).

## When to Use This Pattern

- The target is a complete, submission-grade document (not incremental edits)
- The document has 10+ sections with complex cross-references
- The language is Arabic (RTL) or bilingual
- CLI labors (Fugu, Codex, Kimi) are hitting rate limits, timeouts, or sandbox restrictions

## The Pattern

### Step 1: Build the HTML framework (cover + CSS) manually

Create a self-contained HTML file with:
- `dir="rtl"` on the `<html>` tag
- IBM Plex Sans Arabic font (Google Fonts) for Arabic body text
- Inter font for English/technical terms
- A4 print-ready CSS: `@page {size:A4 portrait;margin:0}`, `.page{width:210mm;min-height:297mm}`
- Cover page with navy background, client/contractor logos, project title
- Document Control block with reference and revision
- Section header styles: `.h2-row`, `.h2-bar`, `.banner`
- Table styles: `.eng-table` with navy header rows, alternating row colors
- Footer with doc ref + page number
- Strip components for metadata rows

### Step 2: Delegate content generation

```python
delegate_task(
    goal="Produce complete 35-section Arabic RTL proposal...\n\nREQUIRED STRUCTURE:\nالجزء صفر — المقدمات\n1. صفحة الغلاف\n...Full structure with ALL headings...",
    context="Source knowledge: gallery names, materials, company data, project details...\n\nDEFINITION OF DONE (all must be true):\n✓ A4 print-ready RTL Arabic HTML\n✓ Arabic primary, English only for technical terms\n✓ Zero prices/cost references\n✓ Clause-by-clause Compliance Matrix\n✓ Project Appreciation naming real galleries/systems/materials\n✓ Shop-drawing / IFC workflow with Code A/B/C loop\n✓ Specialist procurement strategy for long-lead imports\n✓ Populated document control block + working ToC",
    toolsets=["terminal", "file"]
)
```

### Key Success Factors

1. **Specify the EXACT structure** in the `goal` — every section heading in Arabic, every subsection, every appendix. The subagent follows this like a template.

2. **Include ALL source knowledge** in `context` — gallery names (G1-G7), materials (Riyadh yellow stone, Barrisol, Leben, Muxwave, etc.), company data (factory size, production lines, certifications, project references). Do NOT expect the subagent to read OneDrive files.

3. **State the Definition of Done explicitly** — this gives the subagent a self-check list. It will verify each item before returning.

4. **Set toolsets=["terminal","file"]** — the subagent needs file access to write the HTML but doesn't need web search or browser.

5. **Expect 5-10 minutes for 200K+ documents** — delegate_task is synchronous. A 35-section 215KB document with 50-item compliance matrix takes ~10 minutes, 22 tool calls, ~1.7M input tokens, ~75K output tokens.

6. **Verify after delivery** — check line count, file size, verify key sections are present (grep for specific Arabic terms), check the Definition of Done criteria are met.

### Common Issues

- **Lagged file copy**: After delegate_task completes, copy the output file to the OneDrive project folder via write_file or osascript Finder copy. The subagent saves to /tmp.
- **Company stat corrections**: Verify factory area, company age, number of projects against the latest Samaya company profile (v6+ has different numbers from v4). The subagent uses whatever numbers you provide in context — if they're wrong, the output will be wrong.
- **Section numbering**: The subagent follows the structure literally. If a comma or bracket is missing in the goal, the section header will be malformed.
