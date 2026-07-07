# Comprehensive MOS Pattern — Extended 15-Section + HTML-First

Extends the basic `references/method-of-statement-pattern.md` (10-section DOCX) for **image-rich, HTML-first** Method of Statements — LiDAR scanning, heritage documentation, commissioning procedures, etc.

## When to use this over the basic pattern

- The MOS needs **embedded product/process photos** (not just text tables)
- The deliverable is **HTML-first** (browser viewing, printing, sharing) rather than DOCX-first
- The MOS covers **multiple survey rounds** (as-is → after demolish → during construction → final as-built)
- The scope includes **complementary data capture** (360 photos, drone, thermography) alongside the primary method

## Extended MOS structure (15 sections)

| # | Section | When required |
|---|---------|--------------|
| 1 | Introduction & Project Background | Always — project overview, key data table, building context |
| 2 | Scope of Work | Always — tabulate **scan rounds** if multiple stages exist |
| 3 | Equipment & Specifications | Always — product table + photo of selected equipment |
| 4 | Survey of Surrounding Area / Neighbors | When exterior context matters (adjacent buildings, roads, utilities) |
| 5 | 360° Photography Workflow | When 360 photos complement the point cloud (heritage/visual record) |
| 6 | Point Cloud / Cloud Survey — Cloud-to-BIM | Always for scanning MOS — acquisition → registration → classification → export |
| 7 | Execution Methodology | Always — step-by-step field procedure |
| 8 | Data Processing Pipeline | Always for scanning/digital work — registration, filtering, export |
| 9 | BIM Integration Workflow | When the survey feeds a BIM workflow (Revit, AutoCAD, Navisworks, CDE) |
| 10 | Quality Control Plan | Always — QC checks table with acceptance criteria |
| 11 | HSE & Risk Assessment | Always — risk register, PPE, emergency contacts |
| 12 | Deliverables Schedule | Always — per scan round, per milestone |
| 13 | Approval & Sign-off | Always — signature blocks, distribution list |
| 14 | Appendix A — Brochure/Reference | Optional — scanned brochure pages as image reference |

## The 4 Scan Rounds pattern (for construction projects)

When the project has phased construction/demolition, define 4 scan rounds:

| Round | Timing | Purpose |
|-------|--------|---------|
| A — AS-IS NOW | Before any work | Baseline record of existing conditions; feeds demolition design and structural verification |
| B — AFTER DEMOLISH | Post-demo, before new work | Captures exposed structure, MEP risers, hidden conditions revealed by demolition |
| C — DURING CONSTRUCTION | At key hold-points | Progress monitoring: structural frame, MEP rough-in, ceiling closure before and after |
| D — FINAL AS-BUILT | At practical completion | Verification record for handover; BIM model update to as-built; O&M reference |

Each round gets its own scan count estimate, duration, and deliverable set.

## HTML-first generation pattern

For image-rich MOS, generate HTML directly (not DOCX):

1. **Write the HTML as a Python f-string** in a gen script. This lets you:
   - Embed images as base64 (portable single-file output)
   - Use full CSS control (A4 print layout, @page rules, page-break-before)
   - Include responsive tables that work in browser AND print

2. **Add Samaya branding** via inline CSS:
   ```css
   <style>
     :root { --navy: #1E293B; --red: #B01E2F; --gray: #334155; --med-gray: #64748B; }
     body { font-family: Calibri, Arial, sans-serif; font-size: 11pt; margin: 2.5cm; }
     @page { size: A4; margin: 2.5cm 2cm 2cm 2.5cm; }
   </style>
   ```

3. **Embedding images from the web** — workflow:
   - Search Faro/Leica official sites via `browser_navigate` for product images
   - Download via `curl` or `wget` to an `images/` subfolder
   - Convert to base64 in the gen script using `base64.b64encode(open(f, 'rb').read())`
   - Embed inline: `<img src="data:image/jpeg;base64,..." />`
   - For brochure PDFs, extract pages as JPG using PyMuPDF:
     ```python
     import fitz
     doc = fitz.open("brochure.pdf")
     page = doc[i]
     pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
     pix.save("page.jpg")
     ```

## Key differences from basic MOS pattern

| Aspect | Basic (DOCX) | Comprehensive (HTML) |
|--------|-------------|---------------------|
| Sections | 10 | 15 |
| Images | None (text only) | Embedded product + process + brochure photos |
| Output | .docx | .html (single file, print-ready) |
| Scan rounds | Single scope | 4 rounds (as-is → demo → construction → as-built) |
| 360 photos | Not mentioned | Dedicated section |
| Neighbors survey | Not mentioned | Dedicated section |
| BIM workflow | Brief | Full workflow: Revit, AutoCAD, Navisworks, CDE |
| Generation | Python SamayaDoc class | Python f-string HTML + base64 images |
| File size | ~50–200 KB | ~2–5 MB (image-heavy) |

## Typical image sources for LiDAR MOS

| Image type | Source | How to get |
|-----------|--------|------------|
| Scanner product photo | Faro.com / Leica.com product pages | Browse → download via curl |
| Scanner on tripod (field) | Faro press kit / Google Images | Browse Faro newsroom |
| Point cloud screenshot | Generated in Faro SCENE or Cyclone | Render from registration software |
| Surveyor scanning | Stock photo / project photo | Download from licensed source or use project camera |
| Brochure pages | PDF from vendor | PyMuPDF extract → JPG |
| 360 camera | Manufacturer site (Insta360, Ricoh) | Browse → download |

## Pitfalls

- **Image size**: Base64-encoded images are ~37% larger than binary. A 150KB JPEG becomes ~210KB in base64. Keep each image ≤ 200KB (resize if needed).
- **Page breaks**: Use `page-break-before: always` on section titles, not `page-break-after` (avoids orphan blank pages).
- **Brochure extraction**: PyMuPDF `get_pixmap(matrix=fitz.Matrix(2,2))` gives good 1200dpi output. Matrix(1,1) may be too blurry for text.
- **Print layout**: Test browser print with A4 paper size. Some browsers default to US Letter — set `@page { size: A4; }`.
- **Table overflow**: 15+ column tables may overflow A4 width. Keep tables to ≤ 6 columns, or use landscape sections.
- **Image captions**: Always add a figcaption below each image so the reader knows what they're looking at.
- **Delegation fit**: Generating a 15-section, 3MB+ HTML with embedded images is a good candidate for `delegate_task` — the subagent can produce the complete file in isolation without flooding your context window. Pass exact image paths, project data, and section requirements in the `context` field.

### Image embedding — required verification

Subagents frequently download HTML error pages instead of real images. Always verify downloaded images:

```
file image.jpg    # Must say "JPEG image data", not "HTML document"
```

For base64-embedded images, verify decoded bytes start with JPEG magic bytes `ffd8`:
- Run `file` on the actual image file on disk
- If it says "HTML document", the download failed — delete and re-download from a reliable source
- Fallback: extract from brochure PDF using PyMuPDF (more reliable than web download)

### Logo sourcing — use actual logo files

Stakeholder logos live at: `~/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/logos archives/`
- `moc-logo.png` (MoC)
- `pmc-logo-trans.png` (ACE — PMC)
- `cg-logo-trans.png` (CG — Consultant)
- `samaya-logo-trans.png` (Samaya)

Do NOT create custom SVG logos — use the actual PNG files. Embed as base64 img tags in a 4-column logo-strip grid.

### Project data — verify from PROJECT_MEMORY.md

Never use rough estimates for site area. The authoritative source is PROJECT_MEMORY.md ~line 93:
```
| Site Area | 4,616 m² | Duration: 303 days |
```
Search with: `grep -i "site area" PROJECT_MEMORY.md`

### Equipment — confirm with user, do not assume

Common corrections: built-in HDR camera handles 360° imagery (no separate 360 camera needed), processing at office workstation (no field laptop). Mark uncertain items as TBC and ask.

### SVG flowcharts — engineering construction plan quality

Flowcharts must match the quality of construction engineering plans:
- viewBox width = 1305 (174mm at 7.5 units/mm) for A4 fit
- Card layout with feDropShadow, dark navy headers (#1E293B), 12-14pt headings
- Light gray backgrounds (#F1F5F9), dashed borders for secondary boxes
- Minimum 9pt body text, arrow connectors between stages
- Types: horizontal pipeline (workflow), timeline (scan rounds with Gantt bar), vertical columns (data processing stages)
