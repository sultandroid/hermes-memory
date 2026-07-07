# Formal RFI/TQ HTML Format — Samaya Style Guide Reference

## When to use

Any formal Technical Query (TQ) / Request for Information (RFI) submitted to CG or MoC via Aconex. The format follows the approved template derived from `ARM-SIC-MOC-LET-006_RevA.html` (Replica Model submittal).

**Do NOT use this format for:**
- Internal coordination memos (use markdown in `06_RFIs/`)
- Meeting minutes or progress reports (use SamayaDoc .docx template)
- Quick questions to same-team members (email is fine)

## Source of truth

**Style Guide:** `_Style-Guides/samaya-rfi-style-guide/SAMAYA_RFI_HTML_STYLE_GUIDE.md`
**Blank reusable template:** `_Style-Guides/samaya-rfi-style-guide/templates/RFI_TEMPLATE.html`
**Logos:** `_Style-Guides/samaya-rfi-style-guide/assets/` (samaya.png, cg.png, pmc_ace.png, moc.png)

## Format rules (non-negotiable)

| Rule | Setting | Rationale |
|------|---------|-----------|
| Direction | `dir="rtl"`, `lang="ar"` | Arabic is primary per project convention |
| Colour palette | **Monochrome only** — black, white, shades of grey | Formal correspondence; no navy/gold |
| Font stack | `'Noto Naskh Arabic'` (Arabic body) + `'Carlito'` (English/Latin) | Readable in both scripts |
| Page | A4 portrait, 210×297mm, 12mm margins | Printable, fileable |
| Layout | `position:relative` `.sheet` divs with `page-break-after:always` | Pages render separately |

## Required structural blocks

### Every page
- `.doc-strip` — top bar: "DOCCODE · Arabic Title · Page X of Y · Rev · Date"

### Cover page
1. **`.logo-strip`** — 4-column grid: Samaya (Main Contractor), CG (Consultant), PMC, MoC (Employer). Each cell: 10mm logo PNG + role label + company name.
2. **Cover title** — bilingual block: Arabic h1 title, English subtitle, project reference.
3. **`.meta-grid`** — 3-column grid with `.k` (label) and `.v` (value). Fields: project/contract, recipient, issuer, contractual reference, doc code, status.
4. **`.dc-block`** — Document Control: black header bar "Document Control · التحكم بالوثيقة", 5-column grid (doc ref, revision, date, status, distribution).
5. **`.qc-block`** — QC Sign-Off: black header bar, 3-column grid (Prepared by, Reviewed by, Approved by). Each cell: role, name, title, signature/date lines.

### Body pages
1. **Section headings** (`h2`) — black bottom border, uppercase, section number.
2. **Evidence callouts** (`.callout`) — left thick black border (2.5pt), light grey background (`#FAFAFA`), `.lbl` header with document reference.
3. **Data tables** (`.data-table`) — black top+bottom borders on header, `#FAFAFA` header bg, alternating rows, proper RTL alignment.
4. **Questions** — structured as numbered blocks with evidence reference + clarification request.

### Last page
- **Response request** — table with Priority, Response by date, Routing.

## Evidence callout pattern

Every claim in a formal RFI must be backed by a quoted source. Use the callout block:

```html
<div class="callout">
  <div class="lbl">§8.14 Graphics Artwork and Production — الصفحة 23 من وثيقة نطاق العمل</div>
  "Contractor is responsible for development of artwork for graphics, in English
  and Arabic and production of vector files for MoC's approval..."
</div>
```

**Rules for evidence:**
- Always cite the document code and section (e.g., "SOW §8.14", "ER §2.2", "Briefing Pack M2")
- Use verbatim quotes from the governing document (not paraphrased)
- Include the Arabic document reference after the English
- Number evidence blocks (Evidence A, B, C) for cross-referencing in questions

## Logo path convention

When generating an HTML RFI inside a subcontractor's `06_RFIs/` folder (e.g., `Subcontractors/08_Graphics_Contractor/06_RFIs/`), the relative path to logos is:

```
../../../../../../_Style-Guides/samaya-rfi-style-guide/assets/samaya.png
```

Count up from the file to the project root, then into `_Style-Guides/`.

If generating from a different project folder, calculate the relative depth accordingly.

## Print CSS requirements

```css
@page { size: A4 portrait; margin: 0; }
@media print {
  .sheet { margin:0; box-shadow:none; width:210mm; height:297mm; min-height:297mm; ... }
  .sheet:last-child { page-break-after:auto; break-after:auto; }
}
```

Always include `overflow:hidden` on `.sheet` for screen view and `break-inside:avoid` on blocks that should not split across pages.

## Inline English in RTL flow

Use the `.en-inline` class for English text within Arabic paragraphs:

```css
.en-inline {
  font-family: 'Calibri','Carlito','Arial',sans-serif;
  direction: ltr;
  display: inline-block;
  unicode-bidi: embed;
}
```

## Typical file structure

```
06_RFIs/
├── RFI_Register.xlsx
├── INTERNAL_RFI_001_Graphit_Pricing_Capacity.md         ← internal: markdown fine
├── INTERNAL_RFI_002_Adjacent_Trade_Coordination.md      ← internal: markdown fine
├── FORMAL_RFI_003_CG_Scope_Boundary.md                  ← source markdown
├── FORMAL_RFI_003_CG_Scope_Boundary.html                ← FORMAL: HTML template req.
├── FORMAL_RFI_004_CG_MoC_Content.md                     ← source markdown
└── FORMAL_RFI_004_CG_MoC_Content.html                   ← FORMAL: HTML template req.
```

Keep the `.md` source alongside the `.html` — the markdown is the edit-friendly version; the HTML is the submission-ready version.

## Related references

- `references/scope-analysis-rfi-workflow.md` — upstream workflow that identifies what RFIs to raise
- `_Style-Guides/samaya-rfi-style-guide/SAMAYA_RFI_HTML_STYLE_GUIDE.md` — full style guide document
- `_Style-Guides/samaya-rfi-style-guide/templates/RFI_TEMPLATE.html` — reusable blank template
