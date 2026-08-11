# Large Document Extraction with kimi CLI (sub-agent pattern)

When a large PDF (10k+ lines of pdftotext output) needs to be read, understood, and converted to structured markdown, use **kimi CLI as a sub-agent** to parallelize extraction. The user explicitly prefers this ("you can use kimi CLi as agent to help you").

## When to use
- Large design/technical reports (e.g. Stage 4+ Visitor Experience report, 19,497 lines)
- Documents with repetitive per-section structure (galleries, disciplines, packages)
- Any extraction where reading the whole file into context would flood the window

## Workflow

1. **Extract text first** (terminal, not kimi):
   ```bash
   pdftotext -layout "/path/to/report.pdf" /tmp/report.txt
   wc -l /tmp/report.txt
   ```

2. **Verify kimi is available**:
   ```bash
   which kimi && kimi --version
   ```

3. **Dispatch kimi with a focused extraction prompt** (one gallery/discipline batch at a time):
   ```bash
   kimi -p "Read /tmp/report.txt (a 19,497-line pdftotext extraction of <doc>). Extract for EACH <section> the <field1>, <field2>, <field3>. Be faithful to the source - do not invent content. If a section's content is not clearly stated, note 'not specified'. Output as a clean structured list grouped by <grouping>. Return only the structured extraction, no preamble."
   ```

4. **Split into batches** if the document is large — one kimi call per group (e.g. galleries G1-G6, then G7-G14). Each call returns a focused chunk.

5. **Assemble the markdown yourself** from kimi's output — kimi returns raw structured text; you format it into the final `.md` with YAML frontmatter.

## Key prompt techniques
- **Name the exact file path** and line count so kimi knows the scale.
- **List the exact fields** you want per section (Visitor Experience, Key Messages, AV/interactives, Art Commission).
- **"Be faithful to the source — do not invent content"** prevents hallucination.
- **"If not clearly stated, note 'not specified'"** prevents kimi from fabricating missing data.
- **"Return only the structured extraction, no preamble"** keeps output clean.
- **Group by a natural dimension** (floor, discipline, package) so the output maps directly to the final markdown structure.

## Pitfalls
- kimi may take 1-5 min per batch on large files — run batches sequentially or in parallel background jobs.
- kimi's output is a self-report; verify key numbers/amounts against the source PDF before committing to registers (e.g. invoice amounts, NCR statuses).
- For two-column PDF layouts (body left, key messages right), kimi handles the column split well — trust its extraction but spot-check one section.
- Combine with a `delegate_task` sub-agent if you also need the file written to the repo — kimi returns text, you (or a sub-agent) write the file.

## Example (2026-08): Visitor Experience report
- Source: `MOC-ASE-AR-ARC-GEN-DDD-PR01-00` (Stage 4+, V1.0, Aug 2026), 19,497 lines
- kimi extracted all 14 galleries (G1-G14) across Ground/First/Lower Ground/Basement floors
- Output: `04_Docs/02_Plans_and_Procedures/02.1_DMP/02_CG_Responses/ZD-0108_Visitor_Experience_Report.md`
- The extraction fed directly into the AV content RFI (TQ-0028) coordination — the gallery AV/interactive summary table became the coordination anchor.
