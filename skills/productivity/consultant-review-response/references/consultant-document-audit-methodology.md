# Consultant Document Audit Methodology

## Principle: Audit, Don't Rewrite

When a consultant/subcontractor submits a document (SMP, plan, report) for review:
- **Do NOT rewrite their document.** Identify problems, give structured feedback, let them fix it.
- Only fix if the user explicitly says "fix it" or "make the changes."
- Default mode: audit → feedback list → send to author.

## Section-by-Section Audit

1. **Extract** — `pdftotext` for PDFs, `python-docx` for DOCX
2. **Map all sections** — find every section header with line numbers
3. **Check each section for:**
   - Empty sections (header with no content)
   - Duplicate sections (same header in TOC and body)
   - Wrong content type (bullets where table/diagram/template expected)
   - Missing content (template headers with no actual form fields)
   - Format issues (no page breaks, no headers/footers, forms spilling pages)
   - Contractual contradictions (targets not matching ER/SoW)
   - Overuse of "shall" (robotic passive voice)
4. **Categorize** — Critical (contractual wrong), Format (layout), Content (missing)
5. **Present as structured list** — grouped by section, each with clear "what to fix"

## CR Register Format
- Status column: **Open / Closed** — NOT Accept/Reject
- Columns: #, Section, Change, Reason/Contractual Basis, Status
- Each row = one change or issue. Author marks Open/Closed as they work.

## Common Issues to Flag

| Issue | What to Say |
|-------|-------------|
| Empty section header | "Section X has a header but no content" |
| Bullet list where template needed | "Section X is listed as bullets — where is the actual template?" |
| Not a proper risk assessment | "Section X lists aspects but has no likelihood/severity scoring or mitigation matrix" |
| Text-based chart | "Section X describes a chart in text — add an actual diagram" |
| Forms spill across pages | "All appendix forms must fit one page per form" |
| No page breaks | "Every main section must start on a new page" |
| Contractual target wrong | "Target X should be Y per ER/SoW clause Z" |
| "shall" overuse | "Section X uses 'shall' N times — rewrite in active voice" |
