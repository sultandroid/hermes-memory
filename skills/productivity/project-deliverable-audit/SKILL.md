---
name: project-deliverable-audit
description: "Audit project deliverables (drawings, documents) against filesystem by extracting register entries, scanning files, cross-referencing, and updating HTML status reports with targeted patches — never full regeneration. Covers drawing register audit, designer scope-vs-deliverables workflow reports, file boundary cross-contamination detection, RIBA stage mapping, and payment tracking."
version: 2.0.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [BIM, Drawing-Register, Audit, HTML-Report, Samaya, File-Boundary, NRS, RIBA]
    related_skills: [bim-project-register, project-register-manager, evm-analysis-chart]
---

# Project Deliverable Audit — Drawing Status & File Tree

Audit a project's deliverables (drawings, documents) against actual files on disk and update HTML status reports. Used for the Aseer Museum Drawing Status Tree and similar deliverable-tracking HTML reports.

See `references/drawing-scan-methodology.md` for detailed scan methodology, naming conventions, regex patterns, and cross-reference logic.

## Consultant Submittal Review (Subagent Workflow)

For reviewing submitted drawing packages (PDFs) against PMC/CG reviewer comments — see `references/submittal-review-workflow.md`.

This covers: reading the Document Issue Register, mapping actual PDFs, dispatching subagents by discipline with reviewer-comment context, per-discipline MD audit reports, and consolidating into a master CG compliance summary with an action checklist.

## Personnel & Sign-Off Audit for Plan Documents

When reviewing a project management plan document (Resource Plan, DMP, PEP, HSE Plan, BEP, etc.) for personnel and stakeholder accuracy — see `references/plan-document-personnel-audit.md`.

**Key lessons encoded from user corrections:**
- Never leave QA/QC Reviewer or Document Controller blank in sign-off tables. If QA/QC is vacant, add an acting signatory (e.g., Construction Manager) with `(acting)` notation.
- Always fill in the DC name from the known team list.
- Check risk register descriptions for stale personnel labels (e.g., "acting PD" when PD is confirmed).

## 🔴 CARDINAL RULE: NEVER Regenerate — Always Patch

**Do NOT regenerate HTML reports from scratch.** The user's design, layout, and workflow must be preserved. Always:

1. Read the existing HTML file
2. Make **targeted text replacements** via Python `str.replace()` or `patch()` tool
3. Only change status markers, counters, and dates — never restructure

The user's exact words: *"why you change the design/workflow"* — this means preserve every line of the original design.

## Expected-vs-Delivered Audit with Contract/Odoo Cross-Reference

When auditing whether a subcontractor has delivered what was expected, the register or SCOPE_REQUEST.md is only half the story. **You must also verify whether the contractor was actually commercially engaged.** A deliverable gap of 100% may mean the contractor was never contracted, not that they're failing to perform.

See `references/po-scope-extraction.md` for the full Odoo PO extraction workflow, query patterns, payment milestone parsing, and a concrete worked example (Namaa POs P01167 & P01449).

### Workflow

**Phase 1 — Establish expected deliverables:**
1. Read the discipline's submittal register (e.g., FLS_Submittal_Register.xlsx) or the _MANAGER_DASHBOARD/SCOPE_REQUEST.md
2. Note all expected items by reference code (FL-001 through FL-036) and stage (50%/90%/100%/IFC)

**Phase 2 — Check what was actually received:**
3. Scan the sub's 05_Returned_Submittals/ folder for actual submissions
4. Check Email Archive for transmittals or submitted PDFs
5. Cross-reference against project-wide locations (04_Docs/03_Submittals/, 02_Submittals/)

**Phase 3 — Verify contract/engagement status (via Odoo):**
6. Search Odoo for the sub as a vendor (res.partner, name ilike)
7. Check for Purchase Orders (purchase.order, filter by partner)
8. Check for vendor bills or payments (account.move, account.payment)
9. Check the project task for engagement status (project.task, by name or tag)
10. Also check the filesystem for: prequalification PDFs (PQ-00xx), draft SCOPE_REQUEST.md, signed SOW/contract, email evidence of appointment

**Phase 4 — Classify the cause:**
| Finding | Meaning | Action |
|---------|---------|--------|
| No vendor in Odoo + No PO + Task in Initiation | **Not commercially engaged** | Need to onboard the sub — create vendor, issue PO, trigger Day 0 |
| Vendor exists + PO issued + Task active | **Contractor failing to deliver** | Issue formal notice, escalate per contract terms |
| No submittal register exists | **Scope not formalised** | Create SPEC.md and submittal register first |
| Register exists but all progress columns empty | **Engagement never started** | Same as "not commercially engaged" |

**Phase 5 — Report findings:**
- Show all 3 sources side by side: expected (register) vs received (files) vs contracted (Odoo)
- Highlight the root cause: procurement gap or performance gap
- If not contracted, recommend: create vendor, issue PO, sign SOW, trigger Day 0

See `references/po-scope-extraction.md` for concrete query patterns, a worked example (Namaa POs P01167 & P01449), and signal interpretation.

### Pitfalls
- **Prequalification approval is not contract award.** MoC approval (PQ-0025, PQ-0096) only means the sub can be appointed — it does not mean a contract exists. Always check Odoo for a PO.
- **Task in Initiation stage with overdue Dec 2025 deadline = stuck pre-award.** The task was created but never progressed. Do not assume active engagement.
- **No partner record in Odoo means no commercial relationship.** Even MoC-approved subs may not be set up as vendors. This is the strongest signal of non-engagement.
- **SCOPE_REQUEST.md is a Samaya-internal document.** It is what Samaya wants the sub to do — not what the sub agreed to do. Only a signed SOW or PO confirms mutual agreement.
- **Reference drawings from other parties are not sub deliverables.** Files found in Existing_FLS_AsBuilt/ or Stamped_Life_Safety/ may come from the architect or original design team. Always distinguish who produced what.
- **PO notes contain HTML with payment milestones.** Strip HTML with `re.sub(r'<[^>]+>', '\n', notes)` then `html.unescape()` to reveal the true deliverable schedule. Line items alone may not capture the full scope.

## Workflow

### Step 1: Read the Existing Report

```python
# Decode HTML entities
html_d = html.replace("&gt;", ">").replace("&lt;", "<")
# Extract all drawing entries
entries = re.findall(
    r'<span class="mk (ok|pn|xx)">\[(OK|>>|XX)\]</span>\s+(A2742[\-A]+\d+)',
    html_d
)
```

### Step 2: Scan Filesystem for Actual Files

Search these locations in priority order:
1. **`02_Approved_Stamped_Packages/`** — NRS-stamped PDFs
2. **`06_Drawing_Source_Folders/`** — active PDF/DWG files per section
3. **`00_Stamped_CAD_Source/`** — DWG files with stamp/approval
4. **`05_Correspondence_Archive/`** — old revisions (only if user directs)

Use `find` or Python `subprocess.run()` for bulk enumeration. **Do not delegate to labor agents** — they timeout on 500+ file scans.

### Step 3: Cross-Reference Register vs Filesystem

Status priority:
- **Stamped PDF** → `[OK]` (approved by NRS)
- **Active PDF/DWG in source folder** → `[>>]` (pending review)
- **DWG in Stamped CAD Source** → `[>>]`
- **Only in Correspondence Archive** → check with user first
- **No file anywhere** → `[XX]`

### Step 4: Apply Targeted Patches

**Option A — Python bulk replace:**
```python
with open(path) as f: html = f.read()
for dn in changed_entries:
    html = html.replace(
        f'<span class="mk xx">[XX]</span> {dn}',
        f'<span class="mk pn">[&gt;&gt;]</span> {dn}',
        1
    )
with open(path, "w") as f: f.write(html)
```

**Option B — `patch()` tool** for unique replacements:
```
patch(path=path, old_string=old, new_string=new)
```

### Step 5: Update All Counters in One Pass

1. **Summary counters** — Stamped [OK], Pending [>>], Missing [XX] totals
2. **Section headers** — per-discipline counts (e.g., `>>:58 XX:20` → `>>:78`)
3. **Revision number** — `Rev N` → `Rev N+1`
4. **Date** — update to today

Critical: the counter row is one continuous HTML line (no line breaks). Match the exact string.

### Step 6: Add Newly Discovered Drawings

If new drawings exist on filesystem but not in the register:
- Add entries at the end of their section using the correct format
- Update the section header count
- Match existing prefix format exactly: `├── <span class="mk pn">[>>]</span>`

### Step 7: Copy Files to Proper Source Folder

When drawings are found in archive/old revisions, copy to the active folder:
```bash
cp OLD_REV_PATH/A2742-XXXX.pdf \
   06_Drawing_Source_Folders/XXXX_Section_Name/
cp -R OLD_REV_PATH/A2742-XXXX/ \
   06_Drawing_Source_Folders/XXXX_Section_Name/A2742-XXXX/
```

## CSS Fix for Tree View (Prevent Title Wrapping)

Long titles wrap in `<pre>` blocks with `white-space: pre-wrap`. Fix:
```
.tree-box{...white-space:pre;overflow-x:hidden;font-size:7pt;...}
```
Change `pre-wrap` → `pre` and reduce font slightly if needed.

## ⚠️ CRITICAL: Verify Design Stage via DMP Before Any Conclusion

**Before making ANY claim about what stage drawings are at (DD, IFC, AFC), ALWAYS read the DMP (Design Management Plan) first.** The DMP defines the stage breakdown the contract omits:

| Stage | What | LOD | Status in Aseer |
|-------|------|-----|-----------------|
| **Stage 4-A** | Design Development (DD) | LOD 300-350 | **DELIVERED** — 251 drawings |
| Stage 4-B | IFC Construction Package | LOD 350-400 | **NOT STARTED** |
| Stage 5 | Off-site Fabrication Review | LOD 400 | Partially started (premature) |
| Stage 5-6 | On-site Review | LOD 400-500 | Future |

**The contract may label deliverables "IFC Package" but the DMP clarifies they are actually DD (Stage 4-A).** The user explicitly corrected this — get it right on the first pass by reading the DMP. DMP path: `Docs/02_Plans_and_Procedures/02.1_DMP/01_Source_Files/HTML/aser_museum_dmp_RevC03_NRS_Lead.html`

## Cross-Document Verification Protocol

**Never trust a single source document.** Before reporting conclusions on scope, payment, or status, cross-reference ALL of these:

1. **NRS Contract DOCX** — fee breakdown, scope, payment terms (Art. 4, 5, 10, 11)
2. **DMP** — design stage definitions, workflow, LOD matrix
3. **Drawing Register** — actual drawings delivered vs expected
4. **SOW Responsibility Matrix PDF** — who creates/reviews what (appendices A-D)
5. **Invoices (PDF)** — what was billed, when, for which stage
6. **Bank Receipts** — what was actually paid vs invoiced

When documents conflict (e.g. contract says "IFC" but DMP says "DD"), the DMP is authoritative for design stage; the contract is authoritative for payment terms.

## Phase 3 — Contract DOCX Extraction & Analysis

### DOCX Table Extraction
```python
from docx import Document
doc = Document(path)
text = "\n".join([p.text for p in doc.paragraphs])
for table in doc.tables:
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
```
Search for fee/amount: `re.search(r'\d+[,.]?\d*\s*(SAR|EUR|£|\€)', text)`

### Image-Based PDF Fallback
- Try `fitz` → `page.get_text()` → if empty, it's image-based
- Try tesseract OCR; if fails, note as "image-based, manual review"
- Extract images via `page.get_images(full=True)` → `doc.extract_image(xref)` for manual inspection

### Key NRS Contract Data (for reference)
**⚠️ Stage 4 in the contract is labelled "IFC Package" but is actually Stage 4-A DD (LOD 300-350) per the DMP. Stage 4-B IFC (LOD 350-400) has not started.**

| Field | Value |
|-------|-------|
| Total Fee | SAR 1,209,000 |
| Stage 4 (per contract: "IFC Package" — actually **Stage 4-A DD**) | SAR 768,000 (63.5%) — 8 weeks |
| Stage 5 Off-site Review | SAR 270,000 (22.3%) — 3 months |
| Stages 5-6 On-site Review | SAR 171,000 (14.2%) — 4 months |
| Updated Visuals (optional) | SAR 75,000 |
| Resource total | 211 person-days, 7 roles |
| Advance Payment (10%) | SAR 120,900 |
| Payment Terms | 14 days after invoice (Art. 11.3) |
| Review Turnaround | 3 Working Days (Art. 5.5) |
| Penalty Cap | 10% of total fee (Art. 21) |

### NRS Contract Appendices
- **A** — Scope Matrix (responsibility matrix)
- **B** — Resource & Cost Schedule — **prevails for deliverables**
- **C** — Contractor's SoW (back-to-back)
- **D** — Employee requirements

## Phase 4 — Payment vs Deliverable Tracking

When a responsibility matrix or SOW document is available, cross-reference the register against contractual scope:

### NRS Contract Pattern (Parts A-D)

| Part | NRS Obligation | Action |
|------|---------------|--------|
| **A** | NRS Creates (IFC package) | Verify all scope elements have register entries. Flag gaps (e.g. "roof terrace sunshade" with no drawing number) |
| **B** | NRS Reviews/Approves/Stamps (Samaya creates) | List 22+ disciplines needing NRS stamp. Add subcontractor column showing who's responsible (BCG, Glasbau Hahn, ZNA 3297, OfficeDog, Samaya in-house, etc.) |
| **C** | Other Obligations | Meeting attendance, ≤72hr review period, material updates |
| **D** | Exclusions | Items NOT in NRS scope (MEP, structure, BIM, life safety) |

Report each part in a separate table with columns: #, Element, Register Ref, Status, Notes.

## Phase 4 — Payment vs Deliverable Tracking

When invoices/payment data is available, add payment cross-reference:

### Data Sources
- **Annex 4 (Payment Schedule)** — from main contract, lists bundles with % and SAR. May be image-based — use contract reference docs or manual extraction
- **Invoices** — from subcontractor (NRS, etc.). May be scanned PDFs — try OCR, note failures
- **Bank transfer receipts** — confirm actual payment amounts and dates

### Report Structure
1. **Payment schedule table** — Bundle #, Name, Est. %, Est. SAR, Contract Due, Actual Paid, Variance, Status
2. **Invoice tracking** — Invoice ref, Date, Amount, Paid Date, Status (PAID / DUE / FUTURE)
3. **Timeline mismatch analysis** — flag when subcontractor bills next stage before previous stage is complete
4. **Cumulative profile** — contract due vs actual delivery progress (gap %)

### Key columns for payment tracking table
# | Bundle | % | Est. SAR | Contract Due | Actual Paid | Variance | Status | RAG

### Pitfalls — Payment Tracking
- Main contract total (MoC to Samaya) does not equal subcontract total (Samaya to NRS). Keep separate
- Annex 4 percentages are % of Sub-table A (86.96% of total), not % of full contract. Add Sub-table B (13.04%) separately
- Bundle % estimates from reference documents may be approximate — verify against actual signed contract
- Scanned invoices may fail OCR — flag as "image-based, manual review needed"
- 14-day payment terms are common — calculate due dates from invoice date

### ⚠️ ALWAYS Read the Signed Contract's Payment Schedule Before EV Arguments
**The EV report can mislead you.** When the subcontractor pushes back on a payment hold, they will cite the actual signed contract — and the contract may say "Monthly Instalments" even though EV shows overpayment. This happened with NRS: Art. 11 said monthly, not milestone-gated, payments.

**Before giving payment advice or negotiating a restructure:**

1. **Extract Art. 11 (Terms of Payment)** from the signed PDF — use pymupdf (`fitz`) or pdftotext. The contract's payment schedule is authoritative, not the fee proposal or EV report.
2. **Check if the invoicing schedule was formally agreed** — Art. 11.2 often says "per invoicing schedule to be agreed." If no schedule was agreed for later stages, you have leverage.
3. **Check if stage deliverables are blocked by preconditions** — e.g. Stage 5 (off-site fab review) depends on IFC completion (Art. 5.1). If IFC is blocked, Stage 5 work physically can't proceed.
4. **Check penalty/exceptions clauses** — e.g. Art. 20: "No penalty for Customer-caused delays." NRS will cite this.
5. **Amendments require writing** — Art. 18 typically. Any restructured payment plan needs a written contract amendment.

**Key contract articles to check for leverage:**
- Art. 11.1 — Payment milestones (what the subcontractor will cite)
- Art. 11.2 — Invoicing schedule agreement (your counter if none agreed)
- Art. 5.1 — Stage 5 dependency on prior stage completion
- Art. 18 — Written form requirement for amendments
- Art. 20 — Penalty/exceptions clauses
- Art. 14 — Termination terms (who gets what if terminated)

**Your negotiation argument:**
> *"The contract said monthly instalments assuming Stage N would finish on schedule. That schedule is broken by mutual factors beyond either party's control. The invoicing schedule for the next stage was never formally agreed. We need a written amendment reflecting current reality."*

### Earned Value Management (EVM) S-Curve

After building the payment vs deliverable tables, create an EVM S-curve to visualise schedule and cost performance. See `references/evm-analysis.md` for full methodology.
See `references/nrs-contract-payment-terms.md` for the signed NRS contract payment schedule and negotiation leverage articles.

**Data points needed for each period (month):**
- **PV (Planned Value)** — cumulative planned fee from the fee schedule
- **EV (Earned Value)** — value of deliverables actually completed (% complete × budgeted fee for that stage)
- **AC (Actual Cost)** — cumulative payments made to the subcontractor

**Key metrics at the reporting date:**
| Metric | Formula | Interpretation |
|--------|---------|---------------|
| Schedule Variance (SV) | EV − PV | Negative = behind schedule |
| Cost Variance (CV) | EV − AC | Positive = under budget (paid less than earned) |
| SPI | EV ÷ PV | < 1.0 = behind schedule |
| CPI | EV ÷ AC | > 1.0 = under budget |

**SVG S-curve coordinate math (when embedding in a dark-themed HTML report):**
```
y = max_y - (value_in_K / scale_factor)

Where:
  max_y = 352          # Y-axis baseline at bottom of chart area
  scale_factor = 4     # SAR 1,000 = 1 SVG pixel

Example: EV = 384K → y = 352 − (384 / 4) = 352 − 96 = 256
```

**Critical: Subagent QC catches coordinate errors.** When creating the initial SVG yourself, delegate to Claude Code for verification — subagents recalculate every coordinate and catch mismatches between stated values (e.g. "PV at Jun = 614K") and pixel positions. Do not assume your hand-calculated coordinates are correct.

**S-curve construction rules:**
- All three curves (PV, EV, AC) share the same Y-axis scale
- PV curve follows a logistic/S-shape (slow start → rapid ramp → plateau at contract value)
- EV curve lags PV when behind schedule (vertically below PV at any X)
- Mark TODAY with a vertical dashed line at the current month
- Show SV arrow (from EV to PV) and CV arrow (from EV to AC) at TODAY line

## Phase 5 — HTML Chart Embedding

For charts (payment timeline, progress bars):

### SVGs
- Use inline <svg> directly in HTML — <object> and <img> tags fail with local file paths due to browser security
- Set sheet to landscape: <div class="sheet" style="width:297mm;min-height:210mm;">
- Make SVGs standalone and self-contained (no external CSS/JS dependencies)

### Table column widths
- Set explicit style="width:XX%" on each <th>
- Sum must equal 100% across columns
- Test with longest likely text — adjust if text wraps
- Common layout: #(4%), Discipline(22%), Subcontractor(14%), Element(20%), Action(18%), Status(10%), Notes(12%)

## Aseer Museum Section Mapping

| Drawing Range | Section Header | Source Folder |
|---|---|---|
| 1100-1164 | 00 — Existing & Demolition Plans | 1100_Existing_and_Demolition |
| 1200-1204 | 1200 — General Arrangement | 1200_General_Arrangement |
| 1220-1223 | 1220 — Wall Finishes Plans | — |
| 1230-1233 | 1230 — Floor Finishes Plans | 1230_Floor_Finishes |
| 1250-1253 | 1250 — Ceiling Finishes Plans | 1250_Ceiling_Details |
| 1350-1500 | 1350/1500 — Sections | 1350_Sections |
| 1510-1537 | 1510 — Internal Elevations | 1510_Internal_Elevations |
| 1550-1559 | 1550 — Stairs Details | 1550_Stairs_Details |
| 1570-1578 | 1570 — External Details (Benches) | 1570_External_Details |
| 1600-1601 | 1600 — Washrooms / VIP WC | 1600_Washrooms_VIP |
| 1700-1711 | 1700 — Freestanding Walls | 1700_Setworks_Partitions |
| 1720-1799 | 1720 — Setworks Details | 1700_Setworks_Partitions |
| 1800-1820 | 1800 — Showcases | 1800_Showcases |
| 1850-1887 | 1850 — Graphics & Panel Housing | 1850/1860_Graphics_Housing |
| 1890 | 1890 — Painted Finishes | 1890_Painted_Finishes |
| 1900-1909 | 1900 — Floor Type Details | 1900_Finishing_and_Flooring |
| 1910-1913 | 1910 — Ceiling Type Details | — |
| 1920-1926 | 1920 — Wall Type Details | 1920_Wall_Type_Details |
| 1930-1945 | 1930 — Doors & Lift Linings | 1930_Doors_Lifts |
| 1950-1961 | 1950 — Door Types & Schedules | 1950_Door_Types |

## Drawing Register from Document Issue Sheet (DIS) PDF

When NRS sends a DIS-01/DIS-02 PDF as a cover sheet for a drawing package, you can extract the full drawing register directly from the PDF text rather than manually typing entries.

### Workflow

**Step 1: Extract raw text from DIS PDF**
```bash
pdftotext -raw /path/to/DIS-01.pdf output.txt
```

**Step 2: Parse drawing entries with regex**
Each entry line follows the format:
```
MOC-ASE-AR-ARC-{floor}-DDD-{number} Title {scale} {size} {revision}
```

Key regex pattern:
```python
m = re.match(
    r'(MOC-ASE-AR-ARC-(\w+)-DDD-(\d+))\s+(.+?)\s+((?:\d+:\d+(?:/\d+:\d+)?))\s+(A[01])\s*(\d*)',
    stripped
)
```

**Step 3: Map floor codes**
```python
floor_map = {
    "BF": "Basement", "LGF": "Lower Ground Floor",
    "GF": "Ground Floor", "1F": "First Floor",
    "2F": "Second Floor", "GEN": "General",
}
```

**Step 4: Assign section groups by drawing number range**
```python
section_ranges = [
    (1100, 1104, "Existing GA Plans"),
    (1150, 1164, "Demolition Plans"),
    (1200, 1253, "Proposed Plans"),
    (2550, 2559, "Stairs Details"),
    (2700, 2761, "Setwork Details"),
    (2800, 2820, "Showcase Details"),
    (4000, 4053, "Sections"),
    (5510, 5537, "Room Elevations"),
    # ... add ranges as needed
]
```

**Step 5: Generate Excel register**
- Columns: #, Drawing Number, Title, Floor, Scale, Size, Section Group, Status
- Group by section with colored headers
- Add 3D visuals section separately (extracted from DIS PDF "VISUALS" section)

**Pitfalls:**
- The DIS PDF uses `\f` (form feed) as page breaks — handle with `text.split('\f')`
- Some titles contain illegal XML characters (form feeds, control chars) — strip with `re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)`
- pdftotext `-raw` mode gives clean single-line entries; `-layout` mode preserves columns but harder to parse
- Some drawing numbers span two pages (form feed splits the entry) — merge lines starting with MOC across page breaks
- The DIS may list more drawings than have actual PDF files (listed but not physically delivered) — note this in the register
- Visual entries use `VIS{N}` suffix pattern, not `DDD-{N}` — separate parser needed
- The purpose of issue ("I" = Information, "A" = Approval) is marked on the DIS — important for status column

**Reference:** Aseer DIS-01 extracted 246 drawings + 20 visuals into `Aseer_DD_Drawing_Register_26Jun2026.xlsx`

## Cross-Stage Audit Impact Assessment

When a later-stage submission arrives (e.g., Stage 4 DD Showcase Package) and a previous-stage audit report exists (e.g., Stage 3 Design Information Audit by NRS), systematically assess whether the audit needs updating.

### Trigger
- User attaches a previous-stage audit PDF and a current-stage submission, asking: "do we need to update the audit?"
- Designer submits Stage N+1 package while Stage N audit items are still marked "Open"

### Decision Framework

**Step 1 — Identify overlapping items:** Cross-reference each audit item against the new submission's scope. Not all audit items will be covered — only those within the submission's discipline.

**Step 2 — For each overlapping item, check:**
| Status | Meaning | Action |
|--------|---------|--------|
| ✅ **Resolved in new submission** | NRS Proposal column already references Stage N+1 resolution, and the new submission delivers on that | Can close the audit item |
| ⚠️ **Partially addressed** | New submission addresses part of the issue, but gaps remain | Track in closure register as "Partially Resolved" |
| ❌ **Still open** | New submission doesn't touch the audit item | Keep as Open, track separately |

**Step 3 — Check for new issues NOT in the audit:**
The new submission may introduce changes that weren't in the previous stage (e.g., plinth height reduction, sliding doors replacing hinged, numbering system drift). These are **new Stage N+1 review items**, not audit updates. Record them separately for the current-stage review process.

**Step 4 — Recommendation:**
| Scenario | Recommendation |
|----------|---------------|
| Audit items partially/fully resolved in new submission | **Don't update the audit report** — it's a historical Stage N document. Create a **Closure Register** tracking each item → its Stage N+1 resolution. This is standard design audit practice. |
| Audit items still completely unresolved with no Stage N+1 action | Escalate — the designer hasn't addressed known issues |
| Submission introduces major deviations from approved Stage N design | These generate **new Stage N+1 review comments**, not audit updates |

### Why the Audit Report Stays as-is
- The audit is a **Stage N document** — it records discrepancies found at that stage, not their resolutions
- All items may be "Open" because the audit status reflects Stage N finding status, not current resolution
- Updating an old audit creates confusion about which stage the findings belong to
- The closure register bridges the gap: maps audit items → Stage N+1 resolutions cleanly

### Closure Register Template

Simple mapping table (Excel or MD):

```
| Audit Item | Description | Stage 4 Resolution | Status |
|------------|-------------|-------------------|--------|
| 06         | Bench dims swapped | Setworks package corrected dimensions | ✅ Closed |
| 09         | AV totems qty 1→8 | 8no included in Stage 4 schedule | ✅ Closed |
| 16         | Type 6B fabric | Création Baumann proposed (passes Oddy) | ✅ Closed |
| 10         | Projection wall Viroc | Position stated, not yet in submission | ⚠️ Open |
| 08         | Kvadrat FR fail | Alternative sourcing in progress | ❌ Open |
```
## Design Change Register — From Audit to Formal Submission

When audit findings lead to design changes in the next stage, the audit closure register alone is insufficient. You need a **Design Change Register (DCR)** as the formal mechanism to track baseline→proposed changes through consultant approval.

### Trigger
- User has a Stage N audit report (items marked "Open")
- Stage N+1 submission arrives and partially addresses audit items
- Stage N+1 also introduces NEW changes not in the audit (deviations from approved baseline)
- User asks: "do we need to update the audit" → answer is NO → create DCR + Backup Reports

### DCR Structure

| Column | Content |
|--------|---------|
| DCR ID | `DCR-001`, `DCR-002` etc. Sequential across register |
| Date | Date change first identified in submission |
| Stage 3 Baseline | Approved reference (drawing ref, audit item, spec clause) |
| Stage 4 Change | Proposed change as submitted |
| Description | What changed between stages in plain language |
| Trigger | Why initiated (CG review comment / GH fabricator input / NRS proposal) |
| Justification | Designer's technical rationale (quote verbatim from email) |
| Quality / Aesthetic Impact | Assessment: Equivalent / Negative / Minor / Neutral |
| Status | Open / In Review / Approved / Rejected |
| CG Remarks | Current CG review position from the submission review |
| Reference Photo | Embedded screenshot showing the change visually (Stage 3 vs Stage 4) |

### DCR Creation Workflow

**Step 1 — Map audit items to Stage 4 changes:**
Cross-reference each audit item against the new submission. Some will be resolved (✅), some partially addressed (⚠️), some still open (❌). The audit closure tracker shows this.

**Step 2 — Identify NEW changes NOT in the audit:**
Read the Stage 4 submission and CG review comments. Changes introduced in Stage 4 that deviate from approved Stage 3 baseline each get their own DCR. Examples from this session:
- Plinth height 200mm→100mm
- Hinged→sliding doors
- Panel widths unequal
- Dual opening mechanism
- Numbering system drift

**Step 3 — Create the DCR Excel:**
```python
# Standard headers (no cost column — cost is assessed during GH shop drawings, not design review)
headers = ["DCR ID","Date","Stage 3 Baseline","Stage 4 Change","Description of Change",
           "Trigger","Justification (NRS/GH)","Quality / Aesthetic Impact","Status","CG Remarks"]
```

**Format rules (from user correction):**
- **No emoji, icons, or Unicode symbols** in any cell. Plain text only (Yes/Partial/blank, not emoji)
- **Uniform row heights** matching embedded image height (e.g., 195pt for 180pt images)
- **Reference photos embedded** as floating images in the rightmost column, not hyperlinks
- Column L (photo) ~65 chars wide, images scaled to uniform height
- Navy #1E293B header fill, white Calibri 10pt bold headers
- Alt row shading (#F8FAFC), thin border bottom only
- Freeze panes below header row

**Step 4 — Embed reference photos:**
```python
from openpyxl.drawing.image import Image
img = Image(path)
target_img_h = 180  # points — uniform height
if img.height > target_img_h:
    ratio = target_img_h / img.height
    img.width = int(img.width * ratio)
    img.height = target_img_h
ws.add_image(img, f'L{row}')
ws.row_dimensions[row].height = target_img_h + 15  # uniform row
```

Reference photos are typically screenshots from:
- Stage 3 approved drawings (showing the baseline)
- Stage 4 submission drawings (showing the change)
- Finishes schedules, elevations, sections
- Email correspondence showing designer's response

### Backup Reports — Convert Designer Email to Formal Evidence

When the designer (NRS) responds to CG review comments via email, their response IS the justification — but it's not in a submittable format. Convert each response into a **formal Backup Report** for CG submission.

**Backup Report structure (A4 print-ready HTML):**
```
Cover page → Index → One page per DCR
```

Each Backup Report page contains:
1. **Comparison table:** Stage 3 parameter vs Stage 4 parameter (side by side)
2. **Technical justification:** Verbatim quotes from designer's email response
3. **Supporting visual evidence:** Embedded images from drawings
4. **NRS Position statement:** Clear verdict box (green for resolved, red for rejected)

**Production workflow:**
1. Extract designer's responses from email chain (PDF extraction or email text)
2. Map each response to the corresponding DCR
3. Create comparison tables from the response content
4. Embed images from attached PDFs using pdfimages→sips resize
5. Format as A4 HTML with navy header style matching Samaya document standards
6. User prints to PDF for CG submission

**Key formatting rules (from user corrections):**
- No AI "fingerprints" — no emoji, symbols, icons. Plain text only.
- Images resized to fit A4 page (max 160mm height, max width constrained by 210mm page)
- Samaya document template colors: #0F172A / #1E293B navy, #B91C1C accent, #64748B gray text

**Typical items needing Backup Reports (from this session):**
| Item | Change | CG Comment |
|------|--------|------------|
| Plinth height 200→100mm | Dimension change | "Does not match approved design" |
| Hinged→sliding doors | Mechanism change | "Clarify opening mechanism" |
| Unequal panel widths | Dimension asymmetry | "Ensure consistent dimensions" |
| Dual opening mechanism | New mechanism type | "Clarify opening/closing details" |
| Acorian cladding | Material (disputed) | "Why new material?" |
| Section/slope ratios | Geometry correction | "Discrepancy in base slope" |

### Submission Process

1. Create DCR Excel (with embedded photos + audit closure tracker sheet)
2. Create Backup Report HTML (one per change, compiled into single document)
3. Submit DCR + Backup Reports to CG as part of the Stage 4 review response
4. Each change needs CG formal approval (Code A or B) before proceeding to IFC
5. Track approval status in the DCR Status column

### Pitfalls

- **Not all "Open" audit items need Stage 4 resolution.** Some items (structural clashes, ceiling heights) are design-wide and may only be resolved at IFC or coordination stage. Don't flag cross-stage gaps that naturally span multiple stages.
- **CG marking the submission "For Information Only" doesn't mean resolved.** "FYI" status means CG acknowledged receipt but hasn't formally approved. Audit items are only truly closed when CG issues Code A/B on the relevant submission.
- **Don't conflate Stage N audit items with new Stage N+1 review comments.** The audit report and the review comments serve different purposes and follow different resolution tracks.
- **NRS-authored audit + NRS-authored Stage 4 submission = self-review risk.** When the same designer both flags discrepancies (audit) and submits the resolution (Stage 4), independent verification is needed. The closure register should note which items were self-resolved vs independently verified.
- **The NRS Proposal column in the audit may already reference Stage 4.** NRS wrote their own proposed resolution at audit time (e.g., "Within Stage 4 setworks package we have included…"). This doesn't mean the Stage 4 submission actually delivered it — verify against the actual submitted package, not the audit's own claims.
- **Designer email responses are NOT backup reports.** Jim's email chain is internal correspondence. CG needs formal documents (DCR + Backup Report) with comparison tables, justification, and visual evidence. Never submit raw email chains as backup.
- **Don't include cost columns in design-stage DCRs.** Cost impact is assessed during GH shop drawings, not during Stage 3→4 design review. All changes are "neutral" at this stage — putting ✓ in every row adds no value.
- **The designer may argue "this is not a change, it's a refinement"** — but procedurally, anything different from approved Stage 3 baseline IS a change requiring documented justification and CG approval. Enforce the process even when the designer pushes back.
- **CG review comments may reference the wrong drawing/code.** When the consultant misidentifies which showcase a change applies to (e.g., Acorian clad on wrong Type), the Backup Report should clarify the reference and request CG to specify which exact drawing/section the comment applies to.
- **No icons in formal deliverables.** The user called this out explicitly. Backup Reports and DCR Excel must use plain text only — no emoji, Unicode symbols, geometric shapes, or dingbats anywhere.

## CG Design Phase Scheduling (Elbaz-Style)

When a CG consultant (Mohammad Elbaz/cg.com.sa) requires a design phase schedule with specific rules, use this methodology. Applicable to any CG-managed project where the Design Management Plan (DMP) has been approved.

### 🔴 COMPLETENESS RULE: Touch Every Discipline

When updating a CG submission plan or design schedule, EVERY discipline listed in the plan must receive a status update — not just the ones with new data. The user corrected this explicitly: "did you update all, showcase, life and safety, structure, AV...ect?"

**Failure pattern:** Updating only 6 rows (Architectural, Design Consultant, Display Cases, MEP, Structural) while leaving AV, BIM, Exhibition Works, FF&E, Fire Life Safety, Graphics, Low Current, Replicas, Testing untouched. The user notices the gap immediately.

**Correct approach:**
1. Build a matrix of ALL disciplines in the plan
2. For each, determine current status based on available evidence:
   - **Has actual data** (email receipts, register log entries) → REALISTIC status with date
   - **No new data but past original deadline** → PLANNED (REVISED) with reason
   - **Dependent on upstream** → state the dependency and reschedule
3. Add the reason in Remarks — don't just change the label
4. Flag overdue items in red, received items in green, rescheduled in gray
5. Add a legend explaining the status scheme
6. Verify total item count unchanged after all updates

### Input: CG Consultant Email Requirements

CG emails typically require:
1. **DD Drawings** — Design Development with basement-first priority
2. **Material Submittals & Finishing Samples** — can run parallel to DD
3. **IFC Drawings** — depends on DD approval
4. **Coordination Drawings** — depends on all discipline DD approval

### Rules from CG (Elbaz's Email, 20 Jun 2026)

| Rule | Detail |
|------|--------|
| Deadline | DMP Approval + 3 months (e.g., 21 May → 21 Aug) |
| Basement first | Basement floor = priority milestone |
| Staggered | Minimum 5 WD gap between same-discipline submissions |
| Review buffers | Must include adequate CG review time |
| Scope | DD + Materials + IFC + Coordination — all must be APPROVED, not just submitted |

### Review Buffer Standards

| Complexity | Samaya Internal Review | CG Review | Examples |
|-----------|----------------------|-----------|----------|
| Simple | 2 WD | 7 WD | Single drawing/spec, small structural item |
| Medium | 3 WD | 14 WD | Multi-sheet package, discipline submittal |
| Complex | 5 WD | 14 WD (up to 21 WD) | Full discipline DD (NRS 246-dwg set) |

- Resubmission (Code B/C): Samaya 3 WD + CG 7-10 WD
- Working week: Sun-Thu (Saudi Arabia), off: Fri-Sat

### Critical Path Rule

**IFC depends on DD Approval (not just DD submission).** This is the critical bottleneck:

```
DD Submission → CG Review (14-21 WD) → DD Approval
    ↓
IFC Prep (3-10 WD) → Samaya Review (2-5 WD) → CG Submit → CG Review (7-14 WD) → IFC Approval
```

For complex items (MEP, NRS Exhibition), DD approval arrives 4-18 Aug → IFC needs additional 19-27 WD → misses a 21 Aug deadline by 5-34 days.

### Verdict Framework

For each of CG's 4 categories, give a clear verdict:

| Verdict | Criteria |
|---------|----------|
| ✅ POSSIBLE | All items approved by deadline with >5 WD buffer |
| ⚠️ RISK | Fits by ≤5 WD, or conditional on Code A first try |
| ❌ NOT POSSIBLE | Cannot complete full review cycle before deadline |

### Phased Delivery (Recommended)

When the full scope cannot meet the deadline, propose a 3-phase plan:

| Phase | Target | Items |
|-------|--------|-------|
| Phase 1 | Original deadline | DD + Materials + Simple IFC ✅ |
| Phase 2 | Mid-handover | Complex IFC (MEP, AV, FLS) |
| Phase 3 | Handover | Exhibition IFC + Coordination |

**Mitigations to propose to CG:**
1. Parallel IFC prep — start during DD review (saves 8-10 WD)
2. Negotiate 7 WD (not 14) CG review for medium-complexity IFC items
3. Split MEP IFC — issue Basement IFC early while upper-floor DD continues
4. Request 4-week extension for remaining IFC packages

### Oracle Aconex Access

When you need to connect to the project's Oracle Aconex (Construction & Engineering) CDE to cross-reference document statuses — see `references/oracle-aconex-browser-access.md`. The login URL is `https://constructionandengineering.oraclecloud.com/idcsLogin`. Credentials are project-specific and must be provided by the user.

### Example Output Format

See `references/cg-design-phase-scheduling.md` for a worked example (Aseer Museum, 22 items across 10 disciplines with full date math, dependency chains, and verdict).

---

## Pitfalls

### ⚠️ Always Read the DMP Before Claiming a Design Stage
The contract may say "IFC Package" but the DMP defines the real stage split (Stage 4-A DD vs Stage 4-B IFC). Never assume. The user corrected this explicitly: the 251 drawings are DD, not IFC.

### ⚠️ Cross-Reference All 6 Source Documents
Contract DOCX, DMP, drawing register, SOW matrix, invoices, bank receipts — need all six before a reliable conclusion. If one contradicts another, explain the discrepancy.

### ⚠️ Detect Premature Stage Billing
When a subcontractor invoices for the next stage (e.g. Stage 5 Off-site) before the current stage (Stage 4-A DD) is complete and stamped, flag it explicitly. This is a workflow risk the user needs visibility on.

### ⚠️ Don't Regenerate HTML
User explicitly corrected this. Always patch the existing file. Regeneration loses styling, layout, and workflow differences.

### ⚠️ A2742-A-XXXX vs A2742-XXXX
Existing/demolition drawings use `A2742-A-XXXX` naming but the register lists them as `A2742-XXXX`. Scan must account for both.

### ⚠️ Section Counts Must Be Total Across All Sheets
When a section spans multiple tree sheets, show the TOTAL for that section, not the per-sheet subtotal.

### ⚠️ Counter Row Is a Single HTML Line
No line breaks. Must match exact text including whitespace.

### ⚠️ Remove Section Header Suffix When Items Change Status
After moving all entries from [XX] to [>>], remove the `XX:N` suffix entirely. Don't leave `XX:0`.

---

## Aseer Drawing Register Audit (absorbed from bim-drawing-audit + drawing-register-audit)

This section covers the complete workflow for auditing the Aseer Museum Drawing Status Tree against the filesystem, including designer scope-vs-deliverables analysis and RIBA stage mapping.

### Workflow

**Phase 1 — Parse the Register**

```python
import re
with open("Aseer_Drawing_Status_Tree.html") as f:
    html = f.read()
html_decoded = html.replace("&gt;", ">")
entries = re.findall(
    r'<span class="mk (ok|pn|xx)">\[(OK|>>|XX)\]</span>\s+(A2742[\-A]+\d+)\s+Rev\s+([\w\-]+)\s+(.+)',
    html_decoded
)
```

**Phase 2 — Scan Filesystem**

Search these locations (in priority order):
1. `02_Approved_Stamped_Packages/` — NRS-stamped PDFs
2. `06_Drawing_Source_Folders/` — active PDF/DWG files per section
3. `00_Stamped_CAD_Source/` — DWG files with stamp/approval
4. `05_Correspondence_Archive/` — old revisions

**Phase 3 — Cross-Reference**

Status priority: Stamped PDF → `[OK]`, Active source PDF/DWG → `[>>]`, Archive only → `[>>]` (check with user), No file → `[XX]`.

### Naming Convention Handling

- Register uses `A2742-XXXX`; existing/demo/section files use `A2742-A-XXXX`
- Some files have OneDrive suffix: `A2742-1100 (1).pdf`
- Always search for both naming variants
- Stamped PDFs: `A2742-XXXX_NRS_stamped.pdf`

### Designer Scope vs Deliverables (NRS Focus)

When asked \"what's missing from NRS\" or \"NRS scope vs deliverables\":

1. **Read the responsibility matrix** from `Contracts/NSR/Nissen SOW responsibilty matrix.pdf`
2. Cross-reference register categories to scope elements (walls, ceilings, doors, etc.)
3. Identify scope items with NO deliverable in register (e.g. roof terrace sunshade, specification package)
4. Identify items needing re-issue (old revision only)
5. Generate a workflow report with RAG status, gaps, and action items

See `references/nrs_scope_mapping.md` for the full Aseer Museum NRS responsibility matrix.

### RIBA Stage Mapping (Aseer Museum)

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

### Register Structure Reference

See `references/aseer-register-structure.md` for the full 19-section breakdown, file locations per section, naming variants, and RIBA counterpart mapping. The register document is `ASR-SAM-DWG-TREE-001` in `Completed Tender Package From NRS/Aseer_Drawing_Status_Tree.html`.

See `references/excel-register-cross-reference.md` for extracting document numbers from Excel Register Logs (openpyxl) and cross-referencing against plan HTML references.

### Payment Tracking Against Annex 4

When asked to chart payments against deliverables:

1. **Read Annex 4 payment schedule** from the main contract reference
   - 15 bundles (Sub-table A) = 65,153,751 SAR (87%)
   - 4 final payments (Sub-table B) = 9,773,062 SAR (13%)
   - Total: 74,926,813.83 SAR
2. **Map each bundle to deliverable status** using drawing register and contract scope
3. **Track actual payments** from invoice PDFs (PyMuPDF + tesseract OCR)
4. **Flag mismatches** — e.g. NRS invoices Stage 5 while Stage 4 stamping is incomplete

### CSS: Prevent Title Wrapping in Tree View

```css
.tree-box { white-space: pre; font-size: 7pt; overflow-x: hidden; }
```

Change `white-space: pre-wrap` → `pre` and drop font to 7pt when user reports line wrapping.

---

## Project File Boundary Audit (absorbed from project-file-boundary-audit)

Detect and resolve cross-project file contamination in Samaya BIM/TO project folders by examining naming conventions, consultant codes, drawing numbering, and project-scope cross-references.

### Trigger

- User says \"this file doesn't belong here\" / \"هذا الملف لا يتبع هذا المشروع\"
- User asks to \"clean up project folders\" / \"نظف مجلدات المشروع\"
- Routine QA of Samaya BIM project directories

### ⚠️ Entity Isolation Rule

NEVER move files between Samaya ↔ Moqtana / Tqanny / Sada_Uhud, or between any two projects, without explicit user confirmation. Always verify ownership first; report, then ask before any move/copy.

### Methodology

**1. Identify the suspected file(s)**

Key attributes to note:
- Prefix codes (e.g., `A2742-`, `ZNA3297`, `GHM-SAM-ZZ-MED`)
- Consultant/designer references (`NRS`, `Goppion`, `Glasbau Hahn`, `Hasenkamp`)
- Drawing discipline codes (`SC_01` for Showcase, `SDW-` for Shop Drawings)
- Type/ID numbering (`Type 2`, `ID.Nr. 08.03`, `Type 01`)
- Project code in filename (`MOC-ASEER-` vs `ZZ-` for Zamzam)

**2. Cross-reference with project scope**

| Attribute | Aseer Museum (3092) | Zamzam Museum (121/P0639) |
|---|---|---|
| Exhibition Designer | NRS (Nissen Richards Studio) | GHM, Goppion, Hasenkamp |
| Drawing prefix | A2742-18xx | GHM-SAM-ZZ-, A22-71-KZC-ID-DRW- |
| NRS involvement | Yes (designer) | No |
| Showcase codes | SC_01, SC_02, Type 1/2/3 | Different vendor taxonomy |
| Submittal files | `*_NRS_comments_*stamped.pdf` | No NRS pattern |

**3. Confirm mismatch**

Search the correct project's folders for matching files. If naming pattern, consultant code, or drawing discipline matches the other project's known structure, the file is misplaced.

**4. Action**

- Report finding with evidence (file name patterns, consultant cross-reference)
- Offer to move or copy to correct project folder
- Update memory with new cross-contamination patterns discovered

### Known Contamination Pattern: NRS Showcase Drawings (Aseer → Zamzam)

Pattern: `Freestanding Case-Type {N}- ID.Nr. {NN}.NN_SC_01_NRS_comments_*.pdf`

Why it's Aseer:
- NRS (Nissen Richards Studio) is Aseer's exhibition designer only
- SC_01 = NRS Showcase drawing sheet numbering (Aseer discipline 1800)
- Drawing prefix A2742-18xx matches Aseer's 1800_Showcases folder
- Zamzam has no NRS involvement

### Search Command for Cross-Contamination

```bash
# Search Zamzam folders for Aseer patterns
find "Zamzam Museum" -type f \( -iname "*NRS*" -o -iname "*SC_01*" \
  -o -iname "*A2742*" \) 2>/dev/null
```

### Pitfalls

- ⚠️ **OneDrive stubs** — many files appear as 0-byte stubs. Use `find` and `ls -la` to check actual sizes.
- ⚠️ **Same consultant for multiple projects** — e.g. Goppion provides showcases for both Aseer and Zamzam. Cross-reference drawing codes, not just consultant name.
- ⚠️ **Cross-copied reference files** — PM teams sometimes intentionally copy reference PDFs between projects. Check if file is a reference copy vs. project deliverable.
- ⚠️ **Zero-tolerance entity isolation**: Never move files between Samaya ↔ Moqtana/Tqanny/Sada_Uhud without user confirmation.

See `references/aseer-zamzam-patterns.md` for the specific Aseer→Zamzam showcase contamination pattern with full detection commands.
