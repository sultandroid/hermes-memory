# Method of Statement (MOS) — DOCX and HTML Generation Pattern

## When to generate an MOS

Any time a subcontractor, supplier, or in-house team needs a formal construction methodology document --- 3D laser scanning, MEP installation, fit-out works, block work, finishing, etc.

## Two format tracks

| Track | Output | Workflow |
|-------|--------|----------|
| **DOCX** | `.docx` via SamayaDoc | python-docx script, one-off for simple MOS |
| **HTML** (preferred for submittals) | `.html` + `.pdf` via weasyprint | Full HTML template with logos, photos, PMBOK structure |

**Prefer HTML for submittal-quality MOS documents.** HTML supports embedded photographs, 5-stakeholder logo cover page, TOC with snapshot cards, workflow diagrams, and risk matrices. Only use DOCX for internal/draft versions.

## Document ref pattern

```
MOC-ASEER-SIC-1K0-MOS-NNN      (old prefix, Aseer Museum)
MOC-MUS-ASE-1K0-MOS-NNN        (new prefix, MUS = Museum)
```

## PMBOK Structure for MOS

| MOS $ | Title | PMBOK $ |
|-------|-------|---------|
| 1 | Document Control & Revision Log | 4.0 Integration |
| 2 | Purpose, Scope & Definitions | 5.0 Scope |
| 3 | References & Applicable Standards | 4.3 Integration |
| 4 | Roles, Responsibilities & Communication | 9.0 Resources |
| 5 | Equipment, Materials & Software | 9.3 Resources |
| 6 | Execution Sequence & Workflow | 4.0-6.0 Execution |
| 7 | Data Processing & BIM Workflow | 6.0 Schedule |
| 8 | Quality Control & Inspection Plan | 8.0 Quality |
| 9 | Health, Safety & Environment | 10.0 HSE |
| 10 | Risk Assessment & Mitigation | 11.0 Risk |
| 11 | Approval & Authorisation | 4.7 Closure |

## Standard section content

- **$1 Document Control:** Revision log table, doc identification strip (ref, title, project, org, status, security), distribution table
- **$2 Purpose & Scope:** Narrative intro + tabulated scope items + definitions/abbreviations table
- **$3 References:** Project docs table, industry standards table, vendor docs table
- **$4 Roles:** Direct personnel table, supervision/sign-off table, communication protocol table
- **$5 Equipment:** Equipment specs table (8-12 items), software table, photo of primary equipment
- **$6 Execution:** Process flow diagram (6-phase workflow nodes), pre-mob steps table, control network, field procedure (7-step table with operator photo), scan plan requirements
- **$7 Data Processing:** Registration, clean-up, BIM integration (with point cloud + coordination photos side-by-side), BIM workflow step diagram, deliverables table, processing timeline
- **$8 QC:** QC acceptance criteria table (7+ parameters), ITP hold points table (H-01 through H-06), QC responsibility note
- **$9 HSE:** HSE item table (9 items: PPE through Environmental), emergency contact table
- **$10 Risk:** Risk matrix table with L/I/Score/Impact/Mitigation columns, risk score key
- **$11 Approval:** Sign-off table (Prepared/Reviewed x2/Approved), CG review endorsement box

## MOS for DOCX (SamayaDoc)

See the gen script skeleton in the SKILL.md. Standard column widths:

| Table | Column widths (cm) |
|-------|-------------------|
| Revision Log | [1.0, 2.0, 5.5, 2.5, 2.5, 2.5] |
| Scope of Work (# / Item / Description) | [1.0, 3.5, 11.5] |
| Equipment (Item / Spec) | [4.0, 12.0] |
| Personnel (Role / Qty / Responsibility) | [3.0, 1.0, 12.0] |
| Step-by-step (# / Step / Description) | [1.0, 2.5, 12.5] |
| QC (Parameter / Criteria / Method) | [4.0, 5.5, 6.5] |
| HSE (# / Item / Requirement) | [1.0, 3.5, 11.5] |
| Risk (Risk / Impact / Mitigation) | [4.0, 4.5, 7.5] |
| Sign-off | [2.5, 3.5, 4.0, 3.5, 2.5] |

## MOS for HTML (print-ready)

Two template variants exist:

### 1. Colored Template (default)
See `references/samaya-html-print-template.md` for the full design system. Dark navy cover with 5 stakeholder logos, blue accent bars, green status badges. Used for SMP, BEP, Risk Plan, and most formal submittals.

| Element | Style |
|---------|-------|
| Cover | Dark navy `#0F172A` background, white text, 5 stakeholder logos |
| Tables | Navy header `#0F172A`, white text, alternating rows `#F8FAFC`/white |
| Headings | 18pt Montserrat uppercase, blue accent bar |
| Body | 10pt Inter, `#1E293B` |
| Photos | Bordered `.photo-frame` with captions |

**PDF generation:** WeasyPrint (see `references/samaya-html-print-template.md`).

### 2. Monochrome CV-Pack Template (when user requests)
When the user says "use same template" and points to `ASR-SAM-KP-CV-PACK-BIM-001.html`, use the monochrome variant. See `references/samaya-html-print-template.md` § "Design Variant: Monochrome CV-Pack Template" for full CSS detail.

| Element | Style |
|---------|-------|
| Cover | White background, black text, 4-column logo strip |
| Tables | Bordered black headers, no fill |
| Headings | 22pt/10pt Calibri uppercase, black bottom border |
| Body | 9.75pt Calibri/Carlito, black |
| Photos | Full-width, max-width:80% centered, no border |
| Pages | 210×297mm sheets, 14/18mm padding, drop shadow |
| DC/Qc blocks | Black header bar, white text, bordered content |

**PDF generation:** Open in browser → Ctrl+P → Save as PDF. No WeasyPrint needed.

## Personnel Verification Protocol (CRITICAL)

Before writing ANY person's name into a sign-off table or personnel table:

1. **Open SMP Rev03 HTML** at `02.13_Stakeholder_Plan/01_Source_Files/01_HTML/MOC-ASEER-SIC-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html`
2. Extract QC-01 through QC-04 for Samaya management:
   ```
   grep -oP 'QC-0[1-4].*?</td>' file.html
   ```
3. Extract T1-01 through T1-08 for key personnel:
   ```
   grep -oP 'T1-0[1-8].*?</td>' file.html
   ```
4. Also check `~/Stakeholder_Register_Update_Findings.md` for recent changes (departures, new appointments)
5. Cross-reference all roles against the sign-off table being filled

**Do NOT use generic role titles, do NOT leave names blank, do NOT invent from memory.**

## Logo sourcing for MOS HTML documents

For the monochrome CV-pack HTML template, stakeholder logos are NOT custom SVGs. Use the actual logo PNG files from:

```
~/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/logos archives/
├── moc-logo.png           (MoC — Employer)
├── pmc-logo-trans.png     (ACE — PMC)
├── cg-logo-trans.png      (CG — Consultant)
├── samaya-logo-trans.png  (Samaya — Main Contractor)
```

Embed as base64 `<img class="lg">` in a 4-column logo-strip `<div>`. Each cell has `.rt` (role) and `.nm` (name) labels below the image.

## Equipment confirmation rule

Before finalizing any MOS, verify equipment assumptions with the user. Common corrections:
- 360° imagery comes from the **scanner's built-in HDR camera**, not a separate 360 camera
- Data processing happens at the **office workstation** (Technical Office), not a field laptop
- For any item not explicitly listed in project docs or vendor quotations, mark as TBC
- Do NOT add equipment the user didn't ask for — simplify to what's actually being used

**When in doubt, ask rather than assume.** The user will correct you — capture the correction as a pitfall in the skill.

## SVG flowchart sizing for A4 print

When embedding SVG flowcharts in the HTML MOS, they MUST have explicit width/height to render at readable size within the A4 page:

```html
<svg width="100%" style="max-width:100%;height:auto;display:block" viewBox="0 0 1305 450" ...>
```

- **viewBox** must match the design coordinate space (e.g., 1305×450 for wide timeline)
- **width="100%"** ensures scaling to fit 174mm A4 content area
- **style** prevents overflow and maintains aspect ratio
- Without these, SVGs render at full viewBox pixels (1305px) and overflow the page

**Icons** (24×24 viewBox) need `width="24" height="24"` explicitly on the `<svg>` tag.

## Image sourcing verification

When downloading images from the internet for HTML MOS documents:

1. Download with `curl -sL -o <path> <url>`
2. **ALWAYS verify** with `file <path>` — must return "JPEG image data" or "PNG image data"
3. If `file` returns "HTML document" or "text", the download returned an error page — discard and try another source
4. Prefer Wikimedia Commons (CC-licensed) over stock photo sites that block bots
5. Embed as base64 in the HTML for self-contained documents

## Using DOCX templates as language/structure reference

When the user provides a DOCX file as reference (e.g., a generic Method Statement template):

1. Extract text with `python3 -c "import docx; doc = docx.Document('PATH'); [print(p.text) for p in doc.paragraphs if p.text.strip()]"`
2. Extract tables with `doc.tables` and iterate row/cells
3. Map the DOCX's structure onto the existing HTML — do NOT replace content but merge the professional language
4. Key elements to extract: Inclusions/Exclusions, Team/Roles tables, QA/QC stage breakdowns, Scan-to-BIM detailed steps, HSE bullet points
5. Keep all project-specific data (building area, equipment, location) from the project files
6. Use targeted `patch` operations to update specific sections — preserve SVGs, images, and document structure

## Building area verification

Before writing building area in any MOS:
- The authoritative source is PROJECT_MEMORY.md contract data section: `| **Site Area** | 4,616 m² |`
- Do NOT use rough estimates from vendor docs (e.g., "4,000 sqm for scanning" is vendor marketing)
- If floor-level breakdowns aren't in project files, allocate proportionally from the total

## Pitfalls

- The SamayaDoc add_h1/h2/h3 methods use custom styled paragraphs, not Word heading styles
- For HTML: always use `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` prefix for weasyprint on macOS
- WeasyPrint SSL cert errors for Google Fonts are cosmetic; fonts fall back to system sans-serif
- HTML documents may optionally deploy to Surge.sh for client/team review before PDF issue — but only if user explicitly asks for a live link. Default is local-only (open HTML in browser, print to PDF).
- Table body cells: plain text only, no bold, no emoji icons --- applies to both HTML and DOCX
- Every MOS must start with the revision log and end with a sign-off table containing real names
