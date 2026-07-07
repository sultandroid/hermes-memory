# CV Submittal Pack — Template Structure Reference

Based on `ASR-SAM-KP-CV-PACK-SUST-001.html` (Sustainability pack, 1 person, 5 pages) and `ASR-SAM-KP-CV-PACK-BIM-001.html` (BIM pack, multi-person).

All packs share identical CSS and page layout. Differences are only in content.

## CSS Breakdown

- **Font**: Carlito/Calibri via Google Fonts `'Carlito', 'Calibri', 'Arial', 'Helvetica', sans-serif`
- **Base**: 9.75pt, 1.32 line-height, black on white
- **Page wrapper (`.sheet`)**: 210mm × 297mm, padding 14mm 18mm (cover: 12mm 16mm), shadow for screen
- **Print media query**: strict A4 sizing, `overflow: hidden`, `page-break-after: always`
- **Reserved properties** (must match exactly): `--ink: #000000`, `--rule: #000000`, `--paper: #FFFFFF`

## Key CSS Classes

| Class | Purpose |
|-------|---------|
| `.sheet` | Page wrapper, one per page |
| `.sheet.cover` | Cover page (narrower padding) |
| `.doc-strip` | Top document reference line (8.5pt, bottom border) |
| `.logo-strip` | 4-column grid with logos and entity labels |
| `.meta-grid` | 3-column info grid (Project, Submitted to, Issued by, Reference, Doc No., Status) |
| `.dc-block` | Document Control table with `.dc-grid` (5 columns) |
| `.qc-block` | QC Sign-off with `.qc-grid` (3 columns) |
| `.summary-table` | Table of Contents with sticky thead |
| `.exp-block` | Experience entry (employer, dates, bullets) |
| `.edu-row` | Education row (degree, institution, year) |

## CV Section Order (per person)

**Part 1:**
1. `<h1>` Name (large bold, uppercase)
2. `<div class="headline">` Role description line
3. `<div class="contact">` Contact info separated by " · "
4. `<h2>` Professional Summary — paragraph
5. `<h2 class="mission-brief">` Aseer Regional Museum · Mission Brief — styled box with project-specific responsibilities
6. `<h2>` Aseer Coordination Scope — `<ul>` of bullet points
7. `<h2>` Core Competencies — `<div class="skills">` with `<span>` elements
8. `<h2>` Technical Skills & Software — `<p>` with bold category labels

**Part 2:**
1. Name + role subtitle with "Continued · Part 2 of 2" tag
2. `<h2>` Professional Experience — series of `.exp-block` entries
3. `<h2>` Education — `.edu-row` entries
4. `<h2>` Certifications & Workshops — if applicable
5. `<h2>` Languages — `<p>` line
6. For long CVs, add Part 3 with `(continued)` in heading

## Page Numbering Logic

- `cover.html` header says "Page 01 of N"
- `toc.html` header says "Page 02 of N"
- CV pages count from 03 upward: 2 pages per person
- For N people: total pages = 2 (cover + toc) + (2 × N)
- Doc-strip format: `{TEAM_LABEL} · {DOC_TITLE} · Page XX of YY · {section context}` — NO Rev/Date (DOC fills these)

## Multi-Person ToC

Section header row: `<td colspan="4">` with background `#FAFAFA`, uppercase bold, letter-spaced.
Each person row: `#` | `Name` | `Role ⸱ certs` | `Page range (p. 03–04)`

For small teams with appendices, add an "Appendices" section header row at the bottom with rows for each certificate.

## Logo Strip (All Pages)

```html
<div class="logo-strip">
  <div class="cell">
    <img src="../_assets/logos/moc.png" alt="Ministry of Culture" class="lg">
    <div class="rt">Employer</div>
    <div class="nm">Ministry of Culture</div>
  </div>
  <div class="cell">
    <img src="../_assets/logos/pmc_ace.png" alt="ACE Moharram Bakhoum (PMC)" class="lg">
    <div class="rt">PMC</div>
    <div class="nm">ACE Moharram Bakhoum</div>
  </div>
  <div class="cell">
    <img src="../_assets/logos/cg.png" alt="Consultancy Group" class="lg">
    <div class="rt">Consultant</div>
    <div class="nm">Consultancy Group</div>
  </div>
  <div class="cell">
    <img src="../_assets/logos/samaya.png" alt="Samaya Investment" class="lg">
    <div class="rt">Main Contractor</div>
    <div class="nm">Samaya Investment</div>
  </div>
</div>
```

**Note:** The `../_assets/logos/` path is relative to `_archive/HTML/`. If the HTML file lives elsewhere (e.g. `MEP Team/Ad Team/`), adjust: `../../_archive/_assets/logos/`. Logos are always at `CVs/_archive/_assets/logos/`.

**⚠ Common mistake:** Templates in `_archive/HTML/` use `../_assets/logos/` (one level up). A file in `MEP Team/Ad Team/` needs `../../_archive/_assets/logos/` (two levels up then into `_archive/_assets/`). The wrong path `../../_archive/HTML/_assets/logos/` has an extra `HTML/` segment and fails to load. Always verify by resolving the absolute path before finalising.
