# Report Authoring Conventions — Samaya BIM Unit

## Purpose
Standard for ALL HTML reports created for Samaya stakeholders. Ensures consistency, readability, and decision-usefulness.

## Template
- A4 portrait: 210mm×297mm, white bg (#FFF), #1E293B headers, Calibri font
- CSS classes: `.tag.g` (green/done), `.tag.a` (amber/pending), `.tag.r` (red/blocked), `.tag.n` (neutral/future)
- Note boxes: `.note` (blue info), `.note.warn` (amber caution), `.note.r` (red risk)
- Sheet footers: `SHEET X/Y` sequential numbering
- Doc strip header with document reference code

## Language — Stakeholder-First
Every piece of content must answer: **"What does this mean for the decision-maker?"**

| Don't say | Say instead |
|-----------|-------------|
| EXTRACTED | DEFINES NRS VS SAMAYA RESPONSIBILITIES |
| PDF ONLY | DEFINES OBLIGATIONS — NEEDS EXTRACTION |
| REF ONLY | BACKGROUND — NOT CRITICAL FOR PAYMENT |
| All received. 0 stamped. | Complete — usable for IFC production |
| 10/10 Complete | All drawings submitted ✓ |

## Structure
- **Status summaries:** HTML `<ul>` with `<li>` items — scannable, not prose paragraphs
- **Tables:** Clear headers, meaningful Status/Notes columns
- **No emoji icons** in formal documents — use `.tag` CSS classes instead
- **No AI patterns:** Strip "Furthermore,", "Moreover,", "It is worth noting that", "arguably," "essentially", "Let's delve into", "This report will explore..."
- **Voice:** Use contractions (don't, isn't, it's), active voice, short sentences (3-4 max per paragraph)
- **Facts only:** State what IS. Do not add unsolicited recommendations. ("Due 11 Jun" not "pay ~45K, HOLD ~36K")

## SVGs (Charts & Diagrams)
- Inline SVG, white/light background matching template (never dark theme)
- Formal color palette — no bright gradients, no dark #0F172A backgrounds
- Embed directly in HTML, not as external references

## Sheet Structure
1. **Title + Snapshot** — Key metrics, status summary in bullet list, fee/summary table
2. **Detail tables** — Payment register, specialist packages, with stakeholder-value columns
3. **Charts** — EVM S-curve, payment bars (only if they add decision-useful info)
4. **No "Next Steps" or "Decision Points" sheets** unless explicitly requested

Created: 2026-06-03 from NRS EV snapshot session feedback
