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
| Design Risk Register (DRR) | Excel (OneDrive) | `04_Docs/09_Registers/06_Design_Risk_Register/` | Design-phase risks (linked from DMP) |
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

### Step 3: Update RMP DOCX (Word)

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

Check these specific data points across all three documents:

```python
alignment_checks = [
    ("Total risks", 28),
    ("Open risks", 25),
    ("Critical risks", 8),
    ("High risks", 10),
    ("Medium risks", 8),
    ("Low risks", 2),
    ("Scoring scale", "1-4"),
    ("Excel row count", 28),
    ("RMP §1.2 count", 28),
    ("RMP §2.0 total", 28),
    ("RMP §4.2 total", 28),
    ("RBS SCH count", 3),
]
```

### Step 6: Bump Revisions

| Document | Pattern |
|----------|---------|
| Excel title | `Rev XX · YYYY-MM-DD` |
| Register MD | `revision: C03` in frontmatter |
| RMP MD | `revision: C02` in frontmatter |
| Register control table | Append row in `## Register control` |
| RMP Document Control | Append row |

## Pitfalls

### MergedCell write error
Unmerge ALL cells before any structural writes. `ws.unmerge_cells(str(mc))` for each merged range. Re-merge section headers after data is written.

### Extra pipe prefix in markdown tables
When using `patch()` to fix markdown tables, the tool sometimes adds an extra `|` at the start of each line. Always verify the patch result and fix with a follow-up patch if needed.

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

### DRR count in RMP is often stale
The RMP (repo) says DRR has 37 risks. The actual DRR Excel (P03) has 76 risks. Always open the DRR Excel directly and count, rather than trusting the RMP's stated number.

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

## Verification Command

After all updates, verify alignment with:

```bash
# Excel row count
python3 -c "from openpyxl import load_workbook; wb=load_workbook('path.xlsx'); print(f'Excel rows: {wb.active.max_row - 3}')"

# RMP § references
grep -n "Master Risk Register |" risk_management_plan.md | grep -oP '\d+'
grep -n "**Total**" risk_management_plan.md

# Register RBS counts
grep -E "^\| (SCH|SIT|DES|FLS|MEP|APP|COM|PRC|CON|STK|HSE) " risk_register.md

# Revision
grep "revision:" risk_register.md risk_management_plan.md
```

## Related Skills

- `project-register-manager` — BIM submittal registers (appending rows, creating new registers from SOW)
- `aseer-document-control` — Aseer-specific filing conventions, sidecar analysis
- `samaya-technical-office` — project context, entity isolation rules
