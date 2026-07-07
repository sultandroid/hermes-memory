# CV Submittal Pack Template Notes

## Template Source Location

Primary template: `Docs/09_Registers/Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-SUST-001.html`

This is the canonical reference for structure, CSS classes, and layout. Do not recreate from scratch — always copy this and adapt.

## HTML Structure

```
.sheet.cover         → Page 01 (cover + DC + QC)
.sheet               → Pages 02+ (ToC, CV pages)
  .doc-strip         → Header line (team name · page info — NO rev/date)
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
