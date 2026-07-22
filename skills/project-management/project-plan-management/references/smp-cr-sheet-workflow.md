# SMP CR Sheet Workflow — CG Comment Response

## When to use

A sustainability consultant's SMP (or any plan) received Code C from CG and you need to produce a Comment Response Sheet for the consultant to action.

## Workflow

### 1. Audit CG comments against ER/SoW

For each CG comment, determine:
- Is this our contractual obligation? (ER/SoW reference)
- Cost impact? (none / minor / significant)
- Schedule impact? (none / days / weeks)
- Push back or comply?

### 2. Generate CR Register as Excel (not Markdown)

Use openpyxl with Samaya branding:
- Navy `#1F3864` header, white text, Calibri 10pt
- Alternating row shading (green/amber/red per obligation severity)
- Wrap text, thin borders, 100px row height for content rows
- Freeze panes on header row

**Columns (for Fida-facing version):**
- `#` — comment number
- `CG Comment` — verbatim CG text, never paraphrased
- `ER/SoW Reference` — exact section references using `Section` not `Sec` and never `§`
- `Our Obligation` — plain English assessment of responsibility
- `Schedule Impact` — time impact only (no cost column for consultant-facing sheets)
- `Action from Samaya` — what Samaya Technical Office does (coordinate NRS, direct NRS, confirm with procurement, etc.)
- `Action from Fida` — what the sustainability specialist does (add tables, subsections, criteria, references)
- `Response to CG` — proposed response text

**3 sheets:**
1. `CR Sheet` — full 8-column table with all 9 comments
2. `Content Changes for Fida` — detailed instructions with exact text to insert, location in SMP, and checkbox column
3. `Summary` — condensed view with action from Samaya, action from Fida, schedule impact, push-back flag

### 3. NRS framing

NRS is Samaya's sub-consultant. When writing obligations:
- "We direct NRS to incorporate criteria" not "NRS develops specs independently"
- "Samaya sends SMP to NRS for review" not "Fida coordinates with NRS"
- Samaya is the umbrella — NRS works under Samaya's direction

### 4. Rules enforced in every cell

- **No `§` symbol** — use `Section` or `Clause`. This is the #1 recurring error.
- **No AI symbols** — no `->`, `--` (em dash), `·` (middle dot), `•`, `✓`, `✗`
- **Verbatim quotes** — CG comments, ER text, SoW text copied exactly as written
- **Plain engineer English** — short sentences, active voice, no jargon
- **Cost column removed** for consultant-facing sheets — only schedule impact shown

### 5. File locations

- Repo: `03_Plans/12_SMP/SMP_CR_Sheet_Rev01.xlsx`
- OneDrive: `04_Docs/02_Plans_and_Procedures/02.12_Sustainability_Strategy/SMP_CR_Sheet_Rev01.xlsx`
- Source markdown: `03_Plans/12_SMP/cr_sheet_smp_rev01_2026-07-18.md`
- Content changes: `03_Plans/12_SMP/smp_rev01_content_changes_for_fida.md`
