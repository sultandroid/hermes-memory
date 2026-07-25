# HTML Project Plan Audit — Structured QC Extraction

Extract and validate structured data from large self-contained HTML project plan documents (PEP, DMP, BEP, etc.) where sections are delimited by HTML comment markers and content includes embedded data tables, management dashboards, flow diagrams, and milestone tracks.

This is a reference for when the source is an HTML file (not PDF/Excel) containing a complete plan document with inline CSS, SVG icons, and section-by-section layout — common for BIM/project management plans authored as single-file HTML.

## Overview

HTML project plans (e.g. PEP Rev 01, DMP Rev C03) are composed of A4-sized `<section class="page">` blocks, each with:
- A header comment: `<!-- PAGE N :: §X TITLE -->`
- A pg-header with project/doc ref
- A section preamble (Purpose/Scope/Read With/Output grid)
- Content: data tables, flow diagrams, management dashboards, milestone tracks, org charts
- A pg-footer with document code and page number

## Discovery Workflow

### 1. Locate the file and scan for structure

Start by reading the top of the file to understand its format, then find `<h2>` tags for section headings and `<!-- PAGE` comments for page/section boundaries.

```bash
# Check file size and encoding
file /path/to/document.html
wc -l /path/to/document.html
```

### 2. Find section boundaries via HTML comments

The most reliable way to locate sections — `<!-- PAGE N :: §X ... -->` comments appear before each section block:

```
search_files(
    pattern=r"<!-- PAGE",
    path="/path/to/document.html",
    context=0
)
```

This returns all page markers with their line numbers. From this you can map every section number to its start line.

### 3. Read the Table of Contents

Most project plan HTML files have a machine-readable TOC near the top (in the 2000–2200 line range). Extract it to get:
- Section titles and their page ranges
- Sub-section references
- Cross-link notes

### 4. Extract each section by offset/limit

Read section preambles and content tables using the line numbers from the discovery step:

```python
read_file(
    path="/path/to/document.html",
    offset=START_LINE,  # from <!-- PAGE comment
    limit=N             # enough to cover the section
)
```

### 5. Cross-reference TOC against actual content

For each section, verify that:
- The section title in the TOC matches the `<h2>` in the content
- The page ranges in the TOC are correct
- All referenced sub-sections actually exist
- Cross-links (e.g. "see §X") resolve to real content

## Data Extraction Patterns

### Section Guide / Preamble Grid

Each section typically opens with:
```
<div class="sec-preamble">
  <div class="sec-preamble-head">N · Section Guide</div>
  <div class="sec-preamble-grid">
    <span class="tag">Purpose</span><span>...</span>
    <span class="tag">Scope</span><span>...</span>
    <span class="tag">Read With</span><span>...</span>
    <span class="tag">Output</span><span>...</span>
  </div>
</div>
```

Capture all four fields — they define what the section is meant to deliver.

### Data Tables

HTML tables use `<table class="eng-table">` with `<thead>` and `<tbody>`. Extract headers and rows by looking at `<th>` and `<td>` elements:

- **Gate tables**: Gate ID, Name, Entry Trigger, Exit/Output, Tier, Authority
- **LOD matrices**: LOD level, Stage, Verification Authority, Survey/Audit Method, Acceptance Gate
- **Ownership matrices**: Package, Custodian, Cross-check, IFC-Export Authority, Modeller Pool
- **Interface registers**: ID, Party A, Party B, Location, Risk, Closure Method
- **Meeting schedules**: Meeting name, Frequency, Purpose, Chair
- **Status tables**: Action/Rule pairs

### Management Dashboards

Each section usually has a `.mgmt-dashboard` div containing:
- `.md-card--owner` → Who owns this section
- `.md-card--risk` → Linked risk register reference + response time
- `.md-card--kpi` → KPI target value
- `.md-flow` → Trigger → Method → Cadence → Evidence → Escalation workflow

Extract the KPI target from the `.md-card--kpi .md-card-body b` element.

### Flow Diagrams

`.flow` divs contain sequential steps with:
- `.flow-node` → A step, with `.step-num` (number), `b` (role), `.desc` (activity)
- `.flow-arrow` → Separator between steps
- `.flow-node--terminal` → Final step

### Banner / Sub-section headers

Each sub-section is introduced by a `.banner` div with:
- `b` element → Sub-section title
- `.hint` span → Brief description

These define the sub-section hierarchy within each main section.

## Audit Finding Categories

When QC-auditing a PEP or similar document, report findings in these categories:

### 1. Present / Correct
Data exists, is correctly formatted, and internally consistent.

### 2. Present but Incomplete
Data exists but has gaps (e.g. "P?" in risk fields, "TBD" in KPI thresholds).

### 3. Referenced but Missing
The TOC or a cross-link references a section/table that does not exist in the HTML.

### 4. Inconsistent
Data exists but contradicts another part of the document (e.g. cover says "Rev 04" but page headers say "Rev 01"; gate timeline shows W52 but contract end stated as W43).

### 5. Not Present
A standard element that should exist has no definition (e.g. status codes A/B/C/D/E/F used throughout but no definition table; C1-C5 communication hierarchy expected but different format used).

## Search Patterns for Specific Data Points

| What to find | Search pattern | Notes |
|---|---|---|
| Section headings | `<h2>[0-9]+\. ` | All main section titles |
| Page/section boundaries | `<!-- PAGE` | Comment markers with line numbers |
| Key personnel roles | `Acting `, `Eng\. `, `Dr\. ` | Named individuals |
| Review/submittal codes | `Code [A-F]`, `Code A`, `Code B` | Used contextually — may not have definition table |
| Communication hierarchy | `C[1-5] `, `Communication` | May use ladder format instead |
| Stage gates | `G[0-8]`, `Stage Gate` | Gate ladder definitions |
| KPIs | `KPI`, `md-card--kpi` | Dashboard KPI target values |
| LOD levels | `LOD [0-9]+` | Level of Development matrix |
| Timelines / weeks | `W[0-9]+` | Week references in schedules |
| Revision status | `Rev `, `Revision` | Document revision codes |
| RFI workflow | `RFI`, `Request for Information` | May be in Aconex-native, not a separate procedure |

## Common Findings in PEP Audits

1. **Cover revision mismatch**: The document's cover/title may say a different revision than the file name or header page numbering.
2. **Status code definitions absent**: Codes A/B/C used throughout but no definition table found.
3. **Cx (numbered) hierarchy absent**: If the expected format is "C1, C2, C3..." but the document uses a different scheme (e.g. daily/weekly/monthly ladder), flag the difference.
4. **RFI workflow**: Often handled natively in the CDE platform (Aconex) rather than described as a standalone procedure.
5. **KPI values marked "P?" or "TBD"**: Many risk/KPI fields are placeholders awaiting the linked risk register.
6. **Gate timeline vs contract end**: The gate ladder may extend beyond the stated contract completion week.

## Example: PEP Rev 01 QC Audit

A worked example of this workflow is the session producing references for sections 5, 9, 18, 19, 20, 21 of the Aseer Museum PEP:
- 17,795-line HTML, 122 pages
- Located 42 page markers via `<!-- PAGE` search
- Extracted 9 gate definitions (G0–G8), 4 LOD levels, 10 interface registers, 7 meeting schedules
- Found: no status code definition table, no C1-C5 hierarchy, cover says Rev 01 not Rev 04
- Cross-referenced TOC against actual sections
