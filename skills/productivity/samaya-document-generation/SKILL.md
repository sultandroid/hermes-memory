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
sys.path.insert(0, '/Users/mohamedessa/aseer-museum-pm/_Style-Guides/Doc Style Guide')
from samaya_doc_template import SamayaDoc, SamayaColors
```

The repo clone at `~/aseer-museum-pm/` is the reliable source for SamayaDoc. OneDrive paths often return EDEADLK.

## Multi-Turn Task Protocol

When the user says "read all msg", "read the conversation", or similar, consolidate the full thread before acting. Do not jump to a conclusion from the last message alone. Re-read the conversation, identify the current state and pending deliverable, then confirm before producing output.

## Pipeline

### Step 1: Read and Understand the Draft

Extract the full text. Identify:
- Document structure (sections, tables, appendices)
- All TBD / TBC / "To be confirmed" placeholders
- References to other project documents, surveys, or external data sources

### Step 2: Search Project Data to Fill TBDs

Before generating the DOCX, search these sources in order:

| Source | What to look for | How to search |
|--------|-----------------|---------------|
| Repo (`~/aseer-museum-pm/`) | Registers, SOWs, prequal lists, org chart, delivery plans | `search_files`, `grep` for keywords |
| Outlook SQLite | Email previews about relevant assessments, companies, contacts | `sqlite3` query on `~/Library/Group Containers/UBF8T346G9.Office/.../Outlook.sqlite` |
| Prequalification Register | Which company does each scope | Search for assessment/survey companies |
| Project org chart | Who is who, which company is appointed | Direct read |
| Scope of Work | Contractual responsibilities for surveys and assessments | Search for Part 2, Site Assessment, Surveying |

**Fill what you can find.** For values genuinely unavailable, note the source that will provide them rather than leaving bare "TBD".

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
| CG correspondence / RFI / TQ | `05_Comms/drafts/` |
| Plans and procedures | `Docs/02_Plans_and_Procedures/` |
| Contracts / SOW | `Contracts/` or `Docs/02_Plans_and_Procedures/` |

## Style Rules (MANDATORY — user will reject violations)

These rules apply to ALL Samaya DOCX documents. They are non-negotiable.

### No special characters or AI symbols
- Never use: `§`, `→`, `◆`, `📌`, `✅`, `❌`, `⚠️`, `🟢`, `🔴`, `🟡`, `—` (em dash), `•` (bullet), `&mdash;`, `&rarr;`, or any Unicode symbol in body text.
- Use plain text alternatives: "Section 8.2" not "§8.2", "to" not "→", "Approved" not "✅".
- This applies to ALL formal documents — SOWs, reports, registers, letters, transmittals.

### No AI fingerprint
- No AI clichés: seamlessly, cutting-edge, robust, innovative, bespoke, leveraging, delve, navigate, holistic, dynamic, streamline, game-changer, state-of-the-art, world-class.
- No AI phrasing: "It is worth noting that", "It is important to mention", "Please be advised", "In the realm of", "When it comes to".
- No AI symbols: no `§`, `→`, `◆`, emoji status indicators.

### Write like a human engineer
- Short sentences. Active voice. Plain words.
- If a 14-year-old can't understand it, rewrite it.
- British English spelling: colour, programme, centre, metre, organise, licence (noun) / license (verb).
- Do not talk too much. One paragraph per idea. No padding.

### Reference
The full Samaya Style Guide is in `AGENTS.md` under "Samaya Style Guide — Mandatory Reference" and `_Style-Guides/`. Load it before generating any client-facing document.

## Document Numbering — Verify Serial from Aconex

Before assigning any document reference number (TQ, RFI, ZD, PL, etc.), check the last used serial from Aconex via Outlook SQLite:

```sql
SELECT DISTINCT substr(m.Message_NormalizedSubject, 
  instr(m.Message_NormalizedSubject, 'TQ-'), 8) as tq_ref
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%TQ-%'
ORDER BY tq_ref DESC;
```

Extract the highest number from the subject lines. The next document is that number + 1. Do NOT guess or start from 001 — the user will catch it.

The numbering is project-wide (not per-discipline). A single serial sequence covers all TQs regardless of zone code (1E0, 1A0, 1K0, etc.).

### Signature Block

Every formal document (TQ, RFI, letter, transmittal) MUST end with a signature block table:

```python
doc.add_h2("8", "SIGNATURE BLOCK")
sig_headers = ["Role", "Name", "Signature", "Date"]
sig_rows = [
    ["Prepared by", "Eng. Mohamed Sultan Abbas", "", ""],
    ["Reviewed by", "", "", ""],  # Add when a specialist subcontractor reviews technical content
    ["Checked by", "", "", ""],
    ["Approved by", "", "", ""],
]
doc.add_table(sig_headers, sig_rows, col_widths_cm=[4, 5, 4, 4])
```

Four rows: Prepared by, Reviewed by (add when a specialist subcontractor reviews technical content), Checked by, Approved by. Leave blank rows for reviewers to fill. Do NOT use a single-row "Prepared by" table — the user expects the full review chain.

When the document concerns a specialist scope (AV, lighting, MEP, showcases), add a "Reviewed by" row for that specialist between Prepared by and Checked by.

### RFI Audience — Know Who the Recipient Is

When drafting an RFI or Technical Query about AV/media content:

- The **recipient is MoC (via CG)**, not the subcontractor.
- The AV/IT and interactive specialist (Rawasin) is **already appointed** — do not imply gaps in their appointment or scope.
- Do not include obligations on Samaya's side in the RFI. The RFI asks MoC what they will provide, when, and in what format.
- Reference SOW Section 2.2 (AV software/media excluded from Contractor scope, supplied by others) and SOW p.17 (MoC-supplied items: images/film list, commissioned art pieces) as the contractual basis for the RFI.
- Reference the DMP (PL-0029) design stage gates to explain why the information is needed now (before 90% gate / IFC).

### RFI Refocusing — Coordination-and-Schedule Only (user steer, 2026-08)

When the user asks to refocus a content/AV RFI, they want the scope argument stripped out entirely and the emphasis moved to **coordination with the production specialist + delivery dates**. Observed steering:

- **Drop the "who supplies content" dispute.** Do NOT argue scope or ask MoC to confirm supply responsibility. State it plainly in the purpose and move on.
- **Confirm the designated production COORDINATOR** (contact + role) and request a coordination meeting to fix the interface this stage — not "confirm the specialist exists."
- **Anchor delivery dates to actual content types** already defined (e.g. film production lead times, tactile fabrication) mapped against the design gates (50%/90%/100% or IFC), not just generic gate numbers.
- **Attach the worked content brief as an appendix.** If a gallery's visitor-experience content is already defined (e.g. the G12 Archaeology brief: 1 scene-setting film + 2 interactives — tactile replication + rubbing station), include it as Appendix A so the content specialist sees exactly what coordination is needed. The content brief IS the coordination anchor.
- Keep the RFI addressed to MoC (via CG) as coordinator. Ask who to coordinate with and when content arrives.

## Multi-Turn Task Protocol

When the user says "read all msg", "read the conversation", or similar, consolidate the full thread before acting. Do not jump to a conclusion from the last message alone. Re-read the conversation, identify the current state and pending deliverable, then confirm before producing output.

## Pitfalls

- **NEVER use emojis or AI symbols (checkmark, cross, warning, circle symbols) in formal Samaya DOCX documents.** Use text alternatives: Signed, Draft, Not Available, Executed, Pending, Approved, Rejected. The user will reject documents with emoji status indicators. This applies to ALL formal documents — SOWs, reports, registers, letters, transmittals.
- **Never use pandoc for Samaya documents.** The user will reject non-branded output. Use SamayaDoc from the repo.
- **Never hand-code python-docx styling.** The user's first response will be "Why not follow samaya doc style."
- **Always fill TBDs before presenting.** The user will say "all TBD you have to fill according to project status." Search project data first (registers, prequal list, Outlook emails, repo scope docs).
- **OneDrive = unreliable.** The template file and many project files are OneDrive placeholders that return EDEADLK. Use the repo clone instead.
- **SamayaColors.NAVY is NOT #003366.** The actual value is `RGBColor(0x1e, 0x29, 0x3b)`. Guessing wrong navy color = style rejection.
- **Who does what: check the prequalification register first.** When the user asks who does a specific scope, search `01_Registers/prequalification_register.md` for the discipline code before guessing. The PQ register has the definitive assignment.
- **Assessment report approval status: check Adel snapshots.** The file `99_Archive/adel_snapshots/file_list.txt` reveals CG response PDFs in `Approval/` subfolders even when no CG email was sent. An `Approval/` folder with a CG reply PDF means CG responded.
- **Extract NRS comments from Outlook .olk15MsgAttachment files:** These are MIME containers with base64-encoded PDFs. Join `Mail_OwnedBlocks` on `Blocks` to get the `PathToDataFile`, then decode the base64 portion after the `base64` header to recover the original PDF. Use `pdftotext` for text extraction.
- **Verify table rendering.** After generating, check that tables have proper widths (sum to ~16.5cm for A4 portrait) and alternating row shading.
- **Sections with many tables need page breaks.** Use `doc.doc.add_page_break()` — the SamayaDoc class has NO `add_page_break()` method, so call the underlying python-docx `Document` (`self.doc`) directly. Same pattern for any python-docx API the template doesn't wrap (e.g. `doc.doc.sections[0]`). The template exposes `self.doc` as the python-docx `Document` object.
- **Do NOT send interim drafts.** Generate the full completed document in one pass.
- **Git push may fail with divergent branches.** Use `git pull origin main --no-rebase` to merge remote changes before pushing.

## Reference files

- `references/subcontractor-sow-raci-docx.md` — Full 9-section subcontractor SOW + filled RACI matrix DOCX generation pattern.
- `references/assessment-report-tracking.md` — How to find who does assessment work and track their report status across Outlook SQLite, Adel snapshots, and repo registers.
- `references/nrs-comments-investigation.md` — How to find NRS (Nissen Richards Studio) review comments.
- `references/approved-plan-ingestion.md` — Pipeline for converting approved Code B plan PDFs/markdown to formal read-only docs.
- `references/multi-sheet-excel-to-markdown-register.md` — Pattern for extracting data from multi-sheet Excel files (object schedules, BOQs) and producing structured markdown registers.
