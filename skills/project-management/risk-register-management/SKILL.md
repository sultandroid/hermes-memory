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

**Rule:** The JSON (`06_Risk_System/risks.json`) is the operational source of truth. The MD register is auto-generated from it by `risk_sync.py`. The Excel is a derived output. Always edit the JSON, never the MD for bulk changes. The RMP MD is the internal methodology doc. The RMP DOCX is the formal CG submittal.

## DOCX Writing Style Principles

When writing or editing any DOCX that goes to CG/PMC/MoC (including the RMP), follow these rules. **The user will reject documents that violate these — this is the #1 avoidable correction.**

### No Client-Irrelevant Methodology

The client does not care about PMBOK, PRINCE2, or other textbook methodology references. Never include:
- "PMBOK 6th Edition Chapter 11" or similar methodology citations
- Generic methodology frameworks that add no project-specific information
- "This establishes the systematic framework for..." type opening filler

The client wants: what risks exist, how they are scored, who owns them, what will be done. Not which textbook inspired the approach.

### No Internal References

The client cannot access your repo, OneDrive paths, or markdown files. Never reference:
- File paths (`01_Registers/risk_register.md`, `03_Plans/08_Risk/`)
- "project repo" or "repository"
- Markdown format
- Internal tooling or agent references

Replace with generic descriptions: "Project Risk Register (PRR)", "Risk Management System", "Project Document Control".

### No AI Symbols

Replace all typographic symbols with plain ASCII:
- Em dash (—) and en dash (–) -> hyphen (-)
- Section symbol (§) -> "Section" or just section number
- Middle dot (·) -> bullet or hyphen
- Curly quotes -> straight quotes

**The user will call you out on § symbols specifically.** Scan every document before delivery.

### Revision History — Client-Appropriate Language

The revision history table is for the client, not for internal notes. Never include:
- "Format revision — unified table styles, halftone remarks, page breaks, removed internal references"
- Any description of formatting changes, tooling, or internal process

Instead write:
- "REV00 - First issue for CG review"
- "Updated risk counts from design, procurement, site, and HSE departments"
- "Revised scoring methodology per project requirements"

### Write Like an Engineer, Not Like AI

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

### Revision History — Client-Appropriate Language

The revision history table is for the client, not for internal notes. Never include:
- "Format revision — unified table styles, halftone remarks, page breaks, removed internal references"
- Any description of formatting changes, tooling, or internal process

Instead write:
- "REV00 - First issue for CG review"
- "Updated risk counts from design, procurement, site, and HSE departments"
- "Revised scoring methodology per project requirements"

### Language Checklist Before Delivery

- [ ] No PMBOK or external methodology citations
- [ ] No em dashes or en dashes (use hyphens)
- [ ] No section symbols (§)
- [ ] No middle dots (·)
- [ ] No AI buzzwords: systematic, framework(alone), robust, leverage, facilitate, proactive(as filler), streamline
- [ ] No internal file paths, repo references, or markdown mentions
- [ ] Each body paragraph is 1-2 sentences max
- [ ] Active voice throughout
- [ ] Every data point cross-checked against repo or DRR Excel
- [ ] Names and roles from repo only, never inferred
- [ ] Revision history entries are client-facing, not internal notes

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
3. **Re-ID mapping** — the external ID (e.g. PRR-PRC-01 for FX risk) may collide with an existing repo risk (e.g. PRR-PRC-01 for ZNA lighting). Map as: `Excel PRR-PRC-01 → repo PRR-PRC-06` (next available in PRC range). Check the repo RBS table for the category's current max sequential number.
4. **RBS extension** — if the imported risk uses a category not yet in the repo's RBS table (e.g. LOG, OPS, QA, SEC), add a new row to the RBS table in both the register and the RMP. Update the RMP's §4.1 RBS hierarchy if it's a new top-level category.
5. **Scoring clash check** — ensure the risk's numeric P×S score (not the text label) matches the RMP scale. External registers often store P/S as text "High"/"Medium". Convert: Low=1, Medium=2, High=3, Very High=4.
6. Write to the live register (append at end, then renumber if inserting mid-list; see pitfall on row-number shift).
7. **Critical imported risks need treatment files** — if the imported risk scores ≥12, create `treatment/PRR-{CAT}-{NN}.md` within 48 h, same as any other Critical risk.
8. Update the RMP risk counts, RBS distribution, and register architecture table.
9. Log in the weekly review.
10. Tag as "Pending import" in the register cross-reference until PM confirms.
11. **Stale pending-import tags get cleaned up** — other agents may remove stale pending-import cross-references if the risks aren't added within the same session. Either import immediately after audit, or update the tag to show actual status.

### Step 2c: Merge External Risks into JSON SoT (Programmatic Bulk Import)

The current architecture (C08+) uses `06_Risk_System/risks.json` as the single source of truth, with `risk_sync.py` auto-generating `01_Registers/risk_register.md`. For bulk imports of 5+ risks, write a Python merge script against the JSON rather than manually patching the MD.

#### When to Use

- Bulk import of 5+ risks from an external/PM-provided register
- Merging a consolidated register with both overlap and new risks (ID collisions expected)
- Adding new RBS categories alongside new risks
- Any merge where manual MD patching would be error-prone

#### Archive the Script

The merge script is a **generated tool for a single merge event**, not a permanent fixture. Delete it after it runs:

```
rm 06_Risk_System/merge_consolidated.py
```

#### Merge Script Pattern

```python
#!/usr/bin/env python3
"""Merge external register risks into risks.json SoT."""
import json
from pathlib import Path

JSON_PATH = Path("06_Risk_System/risks.json")

with open(JSON_PATH) as f:
    data = json.load(f)

existing_ids = {r["id"] for r in data["risks"]}

# --- 0. Extend RBS categories if needed ---
data["rbs_categories"].update({
    "CNS": "Conservation & Collection",
    "SEC": "ICT & Security",
    "AV":  "AV & Multimedia",
    "QLT": "Quality",
    "TCH": "Testing, Commissioning & Handover",
})

# --- 0a. Extend owners ---
data["owners"].update({
    "Conservation Consultant": "TBC",
    "Security Specialist": "TBC",
})

# --- 0b. Re-ID existing risks when external uses same ID for different risk ---
for r in data["risks"]:
    if r["id"] == "PRR-COM-05":   # external has "EOT rejected" but repo has "Insurance"
        r["id"] = "PRR-COM-07"
        r["history"].append({"date": "YYYY-MM-DD", "action": "Re-ID", "by": "Merge",
                             "note": "Re-ID from PRR-COM-05 to PRR-COM-07"})
        break
existing_ids = {r["id"] for r in data["risks"]}

# --- 1. Update existing risks where external has better evidence ---
updates = {
    "PRR-COM-02": {
        "score": 12, "rating": "Critical", "severity": 4, "probability": 3,
        "title": "Updated title", "event": "...", "consequence": "...",
        "response_action": "...", "owner": "New Owner", "status": "Open",
    },
}

# --- 2. Define and add new risks ---
new_risks = []

def add_risk(rid, cat, title, event, cause, consequence, response, prob, sev, owner,
             status="Open", target_close="", evidence=None):
    """Add risk, auto-resolving ID collisions via next-available-serial."""
    if rid in existing_ids:
        prefix = rid.rsplit("-", 1)[0] + "-"
        n = 1
        while f"{prefix}{n:02d}" in existing_ids:
            n += 1
        rid = f"{prefix}{n:02d}"
    score = prob * sev
    rating = "Critical" if score >= 12 else "High" if score >= 8 else "Medium" if score >= 4 else "Low"
    new_risks.append({
        "id": rid, "category": cat, "title": title,
        "cause": cause, "event": event, "consequence": consequence,
        "probability": prob, "severity": sev, "score": score, "rating": rating,
        "status": status, "owner": owner, "target_close": target_close,
        "created": "YYYY-MM-DD", "last_reviewed": "YYYY-MM-DD",
        "treatment_file": "",
        "evidence": evidence or ["Source: External Register"],
        "response_action": response,
        "actions": [],
        "history": [{"date": "YYYY-MM-DD", "action": "Created", "by": "Merge",
                     "note": "Imported from [source]"}]
    })
    existing_ids.add(rid)

# 5 string params (title, event, cause, consequence, response) then 2 ints (prob, sev) then owner
add_risk("PRR-SCH-04", "SCH",
    "Short descriptive title",
    "Event — what could happen",
    "Cause / root trigger",
    "Consequence / impact",
    "Response / mitigation plan",
    4, 4, "Planning Manager")

# --- 3. Apply updates, add new risks, sort ---
for r in data["risks"]:
    if r["id"] in updates:
        for k, v in updates[r["id"]].items():
            r[k] = v
data["risks"].extend(new_risks)
data["risks"].sort(key=lambda r: r["id"])

# --- 4. Bump revision ---
data["revision"] = "C09"
data["last_updated"] = "YYYY-MM-DD"
data["merge_note"] = f"Merged [source]. Added {len(new_risks)} risks. Updated ratings: [...]. New RBS: [...]."

# --- 5. Validate and write ---
ids = [r["id"] for r in data["risks"]]
assert len(ids) == len(set(ids)), f"Duplicate IDs: {[i for i in ids if ids.count(i) > 1]}"
with open(JSON_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Written Rev {data['revision']} — run risk_sync.py to regenerate markdown.")
```

Then regenerate:
```bash
python3 06_Risk_System/risk_sync.py
```

#### Merge Checklist

| Step | Check |
|------|-------|
| ✅ | New RBS categories added to `data["rbs_categories"]` before risks reference them |
| ✅ | Existing risks re-ID'd when external uses same ID for different risk |
| ✅ | Each new risk has all required JSON fields |
| ✅ | IDs validated — no duplicates before write |
| ✅ | `merge_note` documents what changed and why |
| ✅ | `risk_sync.py` runs without error |
| ✅ | Final MD register verified (counts, snapshot, categories) |
| ✅ | Merge script deleted |

#### Pitfalls

- **ID collision is the most common bug** — read risk event/cause side by side, not just IDs
- **add_risk() must be defined before the calls** — Python executes top to bottom
- **Five string params before ints**: signature is `add_risk(rid, cat, title, event, cause, consequence, response, prob, sev, owner)`. Missing one shifts all params and causes cryptic `missing required positional argument` errors
- **New RBS categories must exist in data before adding risks that reference them** — otherwise `risk_sync.py` fails
- **Re-ID must rebuild `existing_ids`** before add_risk calls, or the freed ID is still treated as taken
- **Every change gets a `history` entry** — Created, Re-ID, Reviewed, etc.
- **Merge script is disposable** — run, verify, delete. Do not commit it.

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
**Cascading symptom:** The Dashboard sheet's Critical/High/Medium/Low counts will also be 0 or blank — not because no risks exist, but because the counts derive from the broken Risk Score column. Fix scoring first, then counts auto-populate.

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

### Risk Close vs Mitigate

When a risk's root cause is eliminated (the specific threat no longer exists), set status to **Closed**, not Mitigated. "Mitigated" means the risk still exists but controls have reduced it. "Closed" means the risk event cannot happen anymore.

Example: PRR-CON-03 (blockwork mandate) — CG approved drywall, so the blockwork threat is gone → **Closed**. The residual coordination work (MEP/AV routing, slab verification) is normal design development, not a risk.

### Owner Names — Use Real People, Not Role Titles

When the PM gives an owner update, use the actual person's name (e.g. "Hani Alghamdi"), not a role title (e.g. "Commercial Manager"). The user corrected this explicitly.

This applies to:
- Risk owner field in the register
- Response action owner
- Any assignment of accountability

If the person is unknown, use the role title as a placeholder but flag it for the PM to fill in the real name.

### Revision Entries Must Be Client-Appropriate

**Hard rule:** Revision entries describe what changed that affects the content, NOT internal formatting details. The user explicitly corrected this.

| Wrong (internal) | Right (client-facing) |
|---|---|
| "Format revision — unified table styles, halftone remarks, page breaks, removed internal references" | "REV00 - First issue for CG review" |
| "Fixed table column widths, added cantSplit, removed markdown paths" | "Updated risk distribution data from departmental reviews" |
| "Removed internal file paths and repo references" | "REV00 - First issue for CG review" |

**User correction signal:** "dont tell such information like this its not usful for the client" — if you wrote formatting/internal details in a revision entry, the user will call it out. The revision log is for the client/CG reviewer, not for the internal team.

### SOW-Protect Out-of-Scope Items

When a risk mixes in-scope and out-of-scope items, split them. Keep Samaya's scope as a risk, flag Employer/third-party scope as SOW-Protect.

Example: PRR-CNS-01 originally had "artifact damage liability, ICOM accreditation, loan conditions" — those are Employer responsibilities, not Samaya's. The in-scope part (dust control, temp/humidity during construction) stayed as a Medium risk owned by HSE Manager.

### CG Response Forecasting for Risk Plans

When the user asks to forecast CG response on a risk plan, evaluate against these criteria:

| Code | Meaning | Typical triggers |
|---|---|---|
| A | Accepted | Standard methodology (PMBOK-aligned), no factual errors |
| B | Minor comments | Missing notes on empty categories, role titles instead of names, vague contingency figures |
| C | Revise & Resubmit | Unfilled data placeholders ("To be confirmed"), incomplete register architecture, contradictions between sections |
| D | Rejected | Wrong methodology, missing required sections, factual errors |

**Key insight for methodology plans:** CG evaluates whether the plan describes a workable process, not whether the live data is complete. "To be recalculated from PRR" is acceptable for EMV values because EMV lives in the register. But "AV Register in progress" while claiming "4-register architecture" is a contradiction that triggers Code B/C.

### Scanned PDF OCR Workflow

When a supplier letter arrives as a scanned PDF (images only, no text layer):

1. Extract images from PDF using PyMuPDF: `page.get_pixmap(matrix=fitz.Matrix(3, 3))`
2. Save as PNG, convert to JPEG for tesseract
3. Run tesseract with `--psm 6` for single uniform block of text
4. For 1-bit images (black/white), invert before OCR: `ImageOps.invert(img)`
5. Cross-reference multiple OCR runs on different image variants to resolve noise
6. If tesseract fails due to encoding issues, run it directly in shell (not via subprocess in Python)

### Unified Register Template

All 4 register sheets (PRR, DDR, HSE, AV) must use the SAME 14-column template:

| # | Column | Type |
|---|--------|------|
| 1 | ID | Text |
| 2 | Category / Discipline | Text |
| 3 | Risk Event | Text |
| 4 | Cause / Hazard | Text |
| 5 | Impact / Consequence | Text |
| 6 | Probability | Number |
| 7 | Severity | Number |
| 8 | Score | **Formula** (P × S) |
| 9 | Rating | **Formula** (IF) |
| 10 | Response Strategy | **Dropdown** (6 options) |
| 11 | Mitigation / Controls | Text |
| 12 | Risk Owner | Text |
| 13 | Target Close | Text |
| 14 | Status | Text |

Column widths: [14, 22, 35, 30, 30, 10, 10, 10, 10, 18, 40, 20, 14, 14]

**Dropdown options:** Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect

**Scoring formulas by register:**
- PRR: `=F{r}*G{r}`, Rating: `=IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low")))`
- DDR: `=F{r}*G{r}`, Rating: `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))`
- HSE: `=F{r}*G{r}`, Rating: `=IF(H{r}>=16,"Critical",IF(H{r}>=10,"High",IF(H{r}>=5,"Medium","Low")))`
- AV: `=IF(F{r}="","",F{r}*G{r})`, Rating: `=IF(H{r}="","",IF(H{r}>=12,"Critical",IF(H{r}>=8,"High",IF(H{r}>=4,"Medium","Low"))))`

**Dashboard formulas reference PRR sheet:**
- Total: `=COUNTA('Master Risk Register'!A2:A100)`
- Critical: `=COUNTIF('Master Risk Register'!I2:I100,"Critical")`
- High: `=COUNTIF('Master Risk Register'!I2:I100,"High")`
- Category distribution: `=COUNTIF('Master Risk Register'!B:B,"*{cat}*")`

### Cleanup Stale Dropdowns

The `build_unified_sheet()` function may leave duplicate dropdowns from the old template. After rebuilding, clear all existing data validations and add a single one:

```python
ws.data_validations.dataValidation = []
dv = DataValidation(
    type="list",
    formula1='"Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect"',
    allow_blank=True,
    showDropDown=False
)
ws.add_data_validation(dv)
dv.add(f'J2:J{last_row}')
```

### Dashboard Formulas After Template Change

After changing the register template to 14 columns, update Dashboard formulas to reference the correct columns:
- Rating is column I (9)
- Category is column B (2)

```python
ws.cell(row=5, column=3).value = f'=COUNTIF({prr_sheet}!I2:I100,"Critical")'
ws.cell(row=5, column=4).value = f'=COUNTIF({prr_sheet}!I2:I100,"High")'
ws.cell(row=5, column=5).value = f'=COUNTIF({prr_sheet}!I2:I100,"Medium")'
ws.cell(row=5, column=6).value = f'=COUNTIF({prr_sheet}!I2:I100,"Low")'
```

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
- `references/register-merge-id-collisions.md` — ID collision patterns and resolutions from the C08→C09 merge, with field structure reference and param order pitfalls
- `references/unified-register-template.md` — Standard 14-column template for all register sheets with identical headers, widths, formulas, dropdowns, and formatting rules
- `project-risk-register` skill's `references/formula-driven-register-pattern.md` — Formula-driven Excel pattern (v2.0) with live P×S→Score→Rating formulas, Dashboard COUNTIF, Risk Matrix COUNTIFS, and Cover live metrics. Use this when the user wants interactive formula-based scoring

## NCR Register Management

NCRs (Non-Conformance Reports) are adjacent to risk management — open NCRs represent materialising quality/HSE risks. The repo's `01_Registers/ncr_register.md` tracks all project NCRs.

### When to create/update

- A new NCR arrives via email from CG (Hossam Mabrouk)
- The user asks about NCR status
- During weekly risk review — open NCRs feed into PRR-STK-02 (work stoppage risk)

### NCR Register Format

```markdown
# NCR Register — Aseer Regional Museum

| NCR # | Date | Source | Subject | Status | Owner | Due Date |
|-------|------|--------|---------|--------|-------|----------|
| NC-001 | date | CG / Internal | Brief description | Open / Closed | Owner | date |
```

### NCR Routing from Email

When a CG NCR email arrives:
1. Extract the PDF from Outlook (AppleScript batch extract)
2. `pdftotext` to read the full NCR — extract: NCR number, date, subject, CG comments, required actions, deadline
3. Route the PDF to: `04_Docs/10_Test_and_Inspection/10.3_NCRs/{NCR-ID}_{Subject}/`
4. Add a row to `01_Registers/ncr_register.md` in the repo
5. Check if the NCR is already referenced in the risk register (PRR-STK-02 tracks open NCR count)
6. If the NCR represents a new materialising risk not yet in PRR, consider opening a new risk

### CG NCR Processing Pattern (from session)

```
NCR: MOC-MUS-CG-ASE-NC-1KH-009
Subject: Unsafe Fabricated Debris Chute (welded drums, no engineering design)
Date: 15-Jun-2026
CG Status: Open — closeout rejected by CG (insufficient evidence)
CG Required: MSRA + competent-person inspection records + verified by HSE Manager + PM approval
Root cause: Internal coordination failure; initial chute bracing inadequate
Corrective action taken: Steel-tube bracing installed, floor anchorage with Hilti bolts
```

### Pitfalls

- **CG may reject closeout even after corrective action** — the submitted evidence must address ALL NCR requirements, not just the immediate fix. Read the CG comment sheet at the end of the PDF.
- **NCR file naming** uses the NCR number as folder name, not the subject
- **NCR register is separate from the risk register** but linked via PRR-STK-02 — update both when NCRs arrive or close
- **NCR folder doesn't exist by default** — create `04_Docs/10_Test_and_Inspection/10.3_NCRs/` if it doesn't exist

## Risk Register Reconciliation — Cross-Check Against Actual Transactions

### When to Use

- User flags that a risk entry is stale or out of sync with actual project events
- A new MoM, decision log entry, or CG approval changes the status of one or more risks
- Before a weekly risk review — ensure the register reflects current reality
- After a batch of email processing — new evidence may upgrade/downgrade existing risks

### The Core Problem

Risk registers drift from reality when:
- A risk was created around an **appointment** (e.g. "MEP Designer not appointed") but the appointment happened and the risk was never refocused
- A **target close date** passes without the risk being reviewed or extended
- New **evidence** (letters, test results, CG responses) arrives but is not added to the risk's evidence list
- The risk's **title/cause** still describes the original threat but the actual threat has evolved

### Reconciliation Workflow

#### Step 1: Identify Stale Entries

Scan the register for these patterns:

| Pattern | What to Check | Example from Session |
|---------|---------------|---------------------|
| **Appointment vs mobilisation confusion** | Risk says "not appointed" but MoM confirms appointment | PRR-DES-01: "MEP designer appointment" still Critical open despite MoM-14 confirming AD Engineering approved |
| **Overdue target_close with no update** | target_close date has passed, status still Open, no history entry | PRR-FLS-02: target_close 16-Jul, no review on 18-Jul |
| **Missing evidence** | New letters, datasheets, or CG responses exist but not in evidence list | PRR-PRC-05: GBH Letter 002 received but not referenced |
| **Stale evidence references** | Evidence cites a stale report number or superseded document | Any risk still referencing "Rpt 16" when Rpt 18 is current |
| **Status mismatch with decisions_log** | decisions_log says "approved" but risk still says "Open - materialising" | Cross-check each risk's evidence against decisions_log entries |

#### Step 2: Cross-Check Each Risk Against Source Documents

For each risk, verify against these sources in order:

1. **MoMs** — does the latest MoM mention this risk? Is the status consistent?
2. **decisions_log.md** — was a decision made that changes this risk's status?
3. **action_items.md** — are the risk's mitigation actions still open/overdue?
4. **Email scan** — did new evidence arrive (letters, CG responses, test results)?
5. **Submittal status** — did the related submittal get approved/rejected?
6. **look_ahead.md** — is the risk still on the critical path?

#### Step 3: Apply Fixes Per Risk

| Fix Type | What to Change | Where |
|----------|---------------|-------|
| **Refocus** | Update title, cause, event to reflect current threat (not the original one) | risks.json + treatment file |
| **Extend target_close** | Push to a realistic new date, add history note explaining why | risks.json |
| **Add evidence** | Append new source references to evidence array | risks.json |
| **Update last_reviewed** | Set to today's date | risks.json |
| **Add history entry** | Document what changed and why | risks.json |
| **Update treatment file** | Refocus risk statement, update action due dates, add reconciliation note | treatment/PRR-{ID}.md |

#### Step 4: Update Treatment Files

For each risk that changed, update its treatment file:

- **Risk statement** — must reflect the current threat, not the original one
- **Action due dates** — push overdue dates to realistic new targets
- **Evidence column** — add new source references
- **Reconciliation note** — add a section at the bottom documenting what was reconciled and why
- **Escalation triggers** — update if the risk's urgency changed

#### Step 5: Regenerate and Commit

```bash
python3 06_Risk_System/risk_sync.py
git add -A
git commit -m "Risk register reconciliation C{NN} — {date}

- PRR-XXX: refocused from 'appointment' to 'mobilisation' — MoM-{N} confirms appointment done
- PRR-YYY: target_close extended {old} → {new}
- PRR-ZZZ: added {evidence} evidence
- PRR-AAA, PRR-BBB: reviewed, no change
- Treatment file PRR-XXX.md: updated with reconciliation note"
```

#### Step 6: Bump Revision

| Document | Change |
|----------|--------|
| `risks.json` | `revision: C{NN}` (increment from current) |
| `risk_register.md` | Auto-generated by risk_sync.py — verify counts |
| `03_Plans/08_Risk/README.md` | Update governance line revision |
| `00_Command_Center/master_dashboard.md` | Update Risk Management lane revision tag |

### Common Reconciliation Patterns (from Aseer Museum)

| Pattern | Original Risk | Actual Status | Fix |
|---------|--------------|---------------|-----|
| **Appointment done, mobilisation pending** | PRR-DES-01: "MEP designer appointment" Critical 4x4 | AD Engineering approved per MoM-14; SOW/fee/LOI not finalised | Refocus title to "mobilisation", update cause/evidence, keep score |
| **Overdue decision, extend target** | PRR-FLS-02: Fire Pump Room, target_close 16-Jul | 7-option study still undecided | Extend to 22-Jul, add history note |
| **New evidence received** | PRR-PRC-05: Patinated brass Oddy risk | GBH Letter 002 received 16-Jul | Add to evidence array |
| **No change, just review** | PRR-APP-01: Renovation licence | Still pending per MoM-14 section 4 | Update last_reviewed, add history note |

### Rescoring Based on Risk Manager Decision with Exit Criteria

When the Risk Manager (user) issues a formal rescoring decision, the change must be precise and documented with clear exit criteria for further downgrade.

#### Decision Pattern

| Element | What to Capture | Example |
|---------|----------------|---------|
| **Who decided** | Role, not name | "Risk Manager" or "Kimi (Risk Manager)" |
| **What changed** | Which dimension(s) moved | Probability 4→3 (appointment done, PO issued, kick-off held) |
| **What stayed** | Which dimension(s) unchanged | Severity stays 4 (first deliverables missed, SOW not CG-approved, critical-path chain) |
| **Why unchanged** | Specific consequence chain | "Blocks IFC-0004 Life Safety (16) and Fire Pump (12)" |
| **Exit criteria** | Conditions for next downgrade | "CG SOW approval + first package delivered → High (9)" |
| **History entry** | Formal record | `{"date": "2026-07-18", "action": "Reframed + Rescored", "by": "Kimi (Risk Manager)", "note": "..."}` |

#### Rules for Rescoring

- **Probability drops** when the root cause threat is eliminated or materially reduced (appointment done, PO issued, kick-off held, first submittal approved)
- **Severity stays** when the consequence chain is unchanged — the same downstream risks (IFC-0004, Fire Pump) are still blocked
- **Do not reduce both dimensions simultaneously** unless the risk event itself has fundamentally changed
- **Exit criteria must be specific and measurable** — not "when things improve" but "CG SOW approval + first package delivered"
- **Document in both risks.json history AND treatment file** — the treatment file gets a "Reconciliation note" section with the full rationale

#### Treatment File Update Pattern

```markdown
## Exit criteria (→ High 9)

1. CG approves MEP SOW under design plan
2. First MEP deliverables package delivered

## Reconciliation note (2026-07-18)

Rescored 4×4→3×4 per Risk Manager decision. Probability reduced (appointment done, PO issued, kick-off held, ZD-0068 Code B). Severity unchanged (first deliverables missed, SOW not CG-approved, critical-path dependency on IFC-0004 and Fire Pump). Exit criteria defined for downgrade to High (9).
```

### Worked Example: PRR-DES-01 Reconciliation (2026-07-18)

**Situation:** User flagged that PRR-DES-01 was still titled "MEP detailed designer appointment / mobilisation slips" with Critical 4x4=16, target_close 23-Jul, and evidence citing only "look_ahead item 1 & 6; MoM-14 M14-2.5; project_status ITC". However, MoM-14 (06-Jul) explicitly documents: "MEP Designer submission completed and approved."

**Diagnosis:** The risk conflated two phases — appointment (done) and mobilisation (pending). The title, cause, and evidence were stale because they still described the original "not appointed" threat.

**Fix applied:**

| Artifact | Before | After |
|----------|--------|-------|
| Title | "MEP detailed designer appointment / mobilisation slips" | "MEP Designer (AD Engineering) mobilisation / first deliverables slip" |
| Cause | "ITC variation / commercial path; replacement consultant LOI not closed; CG no-objection path open" | "AD Engineering appointed per MoM-14 (06-Jul); SOW/fee/LOI not finalised; CG no-objection path open" |
| Evidence | `look_ahead item 1 & 6; MoM-14 M14-2.5; project_status ITC` | Added `decisions_log 2026-07-06 (MEP Designer approved)` |
| Treatment risk statement | "MEP detailed designer not being appointed and mobilised" | "AD Engineering appointed but SOW/fee/LOI not yet finalised" |
| Treatment action due dates | 14-Jul, 15-Jul (overdue) | 20-Jul, 22-Jul (extended) |
| Treatment escalation | "Daily PM + Legal if LOI not issued by 15-Jul" | "Daily PM + Legal if LOI not issued by 20-Jul" |
| Treatment file | No reconciliation note | Added "Reconciliation note (2026-07-18)" section |
| Score | Kept 4x4=16 (mobilisation delay still blocks Life Safety, Fire Pump, energy coordination) | Unchanged |

**Key decision:** Score was kept at Critical because the consequence (blocking Life Safety, Fire Pump, energy/IT coordination) is unchanged by the appointment. Only the threat vector changed from "not appointed" to "appointed but not delivering."

**Treatment file update pattern:**
```markdown
## Reconciliation note (2026-07-18)

MoM-14 (06-Jul) documents MEP Designer appointment as **completed and approved**. 
This risk has been refocused from "appointment" to "mobilisation and first deliverables." 
The appointment itself is no longer the risk — the commercial close-out and kick-off schedule are.
```

### Pitfalls

- **Don't close a risk just because the original threat changed** — the risk may have evolved into a different threat that still needs management. Refocus, don't close.
- **Don't change the score without evidence** — only upgrade/downgrade PxS when new data justifies it. A refocused risk may keep the same score.
- **Treatment files get stale faster than the register** — always update the treatment file alongside the JSON entry. A treatment file with old due dates is worse than no treatment file.
- **risk_sync.py overwrites the MD register** — never edit `risk_register.md` directly. All changes go in `risks.json`.
- **The register's ID migration table** (at the bottom) may reference old IDs that were re-ID'd during reconciliation. Update the migration table if a risk was re-ID'd.

## Related Skills

- `project-risk-register` — Build professional Excel-based risk registers with
  dashboard, heat map, and formula-driven rating system (v2.0 pattern with
  live `=I*J` / nested `IF` formulas). Use this when building or rebuilding an
  Excel register from scratch; `risk-register-management` covers back-end
  data maintenance (JSON MD, RMP) while `project-risk-register` covers
  front-end Excel generation.
- `project-register-manager` — BIM submittal registers (appending rows, creating new registers from SOW)
- `aseer-document-control` — Aseer-specific filing conventions, sidecar analysis
- `samaya-technical-office` — project context, entity isolation rules
