# Engineering Template v2.0 — Style Guide

> Mandatory for ALL Samaya Technical Office / BIM Unit document generation.
> Corrected by Mohamed Essa 2026-06-09: "follow our style guide for any docs we create"
> **This applies to ALL documents — internal team docs, ops guides, and informal working documents included.** Do not skip the style guide because the audience is internal or the document is "not for CG submission." The style guide governs our office's document identity, period.

## Location

```
~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/
```

## Sub-Guides

| Guide | File | Use Case |
|-------|------|----------|
| **Formal Plan A4** | `Samaya-Formal-Plan-A4-Style-Guide.md` | Multi-page submittal plans (SMP, DMP, BEP, Resource Mgmt, etc.) — A4 portrait, navy/sky/green palette, Montserrat+Inter+Menlo fonts |
| **Engineering Deck** | `Engineering-Deck-HTML-Style-Guide.md` | A4 landscape executive decks |
| **RFI Letters** | `samaya-rfi-style-guide/` | Formal TQ/RFI letters |
| **Doc Style Guide** | `Doc Style Guide/Samaya_Doc_Style_Guide_v1.0.md` | DOCX generation via Python |

### Formal Plan A4 Key Rules (from Samaya-Formal-Plan-A4-Style-Guide.md)

- **Fonts**: Montserrat (headings, 800 weight, uppercase), Inter (body), Menlo (metadata/codes). Never Calibri.
- **Colors**: `--primary: #0F172A`, `--secondary: #0284C7`, `--accent: #16A34A` (green for pass/closure), `--fail: #B91C1C` (red), brown `#92400E` (high severity). Note: some older documents use `--accent: #F59E0B` (amber) — check the document's own `:root` tokens.
- **Border radius**: `2px` max — engineering doc, not a web app
- **Page model**: One `.page` = one A4 sheet (210×297mm), `overflow: hidden`, `@page margin: 0`
- **Tables**: Navy header (`--primary` bg, white text), hairline grid (`--border`), zebra even rows, `table-layout: fixed`
- **Badges**: Menlo font, `2px` radius, color-coded (pass/fail/critical/high/low)
- **SVG charts**: Inter font, `→` character arrows (not SVG markers), white boxes with navy stroke, navy end boxes with white text

## Format Options

| Format | Starter | Use Case |
|--------|---------|----------|
| **HTML** | `index.html` + `css/style.css` | Engineering decks, plans, RFIs, management docs |
| **DOCX** | `Doc Style Guide/samaya_doc_template.py` | Formal Word, submittals, CV packs |

## Mandatory HTML Rules

| Rule | Value |
|------|-------|
| Language | Bilingual: English lead, Arabic secondary (titles + labels) |
| Primary colour | `#0F172A` (navy) — headers, borders, substance |
| Secondary colour | `#0284C7` (sky) — banner accents, H2 bars |
| Border radius | `2px` max — NO rounded corners |
| Box shadow | NONE |
| Page size | A4 portrait |
| @page margins | `12mm` top/bottom, `16mm` sides |
| Cover logo row | 5 parties: MoC · ACE · CG · NRS · Samaya |
| Cover DC block | doc-no, revision, status, dates, originator, reviewer, approver, authority |
| Footer (every page) | doc-no · context · page number (`.pg-footer`) |
| English font | Inter (Google Fonts) |
| Arabic font | Tajawal or Amiri (Google Fonts) |
| Monospace | Menlo for codes, tags, refs, gate names |
| Body text | `0.58rem` |
| Tables | `0.5rem` |
| Tag chips | `0.4rem` |
| Status: pass | `--pass` = `#15803D` (green) |
| Status: fail | `--fail` = `#B91C1C` (red) |
| Status: partial | `--warn` = `#92400E` (amber) |
| Status: neutral | `--text-muted` = `#64748B` (gray) |
| Commentary | Halftone gray only |
| Section chips | Every H2 gets a disposition chip |

## Component Classes (from style.css)

| Class | Component |
|-------|-----------|
| `.eng-strip` | Engineering spec strip (3px left rule, grid key-value) |
| `.flowchart` | Tier flowchart (nodes + arrows + RED dashed reject loop) |
| `.snapshot` | Snapshot strip (4-9 horizontal summary cards) |
| `.badge-pass/fail/partial/neutral` | Status badges with icon glyphs |
| `.severity-*` | Table row left-stripe |
| `.phase-banner` | Table category grouping row |
| `.count-bar` | Visual proportional bar next to numbers |
| `.critical` | Critical alert strip (red left-rule + background) |
| `.xref` | Cross-section reference tag |
| `.dc-block` | Document Control block (cover) |
| `.pg-footer` | Page footer strip |
| `.h2-row` | H2 with bar + Arabic subtitle + disposition chip |
| `.banner` | Subsection banner header + halftone hint |

## Quick Start

```bash
cp _Style-Guides/index.html MyDoc_Rev01.html
# Edit: cover, sections, DC block, footer
# Open in Chrome → ⌘P → Save as PDF (Margins: None, Background: ON)
```

## Print Settings

| Setting | Value |
|---------|-------|
| Paper | A4 Portrait |
| Margins | None (CSS `@page` handles it) |
| Background graphics | ON |
| Scale | 100% |

## Pitfalls

- Do NOT use `border-radius > 2px` or `box-shadow` — engineering style is sharp
- Do NOT generate any document without first loading this reference
- HTML must be self-contained (CSS embedded) when deployed to project subfolders
- Verify first line of output is not line-number contaminated (`  N|<...`)
- Verify `wc -c` after writing to detect truncation
