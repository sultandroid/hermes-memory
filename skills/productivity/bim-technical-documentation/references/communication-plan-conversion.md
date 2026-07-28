# Communication Plan PDF → Structured Markdown

## Document Profile

| Field | Value |
|-------|-------|
| Source File | Communication Plan Rev 02.pdf |
| Document Reference | MOC-MUS-ASE-1K0-PL-0018 |
| Pages | 4 (landscape: 960×540 pts) |
| Plan Revision | Rev.02 |
| Matrix Revision | Rev.01 |
| Prepared | PMC (ACE) |
| Updated | 18 Jan 2026 (matrix) / 19 Jan 2026 (contacts) |
| Approval Code | B (Approved with Comments) |
| Target Directory | `00_Contracts/02_Communication_Plan/` |

## Page Map

| Page | Content | Part File |
|------|---------|-----------|
| 1 | Communication Plan Chart — org structure | `01_Part1_Communication_Chart.md` |
| 2 | Communication Matrix (20 items + sub-items) | `02_Part2_Communication_Matrix.md` |
| 3 | Important Communication Rules (13 rules) | `03_Part3_Communication_Rules.md` |
| 4 | Contact Lists (4 parties: MOC, ACE, CG, SAMAYA) | `04_Part4_Contact_Lists.md` |

## Extraction Strategy

### Step 1 — Size assessment
```bash
pdfinfo "source.pdf"
# → Pages: 4, Page size: 960 x 540 pts (landscape)
pdftotext "source.pdf" /tmp/comm_raw.txt       # raw text, ~942 lines
pdftotext -layout "source.pdf" /tmp/comm_layout.txt  # spatial layout, ~177 lines
```

### Step 2 — Read layout first, raw second
The `-layout` output preserves column alignment and is more readable. The raw output catches text the layout pass may have lost. Always read both:

```bash
# Layout gives the table structure
read_file(path="/tmp/comm_layout.txt")
# Raw gives any orphaned text fragments
read_file(path="/tmp/comm_raw.txt")
```

### Step 3 — Map the 4-page structure
Landscape PDFs with landscape tables extract differently from portrait. The form feed (`\f`) character marks page boundaries in pdftotext output.

## Table Reconstruction — Communication Matrix

### Layout in source PDF

The Communication Matrix is a wide landscape table with these columns:

| Item | Abb. | From | To | Action (Review / Reply / Approval) | Info | cc | Frequency | Time of Reply (Days) | Notes |

The Action column is actually 3 sub-columns (Review, Reply, Approval) under the "Correspondence Purpose" header, and Info is a separate column with a checkmark indicator.

### How pdftotext -layout represents it

The `-layout` output preserves spatial alignment as tab/pipe-delimited-ish lines:

```
1   Request For Information    RFI    Contr    CG              √              ACE & MOC    N/A    7
```

The `-layout` output is NOT rigorously delimited — columns are separated by varying whitespace. Reconstruct by:

1. Identify column positions from the header line (first ~3 lines of the layout output)
2. Check which value appears in which position for each row
3. For missing/wrapped values, cross-reference with the raw text output

### Sub-items

Items 6.1, 10.1, 10.2 are sub-rows of items 6, 10. Preserve the numbering (6.1, 10.1, 10.2) as separate rows in the table with a note in the Notes column.

### Checkmark reconstruction

The raw text uses `√` characters in scattered positions. Map them to the correct column:
- When a `√` appears under the "Reply" column of the action header → `✓ (Reply)`
- When under "Approval" → `✓ (Approval)`  
- When under "Review" → `✓ (Review)`
- When under "Info" column → checked in Info column

The layout text output helps here because `-layout` preserves horizontal position, so you can see which header the `√` aligns with.

### Column abbreviations

Use abbreviated headers for a dense pipe table:
```
| # | Item | Abb. | From | To | Action | Info | cc | Frequency | Reply (Days) | Notes |
```

For the Action column, collapse the 3 sub-columns into a single text cell like `✓ (Reply) | ✓ (Approval)`.

### Key insight — max column count

The raw pdftotext output had values from ACE & MOC, N/A, and a number (7, 1, 2) appearing as separate rows between the main table data. These correspond to the `cc`, `Frequency`, and `Time of Reply` columns. The layout output correctly grouped them inline.

## Contact List Tables

### Structure

Contact lists appear on a single page (page 4) as 4 separate tables:
- MOC (Client) — 1 person
- PMC Team (ACE) — up to 9 people
- Supervision Consultant (CG) — 8 people
- Samaya Team (Main Contractor) — up to 9 people

Each table has columns: Sn, Name, Designation, Mobile Number, Company, Email, Joining Status

### Extraction from layout text

The layout text preserves the column alignment:

```
Sn                  Name                    Designation                Mobile Number                  Company               Email               Joining Status
1    Eng.Mohamed Farouk                   Projects Director             541094254                      ACE      mohamed.elmahlawy@ace-mb.com        Done
```

For entries with `—` (placeholder like `ــــــ` ), use `—` in the markdown table to indicate unfilled data.

### Markdown rendering

Use a separate markdown section and table for each party (`## 4.1 MOC`, `## 4.2 ACE`, `## 4.3 CG`, `## 4.4 Samaya`).

## Communication Rules (Page 3)

These are plain numbered paragraphs, trivially extractable. Present each rule as `### Rule N` with the full text verbatim.

## YAML Frontmatter Pattern

Every part file uses this frontmatter:

```yaml
---
title: "Communication Plan — Part N: Description"
doc_ref: MOC-MUS-ASE-1K0-PL-0018
revision: Rev.02
part: N
status: formal_read_only
approved_date: YYYY-MM-DD
approved_by: CG (Consultant Group)
approval_code: B (Approved with Comments)
agent_edit: prohibited
source: "OneDrive — 02.7_Communication_Plan/01_Source_Files/Communication Plan Rev 02.pdf"
---
```

The index file adds: revision history table, approval history table, TOC with links, and related documents section.

## Pitfalls

1. **Landscape PDF vs portrait** — `pdftotext -layout` on landscape PDFs produces much wider lines. The table columns may shift depending on font widths. Compare raw and layout outputs for every row.
2. **Sub-items with shared numbering** — Items 6.1 (Material submittal) is a sub-item of 6 (Material Inspection Request), but they have different abbreviations (MIR vs MS) and different from/to parties. Treat as separate rows with the sub-number preserved.
3. **ACE & MOC appearing in cc column** — This appears as a fixed prefix for many items. In the raw text, it looks like a separate row. Cross-reference with layout to confirm it's the `cc` column value.
4. **No Action column for some items** — Items like "Daily Site Report" and "Weekly Report" have no "Action" checkmark but DO have "Info" checkmarks. Ensure the difference is preserved.
5. **Contact list page header artifacts** — The layout text of page 4 can have artifacts like `ntact List+1+17:335:33` from overlapping PDF rendering. These are OCR artifacts — skip them.
6. **Check AGENTS.md for read-only constraints** — If the target directory is `00_Contracts/`, AGENTS.md Rule 9 may prohibit agent writes. The user's explicit instruction overrides this, but the constraint should be noted in the completion summary.
7. **Follow existing sibling-directory conventions** — Before creating files, inspect an existing `00_Contracts/<N>/` directory for naming conventions. Existing patterns (e.g., `01_Part1_*.md`, `00_INDEX.md`) should be followed for consistency.
