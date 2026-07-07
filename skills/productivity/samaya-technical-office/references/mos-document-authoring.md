# MOS (Method of Statement) Document Authoring — Conventions

## Applicable Documents
Method of Statement HTML documents for Aseer Museum BIM Unit (e.g., MOC-ASEER-SIC-1K0-MOS-001 — 3D LiDAR Survey).

## Field Conventions — What the Document Controller Fills

| Field | Rule | Reason |
|---|---|---|
| **Document No.** | Leave as `—` (em dash) | DC assigns upon issue |
| **Issue Date** | Leave as `—` (em dash) | DC stamps upon issue |
| **Document Ref. (cover)** | Show `— · Rev NN` only (no date) | Same — DC fills |
| **Page footers** | Show `— · Rev NN` in the `.dc` span | DC fills doc number later |
| **Appendix strips** | Same pattern: `— · Appendix Page X of Y` | DC assigns at issue |

**Implementation:** When building the HTML, use `—` for doc number and omit dates entirely. Use `— · Rev 00` as the footer/dc-strip pattern.

## Area / Level Data Table

Structured as an `<table class="eng-table">` with columns: Level, Description, Area (sqm), Est. Scans.

**When updating areas:**
- Always update ALL locations: (1) cover Building field, (2) Section 1 intro paragraph, (3) the table itself, (4) Totals row
- Roof Deck / exterior areas often change — recalculate total after every correction
- Scan estimates should be proportional to area (use same density ratio as original calculation)
- Flag scan estimate adjustments to the user for confirmation

## Figure / Image Sizing

Large base64-encoded images embedded in HTML must be constrained:

```css
.figure img { max-width: 100%; max-height: 130mm; height: auto; width: auto; }
```

Without `max-height`, images at native resolution overflow the A4 page. 130mm (~half page) is the standard cap.

## TOC — Grouped Table Structure

Use multiple `<tbody>` elements with a group-header row to classify the table of contents:

```html
<tbody>
  <tr style="background:#F1F5F9;">
    <td colspan="3" style="font-weight:700; font-size:0.48rem; letter-spacing:0.04em; border-bottom:1.5px solid #0F172A;">
      N — GROUP NAME
    </td>
  </tr>
  <tr><td class="num">X</td><td>Section Title</td><td class="pg">p. NN</td></tr>
</tbody>
```

Standard groups for MOS docs:
1. **PROJECT FOUNDATION** (Introduction, Scope)
2. **SURVEY METHODOLOGY** (Equipment, Surroundings, Photography, Point Cloud, Execution)
3. **DATA PROCESSING & BIM** (Pipeline, BIM Integration)
4. **QUALITY, HSE & DELIVERY** (QC Plan, HSE, Deliverables)
5. **APPROVAL** (Sign-off)
6. **APPENDICES** (A, B, ...)

## Appendices

- **Appendix A** — Manufacturer brochure (Faro Focus Premium, from vendor)
- **Appendix B** — Certification documents (table format with columns: #, Document, Issuer, Scope, Valid Until)

Do NOT embed full PDFs as base64 in the HTML (file becomes too large for Surge upload). Instead:
- Use a descriptive table covering key data (document name, issuer, scope, expiry)
- Store the actual PDFs in a `Certifications/` subfolder alongside the MOS
- Add a note: *"Full PDF copies maintained under project document control"*
- Reference Appendix B in Section 3.3 text and Section 10.6 QC documentation list

## QC Documentation List (Section 10.6)

When adding certification documents to the QC docs list, insert entries between "Calibration certificate" and "Deliverable transmittal sheet":

```html
<li>FARO ISO 9001:2015 Quality Management System Certificate (Appendix B)</li>
<li>CE Declaration of Conformity — Faro Blink Laser Scanner (Appendix B)</li>
<li>ISO/IEC 17025 Calibration Laboratory Accreditation — FARO UK &amp; Exton (Appendix B)</li>
```

## Derivative / One-Page Summary Sheets

It is common to extract one or two sections (e.g., "3.2 Support Equipment" + "4. Survey of Surrounding Area") into a separate single-page HTML for quick reference or printing.

**Rule:** the derivative sheet is NOT the authoritative MOS. If the user later asks to "update Section 4" or "update the original file," patch the **source MOS HTML**, not only the derivative.

Workflow:
1. Create the derivative with a filename that clearly marks it as extracted, e.g., `MOC-ASEER-SIC-1K0-MOS-001_Rev00_Sections_3.2_and_4.html`.
2. When adding new site-specific data (e.g., neighbor names from coordinates), update BOTH files only if the user asks for both. Otherwise default to the source MOS.
3. Use compact inline styles for new tables on fixed-height A4 sheets (`font-size:0.76rem`, reduced padding) so the sheet does not overflow.
4. After patching the source MOS, open it for the user to review; do not rely on the derivative being in sync.

## Identifying Surrounding Neighbors from Site Coordinates

For Section 4 "Survey of Surrounding Area / Neighbors," use the `maps` skill's Overpass recipe to identify actual named features around the given coordinate. See `maps/references/construction-site-context.md` for the full query, parsing script, and Aseer Museum example.

Key presentation rules:
- Use English names (`name:en`) when available; romanize Arabic names if no English tag exists.
- Include distance and approximate direction.
- Highlight items relevant to survey scope: roads/logistics, adjacent buildings, heritage structures, hospitals/mosques (safety/noise constraints).
- Note that OSM data is community-maintained; verify critical distances against the project survey if possible.

## Deployment

MOS HTML files become large (6-7 MB) due to embedded base64 images. Surge upload is slow:
- Use `npx surge` (NOT plain `surge`) — avoids `TypeError: Cannot read properties of undefined (reading 'filename')`
- Deploy via background PTY with 600s timeout
- Upload speed: ~1-2% per 30 seconds → expect 10-25 minutes for 6.7MB file
- After successful deploy, verify with `curl -sI https://domain/` — expect 200 on retry after 10s cold start

See `web-deployment` skill for full Surge workflow.
