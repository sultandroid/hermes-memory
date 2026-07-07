# Samaya Formal RFI/Letter — HTML Format Guide

## Source of truth
The approved reference template for ALL formal TQ/RFI/letters to CG, PMC, or MoC:
`_Style-Guides/samaya-rfi-style-guide/templates/RFI_TEMPLATE.html`

Style guide documentation:
`_Style-Guides/samaya-rfi-style-guide/SAMAYA_RFI_HTML_STYLE_GUIDE.md`

Assets (logos):
`_Style-Guides/samaya-rfi-style-guide/assets/`

## When to use this format
- Formal Technical Query (TQ) to CG
- Formal RFI to MoC (via CG)
- Formal letter to PMC or Employer
- DO NOT use for: internal memos, cover emails, draft notes — those stay as markdown

## Format rules (from approved ARM-SIC-MOC-LET-006 template)

| Rule | Value |
|------|-------|
| **Layout** | RTL (`<html lang="ar" dir="rtl">`) |
| **Primary language** | Arabic — always leads in bilingual headings |
| **English handling** | English-only blocks → LTR; English inline in Arabic → `.en-inline` |
| **Color scheme** | Monochrome only — black, white, grey. NO navy, gold, or brand colors |
| **Fonts** | Arabic: `Noto Naskh Arabic` (Google Fonts) · English: `Carlito` / `Calibri` |
| **Page** | A4 portrait (210mm × 297mm), 12–14mm margins |
| **Print** | `@page { size: A4 portrait; margin: 0; }` with `page-break-inside: avoid` |

## Required blocks on every document

### Cover sheet (page 01)
1. **`.doc-strip`** — top of every page: `DOCCODE · ARABIC TITLE · Page X of Y · REV · Date`
2. **`.logo-strip`** — 4-column grid with logos: Samaya (main contractor), CG (consultant), PMC, MoC (employer)
3. **Cover title** — bilingual, Arabic h1 large, English h2 subtitle
4. **`.meta-grid`** — 3-column grid with keys: project/contract, recipient, issuer, contractual ref, doc code, status
5. **`.dc-block`** — Document Control table: black header bar, 5 columns (doc ref, revision, date, status, distribution)
6. **`.qc-block`** — QC Sign-Off: black header bar, 3 columns (prepared by, reviewed by, approved by) with name, title, signature/date lines
7. **Table of Contents** — `.data-table` with #, topic, page columns

### Body pages (page 02+)
8. **`.callout`** — evidence/citation boxes with thick left black border, light grey background. Use for SOW/ER/Briefing Pack quotes
9. **`.data-table`** — formal tables with black header rows, alternating row backgrounds
10. **`.en-block`** — English-only paragraphs wrapped for LTR alignment
11. **`.bi-block`** — bilingual headings/blocks (RTL, Arabic leads)

## Alignment rules (CRITICAL — user enforces this strictly)

| Content type | Class | `direction` | `text-align` |
|-------------|-------|-------------|-------------|
| English-only paragraph | `en-block` | `ltr` | `left` |
| Arabic-only paragraph | `ar-block` | `rtl` | `right` |
| Bilingual heading/label | `bi-block` | `rtl` | `right` |
| Inline English in Arabic flow | `en-inline` | `ltr` | inline |
| Table cell with English text | `style="text-align:left"` on `<td>` | — | `left` |
| Table cell with Arabic text | default (RTL) | — | `right` |

## Evidence blocks (callouts)

Every formal RFI must reference governing project documents with **verbatim quotes** in callout blocks:

```html
<div class="callout">
  <div class="lbl bi-block">EVIDENCE A — CONTRACTOR'S SCOPE OF WORK §8.14</div>
  <div class="en-block">
    "Contractor is responsible for development of artwork for graphics, in English
    and Arabic and production of vector files for MoC's approval, with a minimum
    3 rounds of review."
  </div>
</div>
```

Each evidence callout must include:
- The document code and section number in the label
- The exact quoted text
- Context about why it's relevant

## Question blocks

Each question in an RFI should be structured as:

```html
<h3 class="bi-block">١. مسؤولية تطوير الرسومات · 1. Artwork Development Responsibility</h3>

<div class="callout">
  <div class="lbl bi-block">CLARIFICATION REQUESTED · التوضيح المطلوب</div>
  <div class="en-block">
    <p><strong>Reference:</strong> SOW §8.14 vs Briefing Pack M2</p>
    <p>Specific question text in English...</p>
    <ul>
      <li>Option A</li>
      <li>Option B</li>
    </ul>
  </div>
</div>
```

## File naming

| Type | Pattern | Example |
|------|---------|---------|
| Formal RFI | `FORMAL_RFI_NNN_CG_Topic.html` | `FORMAL_RFI_003_CG_Scope_Boundary.html` |
| Draft (not for submission) | `FORMAL_RFI_NNN_Topic_DRAFT.html` | `FORMAL_RFI_004_CG_MoC_Content_DRAFT.html` |
| Internal RFI | `INTERNAL_RFI_NNN_Topic.md` | `INTERNAL_RFI_001_Graphit_Pricing_Capacity.md` |

## What NOT to include
- DO NOT include a "Response Requested" section — the user explicitly removes this ("everyone knows response is required")
- DO NOT include "Programme Impact" or "Critical Path Note" sections — the user removes these ("no need to add")
- DO NOT use navy/gold/color — monochrome only
- DO NOT use Inter or Tajawal fonts — use Noto Naskh Arabic + Carlito

## Relative logo paths

From the sub's `06_RFIs/` folder to the style guide assets:
```
../../../../../_Style-Guides/samaya-rfi-style-guide/assets/logo.png
```
(5 levels up from `06_RFIs/` to `Technical Office/`, then into `_Style-Guides/`)

## Revision history

| Date | Change |
|------|--------|
| 2026-06-09 | Added Programme Impact / Critical Path Note removal rule. Added alignment class descriptions (en-block, bi-block, ar-block, en-inline). | User removed "Programme Impact" and "Critical Path Note" sections, and corrected English alignment in blocks. |
