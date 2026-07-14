---
name: risk-register-management
description: Maintain the project risk register (Excel + MD) and keep the Risk Management Plan (RMP) aligned. Covers risk data extraction from repo, Excel rebuild with openpyxl, MD patching, and cross-document verification.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [risk, register, rmp, alignment, excel, openpyxl, project-management]
    related_skills: [project-register-manager, aseer-document-control]
---

# Risk Register Management

## When to Use

- User asks to "update the risk register" or "update the RMP"
- User asks to "align" or "synchronize" risk data across documents
- Any task involving the project risk register (Excel or MD), the RMP markdown or DOCX, the DRR Excel, or their cross-document consistency
- Adding, updating, or closing risks in the live register
- Updating the RMP DOCX for formal CG submittal

## System Architecture

The Aseer Museum Risk Management System (RMS) has four synchronized documents:

| Document | Format | Location | Role |
|----------|--------|----------|------|
| Risk Register (live) | Markdown | `01_Registers/risk_register.md` | Agent + dashboard source of truth |
| Risk Register (formal) | Excel (OneDrive) | `04_Docs/09_Registers/23_Project_Risk_Register/` | External submission package |
| Risk Management Plan (MD) | Markdown | `03_Plans/08_Risk/risk_management_plan.md` | Methodology, scale, RBS, governance |
| Risk Management Plan (DOCX) | Word (OneDrive) | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/03_Word/` | Formal CG submittal version |
| Design Risk Register (DRR, live) | Markdown | `01_Registers/design_discipline_risk_register.md` | Design-phase child risks, agent source of truth, 20+ disciplines, Stage 3 Audit overlay |
| Design Risk Register (DRR, formal) | Excel (OneDrive) | `04_Docs/09_Registers/06_Design_Risk_Register/` | Design-phase risks (linked from DMP), PxI 1-5 scoring, Cover sheet + data + RBS tabs |
| HSE Risk Register | Excel (OneDrive) | Internal | Task-level HSE risks |
| AV Risk Register | Excel (OneDrive) | Internal | AV/multimedia risks |

**Rule:** The MD register is the operational truth. The Excel is a derived output. The RMP MD is the internal methodology doc. The RMP DOCX is the formal CG submittal and must match the MD exactly in all data points.

## DOCX Writing Style Principles

When writing or editing any DOCX that goes to CG/PMC/MoC (including the RMP), follow these rules:

### No Client-Irrelevant Methodology

The client does not care about PMBOK, PRINCE2, or other textbook methodology references. Never include:
- "PMBOK 6th Edition Chapter 11" or similar methodology citations
- Generic methodology frameworks that add no project-specific information
- "This establishes the systematic framework for..." type opening filler

The client wants: what risks exist, how they are scored, who owns them, what will be done. Not which textbook inspired the approach.

### No AI Symbols

Replace all typographic symbols with plain ASCII:
- Em dash (—) and en dash (–) -> hyphen (-)
- Section symbol (§) -> "Section" or just section number
- Middle dot (·) -> bullet or hyphen
- Curly quotes -> straight quotes

### Write Like an Engineer, Not Like AI

Bad (verbose AI tone):
"This Risk Management Plan defines the systematic framework for identifying, analysing, responding to, monitoring, and controlling risks throughout the project lifecycle. It establishes the methodology, tools, governance, and accountabilities for proactive risk management."

Good (direct human tone):
"This Risk Management Plan defines how risks are identified, assessed, and managed on the project."

Principles:
- Cut filler words: "systematic framework", "robust", "proactive", "comprehensive", "streamline", "leverage", "facilitate"
- One sentence per idea. Two max.
- Use active voice ("The PM reviews risks weekly" not "Risks are reviewed weekly by the PM")
- Start sections with the point, not a throat-clearing intro
- Every claim must trace to an approved project source (ER/SoW/CG comment/submittal) - never cite external standards

### Language Checklist Before Delivery

- [ ] No PMBOK or external methodology citations
- [ ] No em dashes or en dashes (use hyphens)
- [ ] No section symbols (§)
- [ ] No middle dots (·)
- [ ] No AI buzzwords: systematic, framework(alone), robust, leverage, facilitate, proactive(as filler), streamline
- [ ] Each body paragraph is 1-2 sentences max
- [ ] Active voice throughout
- [ ] Every data point cross-checked against repo or DRR Excel
- [ ] Names and roles from repo only, never inferred

### Step 1: Extract Current State

Read all sources to understand the gap:

```python
# MD register — risk count, scoring scale, risk IDs
# RMP MD — methodology with the current number
# RMP DOCX — formal CG submittal (Word file via python-docx)
# DRR Excel — design risk register (if referenced in RMP scope)
# HSE/AV registers — if referenced
```

Key checks:
- **Risk count** — all sources must agree on total for each register
- **DRR count** — RMP says "37" but actual DRR Excel may have 76. Always check the actual DRR file
- **Scoring scale** — Master register uses PxS 1-4. DRR uses PxI 1-5. HSE uses CxL 1-5. Document each separately
- **Status counts** — Open/Watch/Mitigated/Closed and Critical/High/Medium/Low
- **RBS categories** — RMP section must match register RBS table (17 categories for repo C01)
- **Appendix C references** — any PRR-ID referenced in RMP must exist in register
- **Version/revision** — all documents should reflect same alignment date
- **PxI thresholds** — DRR uses Critical >=15, High 10-14, Medium 5-9, Low <=4. Verify against the summary table

### Step 2: Update RMP MD (Markdown)

The RMP MD has these sections that may need updating after a register change:

| Section | What to update |
|---------|---------------|
| Frontmatter | `last_updated`, `revision` |
| §1.2 Scope | All four register counts (PRR, DRR, HSE, AV) |
| §2.0 Risk Snapshot | Total + severity counts table |
| §4.2 Current Risk Distribution | Full category table (17 rows) |
| §9.1 Register Architecture | All register counts |
| §9.2 Risk ID Convention | Examples (must reference real IDs) |
| Appendix C | Live PRR-IDs referenced |
| Document Control | Add new version row |

Use `patch()` for each section with unique context lines to ensure correct matching.

### Step 2a: Add New Risks from External Intel (User Input / Supplier Data / Project Update)

When the user provides new risk intel (supplier datasheet, new object list, fabrication insight, site observation), do NOT add directly to any single register. Follow this cross-check flow:

1. **Cross-check existing PRR + DDR first** — search both registers for related risks. The intel may upgrade an existing risk (score change, new evidence) rather than create a new one.

2. **Determine where the risk belongs:**
   - Design-phase risk (material selection, coordination, authority interface, gallery layout) → **DDR** first
   - Executive/portfolio-level risk (schedule, commercial, procurement, stakeholder) → **PRR** first
   - Both — if the risk has a design root cause AND executive consequence, add to BOTH and cross-link them

3. **DDR entries** use 1-5 scoring (PxI): Critical ≥20, High 12-19, Medium 8-11, Low 4-7, Very Low 1-3. Risk IDs follow `DDR-CAT-NNN` (e.g. DDR-MAT-001). Owners use DSN-X codes from the Excel Cover sheet.

4. **PRR entries** use 1-4 scoring (PxS): Critical ≥12, High 8-11, Medium 4-7, Low ≤3. Risk IDs follow `PRR-CAT-NN` (e.g. PRR-PRC-05).

5. **Link DDR ↔ PRR** — each DDR row has a "Linked Risks" column referencing PRR IDs. Each PRR row should reference the relevant DDR ID in its evidence column. This enables traceability from design risk → executive impact.

6. **Sync to DDR Excel** after updating the repo markdown — the Excel is the formal record. Update Cover sheet revision (label in column B, value in column C) and the title row on the Design Risk Register sheet.

7. **Update all counts** — snapshot table, RBS counts, dashboard cross-references, version control table.

### Step 2b: Audit External/PM Register Against Live Register

When the PM or a stakeholder sends an Excel risk register that should be aligned with the live repo register, do NOT assume they are in sync. Auditing an external register requires systematic cross-comparison across multiple dimensions.

### Audit Checklist

| Check | What to Look For | How to Resolve |
|-------|-----------------|----------------|
| **Date reference** | What status report / MoM is the register aligned to? If 5+ weeks stale, all status fields are suspect | Note the basis date; treat all LIVE/Materialising flags as unconfirmed |
| **Scoring formula** | Open the Excel — are Risk Score / Rating columns populated with values, or are they empty because P and S stored as text labels? | Flag as broken; convert P/S to numeric or report to PM |
| **Dashboard counts** | Are the Critical/High/Medium/Low counts actually computed, or are they all empty? | Same cause as broken scoring; fix and recalculate |
| **Risk ID overlap** | Do PRR-XXX-XX IDs in the Excel mean the same thing as same IDs in the repo? | Read the risk event descriptions side by side — same ID may describe a different risk (e.g. Excel PRR-COM-01 = "scope changes" but repo PRR-COM-01 = "EOT dispute") |
| **Missing risks** | What risks exist in the repo but not in the Excel? What risks exist in the Excel but not the repo? | Create a cross-reference table. Repo-missing good risks may need importing; Excel-missing Critical risks are gaps the PM needs to know about |
| **Target close dates** | Does the Excel have target close dates for each risk? If all blank, it lacks accountability tracking | Flag as gap; repo has target dates for all risks |
| **Status freshness** | "Open - Materialising (Rpt 16)" is stale if Rpt 16 is 5 weeks old | Update status or generalise the convention (use "LIVE" without report number) |
| **Evidence column** | Does each risk cite source documents (CG codes, NCR refs, MoM references)? | If not, the register is opinion-based rather than evidence-based |
| **Residual scoring** | Are post-mitigation residual P&S scored? If not, no way to tell if mitigations are working | Flag as gap |
| **Watchlist cross-check** | Compare Excel's Executive Watchlist against current project status from repo (project_status.md, look_ahead.md, NCRs, MoM) | Mark each watchlist item as ✅ Still live / ⚠️ Partial / 🔴 Escalated / 🟡 Downgraded |

### Output Format

Produce a structured audit report with these sections:

```markdown
// Section A: Scoring — BROKEN/WORKING
// Section B: Critical Gap — X risks MISSING from PM's Excel
// Section C: Y Risks in Both — Status Discrepancies (side-by-side table)
// Section D: Dashboard LIVE Watchlist — Reality Check
// Section E: Structural Issues in the Excel
// Section F: Summary — What the PM's Register Gets Right vs Wrong
// Section G: Recommended Actions (numbered, with owners and due dates)
```

### Common Structural Issues Found in External Registers

| Issue | Example from Aseer | Fix |
|-------|-------------------|-----|
| **ID collision** — same ID, different risk | Excel PRR-COM-01 = "scope changes"; repo PRR-COM-01 = "EOT dispute" | ID migration: re-ID one set, or split into separate COM-01/COM-05 |
| **Dashboard empty** — counts not computed | All Dashboard cells for Critical/High/Medium/Low counts are None | Fix scoring formula first, then counts auto-fill |
| **Score column blank** — P×S not derived | All 33 Excel risks show Risk Score = None | P and S stored as text "High"/"Medium" instead of numbers 1-4. Convert to numeric |
| **Status tied to stale report** | "Open - Materialising (Rpt 16)" — Rpt 16 is 5 weeks old | Generalise convention; drop the report number suffix |
| **No target close dates** | All 33 risks have Target Close = blank | Import dates from repo or set during next review |
| **Owner naming inconsistent** | "Project Director / Commercial Manager" vs repo's specific "Technical Office Mgr", "Procurement Lead" | Align to repo role titles |
| **Risk merged when repo splits** | Excel PRR-FLS-01 = one fire risk; repo splits into FLS-01 (IFC-0004) + FLS-02 (Fire Pump decision) | Accept split: the two risks have different causes, owners, and response actions |

### Importing Good Risks from External Register

When an external register has risks the repo doesn't:
1. Evaluate each — is it a genuine EPD (early proactive detection) or noise?
2. Score it per RMP scale (P×S 1-4 for PRR)
3. Assign a new PRR-CAT-NN ID (check for existing unused IDs in the correct category range)
4. Write to the live register
5. Update the RMP risk counts and RBS distribution
6. Log in the weekly review
7. Tag as "Pending import" in the register cross-reference until PM confirms

## Step 3: Update RMP DOCX (Word)

The DOCX is the formal CG submittal version. It must match the RMP MD exactly.

**Approach: content-based matching, not hardcoded indices**

Finding paragraphs by index is fragile because the DOCX has blank paragraphs that shift indices. Always find paragraphs by their text content:

```python
def find_para(doc, contains, start=0):
    for i in range(start, len(doc.paragraphs)):
        if contains in doc.paragraphs[i].text:
            return i
    return -1

i = find_para(doc, 'systematic framework')
if i >= 0:
    for r in doc.paragraphs[i].runs:
        r.text = ''
    if doc.paragraphs[i].runs:
        doc.paragraphs[i].runs[0].text = 'New text'
```

**Table manipulation with rebuild_table()**

Tables in python-docx retain their original `w:tblGrid` column definitions even after rows are cleared. When rebuilding a table with fewer columns than the original, the extra grid columns remain and cause misalignment. The `rebuild_table()` pattern handles this:

```python
def rebuild_table(table, headers, data, col_widths=None):
    # Update header
    for ci, h in enumerate(headers):
        if ci < len(table.rows[0].cells):
            cell = table.rows[0].cells[ci]
            for p in cell.paragraphs:
                for r in p.runs:
                    r.text = ''
                if p.runs:
                    p.runs[0].text = str(h)
    # Remove old rows
    for row in list(table.rows)[1:]:
        row._tr.getparent().remove(row._tr)
    # Add new data rows
    from docx.oxml import parse_xml
    for row_vals in data:
        row_elem = parse_xml('<w:tr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:trPr/></w:tr>')
        for ci, val in enumerate(row_vals):
            tc = parse_xml('<w:tc xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:tcPr><w:tcW w:w="2000" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>placeholder</w:t></w:r></w:p></w:tc>')
            t = tc.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
            if t is not None:
                t.text = str(val)
            row_elem.append(tc)
        table._tbl.append(row_elem)
        # Add cantSplit
        cs = parse_xml('<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="true"/>')
        trPr = row_elem.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}trPr')
        if trPr is not None:
            trPr.append(cs)
```

**DOCX-specific pitfalls:**

- **Save fails silently if Word has the file open.** Close Word before saving. Use `osascript -e 'tell application "Microsoft Word" to quit'` to close it.
- **After removing paragraphs, subsequent hardcoded indices are wrong.** Always use content-based finding, not paragraph indices.
- **Deleting paragraphs via `p._element.getparent().remove(p._element)` shifts all subsequent indices** in the `doc.paragraphs` array. Only do this as the last operation, or use content-matching.
- **Rebuilt tables with fewer columns than original need the `w:tblGrid` trimmed.** Remove excess `<w:gridCol>` elements from `<w:tblGrid>` to prevent extra empty columns in the output.
- **Text in runs may be split across multiple runs** (e.g. "0010003521" in one run and "Design & Build" in another). Setting `r.text = ''` on all runs then setting the first run's text is the safest approach.

### Step 4: Cross-Check DRR Excel

The Design Risk Register (DRR) at `04_Docs/09_Registers/06_Design_Risk_Register/Aseer_Museum_Design_Risk_Register.xlsx` is linked from the RMP scope section. When updating the RMP:

- Open the DRR Excel and count actual risks (not the RMP's stated count)
- The DRR uses P(1-4) x I(1-5) scoring with Critical >=15, High 10-14, Medium 5-9, Low <=4
- These thresholds must be documented on the DRR Cover sheet (add a legend if missing)
- Owner codes (DSN-A, CTR PM, etc.) must be defined somewhere in the DRR file
- The DRR uses risk ID format CAT-LETTER-NNN (e.g. DB-A-001), not PRR-XXX-XX
- RMP says "uniform scoring across all registers" but DRR has its own scale. Update the RMP to acknowledge different scales per register type

### Step 5: Fix Register MD Header Table (if needed)

The register's **Risk Breakdown Structure** table at the top must match the actual risk data below. Common issues:
- RBS count doesn't match actual category count (e.g. SCH shows 4 but only 3 exist)
- Missing categories (e.g. SIT not listed)
- Update with `patch()` like:
  ```
  | SCH | Schedule / Programme | 3 |
  ```
  Add any missing row:
  ```
  | SIT | Site & Existing Conditions | 1 |
  ```

### Step 5: Verify Alignment

Check these specific data points across ALL documents:

```python
# READ the actual register first — these values are examples only
alignment_checks = [
    ("Total risks", "<read from register>"),
    ("Open risks", "<read from register>"),
    ("Critical risks", "<read from register>"),
    ("High risks", "<read from register>"),
    ("Medium risks", "<read from register>"),
    ("Low risks", "<read from register>"),
    ("PRR scoring scale", "1-4"),
    ("DDR scoring scale", "1-5"),
    ("PRR Excel row count", "<read from xlsx>"),
    ("DDR Excel row count", "<read from xlsx>"),
    ("RMP section counts", "<verify each>"),
    ("RBS per-category counts", "<verify each>"),
]
```

**Also verify ancillary files:**
- `03_Plans/08_Risk/README.md` — governance line revision, current snapshot (risk count, treatment coverage)
- `00_Command_Center/master_dashboard.md` — Risk Management lane revision tag
- `reviews/<latest>.md` — documents the changes that triggered this revision
- `01_Registers/risk_register.md` cross-reference table — does it mention any pending imports from external audits?

**Cross-document consistency check (from this session):**
| Document | RMP (§1.2) | RMP (§2) | RMP (§4.2) | RMP (§9.1) | Register | README | master_dashboard |
|----------|-----------|---------|-----------|-----------|----------|--------|-----------------|
| Total risks | 29 | — | 29 | 29 | 29 | 29 | — |
| Critical | — | — | 10 | — | 10 | — | — |
| DRR count | 79 | — | — | 79 | — | 79 | — |
| RMP revision | C03 | — | — | — | C03 ref | C03 | C03 |
| Treatment files | — | — | — | — | — | 10/10 ✅ | — |
```

### Step 6: Bump Revisions

| Document | Pattern |
|----------|---------|
| DDR Excel Cover sheet | Label "Revision" in col B, value `Rev P0X` in col C. Also update the title row text (row 1) on the Design Risk Register sheet. |
| DDR Excel Issue Date | Label "Issue Date" in col B, value `YYYY-MM-DD` in col C. |
| PRR register MD | `revision: C0X` in frontmatter + `|| **C0X** | YYYY-MM-DD | Agent | Description |` in Register control table |
| DDR markdown | `revision: D0X` in frontmatter (D = Design risk register, distinct from PRR's C-series) |
| RMP MD | `revision: C0X` in frontmatter |
| RMP Document Control | Append row |
| `master_dashboard.md` | Update Risk Management lane description to include new revision (e.g. "RMP C03 (14-Jul)") |
| `03_Plans/08_Risk/README.md` | Update governance line, current snapshot (risk count, treatment coverage, revision) |
| `reviews/` | Create new weekly review file documenting what changed and why |

**Always update ALL ancillary files** when bumping the RMP or register — the README and master_dashboard are the entry points that other agents and the PM use to find the current revision state.

### Verification Command

### MergedCell write error
Unmerge ALL cells before any structural writes. `ws.unmerge_cells(str(mc))` for each merged range. Re-merge section headers after data is written.

### Risk ID number-shift hazard when inserting rows

Inserting a new risk in the MIDDLE of a sequential table (e.g. PRR #13 between #12 and #14) shifts ALL subsequent row numbers by +1. The PRR markdown uses sequential numbering `| 13 |`, `| 14 |`, etc. — these are NOT auto-incrementing in Markdown.

**Workflow:**
1. Note the exact last-number-before-insertion and first-number-after-insertion
2. After inserting the new row, fix all downstream numbers: `old_N + 1` for every subsequent row
3. Use targeted `patch()` calls per line, or use `sed -i '' 's/^| 14 |/| 15 |/'` if all downstream lines have the same leading pipe format
4. Verify the full table is sequential after fixing — no gaps, no duplicates (e.g. two rows both showing `| 14 |`)
5. Update the **RBS count** for the affected category (e.g. DES 4→5)
6. Update the **Risk Snapshot** header (total, critical, high, medium counts)
7. Update the **Dashboard cross-reference** if the new risk introduces a new theme

**Pitfall: cascading renumbering errors.** If you fix only the immediate next row but miss rows further down, the table has duplicate numbers (two #14s) plus a gap at the end. Always scan the full table after fixing.

### Extra pipe prefix (`|||`) in markdown tables

When using `patch()` to fix markdown tables, the tool sometimes adds an extra `|` at the start of each line, turning `|| 14 |` into `||| 14 |`. This can happen when patches are applied to lines that already had formatting adjustments.

**Fix:** After all patches are done, verify and clean:
```bash
# Check for triple-pipe artifacts
rg '^\\|\\|\\|' path/to/register.md
# Fix them
sed -i '' 's/^||| /|| /' path/to/register.md
sed -i '' 's/^||/|/' path/to/register.md  # if needed for specific table sections
```
Check each table section individually — some tables use single-pipe starts (`| col |`), others use double-pipe (`|| col |`). A blanket fix may break correct formatting.

### Risk ID collision between registers

The **same PRR-XXX-XX ID** in the PM's Excel and the repo's risk_register.md may describe **different risks**. This is not a typo — it happens when both registers evolve independently and reuse the same ID for different risk events.

**Example:**
| Source | PRR-COM-01 Description | PRR-COM-02 Description |
|--------|----------------------|----------------------|
| PM's Excel (Rpt 16) | "Scope changes post-award" | "SAR 0 certified — cash flow" |
| Repo C05 (14-Jul) | "EOT Claim 01 rejected — dispute" | "Milestone certification lag" |

**Fix:** Before merging registers, read risk event descriptions side by side. Flag all collisions to the PM. Options:
- Re-ID one set (e.g. repo COM-01 → COM-05 if Excel has a legitimate different use of COM-01)
- Keep both under different IDs and clearly document which is which
- Merge into one risk with comprehensive description if they're actually the same event

### External Excel has broken scoring formula

PM-provided Excel registers often store Probability and Severity as text labels ("High", "Medium") instead of numeric values (3, 2). This causes the Risk Score (P×S) and Risk Rating columns to be empty for all rows, even though the formula is present.

**Detection:** Open the Excel and check if the Risk Score column has values for at least one row. If all rows show blank or None, the formula can't multiply text.

**Fix path:**
1. Convert P and S columns from text to lookup values using openpyxl or Excel formulas
2. Or rebuild the register from the repo's numeric data
3. After fixing P/S, the Dashboard counts auto-populate

### External Excel lacks target close dates

Repo registers have target close dates for every risk. PM-provided Exports often omit this column entirely or leave it blank. Flag as a governance gap — without target dates, risk owners have no deadline for resolution.

### Status tied to a stale status report number

The Excel convention "Open - Materialising (Rpt 16)" ties the risk status to a specific report. When Rpt 16 is 5 weeks old, the status label is misleading. Generalise to "Open - Materialising" or "Open - LIVE" without the report number suffix, and track the evidence date separately.

### Dashboard counts null when scoring formula is broken

The Dashboard sheet's Critical/High/Medium/Low counts are typically derived from the Master sheet's Risk Score column. If scoring is broken (P/S stored as text), the Dashboard counts will all be 0 or blank — not because no risks exist, but because the formula can't compute them.

### Watchlist items may have escalated or split since the Excel was created

The Executive Watchlist on the Dashboard should be validated against current repo data. Common findings:
- A single watchlist item in the Excel may have split into multiple separate Critical risks in the repo (e.g. "Fire risk" → PRR-FLS-01 IFC-0004 + PRR-FLS-02 Fire Pump)
- Watchlist items may have escalated from High to Critical since the Excel was frozen
- Some watchlist items may have been downgraded or resolved

### Onedrive Excel write safety
If the Excel file is open in Excel when openpyxl tries to save, the write may silently corrupt the file. Ask the user to close the file first, or use a temp copy and replace after confirming.

### Scoring scale mismatch
The old Excel used PxI 1-5. The RMP C01 uses PxS 1-4 for the Master register. The DRR uses P(1-4) x I(1-5). The HSE register uses CxL 1-5. Each register has its own scale documented in the RMP. Never assume all registers share the same scale.

### Risk ID format consistency
Old format: `PRR-001` (sequential). New format: `PRR-CAT-NN` (category-coded). DRR uses `CAT-LETTER-NNN` (e.g. DB-A-001). Never mix formats. The RMP must document which format each register uses.

### DOCX save fails if Word has the file open
python-docx silently fails to save when Word holds a lock. Before any DOCX write, close Word: `osascript -e 'tell application "Microsoft Word" to quit'`

### Paragraph index shifts after removals
Deleting paragraphs via `p._element.getparent().remove(p._element)` shifts all subsequent indices. Never rely on hardcoded paragraph indices after removals. Use content-based matching instead.

### Table rebuild leaves old grid columns
When rebuilding a table with `rebuild_table()`, if the new data has fewer columns than the original table's `w:tblGrid` defines, the extra grid columns remain and cause misalignment. Trim `<w:gridCol>` elements from `<w:tblGrid>` to match.

### Text split across multiple runs in DOCX
In OOXML, text like "0010003521 -- Design & Build" may be split across separate `<w:r>` elements. Always iterate ALL runs in a paragraph's runs list and clear each, then set only the first run's text. Never assume a paragraph's text is in a single run.

### DDR Excel Cover sheet column layout

The DRR Excel "Cover" sheet uses a non-standard layout:
- **Column B** holds labels (e.g. "Revision", "Issue Date", "Document No.")
- **Column C** holds values (e.g. "Rev P04", "2026-07-14")
- **Column A** is empty/merged from the title graphic

This means `ws.cell(row=row, column=2).value` searches labels, and `column=3` updates values. The typical A/B label-value assumption will silently find nothing.

Additionally, the Design Risk Register sheet (the data sheet) has the revision in **row 1, column 1** as part of the title text. Update both locations when bumping revision.

### DRR count in RMP is often stale
The RMP (repo) says DRR has 37 risks. The actual DRR Excel (P03) has 76 risks. Always open the DRR Excel directly and count, rather than trusting the RMP's stated number.

## Samaya Style — Excel Risk Register Formatting

When creating or updating an Excel risk register (DRR or PRR), apply these formatting rules to match Samaya Technical Office document standards:

### Header Row (row 3 in DRR Excel)
- Fill: navy `#0F172A` (Samaya primary)
- Font: Inter 8pt, white (`#FFFFFF`), bold
- Center aligned, no wrap
- Thin borders `#D1D5DB` on all sides

### Data Rows
- Font: Inter 8pt (bold for Risk ID column only)
- Alignment:
  - Center: `#`, Risk ID, RBS Category, Probability, Impact, PxI, Severity, Strategy, Status
  - Left + wrap text: Risk Event, Cause, Impact description, Response Action, Owner, Contingency, Trigger, Linked Risks, Evidence Source
- Borders: thin `#D1D5DB` on all cells
- Row heights: auto (None) — Excel auto-fits wrapped text
- Zebra stripping: alternating rows with `#F8FAFC` background (light gray)

### Severity Column Fill
- Critical: `#FEF2F2` (light red)
- High: `#FFFBEB` (light amber) or inline `#92400E` text
- Medium: `#FEF9C3` (light yellow)
- Low: `#F1F5F9` (light gray)

### RBS Category Column Fill
- TEC (Technical): `#D1FAE5` (light green)
- SCH (Schedule): `#DBEAFE` (light blue)
- PRO (Procurement): `#FEF3C7` (light amber)
- Other categories: default white or light gray

### Column Widths (for design risk register — 24 columns A-X)

| Column | Content | Width |
|--------|---------|-------|
| A | # (risk number) | 5 |
| B | Risk ID | 14 |
| C | RBS Category | 9 |
| D | Risk Event | 55 |
| E | Cause | 45 |
| F | Impact | 48 |
| G | Prob | 7 |
| H | Impact (score) | 7 |
| I | PxI | 6 |
| J | Severity | 10 |
| K | Strategy | 12 |
| L | Response Action | 55 |
| M | Owner | 22 |
| N | Status | 9 |
| O-X | Dates, residual scores, contingency, triggers, links, evidence | 12-50 |

### Auto Filter
- Must extend to cover ALL data rows (not just the original range)
- Set via `ws.auto_filter.ref = "A3:X{last_row}"`
- When adding rows, update the auto filter range

### Cover Sheet (DRR Excel)
- Revision label in column B, value in column C
- Issue Date label in column B, value in column C
- Design Risk Register sheet row 1 has the revision in the title text — update both locations

### Pitfalls
- **Autofilter doesn't auto-extend** when rows are added below the original range. Always update it explicitly.
- **Conditional formatting** (if any) may have hardcoded ranges. Check and extend when adding rows.
- **Merged cells** in the Cover sheet (row 1-2) break openpyxl writes. Unmerge first, write, then re-merge.
- **Row heights remain "None"** (auto) even with long wrapped text — Excel calculates them. Don't set fixed heights on text-heavy rows.

## Excel Generation Pattern

Write data as a Python list of dicts, then iterate:

```python
risks = [
    {
        "id": "PRR-SCH-01",
        "cat": "SCH",
        "event": "...",
        "cause": "...",
        "impact": "...",
        "p": 4, "s": 4, "pxi": 16,
        "sev": "Critical",
        "strat": "Mitigate",
        "action": "...",
        "owner": "Project Manager",
        "status": "Open",
        "target": "2026-07-24",
        "idd": "2026-07-08",
        "lastrev": "2026-07-12",
        "rp": 3, "rs": 3, "rpxi": 9,
        "contingency": "...",
        "trigger": "...",
        "links": "",
        "evidence": "source_refs"
    },
    # ...
]

for i, r in enumerate(risks):
    row_num = 4 + i  # header at row 3
    bg = gray_fill if i % 2 == 0 else white_fill
    # write each cell...
```

## Discipline Design Risk Study — Front-End Risk Identification

The skills above cover **back-end** register maintenance. This section covers the **front-end**: studying a specific discipline's design documentation to identify risks before they land in the register.

### When to Use

- User asks to "study" or "audit" a discipline's design documentation for risks
- A new set of design docs arrives (schedules, specs, drawings, control strategies) and needs risk evaluation
- Pre-submission QA: before a discipline package goes to CG, assess what risks it carries
- A new subcontractor/consultant (like Studio ZNA) has been appointed — assess scope gaps vs design docs
- User asks to "do a lighting risk study" or similar discipline-specific review

### Pattern: Design Documentation Risk Analysis

#### Step 1: Inventory Available Documentation

Read ALL documentation for the discipline, not just summary files:

| Document Type | What to Extract | Risk Signal |
|---------------|----------------|-------------|
| Luminaire/equipment schedule | Quantities, manufacturers, unit power, beam angles, CCT, CRI | Single-source dependency, lead-time risk |
| Technical specifications | IP/IK ratings, dimming protocol, emergency compatibility | Spec gaps vs conservation/authority requirements |
| Control strategy document | DALI/DMX architecture, scene zoning, BMS integration | Multi-protocol complexity, integration gateway risk |
| Power/heat load study | W per zone, total heat gain, contingency % | HVAC mismatch, chiller capacity risk |
| RCP drawings | Fixture placement vs structure/MEP | Ceiling void clash risk (sprinkler, duct, acoustic) |
| Installation detail drawings | Mounting method, ceiling cut-outs, driver location | Structural suspension point risk |
| Submittal register | Deliverable dates, review durations, gate alignment | Programme risk (late submissions, inadequate review buffer) |
| Consultancy agreement / SOW | Scope boundaries, exclusions, CG comments | Uncovered scope, contract gap risk |
| Fee proposal | Resource days, duration, optional stages | Inadequate resource for scope, additional-cost risk |

**For PDFs on macOS local volumes**, extract with:
```bash
pdftotext "/path/to/document.pdf" - 2>/dev/null | head -200
# Always check text exists (some PDFs have no text layer)
python3 -c "import pymupdf; d=pymupdf.open('path.pdf'); print(len(d[0].get_text()))"
```

If `web_extract` fails on `file://` URLs (common for external drives / network volumes), fall back to `pdftotext` (available via Homebrew `poppler` on macOS).

#### Step 2: Cross-Reference Against Existing Risk Register

Read the existing DDR and PRR entries. For each design document finding, search the register for related IDs:

```python
# Pattern: map each finding to DDR/PRR IDs
findings = [
    {"finding": "No UV/lux caps in spec", "existing_risk": "DDR-LGT-002", "status": "confirmed, gap persists"},
    {"finding": "iGuzzini sole source for 735+ fittings", "existing_risk": "DDR-LGT-003", "status": "confirmed, no approved equals"},
    {"finding": "Heat gain 7.83 kW additive", "existing_risk": "DDR-MEP-003", "status": "confirmed, needs HVAC check"},
    {"finding": "Sprinkler overlap with track positions", "existing_risk": "DDR-FLS-005", "status": "confirmed, needs RCP overlay"},
]
```

For each existing risk:
- **Confirm** — the finding validates an existing risk (update evidence)
- **Upgrade** — the finding increases severity (new data point)
- **Downgrade** — the finding mitigates it (note in remarks)
- **Gap** — no existing risk covers this → **new DDR item needed**

#### Step 3: Identify New Risks Not Yet in Register

Look for these common risk archetypes across disciplines:

| Risk Class | What to Look For | Typical Severity |
|------------|-----------------|------------------|
| **Single-source dependency** | Only one manufacturer specified, no approved equals clause | Medium (low probability but high impact if supply fails) |
| **Conservation compliance gap** | No lux/UV/CRI limits stated in spec — relies on downstream operational setting | Medium-High (MoC rejection risk) |
| **Ceiling coordination clash** | RCP shows fixture positions but no structural/MEP/sprinkler/acoustic overlay | Medium-Critical |
| **Programme / resource mismatch** | Fixed-fee contract but scope broader than resource-days allow | High (Variation Order likelihood) |
| **External/Stramp coordination orphan** | Design intent exists but D&B MEP contractor not appointed who executes | High (LG-024 deliverable without execution pathway) |
| **Object-list dependency cascade** | Design relies on client data (object list) that hasn't been frozen | Critical (cascading redesign) |
| **Dual-protocol control complexity** | Two control protocols (e.g. DALI + DMX/Casambi) requiring integration gateway | Medium (integration point failure) |
| **Emergency lighting dual-function** | House + emergency in same fitting — generator dependency must be confirmed | Medium (FLS coordination) |

#### Step 4: Quantify Where Possible

Add numerical evidence to risk assessments:

```markdown
| Metric | Value | Risk Implication |
|--------|-------|-----------------|
| Total lighting power | 71,159 W (+10% = 78,275 W) | HVAC sizing — confirm chiller capacity |
| Lighting heat gain | 7.83 kW (~26,700 BTU/hr) | Additive to cooling load — DDR-MEP-003 |
| Most loaded zone | G3 Al Muftaha = 6,824 W | Single zone cooling check |
| Highest single-source | iGuzzini = 735+ SP1 fittings | Supply disruption = whole-gallery delay |
| Control zones | ~250+ total | Commissioning programme risk |
| ZNA resource | 32.5 days, 8 weeks, £28,227 fixed | Scope creep threshold — any redesign = VO |
```

#### Step 5: Structure the Risk Study Report

Use this format for the output:

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: >-
  Paths or references to all documents studied
---

# [Discipline] Design Risk Study — [Project]

## 1. What Was Reviewed

Table of documents studied with contents summary.

## 2. [Discipline] Design Philosophy

Key parameters (CCT, CRI, control architecture, fixture mix, layers).

## 3. Conservation Compliance / Standards Compliance

What the docs say vs what standards require. Gaps identified.

## 4. Supplier / Procurement Exposure

Manufacturers, quantities, single-source status, lead-time risk.

## 5. Coordination Interfaces

RCP clashes, structural conflicts, MEP overlaps, AV integration, FLS overlap.

## 6. Scope Gaps / External Interfaces

Scope boundaries that are unclear or unassigned.

## 7. Emergency / Life-Safety Strategy

Where applicable.

## 8. Key Risks Summary Table

| Risk ID | Description | Severity | Owner | Status |
|---------|-------------|----------|-------|--------|
| DDR-XXX-XXX | Clear one-liner | Critical/High/Medium/Low | Party | Open/Mitigated/Closed |

## 9. Immediate Actions Recommended

Numbered, prioritised actions with rationale.
```

#### Step 6: Determine Next Action

End the report with a clear recommendation:

- **Update existing DDR** — patch existing entries with new evidence or upgrade scores
- **Add new DDR entries** — for newly identified risks not yet covered
- **Escalate to PRR** — if a discipline risk has project-level consequence
- **Flag for Technical Office** — for resourcing, procurement, or authority decisions

#### Step 7: Deliver to DDR

If the user confirms, update the DDR markdown with the new findings. Follow the same cross-check rules from [Step 2a](#step-2a-add-new-risks-from-external-intel-user-input--supplier-data--project-update) — search existing DDR first, link to PRR if applicable, use correct scoring scales.

#### Parallel Multi-Discipline Study via Sub-Agents

For large design packages spanning many disciplines (e.g. full museum fit-out with 8-15 trades), studying every discipline linearly burns too many turns. Use parallel sub-agent delegation instead:

**When to use:** The design package covers 3+ distinct disciplines (lighting, AV, structural, acoustics, FLS, showcases, MEP) and each has its own folder or document set.

**Pattern:**

1. **Create one sub-agent per discipline group** (up to 3 concurrent per Hermes limit). Each receives:
   - The exact file paths to study
   - Discipline-specific questions (per the archetypes in `references/risk-archetypes-cheat-sheet.md`)
   - The existing DDR/PRR risk IDs to cross-reference (so they don't duplicate known entries)
   - Explicit instruction to return findings in structured format

2. **Example delegation structure** (Aseer Museum case):
   ```
   Sub-agent 1: Architecture / Exhibition Layout + Showcases + Setworks
   Sub-agent 2: AV/IT/Electrical + Lighting
   Sub-agent 3: Structural / FLS / Acoustics / Accessibility
   Sub-agent 4: MEP submittal status + ZNA contractual + procurement registers
   ```

3. **Each sub-agent returns** structured risk findings with:
   - Findings that CONFIRM existing DDR entries (update evidence)
   - Findings that UPGRADE existing DDR entries (update score)
   - NEW findings not in any register (proposed new DDR entries)
   - Key design parameters extracted (quantities, loads, specs)

4. **Integrate results:** Cross-reference sub-agent reports for conflicts (e.g. Agent 2 says "lighting track positions conflict with ducts" while Agent 3 says "acoustic baffles also in same ceiling zone" — that is a 3-way clash).

5. **Save individual reports** to `09_Agent_Workspace/<discipline>_risk_study_report.md` for traceability.

6. **Update registers in one pass:** compile all new DDR entries + PRR escalations from the integrated results, then update files.

**Pitfalls:**
- Sub-agents may give conflicting scope boundaries (e.g. both lighting agent and AV agent claim the same interface issue) — deduplicate during integration
- Sub-agents may not find existing DDR/PRR entries if the files are large — include specific risk IDs in the context
- Sub-agents may use the wrong scoring scale — explicitly state DDR uses 1-5 PxI and PRR uses 1-4 PxS
- Always verify sub-agent claims against actual design docs before adding to the register — sub-agents can hallucinate risks
- **Sub-agents frequently get appointment status wrong.** A sub-agent studying pre-appointment design drawings may conclude "Glasbau Hahn not appointed" or "AD Engineering not appointed" because the drawings were produced before the specialist was contracted. Always cross-check appointment status against the repo's procurement and submittal registers (`procurement_package_register.md`, `submittal_register.md`, Odoo mapping) before treating a "not appointed" finding as a risk. The repo is the single source of truth for contractual status; design drawings are not.
- Up to 3 concurrent sub-agents only (Hermes limit); queue additional batches sequentially

**Proven instance (2026-07-14):** 6 sub-agents studied Aseer Museum pre-appointment design docs across 11 disciplines. Result: 17 cross-interface risks (9 HIGH) identified, 10 lighting-specific risks, and confirmation of 6 existing DDR entries. Report in `09_Agent_Workspace/Aseer_Museum_Cross-Interface_Risks.md`.

### Reference Files

- `references/design-risk-study-report-template.md` — Reusable Markdown template for discipline risk study reports with all sections pre-structured
- `references/risk-archetypes-cheat-sheet.md` — Quick reference table of common risk archetypes by discipline (lighting, AV, MEP, structural, showcases, graphics)

## Related Skills

- `project-register-manager` — BIM submittal registers (appending rows, creating new registers from SOW)
- `aseer-document-control` — Aseer-specific filing conventions, sidecar analysis
- `samaya-technical-office` — project context, entity isolation rules
