---
name: samaya-document-generation
title: Samaya Document Generation — Draft-to-Complete Pipeline
description: Full workflow for generating Samaya-branded DOCX documents from draft sources — fill TBDs with project data before presenting, use SamayaDoc from repo, handle OneDrive sync issues.
---

## When to Use

This skill covers the complete pipeline when the user provides a draft document (markdown or text) and expects a **completed, Samaya-branded DOCX** — not just a format conversion. It applies when:

- The user sends a draft document and says "make it docx" or "save in proper subfolder"
- The draft contains TBD/TBC placeholders the user expects filled
- The document needs Samaya branding (header, footer, navy/white table styling)

## MANDATORY First Step

Before doing anything with a Samaya document draft:

```python
import sys
sys.path.insert(0, '/Volumes/MIcro/Temp/aseer-museum-pm/_Style-Guides/Doc Style Guide')
from samaya_doc_template import SamayaDoc, SamayaColors
```

The repo clone (`/Volumes/MIcro/Temp/aseer-museum-pm/`) is the **only reliable source** for SamayaDoc. OneDrive paths often return null bytes / "Resource deadlock avoided".

## Pipeline

### Step 1: Read and Understand the Draft

Extract the full text. Identify:
- Document structure (sections, tables, appendices)
- All **TBD / TBC / "To be confirmed"** placeholders
- References to other project documents, surveys, or external data sources

### Step 2: Search Project Data to Fill TBDs

Before generating the DOCX, search these sources in order:

| Source | What to look for | How to search |
|--------|-----------------|---------------|
| **Repo** (`/Volumes/MIcro/Temp/aseer-museum-pm/`) | Registers, SOWs, prequal lists, org chart, delivery plans | `search_files`, `grep` for keywords |
| **Outlook SQLite** | Email previews about relevant assessments, companies, contacts | `sqlite3` query on `~/Library/Group Containers/UBF8T346G9.Office/.../Outlook.sqlite` |
| **Prequalification Register** (`01_Registers/prequalification_register.md`) | Which company does each scope | Search for assessment/survey companies |
| **Deliverables Master List** (`01_Registers/deliverables_master_list.md`) | Contractual deliverables per phase | Search for S-P-* (site assessment) codes |
| **Project org chart** (`00_Project_Charter/org_chart.md`) | Who is who, which company is appointed | Direct read |
| **Scope of Work** (`00_Project_Charter/scope_of_work.md`) | Contractual responsibilities for surveys and assessments | Search for Part 2, Site Assessment, Surveying |

**Fill what you can find.** For values genuinely unavailable, note the source that will provide them (e.g. "To be confirmed by site survey REF-GWY-01") rather than leaving bare "TBD".

### Step 3: Generate with SamayaDoc

```python
doc = SamayaDoc()
doc.create_header(project_name="...", doc_ref="...", doc_type="...", revision="...", date="...")
doc.create_footer(doc_ref, confidential=False)

# Content
doc.add_h1("SECTION TITLE")
doc.add_h2("1.1", "Heading Text")
doc.add_h3("1.1.1", "Sub-heading")
doc.add_body("Body text here.")
doc.add_table(headers, rows, col_widths_cm=[...])

doc.save(output_path)
```

SamayaColors reference:

| Color | RGB | Usage |
|-------|-----|-------|
| NAVY | `RGBColor(0x1e, 0x29, 0x3b)` | H1/H2 headers, table header bg, footer borders |
| DARK_GRAY | `RGBColor(0x33, 0x41, 0x55)` | H3 headings, secondary footer text |
| MEDIUM_GRAY | `RGBColor(0x64, 0x74, 0x8b)` | Doc refs, revision labels |
| LIGHT_GRAY | `RGBColor(0xf1, 0xf5, 0xf9)` | Alternating table row shading |
| ACCENT_RED | `RGBColor(0xb0, 0x1e, 0x2f)` | Critical callouts (reserved) |

### Step 4: Place in Correct Project Subfolder

| Document Type | Subfolder |
|---------------|-----------|
| Mobilization supplement / logistics plan | `MOBILIZATION/` |
| Authority submissions / permits | `Docs/06_Authority_Submissions/` |
| CG correspondence | `Docs/11_Correspondence/` |
| Plans and procedures | `Docs/02_Plans_and_Procedures/` |
| Contracts / SOW | `Contracts/` or `Docs/02_Plans_and_Procedures/` |

## Pitfalls

- **Never use pandoc for Samaya documents.** The user will reject non-branded output. Use SamayaDoc from the repo.
- **Never hand-code python-docx styling.** The user's first response will be "Why not follow samaya doc style."
- **Always fill TBDs before presenting.** The user will say "all TBD you have to fill according to project status." Search project data first (registers, prequal list, Outlook emails, repo scope docs).
- **OneDrive = unreliable.** The template file and many project files are OneDrive placeholders that return EDEADLK. Use the repo clone (`/Volumes/MIcro/Temp/aseer-museum-pm/`) instead.
- **SamayaColors.NAVY is NOT #003366.** The actual value is `RGBColor(0x1e, 0x29, 0x3b)`. Guessing wrong navy color = style rejection.
- **Who does what: check the prequalification register first.** When the user asks who does a specific scope, search `01_Registers/prequalification_register.md` for the discipline code before guessing. The PQ register has the definitive assignment.
- **Assessment report approval status: check Adel snapshots.** The file `99_Archive/adel_snapshots/file_list.txt` reveals CG response PDFs in `Approval/` subfolders even when no CG email was sent. An `Approval/` folder with a CG reply PDF means CG responded.
- **Extract NRS comments from Outlook .olk15MsgAttachment files:** These are MIME containers with base64-encoded PDFs. Join `Mail_OwnedBlocks` on `Blocks` to get the `PathToDataFile`, then decode the base64 portion after the `base64` header to recover the original PDF. Use `pdftotext` for text extraction.
- **Verify table rendering.** After generating, check that tables have proper widths (sum to ~16.5cm for A4 portrait) and alternating row shading.
- **Sections with many tables need page breaks.** Insert `doc.doc.add_page_break()` between major sections for readability.
- **Do NOT send interim drafts.** Generate the full completed document in one pass.
- **Git push may fail with divergent branches.** Use `git pull origin main --no-rebase` to merge remote changes before pushing.

## Reference files

- `references/assessment-report-tracking.md` — How to find who does assessment work and track their report status across Outlook SQLite, Adel snapshots, and repo registers.
- `references/nrs-comments-investigation.md` — How to find NRS (Nissen Richards Studio) review comments: search Outlook SQLite `Message_Preview` for email body text, check cached PDF attachments in `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Files/S0/*/Attachments/`, and fall back to OneDrive document control folders when image-based redlines can't be OCR'd.
