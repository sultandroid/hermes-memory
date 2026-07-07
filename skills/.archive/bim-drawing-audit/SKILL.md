---
name: bim-drawing-audit
description: "Audit drawing registers against filesystem, generate status trees (HTML), and produce designer scope-vs-deliverables workflow reports. Covers register parsing, file scan cross-reference, targeted HTML patching, and RIBA stage mapping."
version: 1.0.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [BIM, Drawing-Audit, Registers, Samaya, HTML, NRS, RIBA]
---

# BIM Drawing Audit — Register vs Filesystem Cross-Reference

## When to Use This Skill

- User asks to **scan / rescan / audit drawing files** against a register
- User asks to **update a drawing status tree** (HTML report)
- User asks to **check designer (NRS/consultant) scope vs deliverables**
- User asks for **workflow gap analysis** on drawing deliverables

## 🔴 CRITICAL RULE: Never Regenerate HTML from Scratch

**Use targeted `patch()` calls only.** The user's HTML reports have a specific design/layout. Regenerating the whole file breaks formatting, counters, and sheet layout. Always:
1. Read the existing HTML file
2. Identify the specific <span> elements that need status changes (XX → >>, etc.)
3. Use `patch()` to replace only the status markers
4. Use `patch()` to update section header counts
5. Use `patch()` to update summary counters
6. Use `patch()` to bump revision number and date
7. For new entries: insert as new lines after the last entry in the section using `html.replace()`

**Never write a Python script that regenerates the full HTML.**

## Step-by-Step Workflow

### Phase 1 — Parse the Register

```python
# Extract drawing entries from HTML status tree
import re
with open("Aseer_Drawing_Status_Tree.html") as f:
    html = f.read()
html_decoded = html.replace("&gt;", ">")
entries = []
for line in html_decoded.split("\n"):
    m = re.search(
        r'<span class="mk (ok|pn|xx)">\[(OK|>>|XX)\]</span>\s+([A-Z0-9\-]+)\s+Rev\s+([\w\-]+)\s+(.+)',
        line.strip()
    )
    if m:
        entries.append({...})
```

### Phase 2 — Scan Filesystem

1. Use `find` to get all PDF/DWG files in `06_Drawing_Source_Folders/`
2. Check `02_Approved_Stamped_Packages/` for stamped PDFs
3. Check `05_Correspondence_Archive/` for old revisions

### Phase 3 — Cross-Reference

- Match register drawing numbers against file stems
- Handle naming variants: `A2742-1100` vs `A2742-A-1100` vs `A2742-1100 (1).pdf`
- Determine status:
  - `stamped` → file in `02_Approved_Stamped_Packages/`
  - `source_pdf` → file in `06_Drawing_Source_Folders/`
  - `archive_only` → only in `Correspondence_Archive/`
  - `missing` → no file anywhere

### Phase 4 — Apply Targeted Updates

For each changed entry:
```python
old = f'<span class="mk xx">[XX]</span> {drawing_no}'
new = f'<span class="mk pn">[&gt;&gt;]</span> {drawing_no}'
patch(path=html_file, old_string=old, new_string=new)
```

For section header updates (summary page + tree pages):
```python
# Use replace_all=True when the same section label appears in both
old_h = '1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>58 <span class="mk xx">[XX]</span>20'
new_h = '1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>78'
patch(path=html_file, old_string=old_h, new_string=new_h, replace_all=True)
```

For summary counters:
```python
patch(path=html_file,
      old_string='class="counter-tile pn"><div class="num">167</div>',
      new_string='class="counter-tile pn"><div class="num">207</div>')
```

### Phase 5 — Identify Designer Scope Gaps

1. Read NRS/designer responsibility matrix (PDF extract via PyMuPDF)
2. Map register categories to scope elements (walls, ceilings, doors, etc.)
3. Identify scope items with no deliverable in register (e.g. roof terrace sunshade, specification package)
4. Identify items needing re-issue (old revision only)

### Phase 6 — Generate Workflow Report

Create a clean HTML report with:
- Cover sheet with summary counters
- Category breakdown table with RAG status
- Scope items NOT in register (gaps)
- Old revision drawings needing re-issue
- Designer obligations (review/approve/stamp matrix)
- Workflow process map and action items

## CSS: Prevent Title Wrapping in Tree View

User preference: *"dont exceed the line"* — titles must not wrap across multiple lines.

```css
/* Before: titles wrap */
.tree-box{white-space:pre-wrap;font-size:7.2pt;...}

/* After: single line, overflow hidden */
.tree-box{white-space:pre;font-size:7pt;overflow-x:hidden;...}
```

Change `white-space: pre-wrap` → `pre` and drop font to 7pt. Apply this when the user reports line wrapping.

## Reporting: Scope vs Deliverables (Not Stamp Status)

When asked "what's missing from NRS" or "NRS scope vs deliverables":
- Focus on **what NRS was contractually obligated to deliver** vs what files exist
- Do NOT conflate "not stamped" with "not delivered"
- Distinguish: delivered to source folder vs delivered as old revision only vs truly missing
- Include workflow process map showing the delivery pipeline

## Payment Tracking Against Annex 4 (Main Contract)

When asked to chart payments against deliverables:

1. **Read Annex 4 payment schedule** from `Contracts/Project Contract/CONTRACT_REFERENCE.md`
   - 15 bundles (Sub-table A) = 65,153,751 SAR (87%)
   - 4 final payments (Sub-table B) = 9,773,062 SAR (13%)
   - Total: 74,926,813.83 SAR

2. **Map each bundle to deliverable status**:
   - Bundle 001 (IFC Dossier, 5%) → drawing register status
   - Bundle 002 (Engineering/Permits, 5%) → BCG progress + authority approvals
   - Bundle 003 (Internal Works, 20%) → setworks/details drawings
   - Bundle 004 (Furniture, 1%) → FF&E design
   - Bundle 005 (Display Cases, 19%) → Glasbau Hahn progress
   - Continue for all 15 bundles...

3. **Track actual payments** from invoice PDFs:
   - Extract via PyMuPDF (`fitz.open(path)`)
   - For scanned invoices: OCR with `tesseract`
   - Record: invoice ref, date, amount, milestone, paid date

4. **Report structure** — HTML report with:
   - Overview counters (design complete %, procurement ready %, in progress %, not started %)
   - Bundle-by-bundle table with progress bars and RAG
   - Monthly distribution timeline (Dec-25 → Dec-26)
   - Actual vs planned payment tracking table
   - Gap analysis (payment due vs delivery achieved)

5. **Flag mismatches**: When NRS invoices Stage 5 while Stage 4 stamping is incomplete.

## Naming Convention Handling

NRS uses `A2742-A-XXXX` naming for existing/demo/sections drawings while the register uses `A2742-XXXX`. When scanning:
- Search for both variants
- Also check for parenthesized filename suffixes: `A2742-1100 (1).pdf`
- Report the naming mismatch if it prevents auto-matching

## PDF Invoice Extraction for Payment Tracking

```python
import fitz
doc = fitz.open(path)
for page in doc:
    text = page.get_text()
    # For image-based PDFs:
    imgs = page.get_images(full=True)
    xref = imgs[0][0]
    img = doc.extract_image(xref)
    # Save and OCR with tesseract
    import subprocess
    r = subprocess.run(["tesseract", tmp, "stdout", "-l", "eng", "--psm", "6"],
                      capture_output=True, timeout=30)
    text = r.stdout.decode("utf-8", errors="replace")
```

For bank transfer receipts: look for amount, currency, date, reference number, beneficiary.

## RIBA Stage Mapping (Aseer Museum)

| Register Section | RIBA Stage | NRS Role |
|---|---|---|
| 1100-1164 Existing/Demolition | 4 | Create |
| 1200-1537 GA/Elevations/Sections | 4 | Create |
| 1550 Stairs | 4 | Create |
| 1570-1578 External | 4 | Create |
| 1600 Washrooms | 4 | Create |
| 1700-1799 Walls/Setworks | 4 | Create |
| 1800 Showcases | 4 | Create |
| 1850 Graphics | 4 | Create |
| 1900-1961 Finishes/Doors | 4 | Create |
| MEP, Structure, Lighting | 5 | Review/Approve/Stamp |
| Shop Drawings | 5 | Review/Approve/Stamp |
| As-built, O&M | 6 | Review |

## Design Review Turnaround

- NRS contractual review period: **≤72 hours** per submission
- Track and flag if not monitored

## Pitfalls

- **A-prefix naming**: NRS existing/demo drawings use `A2742-A-XXXX` while register uses `A2742-XXXX`. Always search for both.
- **Parenthesized filenames**: Some files have `(1)` or similar suffixes from OneDrive sync conflicts.
- **Section headers appear twice**: On the summary page AND inside the tree. Use `replace_all=True` when patching section headers.
- **Counters are on one line**: The entire counter-row is a single HTML line. Use exact string matching.
- **Old revisions diluting results**: Files in `Correspondence_Archive/` count as "delivered" but may be outdated. Flag separately.
- **Regeneration destroys formatting**: Never regenerate HTML from scratch. Always use targeted patches.
- **Title wrapping**: User corrected this — use `white-space: pre` not `pre-wrap` in `.tree-box` to prevent titles from wrapping.
- **Payment-vs-progress gap**: When creating payment charts, flag the gap between cumulative payment due (~72% by Jun-26) and actual delivery progress (~35-48%).

## Reference Files

- `references/nrs_scope_mapping.md` — Aseer Museum NRS responsibility matrix mapping
- `references/drawing_register_categories.md` — Category-to-section mapping for register analysis

## Related Skills

- `bim-project-register` — Excel register CRUD (complementary — this skill handles HTML status trees and scope reports)
- `project-deliverable-audit` — Overlapping: covers same register audit workflow. Consider consolidation with this skill.
- `drawing-register-audit` — Overlapping: same class of work. Consider consolidation with this skill.
