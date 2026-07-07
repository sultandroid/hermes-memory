---
name: evm-analysis-chart
description: "Earned Value Management (EVM) — full lifecycle: S-curve chart creation, stakeholder-facing snapshot reports, vendor/subcontractor EV audits, payment reconciliation, specialist review inventory, and stakeholder reporting standards. Covers PV/EV/AC calculation from contract data, SVG chart production, formal report templates, and multi-tab HTML reports for construction projects."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [evm, earned-value, project-controls, svg-charts, construction, samaya, stakeholder-reporting, vendor-audit, payment-reconciliation]
    related_skills: [samaya-technical-office, claude-code, project-deliverable-audit]
---

# EVM Analysis & S-Curve Chart

## When to Use
- User asks for "EVM S-curve", "earned value chart", "S-curve analysis", "payment vs earned"
- Producing contract financial reports for construction/museum fit-out projects
- Need to visualize PV (Planned), EV (Earned), AC (Actual) over time
- **Also: when correcting previous EVM reports** — check `references/nrs-evm-data.md` for the corrected NRS data (DD vs IFC split, SI007 context)
- **Payment tracking:** `references/nrs-payment-register.md` has the full invoice-level breakdown of AC (INV-4755 advance, monthly instalments)

## Workflow

### 1. Gather Input Data

Extract from contract documents:
- **Total fee** and stage breakdown (Stage 4 DD/IFC, Stage 5 Off-site, Stage 5-6 On-site)
- **Payment schedule** per contract articles
- **Actual payments** made (bank transfers, invoices)
- **Deliverables delivered** (drawings count, stamping status, completion % per stage)

### 2. Calculate EVM Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| PV (Planned Value) | Sum of planned % × stage fee by month | What should have been earned by now |
| EV (Earned Value) | Actual delivered % × stage fee | What work has actually been produced |
| AC (Actual Cost) | Sum of all payments made | What has been paid |
| SV (Schedule Variance) | EV − PV | Negative = behind schedule |
| CV (Cost Variance) | EV − AC | Positive = under budget (paid less than earned). **But check: advance payment may inflate AC.** If advance (10%) was paid separately before monthly invoices, include it in AC — this can flip CV from positive to negative. |
| SPI | EV ÷ PV | <1.0 = behind schedule |
| CPI | EV ÷ AC | >1.0 = under budget |

### 3. Calculate S-Curve Coordinates

Chart coordinate system:
```
y = y_origin - (value_in_K × 0.25)
```

For the standard Samaya template (light, A4 portrait, no banner):
- Chart area: 650px wide × 400px tall, starting at y=95
- Y-axis: 0 SAR at y=357, 800K SAR at y=157
- **Scale: 0.25 px/K** (400px ÷ 8 = 50px per 200K block; 50px ÷ 200K = 0.25)
  - 0K → y=357, 200K → y=307, 400K → y=257, 600K → y=207, 800K → y=157
  - Formula: y = 357 - (K × 0.25)
- X-axis: 6 months spread across 540px (Feb=100, Mar=190, Apr=280, May=370, Jun=460, Jul=550, Aug=640)
- TODAY vertical line at Jun (x=460)

**With SI007 banner:** chart area shifts to y=117, origin to y=379.
- Formula: y = 379 - (K × 0.25)
- 0K → y=379, 200K → y=329, 400K → y=279, 614K → y=225, 800K → y=179
- See `references/samaya-svg-style.md` for full coordinate tables.

**CRITICAL: Never use 0.3 px/K.** This was the original bug — it shifts all Y-coordinates ~30px off, making every curve and arrow gap wrong. Double-check: (379 - y) × 4 should equal the expected SAR value in K within ±2K.

### 4. Build PV/EV/AC Monthly Progression

**PV (Planned):** Front-loaded S-curve. Small start, exponential growth, plateaus at 100%.
```
Feb=30K(349), Mar=90K(334), Apr=200K(307), May=400K(257), Jun=614K(203), Jul=700K(182), Aug=768K(165)
```
Formula check: 357 - (K × 0.25) → Jun=614K: 357-153.5=203.5≈203 ✓

**EV (Earned):** Separate Stage 4-A DD from Stage 4-B IFC. DD drawings delivered = ~460K (60% of Stage 4). IFC = SAR 0 until explicitly delivered. Uses dashed extension for forecast.
```
Feb=15K(353), Mar=40K(347), Apr=85K(336), May=180K(312), Jun=460K(242)
```
Formula check: 357 - (460 × 0.25) = 357 - 115 = 242 ✓

**AC (Paid):** Break down into individual invoices — always identify each by invoice number.
```
AC = INV-4755 (advance 10% = 120,900, paid separately) + INV-4781 (Stage 4 interim 1/2 = 345,657) = 466,557 total
```
Monthly progression: Feb=10K(376), Mar=30K(371), Apr=70K(361), May=180K(334), Jun=467K(262)

⚠️ **Advance payment handling:** The 10% advance (INV-4755 = 120,900) may be paid in a separate transaction from monthly instalments. In this case, the SAR 345,657 Alinma bank transfer paid INV-4781 (345,600 + 57 fees) only. The advance was a separate earlier payment. **Total AC = 466,557.** Check bank transfer purpose lines — if the purpose lists multiple invoice refs but the amount only covers one, the other invoice is likely unpaid.

### 4a. Honest EVM — External Factors

Before reporting schedule variance, check for **external factors** that distort SPI as a performance indicator:

- **SI007-type situations:** If a Site Instruction / change order has blocked work (e.g., 3D renders required before IFC submission), the schedule delay is **owner-directed**, not vendor performance failure.
- **Report separately:** Show EV for the blocked work as SAR 0, but flag the external blocker in a banner.
- **Adjusted narrative:** Don't say "vendor behind schedule (SPI=0.75)" — say "Stage 4-B blocked by SI007. SPI=0.75 reflects owner-directed workflow change, not vendor performance."
- **CPI stays valid:** Cost performance (CPI) is usually unaffected by external blockers and can still be reported as a vendor metric.

### 4b. Define Deliverable Brackets (Work Breakdown)

Before calculating EV, determine how the Stage fee is split across deliverables. **This is a user decision — propose brackets, don't just ask.**

For the NRS contract (Stage 4 = SAR 768,000 for museum interior architecture + scenography):

1. **Architecture DD:** NRS produces 251 DD drawings (walls, ceilings, doors, floors, stairs, setworks, showcases, joinery, interactives). This is the bulk creative work.
2. **Specialist review:** NRS as Design Lead reviews specialist DD submissions (MEP, AV, showcases, lighting).
3. **Coordination:** Determine who does this. If **Samaya handles coordination**, NRS's scope is smaller = DD bracket can be higher (user chose **70%** for NRS's actual NRS contract).
4. **IFC production:** Converting DD to IFC level.

**Process:**
1. Propose a bracket split (e.g., "DD @ 40%, specialist review @ 15%, IFC @ 45%") with rationale
2. The user may override (e.g., "70% for DD")
3. **Accept their number immediately** and recalculate. Do not debate or re-ask. A second "are you sure?" will frustrate — the user's domain knowledge on scope split is authoritative.
4. Document the chosen bracket in the report header/banner

**NRS precedent (from actual session — user chose 70% for DD):**\n- Architecture DD: 70% (user-defined) = SAR 538K ✓\n- Specialist review (Design Lead): 15% = SAR 115K\n- IFC production: 15% = SAR 115K (blocked by SI007)\n- Coordination: 0% (handled by Samaya)\n- Remaining Stage 4 after DD: 30% = SAR 230K\n- Total Stage 4: 100% = SAR 768,000

**Coordination check:** Always ask/confirm who handles coordination. If Samaya does it, NRS's residual scope is smaller = DD can be weighted higher.

### 4c. Report Compactness & Layout

**Every page must earn its keep.** If a sheet has fewer than ~60 lines of content (e.g., a 5-row table), merge it into another sheet rather than wasting a page.

**Signals to merge:**
- Content is only a small table + footer → merge into Sheet 1 after the fee table
- Content is a single SVG with no supporting elements → combine with another chart sheet
- The total page count drops from 4 to 3 without losing unique information

**When merging:**
1. Add a heading (e.g., `<h2>Payment Register</h2>`) to distinguish the section within the larger sheet
2. Insert after the last related content block (e.g., after Fee Structure table)
3. Renumber all sheet footers to the new total (e.g., `1/4 → 1/3`)
4. Verify no orphan `SHEET X/4` references remain

**Avoid duplication across sheets:**
- Bracket breakdown (DD 70%, specialist 15%, IFC 15%) should appear **once** — in the S-curve metrics bar, not also in a separate note box on Sheet 1
- The S-curve SVG internal footer text is redundant with the HTML footer-strip directly below — remove it
- EVM Summary list on Sheet 4 duplicates Sheet 1 status bullets — remove the Sheet 4 version
- S-curve legend (PV = planned, EV = earned, AC = actual) is obvious from metric cards — remove it

**Goal:** 3 sheets maximum for a subcontract EV snapshot. Sheet 1 = snapshot + fee + payment. Sheet 2 = specialist details. Sheet 3 = S-curve.

### 4d. Formal Theme — No Dashboard Colors

**User preference (explicitly reinforced this session):** The report must look like a formal document (legal brief / corporate quarterly), NOT a dashboard.

**Color palette (strict, enforced):**
- `#1E293B` (navy) — headers, titles, primary accents
- `#000000` (black) — body text, key values
- `#444444` (dark gray) — secondary text
- `#64748B` (medium gray) — muted labels, footnotes
- `#CBD5E1` (light gray) — borders, dividers, gridlines
- `#F1F5F9` (very light gray) — subtle backgrounds
- `#FFFFFF` (white) — main background
- **No green, amber, red, or blue** except in status tags (which are small inline elements, not large boxes)

**Metric cards:** Use `#F1F5F9` background with `#CBD5E1` border for ALL cards. Remove colored backgrounds (#F0FDF4 green, #EFF6FF blue, #FEF3C7 amber, #FEF2F2 red). Only the VALUE text may hint at positive/negative (bold black with negative values possibly in red).

**Note boxes:** Use `#FAFAFA` background with navy (`#1E293B`) left border. Remove colored tints and colored left borders. Warning notes use the same style — no amber backgrounds.

**Chart lines:** PV = navy (`#1E293B`), EV = black (`#000`), AC = gray (`#64748B`). No green/blue/amber curve colors. Remove all gradient/transparency fills under curves.

**Exception — status tags:** Keep `.tag.g` (done), `.tag.a` (pending), `.tag.r` (blocked), `.tag.n` (future) as small colored inline badges — these are essential for quick visual scanning by stakeholders.

### 4e. Everything as Lists — No Prose Paragraphs

**User preference (explicit, repeated):** ALL notes, assessments, summaries, and explanations must be formatted as bullet lists. Prose paragraphs are rejected.

**Rules:**
1. Every `<div class="note-box">` contains a `<ul>` — no bare `<p>` text
2. Every assessment -> bullet list
3. Every status -> bullet list
4. Every impact/evaluation -> bullet list
5. Even single-sentence notes become a single `<li>` in a `<ul>`
6. Headings remain bold (`<b>`) but the body is always a list

**CSS for consistency:**
```css
.note-box ul { margin:0.8mm 0 0 2mm; font-size:7.2pt; line-height:1.55; }
.note-box li { margin-bottom:0.2mm; }
```

### 4f. Humanize — Remove AI Patterns

After generating the report, do a **humanization pass** on ALL text content:

**Remove:**
- Transitional phrases: "In conclusion", "Furthermore", "Moreover", "It is worth noting that", "As we can see", "Let's delve into"
- Formulaic structures: "First... Second... Finally..."
- Hedging: "arguably", "essentially", "importantly", "notably"
- Self-referential meta: "This report will explore", "The purpose of this section is to"
- Staccato `+` syntax in prose (OK in tables)
- Dramatic lead-ins to numbers

**Apply:**
- Contractions: "don't", "isn't", "it's", "can't", "hasn't"
- Active voice over passive
- Varied sentence length (2-15 words)
- Short paragraphs (3-4 sentences max)
- Plain number presentation: "SAR 812K" not "a total of SAR 812,000 has been paid"

**Tone:** Write as a competent professional speaking to a peer. Not academic, not marketing, not robotic.

**Output:** Only the rewritten text — no commentary about what you changed.

### 4g. Language Preference — HOLD not REJECT

**User corrected explicitly:** When recommending against paying an invoice, use "HOLD" not "REJECT". "HOLD" implies it can be revisited when conditions change. "REJECT" is final and confrontational.

**Examples:**
- ✓ "INV-4825 — HOLD until Stage 5 work is confirmed"
- ✗ "INV-4825 — REJECT (premature)"
- ✓ "Pay ~45K, HOLD ~36K"
- ✗ "Pay ~45K, REJECT ~36K"

Apply this across all reports, not just EVM — any invoice recommendation should say "HOLD".

### 4h. Stakeholder Language — Every Word Must Serve the Decision-Maker

**User correction history:** The user explicitly rejected status labels like "EXTRACTED", "PDF ONLY", "REF ONLY" as useless to stakeholders. Every table column, status cell, and note must answer: **"What does this mean for the decision-maker?"**

**Rule:** Every status column must be rewritten so a project owner or finance director can immediately understand:
- Is this done? (✓)
- Is this blocked? What by? (⚠️ BLOCKED — SI007)
- Is this at risk? What action needed? (🔴 GAP — escalate to NRS)
- Is this a decision they need to make? (⚠️ DECISION NEEDED: approve renders to unblock IFC)

**Before (rejected):**
```
<th>Status</th>
<td><span class="tag g">EXTRACTED</span></td>
<td><span class="tag a">PDF ONLY</span></td>
<td><span class="tag a">REF ONLY</span></td>
```

**After (stakeholder language):**
```
<th>Stakeholder Value</th>
<td><span class="tag g">DEFINES NRS VS SAMAYA RESPONSIBILITIES</span></td>
<td><span class="tag a">DEFINES NRS OBLIGATIONS VS MAIN CONTRACT — NEEDS EXTRACTION</span></td>
<td><span class="tag n">BACKGROUND — NOT CRITICAL FOR PAYMENT</span></td>
```

**Pattern for all table status columns:**
| Old (jargon) | New (stakeholder) |
|---|---|
| "All received. 0 stamped." | "Complete — usable for IFC production" |
| "10/10 Complete" | "DELIVERED ✓ — all drawings submitted" |
| "DONE / NOT TRACKED" | "DELIVERED ✓ / ⚠️ NO TRACKING IN PLACE" |
| "0 — Blocked by SI007" | "⚠️ BLOCKED by SI007 — Decision needed" |
| "224,757 PAID / 466,443 REMAINING" | "⚠️ HOLD INV-4825 — Stage 5 billed prematurely" |
| "INV-4825 (90K) DUE" | "⚠️ REJECT — Stage 5 not yet earned" |

**When rewriting a table:**
1. Ask: "If a stakeholder reads this cell, do they know what to do?"
2. If the answer is no, replace the text with an action-oriented status
3. Use the template's existing tag classes (g=green=good, a=amber=warning, r=red=risk, n=gray=future)
4. For critical gaps, prepend ⚠️ or 🔴
5. Change the column header from "Status" to "Stakeholder Value" or "Action Required"

### 5. SVG Chart Structure

The SVG chart must match the **Samaya template style** (not dark theme):

- **Background:** `#FFF` white, not dark
- **Size:** Width 650 (portrait A4 compatible, 174mm), variable height depending on table data
- **Title:** `#1E293B` (matches template's `h3` color and `th` background)
- **Body text:** `#000` black
- **Metric cards:** Use Samaya tag colors:
  - Green (PV, CV): `fill="#F0FDF4"` bg, `stroke="#BBF7D0"`, text `#15803D`
  - Blue (EV, Work Done): `fill="#EFF6FF"` bg, `stroke="#BFDBFE"`, text `#1D4ED8`
  - Amber (AC, Owed): `fill="#FEF3C7"` bg, `stroke="#FDE68A"`, text `#92400E`
  - Red (SV, Billed Not Earned): `fill="#FEF2F2"` bg, `stroke="#FCA5A5"`, text `#B91C1C`
  - Gray (Future): `fill="#F1F5F9"` bg, `stroke="#CBD5E1"`, text `#64748B`
- **Chart area background:** `#FAFAFA` (matches template's alternating row)
- **Gridlines:** `#E5E7EB` thin (0.5px)
- **Axes:** `#CBD5E1` 0.5px
- **TODAY line:** Dashed, amber `#92400E`
- **Assessment box:** Yellow warning style (`fill="#FEF3C7"`, `stroke="#FDE68A"`)
- **Table header row:** `fill="#1E293B"` with white text (matches template's `th`)
- **Footer:** `#000` line, `#64748B` text, centered
- **No dark backgrounds, gradients, shadows, or glow effects**

### 6. Drawing the Curves

- **PV:** Solid green (`#22C5E`, stroke-width 2), dot at current month
- **EV (actual):** Dashed blue (`#3B82F6`, stroke-width 2, dasharray 4,2), dot at current month
- **EV (forecast):** Half-opacity dotted blue (stroke-width 1, dasharray 2,2), connecting beyond current month
- **AC:** Solid amber (`#F59E0B`, stroke-width 2), dot at current month

### 7. SV/CV Arrows

- **SV arrow:** Vertical from EV dot up to PV dot. Red (`#B91C1C`), with arrowhead polygon
- **CV arrow:** Vertical from EV dot down to AC dot. Green (`#15803D`), with arrowhead polygon

### 8. Data Table Below Chart

Include a monthly EVM data table as SVG text elements:
- Table header: `#1E293B` fill rect with white text
- Alternating rows (white / `#FAFAFA`)
- Current month values highlighted in color
- Forecast months in gray italic

### 9. Payment Reconciliation Workflow

When updating AC from a payment folder:

1. **List files in the payment directory** — sort by size to detect duplicates (same size = duplicate)
2. **Remove duplicate PDFs** — keep the original, delete `(1)` copies
3. **OCR each unique invoice** using fitz (PyMuPDF) + tesseract:
   - Image-based PDFs: extract PNG at 200dpi, then `tesseract <png> stdout -l eng`
   - Embedded text: `page.get_text()` from fitz
   - Arabic/English mixed: `tesseract -l ara+eng`
4. **Extract for each invoice:** date, invoice ref, description, sub-total, VAT, total due, bank details
5. **OCR the bank transfer receipt** — extract transaction date, amount, exchange rate, fee, beneficiary, purpose text
6. **Cross-reference amounts:** Does the bank transfer amount match any single invoice amount (within fees)?
   - If yes → that invoice is paid
   - If the bank receipt purpose text *mentions* multiple invoice refs but amount only covers one → the others are unpaid
7. **Build the complete ledger** — sum paid invoices = AC
8. **Check for separate advance payments** — the 10% advance may be paid in a separate transaction not captured in the main bank transfer. If the bank transfer amount ≈ one monthly invoice (not monthly invoice + advance), then the advance was paid separately.
9. **Update the AC breakdown** in the EVM legend to show individual invoices
10. **Write a PAYMENT_LEDGER.md** in the payment folder with the complete invoice register, bank transfer details, and reconciliation notes. This becomes the source of truth for the next session.

### 9b. Multi-Transfer Payment Discovery (Critical Pattern)

**Do NOT assume a single bank transfer covers all paid invoices.** In this project, NRS had **three separate Alinma bank transfers** for three separate invoices:

| Receipt File | Date | Amount (SAR) | Paid Invoice |
|---|---|---|---|
| Nissen Richards Studio 10.pdf | 25 Feb | 120,900.00 | INV-4755 (Advance) |
| Nissen Richards Studio 781.pdf | 4 May | ~345,600 | INV-4781 (Stage 4, 1/2) |
| Nissen Richards Studio 805.pdf | 17 May | 345,600.02 | INV-4805 (Stage 4, 2/2) ✓ |

**Key signals that more transfers exist:**
- The bank receipt purpose text mentions more invoice refs than the transfer amount can cover
- Total paid (bank transfer amounts) ≠ single invoice × count
- The bank receipt file name doesn't match the invoice pattern (e.g., "Nissen Richards Studio 805.pdf" vs "INV-4805.pdf")

**When building AC:**
1. List ALL files in the Payment/ directory — not just the PDFs named INV-*.pdf
2. Bank receipts have non-obvious names: check every PDF that is NOT an invoice
3. OCR every bank receipt and extract: date, EUR/SAR amount, exchange rate
4. **Cross-reference by EUR amount**: each invoice was paid at a different exchange rate, so the EUR amounts differ even if the SAR amounts are identical
5. If a EUR amount × exchange rate ≈ an invoice amount exactly (within 2 SAR of invoice), that invoice is **confirmed paid**

___4. If the bank purpose text mentions more invoice refs than the amount covers, that is a **strong signal** more transfers exist — investigate all files, don't assume the extra refs are unpaid.___

### 9c. Separate Purchase Orders (Non-Invoice Payments)

Sometimes payments to the same vendor come via **Purchase Orders**, not invoices under the main contract. In this project:
- **PO P01824** — "3D Render Viewpoints — RIBA Stage 3" — SAR 236,250 for 27 viewpoints @ SAR 8,750 each
- This was the **SI007-mandated** 3D render package that blocked IFC production
- It **superseded** the optional "Updated Visuals" line (SAR 75,000) in the NRS main contract
- It is a **separate contract** from the NRS main agreement (SAR 1,209,000)

**When you see "optional" or "additional" lines in a fee table, investigate whether they were done via a separate PO.** Search the Contracts/ directory for Purchase Orders, not just invoices. If found:
1. OCR the PO and extract: description, quantity, unit price, total, date
2. Note it in the fee table as "superseded by PO" with an amber tag
3. Add a blue info note below the fee table with full PO details
4. Update SI007/delay banners to reference the PO (e.g., "SI007 mandated 3D renders via PO P01824")
5. Copy the PO PDF to the audit folder for traceability

**Pitfall:** The optional line estimated SAR 75,000. The actual PO was SAR 236,250 — 3× higher. Always check actual POs.

### 9e. ER Document Cross-Reference (Employer's Requirements)

When the project has an ER document (extracted text in `Docs/00_Project_Charter/extracted_text/er_document.txt`), incorporate relevant clauses into the report to provide the formal process framework:

**Key clauses to look for:**
1. **IFC → NOC → AFC pathway** — ER defines the formal submission pipeline: Contractor submits IFC docs to PMC → PMC issues No Objection Certificate → Contractor re-issues as AFC. This sets stakeholder expectations on timing.
2. **Internal review first** — ER requires the Contractor's designer to self-certify before external submission. NRS cannot bypass QA.
3. **Complete packages only** — ER explicitly rejects partial submittals. IFC packages must include specs, drawings, method statements, ITPs, material submittals all at once.

**Add a new section (not a note) on Sheet 1** titled "ER Requirements — IFC & Submittal Process" with:
- A 3-row grid (simple table or div) explaining each requirement in plain language
- A blue info note (`<div class="note b">`) with 3 stakeholder-facing takeaways:
  - What it means for NRS deliverables
  - What it means for the timeline
  - What decision the stakeholder needs to make

### 10. Propose, Don't Ask (Bracket Determination)

**User preference (explicitly corrected):** When determining EV bracket splits (what % of Stage fee each deliverable phase represents), the user does NOT want to be asked open-ended questions. Instead:

1. **Analyze the scope** yourself using the contract data, deliverable register, and any coordination/scope notes
2. **Propose a specific bracket** with written rationale
3. **Present it as a recommendation**, not a question
4. If the user overrides (e.g., "70% for DD"), **accept immediately without debate** and recalculate. Do NOT re-ask, re-propose, or say "are you sure?" — the user's domain knowledge on scope split is authoritative.
5. Document the chosen bracket in the report banner/header

**Example (good):** "Proposed brackets: Architecture DD 40% (substantial 251-dwg set delivered). Specialist review 15%. IFC 45%. Accept?"

**Example (bad — don't do):** "What percentage should I use for the DD drawings?"

### 9d. Organizing Audit Outputs

After completing an NRS audit/review:
1. **Place reports in** `Docs/07_Reports/07.5 Audit Report/NRS/`
2. **Place source PDFs in** `Contracts/NSR/Payment/` (invoices + bank receipts)
3. **Place payment ledger in** the audit folder, not the payment folder (move it there after creation)
4. **Keep SVGs in** `_assets/` subfolder under the audit report dir
5. **Sync the source report** back to `Completed Tender Package From NRS/` if it was originally created there
6. **Remove duplicate PDFs** (same file size = probable duplicate; confirm by comparing bytes)

### 9e. Document the Correction History

Maintain a "Key Corrections History" section in the EVM data reference that tracks every EVM number change with the reason. This prevents repeating the same mistakes and provides an audit trail. Each entry should record:
- What changed (e.g., "AC corrected from 466K to 812K")
- Why (e.g., "Discovered 3rd bank transfer for INV-4805")
- When (date and session context)

The 10% advance (SAR 120,900) is allocated **proportionally** across all stages, NOT deducted entirely from Stage 4:

```
Stage 4 share:   10% × 768,000 = 76,800   →  net balance = 691,200  (57.2% of total)
Stage 5 share:   10% × 270,000 = 27,000   →  net balance = 243,000  (20.1%)
Stages 5-6 share: 10% × 171,000 = 17,100  →  net balance = 153,900  (12.7%)
Total:            120,900                            = 1,088,100  + 120,900 = 1,209,000
```

The payment milestones table should use these **net amounts** so percentages sum to 100%.

### 10. Comprehensive Number Audit

After every EVM report update, run a **cross-document audit** to catch stale values and ensure all numbers are consistent across every sheet and SVG.

**Checklist (run after every update, not just initial creation):**

1. **Contract constants check:** Verify `1,209,000`, `768,000`, `270,000`, `171,000` appear in the HTML
2. **Invoice references:** All 4 invoice refs present: `INV-4755`, `INV-4781`, `INV-4805`, `INV-4825`
3. **Invoice amounts:** `345,600` (×2 for INV-4781/4805) and `90,000` (INV-4825)
4. **EVM metrics:**\n   - `AC` = sum of ALL paid invoices, not just the ones found in the first pass (e.g., final AC = `812,100` = `120,900` + `345,600` + `345,600`)\n   - `EV` = what's actually delivered (e.g., `538,000` for DD @ 70% bracket)\n   - `PV` = planned to date (e.g., `614,000`)\n   - `SV` = EV minus PV in K format (e.g., `76K`)\n   - `CV` = EV minus AC in K format (e.g., `274K`)\n   - `CPI` = EV/AC (e.g., `0.66`)\n   - `SPI` = EV/PV (e.g., `0.88`)
5. **Percentage sums:** Check every table adds to 100%:
   - Fee structure: `63.5%` + `22.3%` + `14.2%` = `100%`
   - Milestones (net after advance): `10.0%` + `57.2%` + `20.1%` + `12.7%` = `100%`
6. **Stale value purge:** None of these should remain: `647,100`, `466,500`, `224,757`, `345,657` (old AC), `33/251`, `"IFC package (100%)"`
7. **Drawing count:**
   - Stamped: `33/247` (not `33/251`)
   - Total drawings: `247` (33 stamped + 214 pending)
8. **Outstanding:** `90,000` = INV-4825 only (INV-4805 was confirmed paid via 3rd bank transfer)
9. **Paid %:** AC/Total (e.g., `466,557/1,209,000 = 38.6% ≈ 39%`)
10. **Sheet counters match:** All sheets must use the same denominator (e.g., all `/6`)
11. **No landscape overrides:** No `style="width:297mm;min-height:210mm;"` outside CSS
12. **No "IFC 100%" claims** — Stage 4-B IFC is not delivered unless explicitly confirmed

Use `execute_code` with regex to scan the HTML file for all values above. Fail the build if any check fails.

### 11. Word Document Report Generation

Some stakeholders prefer .docx over HTML. After generating the HTML EV snapshot, produce a companion Word document:

**Workflow: pandoc → python-docx restyle**

```bash
# Step 1: Convert HTML to raw docx
pandoc report.html -o report.docx
```

The pandoc output will have basic structure (headings, tables, lists) but no styling. Images (logos, SVGs) will fail if referenced as relative files — use absolute paths or accept the placeholders.

**Step 2: Restyle with python-docx**

Build a fresh docx from scratch using python-docx, using the HTML data as source. Structure:

| Document section | Elements | python-docx technique |
|---|---|---|
| **Document strip** (ref/code/rev) | Single paragraph, bottom border | `OxmlElement('w:pBdr')` with `w:bottom` |
| **Title block** | Centered subheader + h1 + subtitle lines | Multiple centered paragraphs, varying font sizes (8.5 / 22 / 12 pt) |
| **Metric cards** | 1-row table with 6 cells | Each cell has 3 stacked paragraphs (label/value/sub). Subtle gray shading (`F8FAFC`) with thin borders |
| **Section headings** | Uppercase text + bottom border line | `OxmlElement('w:pBdr')` with `w:bottom`, size 10pt bold |
| **Data tables** | Header row dark bg + white text, alternating row colors, totals row | `set_cell_shading(cell, '1E293B')` for header, `'F8FAFC'` for even rows, `'F1F5F9'` for totals |
| **Note boxes** | Left border accent (navy 3pt) + gray bg | `OxmlElement('w:pBdr')` with `w:left` (sz=18, color='1E293B') + `w:shd` (fill='F8FAFC') |
| **Bullet lists** | Standard •-prefixed paragraphs | Left-indented paragraphs with bullet run prefixed |
| **Footers** | Centered text with top border | `w:pBdr` with `w:top`, centered alignment |
| **Page breaks** | Between sheets | `run.add_break(WD_BREAK.PAGE)` |

**Color scheme for Word documents:**
- `#1E293B` (navy) — headers, title, accents
- `#FFFFFF` (white) — header row text
- `#F8FAFC` — even row shading
- `#F1F5F9` — totals row / metric card bg
- `#E2E8F0` — table borders
- `#475569` / `#64748B` — muted text, footers
- Metric card values: `#92400E` (amber) for EV/AC/SV, `#991B1B` (red) for CV, `#166534` (green) for positive metrics
- Font: **Calibri** throughout (the Samaya template font)

**Resizing trick for metric cards:**
```python
metric_table = doc.add_table(rows=1, cols=6)
for i, cell in enumerate(metric_table.rows[0].cells):
    cell.width = Cm(3.1)  # evenly distribute across page width
```

**Page setup:**
```python
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(1.5)
section.bottom_margin = Cm(1.5)
section.left_margin = Cm(2.0)
section.right_margin = Cm(2.0)
```

**Avoid set_row_height** — it makes rows inflexible with wrapped text. Let content determine row height.

**Pitfalls:**
- pandoc cannot convert SVGs to Word-compatible images without `rsvg-convert` installed. The chart will be a placeholder — accept this or generate a PNG fallback separately.
- Relative image paths (`_assets/logo.png`) will not resolve. Either use absolute paths before converting, or skip images (the text content is the priority).
- python-docx `autofit = True` with `Cm()` column widths works best for table layout.
- For the note box left-border effect, use `w:pBdr` with `w:left` and sz=18 (3pt) — don't use table borders.
- Metric card cells need 3 separate paragraphs, not runs within one paragraph, to stack text vertically.

**Example project:** See `Aseer_NRS_EV_Snapshot.docx` at `Contracts/02_NRS_Contract/03_Analysis_Reports/` for a complete implementation.

---

## 12. Contract Claim Audit Workflow

When a vendor/consultant makes verbal claims about payment, EV, schedule, or scope (from meeting notes, call summaries, or emails), use this structured audit workflow **before** entering negotiation.

### 12.1 Meeting-to-Claims Extraction

Extract discrete, testable assertions from meeting notes:

| Bad (vague) | Good (auditable claim) |
|---|---|
| "He thinks the drawings are worth more" | "Claim: DD drawings = 90% of IFC package value" |
| "He wants to get paid" | "Claim: Pay INV-4825 (SAR 90K) in full" |
| "He wants a different payment schedule" | "Claim: Split remaining SAR 306,900 into equal monthly instalments" |
| "He says it's not his fault" | "Claim: No payment impact from SI007 block — NRS not responsible" |

**Rule:** Each claim must be:
- **Specific** (amount, %, date, reference)
- **Testable** (can be checked against contract text or data)
- **Independent** (one claim per assertion — don't bundle)

### 12.2 Contract Article Mapping

For each claim, find the relevant contract article(s) and extract the verbatim text.

**Mapping table template:**
```
| Claim | Relevant Article | Verbatim Text | Supports Claim? |
|-------|-----------------|---------------|-----------------|
| DD=90% | Art. 4.1 | "IFC CAD package for RIBA Stage 4" | Neither — split not defined |
| Pay INV-4825 | Art. 5 / Art. 11.2 | "Review for conformity with Stage 4" / "schedule agreed in advance" | Partially — Stage 5 dependent on IFC |
| Equal instalments | Art. 18 | "Alterations must be in writing" | No — changes need amendment |
| "Not my problem" | Art. 3.2, 21.2 | NRS not responsible for delays by others; no penalty for Customer delays | Partially — no penalties, but payment = f(work done, not time) |
```

**Key questions for each article:**
- Does the article directly address the claim?
- Does it limit or qualify the claim?
- Are there dependencies (e.g., Stage 5 needs IFC per Art. 5)?
- What formality is required (Art. 18 — written amendments)?

### 12.3 Claim Audit — Structure Per Claim

For each claim, produce a structured audit:

```
**Claim N — [Title]**
- Contractual Basis: [What the contract says, exact text]
- Analysis: [How the claim interacts with the contract — supported, contradicted, or undefined]
- Limiting Factors: [Any contract terms that constrain the claim]
- Verdict: [Supported / Partially Supported / Not Supported / Undefined in Contract]
- Recommended Response: [What to say / concede / push back on]
```

### 12.4 Multi-Scenario Financial Modeling

Model 3 scenarios to show stakeholder the range of outcomes:

| Scenario | Description | When to Use |
|----------|-------------|-------------|
| **A — Full Acceptance** | Accept all vendor claims without modification | Baseline for "what they want" — shows max cost |
| **B — Recommended** | Partial acceptance — concede low-cost items, push back on high-risk ones | The negotiating position — balanced |
| **C — Conservative** | Maintain contract terms, concede nothing | Fallback — shows "what the contract says" |

**Financial metrics to recalculate per scenario:**
- Total EV (recalculate with new bracket splits per claim)
- Total Paid (with any new invoices)
- CV = EV - AC
- CPI = EV / AC
- Remaining at Risk (total contract - paid - earned)
- Narrative: "What changes, what stays the same"

**Template:**
```
| Metric | Baseline | Scenario A | Scenario B | Scenario C |
|--------|----------|------------|------------|------------|
| Total EV | SAR 483K | SAR 753K | SAR 753K | SAR 483K |
| Paid | SAR 812K | SAR 902K | SAR 859K | SAR 812K |
| CV | -SAR 329K (CPI=0.59) | -SAR 149K (CPI=0.83) | -SAR 106K (CPI=0.88) | -SAR 329K (CPI=0.59) |
| Remaining at Risk | SAR 397K | SAR 307K | SAR 350K | SAR 397K |
```

### 12.5 Producing the Formal Audit Response

After the audit analysis, produce a formal response document:

**Format:** .docx (python-docx) for stakeholder distribution. See Section 11 (Word Document Generation) for styling.

**Structure:**
1. **Context** — what triggered the audit (meeting, date, participants)
2. **Vendor Position** — each claim stated verbatim
3. **Contract Audit** — per-claim analysis with article references
4. **Financial Scenarios** — 3 scenarios with before/after metrics
5. **Contract References** — table of relevant articles
6. **Recommendations** — numbered response strategy

**Tone rules (from Sections 4d-4h):**
- Formal (navy/gray/black theme, no dashboard colors)
- Stakeholder language — every cell answers "so what?"
- Use "HOLD", never "REJECT" for invoices
- Bullet lists over prose
- Humanize — contractions, active voice, no AI cadence

**Python-docx production pattern:**
```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Set default font
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(10)

# Helper: colored heading
def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

# Helper: data table
def add_table(headers, rows):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    # Header row: navy bg + white text
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(9)
    # Data rows
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.rows[r+1].cells[c]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    return table
```

### References for this section

- `references/contract-claim-audit-worked-example.md` — NRS Mr. Jim meeting: 4 claims, contract mapping, 3 scenarios, recommended response

---

## Validation

Delegate chart creation to **Claude Code** (subagent) with these checks:

1. SVG is valid XML (parse with xml.etree.ElementTree)
2. All 22+ polyline coordinates are mathematically correct against the Y-axis formula
3. SV and CV arrow gaps match the expected pixel values:
   - SV gap = (EV_y − PV_y) × pixels_per_K_inverse = expected SAR
4. No orphan SVG tags (duplicate attributes, unmatched tags)
5. White background, no dark theme elements
6. All metric cards show correct SAR values
7. Sheet counters consistent (e.g., "SHEET 5/6") — all must use same denominator
8. No landscape sheet divs — every `<div class="sheet">` must be standard A4 portrait
9. If a SI007 banner exists, verify text is accurate and positioned at top of SVG

### Pitfalls

- **🚫 CRITICAL: NEVER use dark theme.** The Samaya template is white/light (`#FFF` background). Dark SVGs (`#0F172A`, `#1E293B` fills with white text) will be rejected.
- **🚫 CRITICAL: Do NOT use landscape orientation** in SVG or sheet divs. A4 portrait only (210mm × 297mm via `class="sheet"`).
- **🚫 CRITICAL: AC can change when new bank transfers are discovered.** Check ALL PDFs in Payment/ directory — bank receipts may have non-obvious filenames. OCR every bank receipt and cross-reference EUR × rate against invoice SAR amounts.
- **🚫 CRITICAL: Formal theme — no dashboard colors.** The user rejected colored metric cards, colored chart curves, and colored note backgrounds multiple times this session. Navy/gray/black only. See Section 4d.
- **🚫 CRITICAL: Everything as lists, not prose.** User explicitly rejected paragraphs in notes/assessments. Every note box must use `<ul>`. See Section 4e.
- **🚫 CRITICAL: Humanize the text after generating.** Remove AI patterns (transitional phrases, hedging, self-referential meta, staccato syntax). Use contractions and active voice. See Section 4f.
- **🚫 CRITICAL: Say "HOLD", never "REJECT"** for invoice recommendations. "HOLD" is revisitable. "REJECT" is confrontational.
- **🚫 CRITICAL: Read the actual signed contract payment article before arguing about payment structure.** EV analysis and contract payment terms can tell different stories. The NRS contract Art. 11 says "Monthly Instalments" for all stages — yet the EV snapshot assumed milestone-based payment. The vendor was technically correct about the contract language. Always extract the verbatim payment table from the signed PDF (Art. 11.x) before building a negotiation position. See `references/nrs-negotiation-worked-example.md` for the full example.
- **🚫 "Monthly Instalments" does NOT mean the invoicing schedule is automatically agreed.** Art. 11.2 may require the invoicing schedule to be "agreed in advance" separately. Even if the contract says "monthly," the specific amounts, dates, and triggers per instalment need separate agreement. Check for this clause before assuming the vendor can invoice at will.
- **Specialist review EV denominator pitfall:** When calculating per-package specialist review EV, the effort weight denominator must be **365 specialist items only**, not 605 (which includes architectural DD items). Using 605 understates EV by ~40%. Formula: `EV = review% × (package_items/365) × 115K`. If you use 605 as denominator, correct to 365.
- **Do NOT assume values** — always verify PV/EV/AC against actual contract data.
- **Do NOT redesign HTML reports from scratch.** Always patch existing files.
- **Separate Stage 4-A DD from Stage 4-B IFC** in EV calculations.
- **Break down AC by invoice number** — never lump payments without identifying each invoice.
- **Stage 5 EV is always zero** until off-site fabrication reviews are evidenced.
- **Check for external blockers** before reporting SPI as vendor performance.
- **Sheet counters must be sequential** — all sheets use the same denominator.
- **Merge small content** — a 5-row table doesn't deserve its own page. See Section 4c.
- **Remove duplication across sheets** — bracket breakdown, EVM summary, SVG footer, legend should each appear once.
- **User expects /workflow outputs** — produce process-oriented deliverables.
- **The user writes in short directives** — respond with bullet points and tables.
- **Propose brackets, don't just ask** — recommend a split with rationale, accept override.
- **Accept user's number immediately** — do not debate or re-ask.

---

## Stakeholder Reporting Standards (absorbed from stakeholder-reporting)

Write for the person who will read this in 30 seconds before a meeting. These standards apply to all EVM reports, vendor audits, and decision-maker documents.

### Core Principles

**1. Stakeholder Language**
- Never use internal processing statuses — "EXTRACTED", "PDF ONLY", "REF ONLY", "NOT TRACKED" mean nothing to a decision-maker
- Replace with what it means for them: "Defines NRS vs Samaya responsibilities" / "Payment basis, all figures verified"
- Every table cell, label, and note must answer "so what?" for the reader
- If a reader would ask "why should I care?", rewrite it

**2. Kill AI Patterns**
- No transitional phrases: "In conclusion", "Furthermore", "It is worth noting", "As we can see"
- No hedging: "arguably", "essentially", "importantly", "notably"
- No formulaic structures: "First... Second... Finally..."
- No self-referential meta-commentary: "This report will explore..."
- Write as a competent professional, not an AI

**3. Format for Scanning**
- Bullet points over prose blocks — every note/assessment should be a `<ul>` list
- Tables with clear columns — stakeholders scan green/amber/red tags
- Metric cards or inline summaries — never bury key numbers in paragraphs
- Short paragraphs (3-4 sentences max) with active voice
- Contractions where natural ("can't", "isn't", "we're")

**4. Formal Design**
- Color palette strictly: navy (#1E293B), black (#000), gray (#64748B/#CBD5E1), white (#FFF)
- Only use green/amber/red/blue for **status communication** (tags that signal done/pending/blocked)
- No emojis, no decorative icons, no gradient backgrounds
- Tags used sparingly — each color must mean something specific
- Metric cards: subtle gray backgrounds, not colored tints

**5. Day-Snapshot Philosophy**
- Reports are "as of today" snapshots unless explicitly asked for a trend study
- Include only: what's delivered, what's paid, earned value, variance, outstanding, next steps
- Strip: contract structure analysis, ER requirements, workflow process maps, resource schedules, penalty clause legal analysis
- When in doubt: if it doesn't affect a decision this week, cut it

---

## Vendor EV Audit Workflow (absorbed from vendor-ev-audit)

Build a day-snapshot EV report for a vendor/subcontractor. Format: clean report (HTML, Samaya template), stakeholder language, no AI patterns.

### Structure (4 sheets)

| Sheet | Content |
|---|---|
| 1 — Snapshot | Title + logos (Samaya + vendor), 6 metric cards (EV, AC, CV, SV, DD Drawings, Invoices Paid), status as bullet-point list, fee summary table |
| 2 — Payment Register | All invoices with amounts, dates, proof references (bank receipts), status tags. No bar chart (duplicates S-curve on Sheet 4). |
| 3 — Specialist Packages | Table per specialist package: total expected items, NRS work done, status, delay cause, EV contribution. Consolidate note boxes into ONE. |
| 4 — EVM Analysis | S-curve chart (PV/EV/AC polylines) with tight viewBox. Metrics bar above chart with all values. No legend, no EVM Summary (duplicates Sheet 1). |

### Style Rules (Vendor Reports)

- **Stakeholder language only** — every cell answers "what does this mean for me?"
- **Formal theme — no dashboard colors.** Metric cards: `#F1F5F9` gray. Chart lines: navy (`#1E293B`) PV, black (`#000`) EV, gray (`#64748B`) AC.
- **Human tone** — contractions, active voice, short sentences
- **No duplication** — every data point appears ONCE across all 4 sheets
- **S-curve SVG must be tight** — shrink viewBox after removing legend/summary sections

### Delegation Workflow

| Task | Recommended Labor |
|---|---|
| OCR invoices + bank receipts | Codex / Kimi |
| SVG chart creation/update | Claude Code |
| Bulk HTML edits/patches | Kimi / Claude |
| Deep file search | Kimi |
| Email scanning (Outlook SQLite) | Kimi |
| Final verification pass | Claude Code |

### Payment Reconciliation

Always OCR ALL PDFs in the payment folder:
1. Extract each invoice: date, number, description, amount, VAT
2. Extract each bank receipt: date, EUR amount, exchange rate, SAR total, reference, beneficiary
3. Match invoices to receipts (EUR×rate should match invoice SAR exactly)
4. Check for duplicates by file size and content
5. Build complete ledger before reporting AC

### Outstanding Invoice Recommendations

- Never use "REJECT" — always "HOLD" with explanation
- If partial work confirmed, recommend **partial pay for confirmed value**, HOLD the balance
- Format: "Recommend pay ~45K for confirmed review work, HOLD ~36K balance"
- Every invoice recommendation must say: what to do, why, and how much

References: `references/outlook-scanning.md` (Outlook SQLite queries for email discovery), `references/evm-coordinate-math.md` (S-curve coordinate formula reference), `references/nrs-negotiation-worked-example.md` (complete NRS payment negotiation analysis with contract cross-referencing).

---

## EVM Reporting — Day-Snapshot Standard (absorbed from evm-reporting)

### Purpose

Build a day-snapshot earned value report for contractor/subcontractor deliverables vs payments paid. Not a full contract study — no contract structure tables, resource schedules, workflow maps, penalty clauses, or ER requirements.

### What to Include (only these)

1. **What's delivered** — actual deliverables received (drawings, documents, reviews)
2. **What's paid** — total AC (all invoices confirmed via bank receipt OCR)
3. **Earned Value** — calculated using agreed bracket % of contract fee
4. **Variance** — CV (EV - AC) and SV (EV - PV), with CPI and SPI
5. **Outstanding** — unpaid invoices, with recommendation (HOLD, not REJECT)
6. **Next steps** — what's needed to close the gap

### Multi-Bracket EV Calculation

For projects with multiple work types (DD + specialist review + IFC), calculate EV as:

1. **Architecture DD** = bracket% × Stage 4 fee (e.g., 70% × 768K = 538K)
2. **Specialist review** = review% × specialist bracket (e.g., 12.3% × 115K = 14K)
3. **Stage 5 shop dwgs** = review% × Stage 5 fee (e.g., 17.4% × 270K = 47K)
4. **Total EV** = sum of all components
5. **CV** = Total EV - AC, **CPI** = Total EV / AC

### DD/Specialist Dependency — Tiered Approach

When DD drawings feed into specialist coordination, claiming 100% DD EV while specialist coordination is at low progress misrepresents true status. Use Scenario B (recommended):

| Component | Logic | EV |
|---|---|---|
| DD — unconditional | 75% × bracket | Guaranteed |
| DD — coordination-dependent | 25% × bracket × specialist_progress% | Tracks with coordination |
| Specialist review | (items_reviewed / total_items) × bracket | Per-package |
| **Total DD EV** | unconditional + dependent | |

**Implementation:**
1. Estimate standalone vs coordination-dependent portions (75/25 default)
2. Standalone: plans, sections, elevations, material specs — won't change
3. Dependent: MEP integration, ceiling zones, service routes — will need revision
4. Recovery path: as specialist coordination advances, dependent portion fills up

### Specialist Review Inventory

To calculate precise specialist review %, use project registers (Excel), not filesystem scanning:
1. Find xlsx files in `Docs/09_Registers/` — Drawing Register, Submittal Tracker
2. Count total expected per package from the register
3. Count NRS-reviewed items from stamped packages and NRS comment PDFs
4. Calculate % per package, then aggregate

See `references/specialist-review-inventory-methodology.md` for full methodology and fallback approaches when no register exists.

### Email Scanning for EV Evidence

When user says "check outlook" during an EV engagement, scan project-related folders:

1. **SQLite fast scan** (1000x faster than AppleScript):
   ```bash
   DB="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
   sqlite3 "$DB" "SELECT datetime(m.Message_TimeReceived,'unixepoch') as dt, m.Message_NormalizedSubject, m.Message_SenderList, f.Folder_Name FROM Mail m JOIN Folders f ON m.Record_FolderID=f.Record_RecordID WHERE m.Message_TimeReceived>=strftime('%s','now','-7 days') ORDER BY m.Message_TimeReceived DESC"
   ```
2. Route attachments to correct subfolder under `11_Correspondence/`

See `references/nrs-earned-value-calculation.md` for the worked NRS example with full EV metrics, and `references/outlook-scanning.md` for complete Outlook query patterns.
