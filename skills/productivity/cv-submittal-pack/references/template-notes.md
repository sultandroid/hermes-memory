# CV Submittal Pack Template Notes

## Template Source Location

Primary template: `Docs/09_Registers/Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-SUST-001.html`

This is the canonical reference for structure, CSS classes, and layout. Do not recreate from scratch — always copy this and adapt.

## HTML Structure

```
.sheet.cover         → Page 01 (cover + DC + QC)
.sheet               → Pages 02+ (ToC, CV pages)
  .doc-strip         → Header line (team name · pack title · page info — NO rev/date)
  .logo-strip        → 4-column grid of logos (MoC, ACE, CG, Samaya)
  h1                 → Team name (cover page)
  .meta-grid         → 3-column grid with Project/Contract, Submitted to, Issued by, Reference, Doc No., Status
  .dc-block          → Document Control table (Document No., Revision, Issue Date, Status, Distribution)
  .qc-block          → QC Sign-Off table (Prepared by, Review by QC, Approved by)
  .summary-table     → Table of Contents with personnel list
```

## CSS Classes to Know

| Class | Purpose |
|-------|---------|
| `.doc-strip` | Page header line with doc/team name and page info |
| `.logo-strip` | Four-party logo row |
| `.meta-grid` | Cover page metadata (3-column grid) |
| `.dc-block` | Document control table |
| `.qc-block` | QC sign-off table |
| `.summary-table` | Table of contents |
| `.mission-brief` | Aseer Regional Museum · Mission Brief heading + paragraph box |
| `.exp-block` | Professional experience entry |
| `.exp-head` | Experience header (role + dates) |
| `.edu-row` | Education entry |
| `.contact` | Person contact info bar |
| `.skills` | Core competencies list |

## Key CSS Values

- Font: `'Calibri','Carlito','Arial','Helvetica',sans-serif` from Google Fonts
- Page: A4 portrait, 210mm × 297mm, padding 14mm 18mm (cover: 12mm 16mm)
- Ink: black (#000000) on white (#FFFFFF)
- Logos: height 10mm, object-fit contain
- Print `@media` rules enforce exact sizing and page breaks

## Per-Page Pattern

Every `.sheet` div (including cover) must have:
1. `.doc-strip` — the page header
2. `.logo-strip` — the four logos
3. Content specific to that page type

## CV Page Details

Each person gets:
- **Part 1:** Professional Summary, Mission Brief, Coordination Scope, Core Competencies, Technical Skills
- **Part 2:** Professional Experience (chronological), Education, Certifications, Languages

Part 2 header includes a "Continued · Part X of Y" tag in the upper right.

## Sub-Consultant Naming

When the team is from a sub-consultant (e.g. AD Engineering Company), structure the cover title as:

```html
<h1>AD Engineering</h1>
<div style="font-size: 14pt; font-weight: 700;">MEP Design Department</div>
<div style="font-size: 11pt; font-weight: 600; color: #595959;">Aseer Regional Museum · Project 3092</div>
```

The logo strip always stays as MoC / ACE / CG / Samaya. The sub-consultant appears only in the title block and in Mission Brief body text.

## Appendix Pages (Small Teams)

For packs with 1–3 people, append a certificate appendix page. Use this block structure:

```html
<div class="appendix-block">
  <div class="head">Saudi Council of Engineers — Consultant Registration Certificate</div>
  <div class="body">
    <p><span class="k">Name:</span> Person Name</p>
    <p><span class="k">SCE No.:</span> 12345</p>
    <p><span class="k">Classification:</span> Consultant</p>
  </div>
</div>
```

Add these styles to `<style>`:
```css
.appendix-block { margin-top: 5mm; }
.appendix-block .head { background: #000; color: #FFF; font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 1.2mm 3mm; }
.appendix-block .body { border: 0.8pt solid #000; border-top: none; padding: 3mm; font-size: 8.5pt; }
.appendix-block .body .k { font-size: 7pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #444; }
```

## Page Numbering for Small Packs with Appendices

total_pages = 2 (cover + toc) + (2 × num_personnel) + num_appendix_pages
