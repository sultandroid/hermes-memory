---
name: cv-submittal-pack
title: CV Submittal Pack — AEC Key Personnel
description: Create formal Key Personnel CV submittal packages for Aseer Museum (and similar Samaya projects) following the branded A4 template. Covers extracting CV text, building HTML from template, converting to PDF, and filing.
triggers:
  - User wants to submit CVs for consultant/team approval (CV submittal, CV pack, key personnel submission)
  - User mentions creating a submittal package for a team
---

# CV Submittal Pack — AEC Key Personnel

## Overview

Create formal CV submittal packages following the existing branded template. Each pack is a multi-page A4 PDF with cover page (document control + QC sign-off), table of contents, and 2-page CV sections per person. Packs live under `Key_Personnel_Register/CVs/{Team Name}/`.

## Template Source

The reference template is at the `_archive/HTML/` folder:

```
Docs/09_Registers/Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-BIM-001.html
- or any existing pack in _archive/HTML/
```

Copy the closest existing pack's HTML and adapt (same CSS, same page structure).

## Naming Convention

Final files stored WITHOUT document numbers (DC assigns those later):

| Pack type | Pattern |
|-----------|---------|
| **Full team pack** (multiple people) | `{Team Name} · Key Personnel CV Submittal Pack.html` |
| **Supplementary — single person** | `{Team Name} · Key Personnel CV Submittal Pack · {Person Name} · {Role}.html` |
| **Archived (with doc number)** | `{Team} · Key Personnel CV Submittal Pack · ASR-SAM-KP-CV-PACK-{TEAM}-{NNN}.pdf` |

When adding a new individual to an existing team's register, create a **supplementary single-person pack** with the person's name in the filename. This distinguishes it from the main team pack without requiring a new document number or restating the main pack's scope.

## Page Structure

### Multi-person pack (2+ people)

| Page | Content |
|------|---------|
| p.01 | Cover + Document Control + QC Sign-off |
| p.02 | Table of Contents — Personnel Summary |
| p.03–04 | CV Person 1 (Part 1 of 2, Part 2 of 2) |
| p.05–06 | CV Person 2 (Part 1 of 2, Part 2 of 2) |
| ... | Repeat per person |

### Supplementary single-person pack

| Page | Content |
|------|---------|
| p.01 | Cover — subtitle reads "Supplementary CV Submission — {Role}" with person's name below team name |
| p.02 | Table of Contents (single entry, section header reads "Supplementary") |
| p.03 | CV Part 1 |
| p.04 | CV Part 2 |

**Cover differences for supplements:**
- Title block subtitle changes from the team-scope description to "Supplementary CV Submission — {Role}"
- Person's name appears below the team heading on the cover
- Contents line references single CV: "CV 01 (p. 03 — p. 04)"
- doc-strip includes person's name for traceability

**TOC differences for supplements:**
- Section header row reads "{Team} — Supplementary" to distinguish from main pack
- Single row in table of contents

## Template Elements (All Pages)

- **doc-strip**: `{PROJECT_NAME} · {TEAM_NAME} · Key Personnel CV Submittal Pack · Page XX of YY · {section context}` — no doc reference/Rev/Date (DOC fills those)
- **Logo strip**: 4-column grid — MoC (Employer), ACE Moharram Bakhoum (PMC), Consultancy Group (CG), Samaya Investment (Main Contractor). Logos from `_assets/logos/{moc,pmc_ace,cg,samaya}.png`
- **Font**: Carlito/Calibri via Google Fonts
- **Page**: A4 portrait (210mm × 297mm), black-and-white formal style

## Cover Page (p.01)

- Title block: "Project Key Personnel — CV Submission Pack"
- Team name heading (large bold)
- Subtitle: "Aseer Regional Museum · Project 3092"
- **Meta-grid** (3 columns):
  - Project / Contract: `Aseer Regional Museum · Project 3092 · Contract 0010003521 (MoC ↔ Samaya)`
  - Submitted to: `CG — Eng. Mohammed Elbaz (Acting PM) · Abdrabo Shahin (Sr Structure Engineer)`
  - Issued by: `Samaya Investment — via Samaya Technical Office`
  - Reference: `KP Reg MOC-ASEER-SIC-1K0-KP-0001 · DMP §5.1.2 · SoW §5.5 · §13.7 / §13.8`
  - Doc No.: leave `—` for DOC to fill
  - Status: `Pending CG review and onward MoC approval. Once approved, KP cannot be removed without prior written MoC approval.`
- **Document Control table** (5 columns): Document No. | Revision | Issue Date | Status | Distribution
- **QC Sign-off table** (3 columns): Prepared By (Eng. Mohamed Sultan, Samaya TO Mgr) | Review By QC (Eng. Abd Elmohaymen Medhat, QA/QC Mgr) | Approved By (Eng. Muhammad Waris Sultan Khan, Samaya Proj Dir)
- Contents line at bottom

## Table of Contents (p.02)

- Header: `Table of Contents — Personnel Summary by Project Role`
- Table columns: `#` | `Name` | `Project Role` | `Page`
- Section header row per team with background

## CV Pages (p.03+)

Each person gets 2 pages:

**Part 1:** Name + role headline, contact bar (phone · email · location · years · certs), Professional Summary, Mission Brief (project-specific responsibilities using Aseer Museum context), Coordination Scope (bullet points), Core Competencies, Technical Skills & Software

**Part 2:** Header with "Continued · Part 2 of 2", Professional Experience (role by role with employer, dates, bullet points), Education, Certifications & Workshops, Languages

## ⚠ Critical Rules

1. **Document numbers** — existing template packs use document numbers (e.g. ASR-SAM-KP-CV-PACK-SITE-001). The DC variant rule below applies when the DC explicitly handles numbering; otherwise follow the template's existing pattern. When in doubt, match the reference template you're copying.
2. **Team naming** — use descriptive team names (e.g. "Aseer Sustainability Consultancy", "AD Engineering MEP Design Team"), not internal code names.
3. **Submit to CG** — all packs go to CG (Eng. Mohammed Elbaz) for review, then MoC approval. State this in the status field.
4. **QC sign-off** — always the same three people: Mohamed Sultan (TO Mgr), Abd Elmohaymen Medhat (QA/QC Mgr), Muhammad Waris Sultan Khan (Proj Dir). ⚠ Never use "Adel Darwish" — he is Projects Director support role, not PD.
5. **Sub-consultant entity** — if the team is from a sub-consultant (e.g. AD Engineering), their name goes in the cover subtitle/title block, NOT in the logo strip. The logo strip stays fixed as MoC (Employer) / ACE Moharram Bakhoum (PMC) / Consultancy Group (CG) / Samaya Investment (Main Contractor). The sub-consultant relationship is stated in the Mission Brief body text.

## Workflow Steps

1. Extract CV text from source PDFs using `pdftotext /path/to/cv.pdf -`
2. Find the closest existing HTML pack in `_archive/HTML/` as template
3. **Find and read the team's SOW document** — search under `02_Plans_and_Procedures/` for the relevant SOW (e.g. `SOW_{Team}.html`, `SoW extracts`). Read it to extract actual scope items for the Mission Brief. Do NOT ask the user for direction.
4. Adapt the HTML: change doc-strip, team name, page numbers, contents, and CV sections
5. Build CV text content (summary, scope, competencies, experience) from extracted text, using the SOW to inform the Mission Brief and Coordination Scope
6. Save HTML to the appropriate team folder (e.g. `Sustainability Team/`)
7. **Open the HTML in the browser for user review** — do NOT convert to PDF unless the user explicitly requests it. The user reviews and iterates on the HTML layout first. Mention in your response that the HTML is open for review.
8. **Check for overflow** using browser_console (see Overflow detection below)
9. When the user requests PDF conversion, generate via Chrome headless:
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless --print-to-pdf=/tmp/output.pdf --no-pdf-header-footer \
     file:///tmp/input.html
   ```
10. Copy both `.html` and `.pdf` to `Key_Personnel_Register/CVs/{Team}/`
11. Verify PDF renders correctly (page count via `fitz`, no overflow)
12. Update the Key Personnel Register Excel (.xlsx or .xlsx.bak) with new entries. Note: openpyxl cannot read .bak files directly — copy to .xlsx first, edit, then copy back.

## ⚠ Pitfalls

### Logo path resolution

Logos live at `CVs/_assets/logos/` (NOT `CVs/_archive/_assets/logos/`). From different HTML locations the relative path differs:

| HTML location | Relative logo path |
|---|---|
| `CVs/_archive/HTML/` | `../../_assets/logos/` |
| `CVs/Sustainability Team/` | `../_assets/logos/` |
| `CVs/Samaya Team/Stracture/` | `../../_assets/logos/` |

Always verify by resolving the path before finalising. The base directory is always `CVs/_assets/logos/` — count directory levels up from your HTML location.

### CV text extraction failure

`pdftotext` may return empty output for formatted/image-heavy PDFs. Fall back to PyMuPDF (fitz):

```python
import fitz
doc = fitz.open(path)
for page in doc:
    text = page.get_text()  # returns empty string if image-based
doc.close()
```

**Image-based PDF OCR rescue technique (when both pdftotext and fitz.get_text() return empty):**

Render each page at high resolution then OCR with pytesseract. 5x resolution is the sweet spot for A4 CV scans — lower doesn't work well, higher is slow:

```python
import fitz
from PIL import Image
import pytesseract

doc = fitz.open(path)
for i in range(doc.page_count):
    page = doc[i]
    pix = page.get_pixmap(matrix=fitz.Matrix(5, 5))   # 5x = ~300 DPI for A4
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    gray = img.convert('L')
    text = pytesseract.image_to_string(gray, lang='eng', config='--psm 4')
    print(text)

    # PSM 4 (assume single column of text) works best for CV layouts
    # Fall back to PSM 11 (sparse text) for decorative/image-heavy pages
    # Fall back to PSM 3 (default) if nothing works
doc.close()
```

Prerequisites: `pip install pytesseract pillow` + `brew install tesseract`.

Render each page at high resolution and OCR with pytesseract:

```python
import fitz
from PIL import Image
import pytesseract

doc = fitz.open(path)
for i in range(doc.page_count):
    page = doc[i]
    # 5x resolution is the sweet spot for A4 scans
    pix = page.get_pixmap(matrix=fitz.Matrix(5, 5))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    gray = img.convert('L')
    text = pytesseract.image_to_string(gray, lang='eng', config='--psm 4')
    # PSM 4 (assume single column) works best for CV layouts
    # PSM 11 (sparse text) as fallback for decorative/image-heavy pages
    if not text.strip():
        text = pytesseract.image_to_string(gray, lang='eng', config='--psm 11')
    print(text)
doc.close()
```

Prerequisites: `pip install pytesseract pillow` + `brew install tesseract`.

### Directory names with trailing spaces

Some folders have trailing spaces (e.g. `"Ad Team "`). This breaks shell commands (`cd "path "` fails). Use Python `os.listdir()` to detect the actual name, then reference it from Python code:

```python
import os
entries = os.listdir(base_dir)
target = [e for e in entries if e.startswith("Ad")][0]  # fuzzy match
```

### Overflow detection and compression

**Check page heights before delivering.** After building the HTML, open in a local browser and check page overflow:

```javascript
// In browser_console:
Array.from(document.querySelectorAll('.sheet')).map((s, i) =>
  `${i+1}: ${s.scrollHeight}px / ${s.clientHeight}px (overflow: ${s.scrollHeight > s.clientHeight})`)
```

The A4 printable area is ~269mm (297mm - 14mm top - 14mm bottom) ≈ 1017px at screen resolution. Any page exceeding that scrollHeight in screen mode will overflow the print layout. Always verify with a Chrome headless PDF generation before finalising.

**Compression techniques when a page overflows:**
- Merge 3+ consecutive short-duration/early-career roles into a single "Earlier Career" entry with one combined bullet point
- Trim verbose bullet points: remove filler phrases, use `&` instead of `and`, shorten date formats (e.g. `Feb 2024` not `February 2024`)
- Collapse long certification/education lists into a single `.edu-row.certs` entry with `·` separators and `font-size: 8pt`
- Reduce `h2` margin from `3.5mm` to `2.5mm` and `.exp-block` margin-bottom from `2.5mm` to `1.5mm` for the overflow page only

**Dense Mission Brief pushing Part 1 overflow**

When the Mission Brief and Coordination Scope contain 8+ specific bullet points (from a detailed SOW), Part 1 can overflow. Mitigations:
- Keep Professional Summary to 3-4 lines max
- Trim Core Competencies to 12-15 entries (omit obvious overlaps)
- Keep Technical Skills &amp; Software to a single paragraph
- If still tight, reduce `h2` margins or font-size on the sheet only

### Supplementary single-person pack overflow

Single-person packs (cover + TOC + one CV) can also overflow Part 2 when a person has 7+ employers. Apply the same compression techniques from the overflow section above. The `edu-row.certs` pattern (single-row, `·`-separated, 8pt font) aggressively compresses certifications that would otherwise take 10+ individual rows.

For packs with 1–3 people, include an appendix page for certificates (SCE, BMR, professional registrations) after the CV pages. This fills pages without wasting space. The TOC should list appendix entries with a section header.

#---

## Variant Rules (absorbed from `key-personnel-cv-submittal-pack`)

### DC-Handled Fields — Labels Stay, Values Blank

When creating CV packs, the Document Control block keeps its label structure but values are left blank for the DOC to fill:

- **Doc No.** — keep the label cell, value = `—`
- **Revision** — keep the label cell, value = `—`
- **Issue Date** — keep the label cell, value = `—`
- **Status** — keep the label cell, value = `—`
- **Distribution** — pre-fill as normal (`CG · PMC · MoC`)
- **doc-strip headers** — do NOT include `· Rev XX · YYYY-MM-DD` suffix; only team name · pack title · page info

The Document Controller stamps these in later. Never use placeholder text like `[TBD]` — use `—` (em dash) or leave the value tag empty. The structure/labels stay so the DOC knows where to fill.

### Mission Brief Accuracy (Most Scrutinised Field)

- **Find the team's SOW document yourself** — search the project's `02_Plans_and_Procedures/` tree for the relevant SOW (e.g. `SOW_Sustainability_Team.html`, SoW extracts under `Contractual_Requirements/`). Do NOT ask the user to point you to it.
- **Read the SOW** to extract the actual scope items, deliverables, and coordination points. Reference specific deliverables (e.g. "monthly site sustainability audits", "8-stream waste tracking", "ITCA coordination") — not generic phrases.
- Cross-reference the SOW with the person's CV to map their experience to the specific project scope
- Do NOT use generic boilerplate copied from other packs' Mission Briefs
- Each person's role, responsibilities, and reporting line must reflect their SOW/proposal
- Reference the correct SoW clause (e.g. §13.9) and compliance framework (Mostadam / SBC 1001)
- If the person is from a sub-consultant, name their company in the role title
- **⚠ NO personal names in Mission Brief body text** — use role titles only (e.g. "Reports to the Samaya Project Director" not "Reports to Eng. X"). Names in the QC sign-off block on the cover page are fine (they are formal DC fields), but anywhere in the Mission Brief paragraph or Coordination Scope bullet points, reference the role, not the person.
- **Position the person correctly within their SOW package** — read the SOW to determine if they belong to Package A (design-phase), Package B (construction-phase / advisory), or are in-house Samaya staff. State this in the Mission Brief heading (e.g. "Environmental & Sustainability Manager (Construction-Phase Compliance) — Samaya Sustainability").

### Team Name Consistency

All packs that are part of the same umbrella (e.g. Samaya Sustainability) must use the **same team name** across all packs. Do not invent different names for different sub-teams unless they are truly separate organisations. Use descriptive team names (not internal code names).

### Key Personnel Reference Data

| Item | Value |
|------|-------|
| Project | Aseer Regional Museum · Project 3092 |
| Contract | 0010003521 (MoC ↔ Samaya) |
| Submitted to | CG — Eng. Mohammed Elbaz (Acting PM) · Abdrabo Shahin (Sr Structure Engineer) |
| Issued by | Samaya Investment — via Samaya Technical Office |
| Reference | KP Reg MOC-ASEER-SIC-1K0-KP-0001 · DMP §5.1.2 · SoW §5.5 · §13.7 / §13.8 |
| QC Prepared By | Eng. Mohamed Sultan — Samaya Technical Office Manager |
| QC Reviewed By | Eng. Abd Elmohaymen Medhat — Samaya QA/QC Manager |
| QC Approved By | Eng. Muhammad Waris Sultan Khan — Samaya Project Director |
| Status Text | "Pending CG review and onward MoC approval. Once approved, KP cannot be removed without prior written MoC approval." |
| Logos path | `Key_Personnel_Register/CVs/_assets/logos/` (moc.png, pmc_ace.png, cg.png, samaya.png) |

### Template Notes Reference

`references/template-notes.md` — Detailed CSS class reference, per-page patterns, and template source location notes (absorbed from `key-personnel-cv-submittal-pack`).

---

# Reference Files

Logos at: `Key_Personnel_Register/CVs/_assets/logos/`
Sample packs at: `Key_Personnel_Register/CVs/Sustainability Team/`
Archive templates at: `Key_Personnel_Register/CVs/_archive/HTML/`
