---
name: evm-reporting
description: "Build earned-value snapshots for contractor/subcontractor deliverables vs payments. Day-snapshot format: what's delivered, what's paid, EV calculation, variance, outstanding, next steps. Stakeholder language only — no legal/technical jargon."
version: 1.0.0
author: Mohamed Essa / Samaya
license: internal
platforms: [macos]
metadata:
  hermes:
    tags: [evm, earned-value, reporting, stakeholder-report, financial-analysis, payment-reconciliation]
    related_skills: [sub-labor-orchestrator, document-analysis]
---

# EVM Reporting — Earned Value Snapshot

## Purpose

Build a **day-snapshot** earned value report for contractor/subcontractor deliverables vs payments paid. Not a full contract study — no contract structure tables, resource schedules, workflow maps, penalty clauses, or ER requirements.

## What to Include (only these)

1. **What's delivered** — actual deliverables received (drawings, documents, reviews)
2. **What's paid** — total AC (all invoices confirmed via bank receipt OCR)
3. **Earned Value** — calculated using agreed bracket % of contract fee
4. **Variance** — CV (EV - AC) and SV (EV - PV), with CPI and SPI
5. **Outstanding** — unpaid invoices, with recommendation (HOLD, not REJECT)
6. **Next steps** — what's needed to close the gap

## What to EXCLUDE (stakeholders don't need)

- Contract structure appendix tables
- Resource schedules (person-days, rates)
- Penalty clauses and delay provisions
- Workflow maps and process flows
- ER / Employer's Requirements extracts
- Specialist discipline lists
- Stamping status (unless user specifically asks)
- RIBA stage detail breakdowns

## Stakeholder Language Rules

- **Column headers**: "Stakeholder Value" not "Status"
- **Status tags**: complete sentences, not one-word labels
  - ✗ "EXTRACTED" → ✓ "PAYMENT BASIS — ALL FIGURES VERIFIED"
  - ✗ "PDF ONLY" → ✓ "DEFINES NRS OBLIGATIONS — EXTRACTED"
  - ✗ "REF ONLY" → ✓ "BACKGROUND — NOT CRITICAL FOR PAYMENT"
- **Recommendation tone**: "HOLD" not "REJECT"
  - ✗ "REJECT — premature" → ✓ "HOLD — partial EV only"
  - ✗ "REJECT invoice" → ✓ "Recommend partial pay ~45K, HOLD balance ~45K"
- **Every table cell** should answer: "What does this mean for the decision-maker?"
- **Every note box** should answer: "What decision is needed?"

## Workflow

1. **Delegate to sub-agent** — always use Claude/Kimi/Codex for heavy work
2. **Gather data**:
   - OCR all invoice PDFs via fitz → tesseract
   - OCR all bank receipt PDFs (check for multiple transfers)
   - Search project files for evidence of delivered work
3. **Establish brackets** — ask user for % breakdown of contract value, or propose based on work done
4. **Validate bracket methodology** — before calculating EV, delegate to Claude for dependency analysis (e.g., does DD depend on specialist coordination? Are there multi-bracket dependencies?). Present 2-3 scenario options to user for approval — don't proceed with a single default. This prevents the "you claimed 100% DD but specialist is only at 13%" correction.
5. **Calculate EV** — EV = bracket% × stage fee
6. **Calculate variance** — CV = EV - AC, SV = EV - PV
7. **Build report** — 4 sheets max: Snapshot, Payment Register, EVM Chart, Next Steps
8. **Audit via Codex** — check all numbers cross-reference, no stale values
9. **Deliver** — both copies (audit folder + source folder)

## Email Scanning for EV Evidence

When user says "check outlook" during an EV engagement, scan project-related folders for contractor correspondence:

1. **SQLite fast scan** (1000x faster than AppleScript):
   ```bash
   DB="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
   sqlite3 "$DB" "SELECT datetime(m.Message_TimeReceived,'unixepoch') as dt, m.Message_NormalizedSubject, m.Message_SenderList, f.Folder_Name FROM Mail m JOIN Folders f ON m.Record_FolderID=f.Record_RecordID WHERE m.Message_TimeReceived>=strftime('%s','now','-7 days') ORDER BY m.Message_TimeReceived DESC;"
   ```
2. **Search project folder** for the sender name or download attachments to look for: Project Query Trackers (scope boundaries), RFIs clarifying exclusions (e.g., "interactives outside our scope"), submittal trackers (review status per package), fee proposals (bracket confirmation)
3. **Route attachments** to correct subfolder under 11_Correspondence/

## Subagent Delegation Split

For report generation, use this labor split:
1. **Kimi** — rewrites/refines prompts, converts rough requests into structured instructions
2. **Claude** — heavy rendering: SVG chart design, HTML table formatting, CSS styling
3. **Codex** — verification pass: cross-check numbers, find stale values, validate math
Do not do all three workstreams in one agent.

## S-Curve Coordinate Verification

The S-curve uses: `y = baseY - (valueK × pixelsPerK)`
where `pixelsPerK = chartHeight / maxK`, `chartHeight = baseY - topY`

Example:
- baseY (0K) = 460, topY (800K) = 140 → chartHeight = 320px, pixelsPerK = 320/800 = 0.4
- For 483K: y = 460 - (483 × 0.4) = 460 - 193 = 267

Derive pixelsPerK from your chart's actual gridline spacing: `pixelsPerK = gapBetweenGridlines / valueBetweenGridlines`
- Example: gridlines at y=446 (0K), y=372 (200K) → 74px per 200K = 0.37px per 1K

Verify by placing `<circle>` at each curve endpoint — if it doesn't align with the value label, coordinates are wrong. Test PV/EV/AC at TODAY (June) before finalizing.

After editing SVG content, grep for two `</svg>` tags (one per chart sheet). Removing content between them must leave the closing tag intact.

## Bracket Estimation

When the user says "you decide the brackets", propose:
- Architecture DD: % of Stage 4 based on drawings delivered
- Specialist review as Design Lead: % remaining
- IFC production: % remaining
- Coordination: 0% if Samaya handles it

Always ask user to confirm or override the % before finalizing EV.

## Multi-Bracket EV Calculation

For projects with multiple work types (DD + specialist review + IFC), calculate EV as:

1. **Architecture DD** = bracket% × Stage 4 fee (e.g., 70% × 768K = 538K)
2. **Specialist review** = review% × specialist bracket (e.g., 12.3% × 115K = 14K)
3. **Stage 5 shop dwgs** = review% × Stage 5 fee (e.g., 17.4% × 270K = 47K)
4. **Total EV** = sum of all components
5. **CV** = Total EV - AC
6. **CPI** = Total EV / AC

### DD/Specialist Dependency — Unconditional vs Coordination-Dependent Split

**Problem:** When DD (design development) drawings feed into specialist coordination, claiming 100% DD EV while specialist coordination is at low progress (e.g., 13%) misrepresents true project status. DD drawings may need revision after specialist inputs (MEP, HVAC, structural interfaces, lighting, IT pathways, BMS points).

**Tiered approach — present to user before accepting 100% DD:**

| Scenario | DD Logic | DD EV | Total EV | When to use |
|---|---|---|---|---|
| A — Full DD upfront | 100% × bracket | Full bracket | Highest | External reporting, or if DD is a discrete deliverable with no dependency |
| B — Discounted (recommended) | Split into unconditional + coordination-dependent portions | 75-80% of bracket, plus dependent % tracking specialist progress | Moderate | **Most defensible** — transparent, fair to vendor, clear recovery path |
| C — Performance blanket | Apply flat "usefulness" multiplier | Low | Worst | Avoid — penalizes vendor for owner delays, arbitrary multiplier |

**Scenario B implementation:**

1. **Analyze the deliverables** and estimate what portion is standalone (won't change after coordination) vs coordination-dependent:
   - Standalone (75-80%): plans, sections, elevations, material specs, room layouts, stair details — architectural output that doesn't change
   - Coordination-dependent (20-25%): MEP integration, structural interfaces, ceiling zones, service routes, lighting layouts, IT pathways, BMS points — WILL need revision

2. **Calculate unconditional DD EV:** = standalone% × DD bracket (always earned)

3. **Calculate dependent DD EV:** = dependent% × DD bracket × specialist_coordination_progress%

4. **Total DD EV** = unconditional + dependent

5. **Recovery path:** As specialist coordination advances (50%, 80%, 100%), the dependent portion fills up proportionally. Vendor can recover the full DD bracket once coordination is complete.

6. **Fairness rules:**
   - If specialist delay is on the **owner/client side** (not vendor), use max(submitted%, reviewed%) for the dependent trigger — don't penalize vendor for submission delays they don't control
   - Document which deliverables are "coordination-dependent" (memo from vendor) for audit trail
   - This is not a permanent haircut — it's a timing adjustment

**Example (NRS Aseer Museum):**
```
Stage 4 fee: SAR 768K
DD bracket: 70% = SAR 538K (user-agreed)
Specialist progress: 12.3% (45/365 items)

Scenario A (full DD): 538K DD EV → total EV 600K, CV -212K, CPI 0.74
Scenario B (75/25 split):
  - Unconditional: 75% x 538K = 403.5K
  - Dependent: 25% x 538K = 134.5K x 12.3% = 16.5K
  - Total DD EV: 420K → total EV 483K, CV -329K, CPI 0.59
```

**Pitfall:** Don't use Scenario C (blanket "usefulness" multiplier) — it's methodologically weak, the multiplier is arbitrary, and it permanently discounts work that could become fully valuable later. Vendors will legitimately object.

## Specialist Review Inventory — Finding Evidence

To calculate precise specialist review %, do NOT estimate visually. Instead:

1. **Find the project registers**: search for xlsx files in Docs/09_Registers/
   - Drawing Register: lists all drawings per package with counts
   - Submittal Tracker / IFC Log: lists all submittal items per discipline
2. **Count total expected per package** from the register (by filtering by discipline sheet/column)
3. **Count NRS-reviewed items** by searching project folders for:
   - Stamped packages with NRS stamps in filename or path
   - Files with "reviewed" or "approved" status mentioning NRS/Nissen
   - REBA / coordination spreadsheets with NRS comments
4. **Calculate %** = NRS-reviewed / total expected per package
5. **Calculate EV** = % × bracket amount for that package
6. **Build a table** with columns: Package, Total Expected, NRS Reviewed, %, EV

### Table columns (use these exact headers):
```
# | Specialist Package | Total Expected | NRS Work Done | Status | Delay Cause | EV Contribution | EV (SAR)
```

- "Total Expected" column is essential — stakeholders need to see the denominator
- Mark packages with no NRS work as "NOT STARTED" with the delay cause
- Distinguish: delayed by Samaya vs delayed by Specialist
- Add summary row: total items, total reviewed, overall %, total EV

## Invoice Recommendation Rules

- **Never use "REJECT"** — always "HOLD" with explanation
- If partial work confirmed (e.g., NRS reviewed some specialist shop drawings), recommend **partial pay for confirmed value**, HOLD the balance
  - Format: "Recommend pay ~45K for confirmed review work (showcase + AV shop dwgs), HOLD ~36K balance"
- If no earned value: "HOLD — Stage 5 billed before Stage 4 closed" (not "REJECT")
- If no earned value: "HOLD — partial EV only" (not "REJECT — premature")
- Every invoice recommendation must say: what to do, why, and how much

## Payment Reconciliation

- Scan payment folder for ALL PDFs
- Check for duplicate files (same size = duplicate)
- OCR each unique invoice → extract: date, number, amount, description
- OCR each bank receipt → extract: date, EUR amount, SAR amount, rate, beneficiary
- Cross-reference: which invoice matches which receipt?
- Build complete ledger: all invoices paid or outstanding

## Style Rules (DO NOT VIOLATE)

- **Lists, not prose.** Use HTML `<ul><li>` for status notes and assessment boxes. Never paragraph blocks.
- **No emoji or icons.** Formal document only. Remove all emoji, warning signs (⚠️), bullet characters (•), checkmarks, colored circles, or any pictographic elements. Use plain text labels only.
- **No AI language patterns.** Rewrite generated text through Kimi first (prompt rewrite), then Claude for execution. Specific phrases to kill: "It is worth noting", "Furthermore", "As we can see", "Let's delve into", "It's important to highlight", "This report will explore/analyze/examine", hedging words (arguably, essentially, notably). Use contractions (don't, isn't, can't, it's). Active voice. Short sentences.
- **No dramatic lead-ins.** Present numbers plainly. "CV = -218K" not "a troubling variance" or "a noticeable gap". Data speaks for itself.
- **Logos on title page only.** Samaya left, vendor right. Transparent PNGs, ~36px height. Not on any other sheet.
- **Minimal colors.** Use only the template palette (#1E293B headers, white bg, #FAFAFA alternating rows). No extra accent colors.
- **"HOLD" not "REJECT".** User explicitly corrected this. Always frame invoice recommendations as HOLD with explanation.
- **Stakeholder column headers.** "Stakeholder Value" not "Status". "% of Bracket" not "EV Contribution". Every header must answer "what does this mean for me?"
- **Sheet renumbering.** When adding/removing sheets, update ALL footers (Sheet X/N). Search for every occurrence.
- **Wide tables (8+ columns on A4):** A4 usable width is ~182mm (210mm sheet - 14mm side padding). For 8+ column tables, the default `td{padding:0.5mm 0.8mm; font-size:6.8pt}` overflows. Fix: reduce padding to `0.3mm 0.5mm`, font to `6.5pt`, add `word-break:break-word`, and compress the longest cell text. Adjust column widths to give more space to the widest columns (package name, work description), less to narrow ones (%, EV, items). Text in "NRS Work Done" and "Delay Cause" cells should be terse — no full sentences, use abbreviations (e.g., "23+ dwgs, 8 stamped, 4 cycles" not "23+ dwgs reviewed, 8 stamped, 4 submittal cycles").

## Samaya Template Palette (strict)

Only these colors — no others:

| Role | Hex | Usage |
|---|---|---|
| Dark navy | `#1E293B` | Headers, title text, table header backgrounds |
| Black | `#000` | Body text, primary values |
| Dark gray | `#444` | Secondary text, metadata |
| Muted gray | `#64748B` | Labels, footnotes, muted data |
| Border gray | `#CBD5E1` | Borders, gridlines, dividers |
| Light gray | `#F1F5F9` | Card backgrounds, alternating rows |
| Near white | `#FAFAFA` | Note backgrounds |
| White | `#FFF` | Main background |

Status tags — these are the ONLY colored elements:

| Tag | Background | Text | Border |
|---|---|---|---|
| `.tag.g` (done) | `#F0FDF4` | `#15803D` | `#BBF7D0` |
| `.tag.a` (pending) | `#FEF3C7` | `#92400E` | `#FDE68A` |
| `.tag.r` (blocked) | `#FEF2F2` | `#B91C1C` | `#FCA5A5` |
| `.tag.b` (info) | `#EFF6FF` | `#1D4ED8` | `#BFDBFE` |
| `.tag.n` (neutral) | `#F1F5F9` | `#64748B` | `#CBD5E1` |

## Pitfalls

- **EV calculation mismatch**: Item count % and value % are different. 45/365 items = 12.3% but 9K/115K bracket = 7.8%. Don't mix them. Always state the base: "12.3% of items (% of bracket value)" or use only one method. If using effort-weighted EV, say "(effort-weighted)" next to the percentage.
- **Multiple bank transfers**: Don't assume one transfer covers everything. Check all receipt PDFs.
- **Invoice amounts vs transfer amounts**: They may differ by bank fees (SAR 50-60). Account for this.
- **Invoices can be paid out of order**: Advance may not match the first receipt. Check dates.
- **Arabic OCR**: Use `ara+eng` language pack for mixed-language receipts.
- **Stale values**: After updating any number, grep for the old value across ALL related reports. One missed patch = wrong report. Common stale hiding spots: SVG-embedded metric cards (`<text>` elements inside chart headers), legend annotations, and footnote values in other report files (Contract Study, Payment vs Deliverables, Scope vs Deliverables). In one session, a stale `+71K` CV survived in a Contract Study SVG metric card for 18 patches because it was inside an SVG `<text>` element — grep found the string but the patch missed it because the surrounding context was unique.
- **SVG stale value check**: After patching, run Codex audit with explicit instruction to check SVG-embedded metric cards (`<text>` fill/stroke color AND value text). Codex found a stale `+71K` inside an SVG metric card in the same session that grep-only verification missed.
- **Embedded SVGs**: After updating SVG files, re-embed them into the HTML. The embedded copy is what renders. Two-step: write the SVG file, then read it back and inject into the HTML.
- **Sheet footers after removal**: When removing or adding sheets, update ALL footer "SHEET X/N" references. Grep for "/5" and "/4" patterns.
- **Escape drift**: When patching HTML, read exact content first. Escaped quotes (\") in patch calls don't match literal quotes in the file.
- **Sibling subagent overwrites**: If a subagent modified a file earlier in the session, re-read before writing. Always verify the file state.
- **S-curve coordinates**: Formula is `y = baseY - (valueK × pixelsPerK)` where `pixelsPerK = chartHeight / maxK`. Derive from gridline spacing: `pixelsPerK = gapPx / gapValue`. Verify coordinate math against axis labels before finalizing. Use `circle` to mark PV/EV/AC intersection points.
- **"EV Contribution" column naming**: User asked "what this refer to" — column must specify the base. Write "% of 115K Bracket" not "EV Contribution". Always state what the % is of.
- **Assessment box redundancy**: Sheet 2 assessment box duplicates Sheet 1 status list. Don't add it. User explicitly removed it.
- **Remove aggressively**: If a section doesn't add new info, user will ask "do we need this?" Remove before they ask. Decision cards, summary boxes, bracket breakdowns — if it repeats something already stated, cut it.
- **Don't break SVG rendering**: When replacing large SVG sections, ensure the closing `</svg>` tag remains. Two `</svg>` tags exist (one per chart sheet) — count them.
- **SVG-embedded metric cards**: Metric cards rendered as SVG `<text>` elements (e.g., inside a chart header bar) can hide stale values. Normal text grep finds these, but Codex audit must explicitly check metric card `<text>` fill/stroke attributes AND the text content — a card can have correct text color (red for negative) but wrong value text. In this session, Codex found a `+71K` CV metric card inside an SVG while grep-only search missed it because the stale value wasn't in a standard HTML element.
