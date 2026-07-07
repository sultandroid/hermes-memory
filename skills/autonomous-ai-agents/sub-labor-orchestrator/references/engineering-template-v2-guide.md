# Engineering Template v2.0 — Quick Reference

**Location:** `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/`

## Palette (Print-Safe)
| Token | Hex | Usage |
|-------|-----|-------|
| --primary | #0F172A | Navy, headers/borders |
| --secondary | #0284C7 | Sky, banner accents |
| --text-muted | #64748B | Halftone commentary |
| --border | #E2E8F0 | Table borders |
| --fail | #B91C1C | Red reject/critical |
| --pass | #15803D | Green accept |
| --warn | #92400E | Amber partial |

## Typography
- English: Inter (Google Fonts)
- Arabic: Tajawal or Amiri
- Monospace: Menlo for codes, tags, refs
- Body: 0.58rem, tables 0.5rem, tags 0.4rem

## Page Setup
- A4 portrait, @page size A4, 12mm top/bot, 16mm sides
- Background graphics ON for print
- Scale 100%

## Cover Page
- 5-party logo row: MoC (Client) · ACE (PMC) · CG (Consultant) · NRS (Design) · Samaya (Contractor)
- Title: English H1 + Arabic subtitle
- DC block: Document No, Revision, Status, Issue Date, Reply By, Originator, Reviewer, Approver, Authority
- Confidential footer

## Every Page
- `.pg-footer` with doc-no, context, page number
- H2 with section number + disposition chip

## Components
| Class | Usage |
|-------|-------|
| .eng-strip | Engineering spec strip (3px left rule) |
| .flowchart | Tier flowchart with RED dashed reject |
| .snapshot | Summary cards (4-9 horizontal) |
| .badge-pass/fail/partial/neutral | Status badges with icons |
| .severity-* | Table row left-stripe |
| .phase-banner | Category grouping row |
| .dc-block | Document Control block |
| .pg-footer | Page footer strip |

## Print Settings (Chrome)
- Paper: A4 Portrait
- Margins: Default (CSS @page handles)
- Background graphics: ON
- Scale: 100%

## Source Files
- Template: `index.html` — full demo, copy and modify
- CSS: `css/style.css` (825 lines)
- Style guide: `Engineering-Deck-HTML-Style-Guide.md` (1143 lines)
- Word template: `Doc Style Guide/samaya_doc_template.py`
