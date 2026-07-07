---
name: vendor-ev-audit
description: "Earned Value snapshot for vendor/subcontractor: what's delivered vs what's paid. Stakeholder-facing report with payment register, specialist review breakdown, EVM S-curve. Samaya template."
version: 1.0.0
author: Hermes Agent
tags: [EVM, earned-value, vendor-audit, payment-reconciliation, stakeholder-report, Samaya]
---

# Vendor Earned Value Audit

Build a day-snapshot EV report for a vendor/subcontractor. Format: clean report (HTML, Samaya template), stakeholder language, no AI patterns.

## Structure (4 sheets)

| Sheet | Content |
|---|---|
| 1 — Snapshot | Title + logos (Samaya + vendor), 6 metric cards (EV, AC, CV, SV, DD Drawings, Invoices Paid), status as bullet-point list, fee summary table |
| 2 — Payment Register | All invoices with amounts, dates, proof references (bank receipts), status tags. No bar chart (duplicates S-curve on Sheet 4). |
| 3 — Specialist Packages | Table per specialist package: total expected items, NRS work done, status, delay cause, EV contribution. Consolidate note boxes into ONE. |
| 4 — EVM Analysis | S-curve chart (PV/EV/AC polylines) with tight viewBox. Metrics bar above chart with all values. No legend (obvious from axis). No EVM Summary (duplicates Sheet 1 status). No bracket breakdown (shown in metrics bar). |

## Style Rules (DO NOT VIOLATE)

- **Stakeholder language only.** No technical jargon like "EXTRACTED", "PDF ONLY", "REF ONLY". Every table cell must answer: "What does this mean for me? Is it actionable / done / blocked / at risk?"
- **Bullet points, not prose.** Use HTML `<ul><li>` lists. Never paragraph blocks.
- **Formal theme — no dashboard colors.**
  - Metric card backgrounds: `#F1F5F9` (neutral gray). Never colored tints (no green, blue, amber, red backgrounds).
  - Note boxes: `#FAFAFA` background with navy (`#1E293B`) left border. No colored boxes.
  - SVG chart lines: navy (`#1E293B`) for PV, black (`#000`) for EV, gray (`#64748B`) for AC. No green/blue/amber lines.
  - Status tags: `#F1F5F9` background with `#1E293B` text. No colored badges.
  - Only exception: negative values (CV, SV) can use bold to emphasize, not red color.
- **Human tone.** No AI patterns: no "It is worth noting", "Furthermore", "As we can see", "Let's delve into", "It is important to highlight that", "Notably", "Arguably", "Essentially". Use contractions (don't, isn't, can't). Active voice. Short sentences (3-4 max per note).
- **Lists for status.** Status tags in parentheses using `.tag-text` spans, italic. User prefers clean text over colored badges. Never use "HOLD — HOLD". Single word: "HOLD", "PAID", "DUE". Recommendation goes to user as decision, not stated as report fact.
- **Numbers clean.** No dramatic lead-ins. "CV = -218K" not "a troubling variance of".
- **No duplication.** Every data point appears ONCE. If Sheet 1 status list covers EV/AC/CV/SV, don't repeat on Sheet 4 as EVM Summary. If metrics bar shows bracket breakdown, don't add a separate bracket section. Check all 4 sheets for overlap before finalizing.
- **S-curve SVG must be tight.** After removing legend/EVM summary/bracket breakdown, shrink viewBox to match content. No orphan separator lines. Max y-coordinate should be within 10-20px of viewBox bottom.

## Workflow (always delegate)

| Task | Labor | Reason |
|---|---|---|
| OCR invoices + bank receipts | Codex / Kimi | Image-based PDFs need tesseract |
| SVG chart creation/update | Claude Code | SVG generation + coordinate math |
| Bulk HTML edits/patches | Kimi / Claude | 5-50 patch operations |
| Deep file search | Kimi | Faster rg/grep across large trees |
| Email scanning (Outlook SQLite) | Kimi | AppleScript + SQLite queries |
| Final verification pass | Claude Code | Cross-check all numbers |

## Bracket Calculation

Let the USER define the percentage split between work phases. Default approach:

1. Ask the user what % of the stage/fee the completed work represents
2. Calculate EV = % × stage fee
3. For specialist reviews: split the specialist bracket across packages by **effort weight, not simple item count**. Reviewed items may be lighter (1 round) while unreviewed packages may be heavier (multiple rounds expected).
4. Always get **actual item counts from project registers** (Excel/CSV drawing registers, submittal logs) — never estimate package sizes.
5. Cross-reference invoice amounts against bank receipt OCR (exact match EUR×rate = SAR)
6. For specialist packages table:
   - Find the project's drawing register or submittal log
   - Count items per specialist package (SLF, showcases, AV, structure, lighting, MEP, security, HVAC, IT, signage, BMS, landscape)
   - Count NRS-reviewed items by examining returned submittal folders and NRS comment PDFs
   - Calculate % per package, then aggregate to total specialist bracket %

## Payment Reconciliation

Always OCR ALL PDFs in the payment folder:
1. Extract each invoice: date, number, description, amount, VAT
2. Extract each bank receipt: date, EUR amount, exchange rate, SAR total, reference, beneficiary
3. Match invoices to receipts (EUR×rate should match invoice SAR exactly)
4. Check for duplicates by file size and content
5. Build complete ledger before reporting AC

## Pitfalls

- **Sibling overwrites.** If a subagent wrote to a file earlier, re-read it before writing again.
- **Escape drift.** When patching HTML, read the exact content with read_file first — escaped quotes (`\"`) in the tool call don't match literal quotes in the file.
- **OneDrive locks.** Files under OneDrive mounts may have `fileprovi` locks. Download to `/tmp/` first, then copy to destination.
- **Outlook dual inbox.** Exchange account may show 0 msgs in Inbox. Check all folders including Deleted Items and project subfolders.
- **S-curve coordinates.** Formula: `y = maxY - value/scale`. Verify against axis labels before reporting done.
- **SVG viewBox shrinkage.** After removing sections from an SVG (legend, EVM summary, internal footer), shrink viewBox AND `<rect>` height together. Orphan separator lines produce large empty gaps. Max content y-coordinate should be within 10-20px of viewBox bottom.
- **Sheet 2 missing footer.** When removing an SVG block from Sheet 2, the footer-strip and closing `</div></div>` may be inside the removed block. Check that the sheet still closes properly after removal.
