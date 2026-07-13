---
name: samaya-docx-template
title: SamayaDoc Template — DOCX Generation
description: Use Samaya branded DOCX template for all formal documents. Import SamayaDoc class from the style guide.
---

## MANDATORY — load this skill first

**This skill MUST be loaded (`skill_view(name='samaya-docx-template')`) BEFORE writing any DOCX generation script.** The SamayaDoc class name, import path, style rules, table-width workaround, and OneDrive copy workflow are defined here. Generating without this skill loaded means you will fall back to hand-coded styles, which the user will reject. This is the #1 avoidable error.

## When to use

Any time you generate a `.docx` file **for Samaya** — SOW, report, letter, transmittal, register, meeting minutes.

**Style reference:** The canonical Samaya Stakeholder Management Plan HTML style is deployed at `https://samaya-factory.com/build/technical-office/stakeholder-management-plan.html`. When asked about document style or format, use this as the reference implementation for Samaya project plans.

**DO NOT use SamayaDoc when generating documents FOR a subcontractor to submit TO Samaya.** Those are the subcontractor's own documents and must use their branding, not Samaya's. Use standalone python-docx with the subcontractor's logo and color scheme instead. The cover should say "Submitted to: Samaya Investment" and "Prepared by: [Subcontractor Name]".

This includes **prequalification packages** (letter + RACI + risk register) prepared on behalf of a subcontractor who lacks museum experience — see `references/subcontractor-prequalification-package.md`.

Also use when:
- **Reformatting an external document** (consultant/contractor deliverable) to Samaya branding — extract content from the original, apply SamayaDoc styles, and file in the project folder
- **Checking document compliance** against project standards (BEP, ISO 19650, naming conventions) before or after reformatting — the review workflow is documented below

## Template location

```python
# Standard path (TCC-blocked for terminal reads):
# ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide/samaya_doc_template.py

# Fallback path (Group Containers, often readable when CloudStorage is blocked):
# ~/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide/samaya_doc_template.py
```

## File placement conventions

| File type | Location | Notes |
|-----------|----------|-------|
| `SCOPE_REQUEST.md` | `_MANAGER_DASHBOARD/` | Source markdown — management/editing copy |
| `SCOPE_REQUEST.docx` | Sub root (parallel to `_MANAGER_DASHBOARD/`) | Formal deliverable for issue to bidders |
| `SITUATION_REPORT.md` | `_MANAGER_DASHBOARD/` | Status tracking |
| All other `.md` files | `_MANAGER_DASHBOARD/` | Research notes, email drafts, contract status |
| Technical files (PDFs, xlsx, dwg) | `01_*` through `07_*` subdirs | Per discipline folder |

## Python usage

```python
# Try CloudStorage path first; fall back to Group Containers if TCC-blocked
import os, sys
_template_dir = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
if not os.path.exists(_template_dir):
    _template_dir = "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
sys.path.insert(0, _template_dir)
from samaya_doc_template import SamayaDoc, SamayaColors

doc = SamayaDoc()
doc.create_header(project_name="Aseer Regional Museum", doc_ref="MOC-ASEER-SIC-1K0-XXX-001", doc_type="RPT", revision="A", date="Jun 2026")
doc.create_footer("MOC-ASEER-SIC-1K0-XXX-001")
doc.add_h1("DOCUMENT TITLE")
doc.add_h2("1.0", "SECTION HEADING")
doc.add_body("Standard body text.")
doc.add_table(["#", "Description"], [["1", "Item"]])
doc.save("/path/to/output.docx")
```

### Available methods (SamayaDoc API)

| Method | Signature | Notes |
|--------|-----------|-------|
| `add_h1` | `(text)` | 18pt Bold Navy, uppercase, bottom border |
| `add_h2` | `(number, text)` | Two positional args: number prefix then heading text |
| `add_h2_u` | `(text)` | Unnumbered h2 |
| `add_h3` | `(number, text)` | 12pt Bold Dark Gray |
| `add_body` | `(text)` | 11pt Calibri justified. **No `add_bullet()` exists** — use `add_body("- item text")` for bullet lists |
| `add_rich_body` | `(segments)` | For mixed bold/normal segments |
| `add_remark` | `(text, size=9)` | Halftone gray #64748B, 9pt, compact spacing. Use for descriptive sentences between headings/tables, timestamps, legend definitions |
| `add_table` | `(headers, rows, col_widths_cm=None)` | `col_widths_cm` works correctly (sum to ~16.5cm for A4) |
| `create_header` | `(project_name, doc_ref, doc_type, revision, date)` | Call before `create_footer()` |
| `create_footer` | `(doc_ref)` | Call after `create_header()` |
| `save` | `(path)` | Save to final location |
| `save_temp` | `()` | Save to temp file |

## HTML-to-content extraction for DOCX generation

When the source content is a large HTML file on a private network path (OneDrive, local filesystem) that `web_extract` cannot read (returns "Blocked: URL targets a private or internal network address"), use `html2text` via terminal to extract the text, then read in chunks via `read_file` with offset/limit.

See `references/html-to-content-extraction.md` for the full workflow including:
- RevC05→SMP→DOCX merge pattern (7-step pipeline)
- Contradiction-fixing rules: contract (ER/SoW) always wins over consultant strategy documents
- Common RevC05 errors: waste diversion (75%→60%), Oddy aging (49-day→14-day)
- DOCX generation script patterns for large multi-section documents

## External Document Intake & Reformatting Workflow

When receiving an external document (consultant deliverable, reference standard, vendor document) that needs Samaya-branded reformatting, follow this sequence:

### Workflow

1. **Extract content** from the original DOCX via `python-docx` — read paragraphs and tables, preserve structure
2. **Check compliance against project standards** before reformatting:
   - Open the project BEP (`Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/`) and extract discipline codes, naming conventions, format requirements (Table 24, 30, 31)
   - Compare discipline codes, numbering format, sequential digit length, type/category system
   - Identify gaps (missing disciplines, mismatched codes, format differences)
   - Produce a structured compliance finding with severity ratings (Critical / Moderate / Low)
3. **Reformat using SamayaDoc** with the extracted content, mapped to correct section structure
4. **Assign a document reference** matching the project's ISO 19650 container code pattern (`223032-SAM-XX-XX-{TYPE}-{DISC}-###`)
5. **Save directly to the project folder** — never to Desktop as a staging area

### SOW contract-accuracy verification (mandatory for scope documents)

When writing a Scope of Services (SOW) for a contractor, consultant, or in-house role, every scope statement must be grounded in the actual contract. **The SoW and ER are the authority, not assumptions.**

**Verification sequence:**
1. Locate the relevant contract sections — SoW (often §13.x) and ER (often §2.x, §3.x)
2. Extract verbatim text from the contract PDFs using PyMuPDF (`fitz`)
3. Map each intended scope bullet to a specific SoW/ER clause — if no clause supports it, it does not belong in the SOW
4. After drafting, **dispatch labors (Kimi, Codex, Claude) for second-opinion cross-verification** — give them the source PDFs and ask: "does the contract require X?" They will read the documents independently and flag any invented obligations
5. Only after both self-verification + labor cross-check, finalize and save

**Common traps that trigger user correction:**
- Adding certification targets (Silver/Gold/Bronze rating, points thresholds) that the contract does not mandate — the ER may list "Mostadam Manual" as a reference code but never require achieving a specific level
- Expanding scope with tasks the designer/subcontractor handles (energy modelling, daylight simulation) — the contractor's Sustainability Manager reviews for compliance, not produces
- Including Commissioning Authority (ITCA) responsibilities that belong to the MEP contractor
- Referencing documents or codes not cited in the SoW/ER (e.g., LEED on a Mostadam project)

**Mandatory cross-reference table for sustainability SOWs:**

| Task statement | Check against | If not in contract |
|---|---|---|
| "Achieve X rating / Y points" | SoW §13.9 + ER sections listing targets | ❌ Remove — state "support per project requirements" |
| "Manage Mostadam credits" | ER §3.7.XIII (or applicable codes section) | If code is listed as reference only, rephrase to "review codes for compliance" |
| "Submit to portal / assessor" | SoW deliverable schedule + ER submittal requirements | ❌ Remove unless explicitly required |
| "Lead certification" | SoW obligations clause | Rephrase to "support certification as required" |

### Output location rules

| Document type | Target folder |
|--------------|---------------|
| BEP companion / naming standard reference | `Bim Unit/Aseer-Museum/Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/` |
| Subcontractor SOW | Subcontractor's `_MANAGER_DASHBOARD/` (source .md) + sub root (.docx) |
| Submittal-related | Project's `04_Submittals/` or submittal section |
| Technical reference / standards | Project's `Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/` or `_Style-Guides/` |
| General technical note | `Bim Unit/Aseer-Museum/10_Plans/` or `Docs/02_Plans_and_Procedures/reference/` |

### BEP compliance checklist (for Aseer Museum)

When reviewing a document against the project BEP (Rev R02, Table 24/30/31):

| Check | What to verify |
|-------|---------------|
| Discipline codes | Must match BEP Table 30 (AR, ST, ID, HV, EL, PL, FF, IT...), not single-letter US codes (A, S, M, E, F, T) |
| Container code format | CDE-level: `223032-SAM-XX-XX-{Type}-{Disc}-{###}` per BEP Table 24 |
| Sequential numbering | 3 digits (001) at CDE level; 2-3 digits at title-block level — check which level the doc addresses |
| Missing disciplines | ID (Interior Design) is critical for museum fit-out — ensure it's covered |
| ISO 19650 distinction | The doc must acknowledge the difference between title-block code and full CDE container code |

See `references/document-compliance-review.md` for the detailed compliance analysis methodology with worked example.

### Retrofitting Samaya branding onto existing DOCX

When you have an existing `.docx` that was NOT created with `SamayaDoc` and needs Samaya-branded formatting (header, footer, margins, heading styles, table styles, symbol cleanup), see `references/retrofit-samaya-branding.md`. This covers the full workflow: close Word, set margins, create header/footer, classify paragraphs by heading level, format all tables, clean symbols, save, reopen.

## Table column widths

`SamayaDoc.add_table()` accepts `col_widths_cm` and applies `Cm(w)` to each cell — this works correctly with the current template. A4 text area = 16.5cm total (21cm page - 2.5cm left - 2.0cm right).

When using `col_widths_cm`, ensure the sum of widths equals ~16.5cm for A4 portrait. Example:
```python
doc.add_table(
    ['#', 'Description', 'Value'],
    [['1', 'Item', 'SAR 100']],
    col_widths_cm=[1.0, 10.0, 5.5]  # sum = 16.5
)
```

If you are NOT using `SamayaDoc` and are hand-coding with raw `python-docx`, use `set_table_widths()` after creation (see `references/docx-generation-example.md`).

### Writing & Language Rules (mandatory — from Samaya style guide Section 11)

Apply these to ALL Samaya documents, whether DOCX, HTML, or markdown:

### Language level
- **Level 6 English (CEFR B2–C1)** — short sentences (15–22 words), active voice, everyday vocabulary.
- No AI-generated clichés: avoid "seamlessly", "synergistic", "cutting-edge", "state-of-the-art", "holistic", "leverage", "robust", "innovative", "bespoke", "delighted to", "committed to excellence", or padded introductions.
- Get to the point. Every sentence carries information weight. Delete filler.

### Stakeholder names — use proper names, not generic roles
- Use **Samaya Investment** (not "the Contractor" or "the Company")
- Use **Ministry of Culture (MoC)** (not "the Client")
- Use **Consultancy Group (CG)** (not "the Consultant")
- Use **ACE Moharram-Bakhoum (PMC)** (not "the Project Manager")
- Use **Nissen Richards Studio (NRS)** (not "the Designer" or "the Lead Designer")
- This applies to ALL documents — plans, SOWs, emails, reports, review comments
- **User correction signal:** If the user says "dont say Contractors you have to mention all the stakeholders with their names like Samaya Inv", you used generic terms. Fix immediately.

### Symbols and characters
- **Never use the section symbol** - write "Section 2.1" or "2.1" instead.
- **Never use decorative dashes** - use plain hyphen not em-dash or en-dash.
- **Never use bullet symbols** - use plain hyphen not bullet characters.
- **No accented characters** - write "cafe" not "cafe with accent", "facade" not "facade with cedilla".
- No ornamental dingbats, checkmarks, stars, arrows, or progress dots - use plain text or standard bullet marks.

### Icons
- No icons anywhere in the document body. Icons are decorative and add no verifiable information.
- The only permitted non-text visual elements: tables, spec-strips, badge pills (mono text, 2px radius), SVG line charts (Feather/Lucide style, for org charts/process flows only).
- Header logos (Samaya/Client) are the only images allowed outside the cover page.

### No AI fingerprint
Documents must not betray AI generation:
- No self-referential language ("I have", "we have prepared", "this document was created by…").
- No meta-commentary about the document ("the following sections will cover…", "as shown above").
- No hedging qualifiers ("arguably", "it could be said", "one might consider").
- State facts directly. If uncertain, flag as "TBC" or "subject to confirmation".
- Dates, names, references, and numbers must be traceable to a source document. Mark estimates as [TBC].

### Human voice
- Write as a senior engineer dictating: contractions allowed in cover letters ("We'll", "It's").
- Use "Samaya" (not "the Contractor" or "the Company").
- Prefer concrete numbers over ranges ("6 production lines" not "several lines").
- Address the reader as "the Client" or "RCRC" — never "you".
- Write for a Saudi government evaluator who reads 30 proposals — make yours the one they understand on first scan.

## Style rules

- **H1:** 18pt Bold Navy `#1E293B`, uppercase, bottom border
- **H2:** 14pt Bold Navy, numbered, uppercase, bottom border
- **H3:** 12pt Bold Dark Gray `#334155`, uppercase, bottom border
- **Body:** 11pt Calibri justified, 6pt space after
- **Tables:** Navy header (9.5pt white bold), alternating rows `#F1F5F9`/white
  - All table cells: left-aligned. Header row stays bold on navy background. Body cells: plain black text (no bold), no emoji icons.
  - Column widths set via `set_table_widths()` after creation — NEVER via `col_widths_cm` parameter
- **Margins:** A4 portrait, 2.5cm top/left, 2.0cm bottom/right
- **Colors:** Navy `#1E293B`, Red `#B01E2F`, Dark Gray `#334155`, Medium Gray `#64748B`

## Arabic DOCX generation workflow (MANDATORY)

When generating a DOCX with Arabic content, follow this exact sequence to avoid the two most common user corrections.

### Step 1: Word choice audit
Before writing any Arabic text, scan your vocabulary against the substitution table below. The user will reject formal/administrative Arabic. Write as a site engineer would speak — short sentences (10-15 words), common everyday vocabulary, avoid compound nouns and formal administrative language.

| Don't use (formal) | Use instead (simple) |
|---|---|
| مقرر نقاش | مذكرة نقاش |
| جدولة عرضية | جدول عرض |
| الأغراض | القطع |
| المعرضات | الواجهات |
| فريق التصميم | الاستشاري |
| مخطط المخاطر | المخاطر |
| الملاحظات النهائية | ملاحظات ختامية |
| الإجراءات التخفيفية | الحل |
| نطاق النقاش | نطاق النقاش (keep) |
| الجهة المسؤولة | المسؤول |
| الموعد النهائي | آخر موعد |
| الأولوية | أولوية |
| الاحتمالية | الاحتمال |
| التأثير | التأثير (keep) |
| الإجراءات التخفيفية | الحل |
| الوثائق المرفقة | المستندات المرفقة |
| الملاحظات | ملاحظات |
| التوقيعات | التوقيعات (keep) |

### Step 2: RTL direction on every Arabic paragraph
Every paragraph containing Arabic text MUST have RTL direction set. The `SamayaDoc` class does NOT do this automatically — you must call `set_rtl()` on each Arabic paragraph:

```python
def set_rtl(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    pPr.append(bidi)
```

Also set `p.alignment = WD_ALIGN_PARAGRAPH.RIGHT` for Arabic paragraphs. For bilingual documents, English paragraphs stay left-aligned, Arabic paragraphs right-aligned with RTL.

### Step 3: Verify before presenting
Before showing the document to the user, do a quick self-audit:
1. Scan all Arabic text for formal/compound words — replace with simple alternatives
2. Check every paragraph has RTL direction (not just alignment)
3. Verify tables render correctly (Arabic text in right-aligned cells)

**Pitfall:** If you skip this audit, the user will correct you with "arabic words not fammlier you use deffecults words , also the direction" — this is a known correction pattern. A single comprehensive pass is faster than 2 fix rounds.

---

## Pitfalls

- **Revision history: only show actual CG submissions, not internal drafts.** The revision history table should reflect what was actually submitted to CG, not every internal draft iteration. If Rev 00 (Code C) and Rev 01 (Code C) were the only submissions before approval, the table should show Rev 00, Rev 01, Rev 02 (Approved), and the current Rev — not Rev 00, 01, 02, 03, 04 where 02 and 03 were internal drafts never submitted. User correction signal: "i think this Rev02 we submit 2 times only before." Verify against CG_STATUS.md and PROJECT_MEMORY.md before writing the revision table.

- **Cover page: keep it brief for CG submittals.** CG reviewers do not need a verbose change log on the cover. The cover should show: document title, revision, date, superseded revs, and reference documents only. Do NOT list every stakeholder change, KPI count, or internal audit note on the cover. That information belongs in the revision history table inside the document. User correction signal: 'dont talk too much the cover page, dont tell information in general are dosnot important to cg to tell.'

- **CG Comment Disposition: reference the CR sheet, do NOT repeat comments in the document body.** The full CG comment-by-comment disposition matrix (2+ pages of tables) does not belong in the plan body. Replace with a one-line summary: 'All 25 CG comments (R1+R2) closed in Rev 02. Full disposition per attached CR sheet.' The user explicitly said: 'we can refere to the attached CR sheet only no need to repeate here.' This saves 2 pages and avoids CG reviewers seeing their own comments re-listed.

- **ALWAYS load this skill (`skill_view(name='samaya-docx-template')`) before generating any DOCX** — the SamayaDoc class name, style rules, import path, and table-width workaround are all here. Generating without this skill loaded risks missing the template entirely and falling back to hand-coded styles, which the user will reject. See the MANDATORY notice at the top of this skill.

- **RUN symbol & AI-fingerprint cleanup AFTER EVERY DOCX edit — this is the #1 user correction signal.** The user will say "you forget dont use section symbol or any AI symbols or finger prints ... write like humman" if you skip it. The cleanup procedure is documented in the "Mandatory symbol & AI-fingerprint cleanup after EVERY DOCX edit" section above. Do not assume the previous edit pass already cleaned it — run the scan again. The user expects you to catch this yourself without being reminded.

- **After bulk formatting edits (page breaks, cantSplit, column widths), run the image rendering fix.** python-docx edits that trigger Word re-layout can cause embedded PNGs to disappear. The fix is documented in `references/docx-image-rendering-fix.md`. Always check the zip contents before reporting images as "gone" — they are structurally intact, just missing rendering hints.

- **SOW generation: use SamayaDoc, not raw python-docx.** Hand-coding styles with raw `python-docx` (setting fonts, fills, borders manually) produces a document that looks correct but misses the Samaya template's header/footer, color scheme, and document control block conventions. Always import `SamayaDoc` from the style guide. If the template path is blocked, use the Group Containers fallback path documented above. If both are blocked, generate the DOCX via the standalone SOW pattern in `references/standalone-sow-docx-pattern.md` (CV-pack color scheme) rather than raw hand-coded styles.

- **SOW/ER PDFs not found: use existing project documents as fallback.** When the SOW and ER PDFs are not in the project directory (common when they are stored on Aconex CDE or in email attachments), use these existing project documents as authoritative sources:
  1. `SCOPE_REQUEST.md` in the subcontractor's `_MANAGER_DASHBOARD/` — contains scope, authority basis (ER section references), programme, and interfaces
  2. `NRS_Acoustic_Materials_Spec.md` in `03_Specifications_and_Standards/` — contains material performance criteria, certification requirements, and preferred manufacturers
  3. `SPEC.md` in `_MANAGER_DASHBOARD/` — contains deliverables by stage, exclusions, and coordination interfaces
  4. TOS technical proposals received from bidders — contain product-specific performance data
  Cross-reference all sources and note any gaps. Flag in the document that SOW/ER PDFs were not available for direct verification and scope was compiled from project documents.

- **Commercial readiness before acceptance:** Do NOT include an execution-ready acceptance/signature block in a SOW or R&R if the commercial arrangement (subcontract, PO, service agreement, payment terms) is not yet finalized. The user will say "we have to deal with them commercially also we didnt done yet." Draft the technical scope for review, but mark acceptance as draft/pending until commercial terms are confirmed. If sending to PD for review, note in the email that signing awaits commercial finalization.

- **SOW content: never exceed contract scope.** When writing a Scope of Services for a contractor or in-house role, the responsibilities must strictly match what the SoW and ER contractually require. Do NOT add certification targets (e.g. Silver rating or points thresholds) unless the contract explicitly mandates them. Adding unrequested targets creates contractual liability the contractor did not price for. When in doubt, state 'support the certification process per project requirements' rather than committing to a specific rating or points target. **Always dispatch labors (Kimi, Codex, Claude) to cross-verify SOW claims against the source contract PDFs** — give them the PDFs and ask for a second opinion on each scope statement.

- **Output location: save directly to project folder, never Desktop.** When reformatting an existing document, determine the correct project folder first (see Output location rules table). Saving to Desktop as a staging area adds a manual copy step the user shouldn't need to do. The output goes straight into the project's `Docs/` or `Bim Unit/` tree.

- **Template import via Group Containers path:** When the standard CloudStorage path is TCC-blocked for `sys.path.insert()`, use the Group Containers path instead: `/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide`. Do NOT write directly to the Group Containers path for final output — it produces zero-byte placeholders. Always stage to /tmp and AppleScript `duplicate` to OneDrive.

- **AppleScript OneDrive operations (preferred patterns):**
  - COPY file to OneDrive: `tell app "Finder" to set src to POSIX file "/tmp/file.docx" as alias; set dest to POSIX file "/path/to/dest/" as alias; duplicate src to dest with replacing`
  - DELETE file: `tell app "Finder" to set f to POSIX file "/path/file.docx" as alias; delete f`
  - RENAME file: `tell app "Finder" to set name of f to "NewName.docx"` (after getting reference via `every file of folderRef`)
  - DELETE folder: `do shell script "rm -rf " & quoted form of "/path/to/folder"` via osascript (works where Finder delete may hang)
  - LIST files in folder: `set fileList to every file of fRef` then iterate
  - VERIFY disk writes: `cp` and `write_file` to Group Containers path produce zero-byte OneDrive placeholders, not real files. Always use AppleScript `duplicate` (see above) for OneDrive writes. After copy, verify via `xxd -l 8` on the Group Containers path — first 2 bytes must be `PK` (for DOCX) or `%PDF` (for PDF). All-zeros means placeholder not written; redo via AppleScript.
- **Contract verification: user expects labors for cross-check.** When writing SOW content with contractual scope claims, dispatch Kimi/Codex/Claude in parallel to read the source SoW/ER PDFs and confirm accuracy before you finalize. The user will correct you if you invent obligations. See the "SOW contract-accuracy verification" section above.
- Header logo path is hardcoded to OneDrive (`LOGO_PATH` = CloudStorage path); falls back to `[SAMAYA]` text if offline. The fallback is expected when running via terminal (TCC sandbox blocks logo access) — the DOCX produces correct content without the logo. If a logo is critical, run the gen script with DYLD_FALLBACK_LIBRARY_PATH set and the logo path accessible.
- Always call `create_footer()` after `create_header()` for proper section linkage
- Use `add_rich_body()` for mixed bold/normal segments instead of markdown
- **Table column widths: `col_widths_cm` works correctly with SamayaDoc.** The `add_table()` method applies `Cm(w)` to each cell. A4 text area = 16.5cm total. The old workaround (`set_table_widths()` via XML) is only needed when hand-coding with raw python-docx, not when using SamayaDoc. See the "Table column widths" section above.
- DOCX saves at sub root; source .md in _MANAGER_DASHBOARD/ — never reverse this
- **NEVER modify the template file** (`samaya_doc_template.py` in `_Style-Guides/`) — all fixes go in the gen script. Template is shared code; patching it breaks every doc generated afterward.
- **Entity decoder re-introduces symbols:** The `cell_to_text()` and `html_to_segments()` helpers decode HTML entities (`&sect;` → `§`, `&mdash;` → `—`, `&middot;` → `·`). If the user wants no symbols in the output, these must map to plain text (`&sect;` → `Sec `, `&mdash;` → space, `&middot;` → space). The `--clean` flag on the converter script handles this automatically. If you're writing a one-off gen script, use the same entity mapping as the converter's `clean_ai_fingerprints_and_symbols()` function.
- **Close/reopen protocol (mandatory before any DOCX edit).** Before editing an existing DOCX via python-docx: (1) close Word first via osascript (tell Microsoft Word to close every document saving yes), (2) make edits, (3) save, (4) reopen via open command. Without step 1, Word holds a lock and python-docx can corrupt the file or produce a stale version. Without step 4, the user has to manually find and reopen. The user will call you out if you skip this.

- **Iterative document updates: patch existing file only, never regenerate.** When the user asks to update an existing DOCX, do NOT regenerate the entire file from scratch -- that overwrites any manual edits they made in Word. Instead, edit the existing DOCX directly via python-docx (read, modify, save with same path). For inserting new paragraphs/tables between existing ones, use lxml XML tree manipulation: `body.insert(list(body).index(ref) + 1, element)` where `body = doc.element.body`. Build new elements as `OxmlElement('w:p')` with manual run construction. The user explicitly said: when updating a file, only change what needs changing so you keep any other changes they made.
- **STRICT PROJECT ISOLATION — never cross-reference another project.** When the user names a project (RCRC, Aseer, Zamzam, etc.), use ONLY that project's data. Never mention another project's team, org chart, gallery names, doc refs, or scope in commentary, analysis, or deliverables unless the user explicitly says "use same team as X project." A single wrong project reference in a deliverable or review comment undermines credibility and triggers user frustration. This applies to: section-by-section reviews, proposal content, org charts, CV references, and any written output. If you need to reference a similar project for context (e.g. past experience), label it clearly as "past project" not as a current-project reference.
- **DOCX close/reopen protocol (mandatory).** Before editing an existing DOCX via python-docx: (1) close Word first via `osascript -e 'tell application "Microsoft Word" to close every document saving yes'`, (2) make edits, (3) save, (4) reopen file via `open <path>`. Without step 1, Word holds a lock and python-docx can corrupt the file or produce a stale version the user cannot see. Without step 4, the user has to manually find and reopen the file.
- **Strip AI fingerprints after every DOCX generation/edit pass.** Run a cleanup pass that removes: em/en dashes, smart quotes, bullet symbols, section symbol, degree symbol, accented characters. Rewrite AI-sounding openings ('This document outlines the technical methodology proposed by' -> concise name + verb like 'SDE proposes'; 'applies a three-phase assessment protocol' -> 'uses three phases'; 'SDE operates under a project-specific quality plan aligned with ISO 9001:2015 principles' -> 'SDE follows ISO 9001:2015 principles'). Remove meta-commentary, hedging ('arguably', 'it could be said'), and self-referential language ('this document was created by'). The user explicitly asked for 'like human written' - every sentence should carry information weight, no filler. **Checklist: scan for these exact characters before presenting - § • — – · → × ° " " ' ' é è ê ë à â ä ù û ü ô ö î ï ç.**
- **Flowcharts in DOCX: prefer SVG for first gen, tables for later edits.** SVG via cairosvg renders cleanly. If the user wants editable charts, replace with styled tables using arrow characters (> v) as connectors. Do NOT use Word VML shapes — python-docx cannot build them reliably. See `references/standalone-subcontractor-docx-pattern.md` for both patterns.

- **Word heading styles (Heading 1/2/3) must be applied after SamayaDoc generation.** SamayaDoc's `add_h1()`/`add_h2()`/`add_h3()` apply direct formatting (font size, bold, color) but do NOT set the Word paragraph style. The user will reject documents where all paragraphs show as "Normal" style in Word's style pane. After generating all content, apply Word heading styles by matching paragraph text patterns:
  ```python
  for p in doc.paragraphs:
      t = p.text.strip()
      if t == 'DOCUMENT TITLE':
          p.style = doc.styles['Heading 1']
      elif len(t) > 3 and t[0].isdigit() and '.0' in t[:4]:
          p.style = doc.styles['Heading 2']
      elif len(t) > 3 and t[0].isdigit() and '.' in t[:5] and '.0' not in t[:4]:
          p.style = doc.styles['Heading 3']
  ```
  Also define heading style fonts to match Samaya branding (Calibri, 18/14/12pt, navy/dark gray). User correction signal: "all titles and pargarphs in normal style , doc not style base H1/H2."
- **Removing table rows: always remove highest index first.** `tbl._tbl.remove(tbl.rows[2]._tr)` before `tbl.rows[1]._tr`, or the index shifts and you delete the wrong row.
- **Table body cells: plain text only** — no `**bold**`, no emoji/icons (🔴🟠). User explicitly rejects these. Use plain severity labels like "Critical" vs "Moderate".
- **Equipment list: verify with user before finalizing.** Never assume what equipment the team actually has. User will correct: "we use the built-in camera, not a separate 360 camera", "no field laptop — processing is at the office workstation". Default to listing only confirmed equipment. Mark uncertain items with a note or ask early.
- **Project data: always check PROJECT_MEMORY.md before writing.** Don't use rough estimates for site area, contract numbers, or dates. The project's own data table (line ~93 in PROJECT_MEMORY.md) has the authoritative site area, contract duration, and handover date. Cross-reference and cite your source.
- **Verification pattern for published values:** After writing any project-specific number (area, dates, counts), search PROJECT_MEMORY.md for the authoritative value. If they differ, fix the document and note the corrected source in the revision log. area is 4,616 m² not "~4,000".
- **Stakeholder logos: NEVER create custom SVG logos.** Use actual files from `_Style-Guides/logos archives/` (moc-logo.png, pmc-logo-trans.png, cg-logo-trans.png, samaya-logo-trans.png, rcrc-logo.svg, bma-logo.svg). Embed as base64 img tags. Authoritative Samaya PNG at `_Style-Guides/samaya-rfi-style-guide/assets/samaya.png` (1885x621, 50KB, RGBA transparent).
- Base64 truncation when patching HTML: verify base64 integrity after any data URI patch. Regenerate via Python base64.b64encode() and replace via script, not patch.
- **SamayaDoc API: `add_bullet()` does NOT exist.** Use `doc.add_body("- item text")` for bullet lists. The `add_body()` method renders as 11pt Calibri justified body text — prefix with dash for list items. This is a common error; the SamayaDoc class provides `add_body`, `add_h1`, `add_h2`, `add_h2_u`, `add_h3`, `add_rich_body`, `add_remark`, `add_table`, `create_header`, `create_footer`, `line`, `save`, `save_temp`.
- MEP scope completeness: cross-reference design packages against references/mep-scope-completeness.md before pricing. Scenographic sets only cover exhibition-facing power and AV containment.
- **Arabic-led bilingual documents:** When the document is bilingual (AR/EN), put Arabic content first. Cover title, eyebrow, and metadata labels should appear in Arabic before English. Add RTL CSS: `.ar{font-family:var(--font-arabic);direction:rtl;text-align:right}`. Wrap Arabic blocks with `dir="rtl"` or class `ar`.

- **Arabic word choice — use simple everyday words, not formal/technical.** This user (Mohamed Essa) corrected this explicitly. Avoid difficult/formal Arabic. Use the substitutions below:

  | Don't use (formal) | Use instead (simple) |
  |---|---|
  | مقرر نقاش | مذكرة نقاش |
  | جدولة عرضية | جدول عرض |
  | الأغراض | القطع |
  | المعرضات | الواجهات |
  | فريق التصميم | الاستشاري |
  | مخطط المخاطر | المخاطر |
  | الملاحظات النهائية | ملاحظات ختامية |
  | الجدول الزمني | الجدول الزمني (keep) |
  | الإجراءات التخفيفية | الحل |

  General rules: short sentences (10-15 words), common everyday vocabulary, avoid compound nouns and formal administrative language. Write as a site engineer would speak, not as a government document.

- **RTL direction in DOCX:** When generating Arabic DOCX, set RTL on every paragraph using the `set_rtl()` helper:
  ```python
  def set_rtl(paragraph):
      pPr = paragraph._p.get_or_add_pPr()
      bidi = OxmlElement('w:bidi')
      pPr.append(bidi)
  ```
  Call this on every paragraph that contains Arabic text. Also set `p.alignment = WD_ALIGN_PARAGRAPH.RIGHT` for Arabic paragraphs. For bilingual documents, English paragraphs stay left-aligned, Arabic paragraphs right-aligned with RTL.
- **Personnel names in sign-off/tables: verify against REPO sources, not just the SMP HTML.** The SMP HTML itself may contain outdated or wrong names (e.g. Adel Darwish instead of Eng. Waris Sultan as PD). Always cross-check against these authoritative repo sources in order:
  1. `Technical_Office/Specialist_Management/specialist_register.md` — definitive role-to-person mapping
  2. `03_Plans/10_Resource/resource_management_plan.md` — team roster with status
  3. `99_Archive/00_Project_Overview/PROJECT_MEMORY.md` — latest project updates
  Only after all three agree, use the name. If they disagree, flag the discrepancy. Do NOT trust the SMP HTML alone — it may be a draft with stale data.

- **Stakeholder descriptions: keep them concise - no internal tracking detail.** Do NOT include CV status, PQD status, target dates, PO/fee details, or internal progress notes in stakeholder register entries. Show only: role name, person/firm, and basic approval status (Approved/TBC/TBD). See references/stakeholder-data-rules.md for full rules. User correction signal: no need extra information.
- **Reference drawings must match the subcontractor's scope.** Do NOT include interior architecture drawings (GA plans, sections, wall details, room elevations) for a landscape subcontractor. Only site/external/irrigation drawings are relevant. Verify each drawing against the SOW scope before copying. See `references/subcontractor-prequalification-package.md` for the drawing selection rules.
- **Prequalification routing: procurement contacts the supplier, not you.** When preparing a prequalification package on behalf of a subcontractor, save to `00_Prequalification/` and email procurement to send it to the supplier. Procurement does NOT stamp the doc — the supplier stamps and signs it. The email should explain why you prepared it (sub lacks museum experience) and what the supplier must do (review, stamp, sign, return).

## Offer Gap Analysis section in SOW

When a subcontractor scope document (SCOPE_REQUEST.md) is used for competitive evaluation (multiple candidates bidding), add a formal §8 Offer Appraisal section after commissioning that documents the gap analysis against each offer received.

### §8 structure

```
## 8. Offer Appraisal — Candidate Comparison

### 8.1 [Company Name] — Gap Analysis ([date])

Context paragraph describing their proposal role and fee.

| SOW Section | Required Scope | Their Offer | Gap Severity |
|------------|---------------|-------------|-------------|
| §2.x | [exact scope item] | [what they exclude or under-offer] | Critical / Moderate |

Summary: one-paragraph verdict — recommended for lead role or not.

### 8.2 Fee Benchmarks

| Candidate | Fee (SAR) | Role | Scope Match | Cycle Time |
|-----------|----------|------|-------------|-----------|
| [Name] | [amount] | [description] | ~XX% | [duration] |
```

### Table formatting rules for gap analysis

- 4-column gap table: SOW Section (2.5cm), Required Scope (5.0cm), Their Offer (5.0cm), Gap Severity (3.0cm) = 15.5cm total
- 5-column fee table: Candidate (3.0cm), Fee (2.5cm), Role (4.0cm), Scope Match (3.0cm), Cycle Time (3.0cm) = 15.5cm total
- All cells left-aligned. No bold text in body cells. No emoji icons (🔴🟠) — use plain text severity labels: "Critical" / "Moderate". Gap Severity values: "Critical — missing" or "Moderate — acceptable if [condition]"
- Summary paragraph: plain text, no bold emphasis

### Sources for gap analysis

Read the candidate's offer document (scanned PDF, email quotation, formal proposal) and map every scope exclusion to the SOW section. Key areas to check:
- Role definition — are they design producer or design verifier?
- Exclusions list — what do they explicitly say is "not included" or "out of scope"?
- Cycle time — does their review/production timeline fit the programme?
- BIM policy — do they produce/coordinate BIM or exclude it?
- Site/construction support — do they include inspection, RFI, FAT, commissioning?
- Authority submissions — included or extra cost?
- Survey / existing-services assessment — included or excluded?

See `references/mep-offer-appraisal.md` for a worked example (AD Engineering vs MEP Designer SOW).

## Programme section in subcontractor docs — use Baseline dates, with Recovery Programme fallback

When writing a **Programme / Schedule** section in any subcontractor SOW or scope document:

- Do NOT use generic `T+X` durations (T+21, T+30, T+60 days from appointment)
- Instead, open `Docs/02_Plans_and_Procedures/02.8_Master_Programme/` and read:
  - `Design_Phase_Master_Programme_Plan.md` (baseline milestone table in §4)
  - `Design_Schedule_Programme.mmd` (Mermaid Gantt for specific disciplines)
- Pick the relevant baseline milestone dates for that subcontractor's discipline
- Show **Baseline Duration** + **Baseline Calendar dates** in a 3-column table
- Reference the master programme doc number (`MOC-ASEER-0PS-SH-006`) as the basis

**Recovery Programme (when baseline has passed):** If the subcontractor appointment is delayed and the original baseline window has already elapsed:
  - Replace the baseline table with a **Recovery Programme** starting from the actual appointment date
  - State the current project stage (e.g. "Starting at 50% design stage")
  - Use overlapping gates (start 90% work during CG 50% review period)
  - Include a **fast-track backbone** row — critical-path deliverables (transformer sizing, MDB SLD, major containment) issued at the 50% gate to release long-lead procurement
  - Add a note that the original baseline (`MOC-ASEER-0PS-SH-006`) is superseded by this recovery programme
  - Explicitly state the acceleration requirement (overlapping gates, 6-day week, parallel discipline tracks)

## SVG chart embedding into DOCX

When the source HTML or spec includes charts (headcount curves, phase strips, org charts, EVM S-curves), embed them as **SVG → PNG via cairosvg** rather than recreating them in Word:

1. Define the SVG as a Python string constant in the gen script
2. Call `render_svg_to_png(svg_content, width, height)` to get a temp PNG
3. Insert into the DOCX body via `run.add_picture(path, width=Cm(N))`
4. The temp file is cleaned with `os.unlink()` immediately after insertion

**macOS cairo fix:** cairosvg needs the Homebrew cairo library. Always run with:
```
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```

**RGBA->RGB conversion (critical for Word rendering):** cairosvg outputs RGBA PNGs. Word on macOS does NOT render RGBA PNGs reliably — they appear as broken images. Convert to RGB with white background immediately after generation:

```python
from PIL import Image
import io

def rgba_to_rgb(png_bytes):
    img = Image.open(io.BytesIO(png_bytes))
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format='PNG')
        return buf.getvalue()
    return png_bytes
```

Then apply before writing to zip:
```python
png_data = rgba_to_rgb(cairosvg.svg2png(bytestring=svg_string.encode(), output_width=1740))
```

**cNvPr name fix:** After python-docx saves, the `pic:cNvPr` elements get temp filenames (`tmpXXXX.png`) instead of proper names like `"Picture 1"`. This also breaks Word rendering. Fix via lxml zip manipulation — match cNvPr to wp:docPr by position:

```python
import zipfile, os
from lxml import etree

with zipfile.ZipFile(docx_path, 'r') as zin:
    doc_xml = zin.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    NS = {'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
          'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
    docprs = root.findall('.//wp:docPr', NS)
    cnvprs = root.findall('.//pic:cNvPr', NS)
    for i, cnvpr in enumerate(cnvprs):
        if i < len(docprs):
            cnvpr.set('name', docprs[i].get('name', f'Picture {i+1}'))
    fixed = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    with zipfile.ZipFile(docx_path + '.tmp', 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, fixed)
            else:
                zout.writestr(item, zin.read(item.filename))
    os.replace(docx_path + '.tmp', docx_path)
```

**Pitfall:** If you skip both the RGBA->RGB conversion AND the cNvPr name fix, the user will see "all images broken" in Word. The images are structurally valid (correct bytes, correct rels) but Word on macOS refuses to render them without these two fixes. Always verify by opening in Word, not just by checking the zip contents.

See `references/svg-chart-embedding.md` for full implementation.

### Flowchart SVGs (process diagrams)

For process flowcharts (control cycles, installation methodology, org charts), see `references/flowchart-svg-patterns.md`. Key rules:
- Crop viewBox to actual content bounds or the image won't center
- L-shaped arrows need explicit path routing (not just x1/y1→x2/y2) — a down-arrow from Step 4 (x=940) must route to Step 5 (x=130) via L-shaped path, not drop straight down into empty space
- Arrow endpoints must touch the target box edge exactly — 10px gap = visible disconnect in Word
- Use 16px font for box titles, 13px for subtitles — smaller is unreadable when printed. Thicker arrows (stroke-width=3) and larger markers (14x10px) improve readability
- Run with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` for cairosvg
- **Word opens in same position as last closed** — if user says "open it" and nothing appears, it may be behind other windows. Verify with `open -a "Microsoft Word" <path>` and a brief wait

## Inline SVG flowcharts (for HTML documents)

For HTML documents, create flowcharts directly as **inline SVGs** — no base64, no external files, no cairosvg conversion. This is more reliable and produces smaller files than embedded PNGs.

### SVG flowchart patterns (all monochrome #000 for CV-pack template):

**1. Process pipeline (horizontal):** Boxes connected by arrows, left to right. Each box is `<rect rx="3" ry="3">` with `<text>` inside. Arrow is `<path d="M...L...">` with marker-end arrowhead.

**2. Timeline (horizontal with columns):** Rows of boxes for each phase, with milestone markers on a timeline axis at the bottom. Deliverable details below in dashed border boxes.

**3. Data flow (vertical columns):** Multiple parallel columns, each with Input → Process → Output sub-boxes stacked vertically. QC gates as diamond shapes.

### SVG sizing for A4:
- Width: 174mm (full text width). In SVG units: use `viewBox="0 0 1740 600"` (174mm at 10 units/mm) for horizontal flowcharts.
- Height: 40-70mm depending on content density.
- Font size in SVG: 6.5-8pt for labels, 10pt for headers. `font-family="Calibri, Arial, sans-serif"`.
- Scale: the viewBox units map directly to the printed size — 10 units = 1mm visually.

### Quick generator pattern:
```python
def make_flowchart_svg(stages, width=1740, height=600):
    """stages: list of dicts with 'label', 'sub', 'x', 'w'"""
    svg = f'<svg viewBox="0 0 {width} {height}" ...>'
    # boxes + arrows + labels
    return svg
```

### Stakeholder logos as SVGs:
- 4-column grid, each `viewBox="0 0 200 100"`
- Use geometric shapes (circles, shields, triangles) with monogram lettering
- No colors — solid black #000 for CV-pack style
- Fill 10mm height via CSS `height: 10mm; object-fit: contain;`
- Example: shield for MoC, interlocking rings for ACE, square+circle for CG, pyramid for SAMAYA

## HTML Print-Ready Document Pattern (preferred for formal submittals)

**CRITICAL — For ALL new HTML engineering documents, use the Samaya Document & Engineering-Chart Framework v1.0:**
`~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Samaya-Document-Engineering-Chart-Framework-v1.0.md`

The framework provides: auto-numbering engine, TOC/LoF/LoT generation, cross-references, 14 chart types (SVG + CSS), and 100+ page architecture. This supersedes all previous HTML templates.

When creating a formal project plan (SMP, BEP, DMP, MOS, Risk Plan), **prefer the HTML print-ready framework** over DOCX. The HTML format supports:

- Dark navy cover page with all 5 project logos (MoC, PMC, CG, NRS, Samaya)
- TOC with snapshot metric cards
- Embedded photographs (real site images, not placeholders)
- Workflow node diagrams, risk matrices with colour-coded scores
- A4 print layout via CSS @page rules
- PDF generation via WeasyPrint

See `references/samaya-html-print-template.md` for the full design system.

### Project folder creation

When starting a new document type under `02_Plans_and_Procedures/`:

```
mkdir -p 02.XX_Document_Type/{00_Master_Index,01_Source_Files/01_HTML/assets,01_Source_Files/02_PDFs,01_Source_Files/03_Word,01_Source_Files/04_Assets,02_CG_Responses,03_Supplementary,04_Registers,05_Compliance_Audit,06_Legacy_Files,07_Guidelines}
```

Copy logos from `02.13_Stakeholder_Plan/01_Source_Files/01_HTML/assets/`.

### PDF generation from HTML

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib weasyprint "input.html" "output.pdf"
```

### Surge deployment (only if user requests)

```bash
cd "01_Source_Files/01_HTML"
surge --domain project-doc-ref.surge.sh .
```

## Dual HTML + DOCX generation pattern

When a deliverable needs both formats, generate from a single source:

1. Write the full HTML as a Python f-string constant with SVG charts inline
2. Write the DOCX using SamayaDoc with same content structure
3. Both render from the same data — revision log, tables, definitions
4. Output HTML goes to `01_Source_Files/01_HTML/`, DOCX to `01_Source_Files/03_Word/`
5. Version both together (same Rev tag, same date)

This avoids drift between source and deliverable.

## Project-knowledge-driven document updates

When updating a formal plan (Resource Mgmt, Communication, DMP, etc.) with new project knowledge:

1. **Source the knowledge:**
   - Email archive: scan `~/Documents/04_Outlook_Connection/mails/NN.md` for project-specific updates (CG codes, personnel, subs)
   - Session search: query recent conversations about the project
   - PROJECT_MEMORY: read `PENDING_PROJECT_MEMORY_UPDATES.md` or `PROJECT_MEMORY_WEEK*.md`
   - CG_STATUS.md in the plan's `02_CG_Responses/` folder
   - **Cross-document alignment:** read a related/companion plan (SMP, DMP, PEP) that was recently revised; extract role changes, org structure updates, and escalation changes that need syncing into this document

2. **Identify what changed:**
   - New personnel / role changes (Tech Director, Submittals Coord)
   - New subcontractors nominated (Lumotion, ZNA Studio, ICT Security)
   - Updated reference documents (Master Programme Rev.03)
   - New resource risks from project events (microcement stoppage)
   - Doc ref changes

3. **Map to document sections:**
   - Personnel → Org chart, Location Matrix, Outsourced table
   - Subs → Sub-Contractor Integration table, Outsourced table
   - Doc refs → Authority Basis, Companion Documents
   - Risks → new Resource Risk Register section

4. **Update revision log** with explicit delta description

## DOCX→HTML sync (Master-DOCX → HTML catch-up)

When the DOCX is the master (updated by a stakeholder) and the existing HTML must be updated to match:

1. Extract DOCX paragraphs with python-docx to find what changed
2. Build a section-by-section change map
3. **Delegate the HTML rebuild to a subagent** — the HTML file is too large to rebuild inline
4. In parallel, create starter Excel registers (Physical Resource, Personnel Deployment, Risk) and compliance audit files
5. Update CG_STATUS.md to reflect the new revision

See `references/docx-to-html-sync.md` for the full step-by-step workflow with exact delegation prompt structure and verification checklist.

## Halftone remark paragraphs using `add_remark()`

Descriptive/commentary sentences between headings and tables (e.g. "4 spheres of influence showing...", "2x2 graphical classification...", "snapshot baselined...") must render in **halftone** — medium gray `#64748B`, 9pt. This visually distinguishes explanatory text from actionable content.

### Preferred approach: `doc.add_remark()`

Use the `add_remark()` method on `SamayaDoc` instead of `add_body()` for remark content:

```python
# Instead of:
doc.add_body("4 spheres of influence showing the contractual hierarchy.")
doc.add_body("R = Responsible, A = Accountable, C = Consulted, I = Informed.")

# Use:
doc.add_remark("4 spheres of influence showing the contractual hierarchy.")
# → 9pt halftone #64748B, compact spacing (2pt before/after, 11pt line)
doc.add_remark("R = Responsible, A = Accountable, C = Consulted, I = Informed.")
```

| Use `add_body()` for | Use `add_remark()` for |
|---|---|
| Project metadata, policy statements, scope descriptions | Short descriptions of tables/charts |
| Formal content paragraphs with contractual weight | Explanatory notes, commentary, timestamp notes |
| Paragraphs > ~180 chars of substantive content | RACI legend definitions, "This snapshot baselined..." notes |

### Post-processing fallback (editing existing docs)

When retrofitting an existing DOCX that wasn't generated with `add_remark()`, use this heuristic — short (<180 chars), non-bold paragraphs after headings are treated as remarks:

```python
from docx.shared import Pt, RGBColor

HALFTONE = RGBColor(0x64, 0x74, 0x8B)
for p in doc.paragraphs:
    text = p.text.strip()
    if not text or len(text) < 15:
        continue
    if p.runs and p.runs[0].font.bold:
        continue  # skip headings
    if len(text) < 180:
        for run in p.runs:
            run.font.size = Pt(9)
            run.font.color.rgb = HALFTONE
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
```

Contractual references (SoW section numbers, ER clauses, code names, CG comments) in DOCX body text must render in **halftone** — medium gray `#64748B`, 9pt. This visually distinguishes the reference from the task statement.

```python
from docx.shared import RGBColor, Pt
HALFTONE = RGBColor(0x64, 0x74, 0x8B)
for p in doc.paragraphs:
    for run in p.runs:
        if any(pat in run.text for pat in ['Section 13.9', 'Section 3.7', 'ER Section', 'SBC 60']):
            run.font.color.rgb = HALFTONE
            run.font.size = Pt(9)
```

Apply this after generating the document, before saving.

## Align coordination/reporting with project Communication Plan

When writing a SOW, R&R, or any document with coordination/reporting sections, **do NOT invent the structure.** Read the project's Communication Plan first:

1. Open `.../02.7_Communication_Plan/01_Source_Files/01_HTML/Aseer_Communication_Plan_RevC02_Comprehensive.html`
2. Extract Table 9 (Party Contact Matrix), Table 13 (Report Cadence), Table 31 (Document Distribution Matrix)
3. **Routing rule:** MoC is NEVER direct — all communication routes Samaya → CG → PMC → MoC.
4. Reference the Communication Plan by doc number in the governance section.

**Pitfall:** If you write a coordination table without checking the Communication Plan, you will invent routing that contradicts the project's approved document. The user will correct you.

## Sustainability document framing — compliance, not points

**Critical rule for ALL sustainability documents (strategy, plan, SOW, R&R):** the ER mandates code compliance (Mostadam Manual + SBC 1001), NOT a rating tier or points target. Never frame the document around chasing Silver/Gold/Platinum or accumulating points.

### What to strip from any sustainability document

| Language to remove | Replace with |
|---|---|
| "Target Silver 45+ pts" | "Comply with Mostadam Manual requirements" |
| "Gold stretch goal 60+ pts" | Remove entirely |
| "Target pts" column header | "Compliance" |
| "~X pts" credit pool labels | Remove entirely |
| "TOTAL POINTS" summary row | Remove entirely |
| "Voluntary target / stretch" | Remove entirely |
| "credit pool" | "compliance category" |
| "credit-targeting log" | "compliance log" |
| "Stretch ≥ X% (Y+ pts)" | Remove entirely |
| "Pre-credit application" | "Pre-compliance review" |
| "Owner of design-stage credits (~X pts)" | "Owner of design-stage compliance" |
| "Rating tier" DC block line | Remove entirely |

### What to keep

- ER section references verbatim (e.g. ER §2.5 "targeted points" is a section title — keep as factual citation)
- Revision log entries describing historical changes (factual record)
- Code names: Mostadam Manual, SBC 1001, SBC 601/602, SASO, ASHRAE 90.1
- Compliance matrices with credit names and actions
- Subcontractor obligations tables
- Procurement sustainability specifications
- Reporting cadence and verification procedures

### Verification checklist before presenting

1. Scan for: Silver, Gold, 45+, 60+, "pts", "stretch", "rating tier", "credit pool", "total points", "target pts", "targeted points"
2. Check column headers — "Target pts" → "Compliance", "Stretch" → "Status"
3. Check DC block — no "Rating tier" line
4. Check snap cards / metric cards — no voluntary target/stretch badges
5. Check compliance matrix — no TOTAL POINTS summary row
6. Check RACI matrix — no "owner of X credits (~Y pts)" language
7. Check body paragraphs — no "Samaya commits to SILVER" or "aspiration" language

**Pitfall:** If you present a sustainability document with points-chasing language, the user will correct: "we didn't request for any target just to comply and apply codes, no need to collect points." The ER mandates code compliance, not a rating. A single comprehensive pass stripping all points language is faster than 3 fix rounds.

## Mandatory symbol & AI-fingerprint cleanup after EVERY DOCX edit

**This is the #1 avoidable user correction.** The user will say "you forget dont use section symbol or any AI symbols or finger prints ... write like humman" if you skip this. Run this cleanup pass on every DOCX after any edit — generation, reformatting, or revision bump.

### Step 1: Scan for symbols

```python
symbols = ['\u00a7', '\u2022', '\u00b7', '\u2014', '\u2013', '\u2192', '\u00d7', '\u00b0',
           '\u25cf', '\u25cb', '\u201c', '\u201d', '\u2018', '\u2019',
           '\u00e9', '\u00e8', '\u00ea', '\u00eb', '\u00e0', '\u00e2', '\u00e4',
           '\u00f9', '\u00fb', '\u00fc', '\u00f4', '\u00f6', '\u00ee', '\u00ef', '\u00e7']
for i, p in enumerate(doc.paragraphs):
    for ch in symbols:
        if ch in p.text:
            print(f"P{i}: symbol '{ch}'")
# Also scan table cells
for ti, t in enumerate(doc.tables):
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            for ch in symbols:
                if ch in cell.text:
                    print(f"T{ti}R{ri}C{ci}: symbol '{ch}'")
```

### Step 2: Replace symbols with plain text

| Symbol | Replace with |
|--------|-------------|
| em dash (\u2014) | ` - ` |
| en dash (\u2013) | ` - ` |
| middle dot / bullet (\u00b7, \u2022) | ` - ` |
| section symbol (\u00a7) | `Sec. ` |
| arrow (\u2192) | ` > ` |
| filled/open circles (\u25cf, \u25cb) | `[P]` / `[V]` |
| smart quotes (\u201c \u201d) | `"` (straight quote) |
| smart apostrophe (\u2018 \u2019) | `'` (straight apostrophe) |
| accented chars (\u00e9, \u00e8, etc.) | plain ASCII equivalent |

Apply via run-level replacement to preserve formatting:
```python
replacements = {
    '\u2014': ' - ', '\u2013': ' - ', '\u00b7': ' - ', '\u2022': ' - ',
    '\u00a7': 'Sec. ', '\u2192': ' > ',
    '\u25cf': '[P]', '\u25cb': '[V]',
    '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
}
for p in doc.paragraphs:
    for run in p.runs:
        for old, new in replacements.items():
            if old in run.text:
                run.text = run.text.replace(old, new)
# Same for all table cells
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    for old, new in replacements.items():
                        if old in run.text:
                            run.text = run.text.replace(old, new)
```

### Step 3: Rewrite AI-sounding phrases

Scan for these patterns and rewrite to plain engineering English:

| AI phrase | Rewrite to |
|-----------|-----------|
| "This plan sets out how" | "Samaya does X per this plan" |
| "This document outlines" | Remove — start with the action |
| "aligned to" | "per" |
| "Hierarchical decomposition" | "Breakdown" |
| "Defines how" | "Covers how" |
| "are managed, tracked, maintained, and controlled" | "are managed and tracked" |
| "etc." | "and others" |
| "in accordance with" | "per" |
| "in order to" | "to" |
| "ensures that" | "makes sure" |
| "comprehensive" | Remove (filler) |
| "the following sections" | Remove — just present the sections |
| "as shown above" | Remove — trust the reader |
| "it should be noted" | Remove — state the fact directly |
| "seamlessly", "synergistic", "cutting-edge", "state-of-the-art", "holistic", "leverage", "robust", "innovative", "bespoke" | Remove all — these are AI cliches |

### Step 4: Verify zero symbols remain

```python
remaining = 0
for i, p in enumerate(doc.paragraphs):
    for ch in symbols:
        if ch in p.text:
            remaining += 1
for ti, t in enumerate(doc.tables):
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            for ch in symbols:
                if ch in cell.text:
                    remaining += 1
assert remaining == 0, f"{remaining} symbols still present"
```

**Pitfall:** If you skip this cleanup, the user will correct you with "you forget dont use section symbol or any AI symbols or finger prints ... write like humman" — this is a known correction pattern. A single comprehensive pass is faster than 2 fix rounds. The user expects you to catch this yourself without being reminded.

## Comprehensive audit before presenting — do NOT wait for user to find issues

**Rule: before presenting any deliverable to the user, do a full self-audit against all known user preferences and project standards.** The user will not point out issues one by one — they expect you to catch everything yourself. Letting the user find issues will cause frustration: "dont wait me to ask you one by one" is a signal that you should have been more thorough.

**Mandatory audit checklist for any document (run every step before presenting):**
1. **Contract scope:** Every task statement must be grounded in a specific SoW/ER clause. **Dispatch labors (Kimi/Codex/Claude) with the source PDFs for independent verification of scope claims** — this is not optional. See the "SOW contract-accuracy verification" section above.
2. **Style rules:** No section symbol, no emoji/icons, halftone references (#64748B 9pt), SamayaDoc template used, correct margins/colors/fonts.
3. **Project plan alignment:** Communication Plan (02.7), Stakeholder Plan (02.13) — check before writing coordination/reporting sections. Never invent routing. Verify MoC is never direct.
4. **Language:** Level 6 English, no AI fingerprints, no hedging, no meta-commentary.
5. **File placement:** Correct subfolder under 04_Docs/, not old Docs/ path.
6. **Odoo descriptions:** Project-oriented, no AI commentary, no icons, short bullets. See odoo skill.
7. **Commercial readiness:** If the document has an acceptance/signature block, confirm the commercial arrangement (contract/PO/payment terms) is actually in place. Do NOT include acceptance language if the commercial side is not finalized.

**Pitfall:** If you skip this audit and wait for the user to review, expect multiple rounds of corrections with increasing frustration. The user expects you to catch everything — style, routing, contract scope, placement, commercial readiness — in one shot. A single comprehensive pass is faster than 5 fix rounds.

## HTML format decision: Color vs. Monochrome

Two HTML template styles exist for Samaya formal documents:

| Style | Template | Best for |
|-------|----------|----------|
| **Color (navy/red)** | `samaya-html-print-template.md` ref | Proposals, presentations, MoC-facing documents |
| **Monochrome (black/white)** | `cv-pack-html-template.md` ref — matches `ASR-SAM-KP-CV-PACK-BIM-001.html` | Method of Statements, technical plans, CG submittals, CV packs |

**Default:** If the user doesn't specify, ask or default to the monochrome CV-pack template for technical documents. The CV-pack style is what GC/consultant reviewers are accustomed to seeing.

### Monochrome template structure

See `references/cv-pack-html-template.md` for full CSS, page structure, and image embedding workflow. The key classes are `sheet`, `doc-strip`, `logo-strip`, `meta-grid`, `dc-block`, `qc-block`, `summary-table` — all black-on-white, no colors.

To start any formal HTML document:
```
1. skill_view(name='samaya-docx-template')
2. Read the CV pack HTML at .../HTML/ASR-SAM-KP-CV-PACK-BIM-001.html for latest CSS
3. Follow `references/cv-pack-html-template.md` for structure
```

### Image embedding — common failure and fix

Subagents frequently download HTML error pages instead of real JPEG images:
- Always run `file image.jpg` to verify it says "JPEG image data" (not "HTML document")
- Verify base64 decodes with JPEG magic bytes `\xff\xd8`:
  ```python
  import base64
  decoded = base64.b64decode(b64_string)
  assert decoded[:2] == b'\xff\xd8', "Not a real JPEG"
  ```
- PDF brochure extraction via PyMuPDF (`fitz`) is more reliable than web downloads for product images. Extract at 3x resolution for print quality:
  ```python
  pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
  pix.save("output.jpg")
  ```
- **Image sourcing workflow (preferred):** Wikimedia Commons (commons.wikimedia.org) for CC-licensed real photos. Search via browser, download full resolution via curl, verify with `file`, then base64 embed. Avoid hotlinking — embed as data URIs so the HTML is self-contained.
- **When fixing broken base64 in existing HTML:** Use both regex patterns (alt-before-src, src-before-alt) and iterate until `file` verification confirms all images are JPEGs:
  ```python
  patterns = [
    r'(<img[^>]*?alt="ALT"[^>]*?src=")data:image/[^;]+;base64,[A-Za-z0-9+/=]+(")',
    r'(<img[^>]*?src=")data:image/[^;]+;base64,[A-Za-z0-9+/=]+("[^>]*?alt="ALT")'
  ]
  ```
- **Stakeholder logos:** Prefer inline SVGs over text or base64 images for logos. Create 4-column grid with `viewBox="0 0 200 100"` SVGs. Keep them monochrome (#000) for the CV-pack template style.

## DOCX formatting fixes (page breaks, table splitting, column widths)

When the user asks to "fix tables", "don't split tables", "add page breaks", "fix column widths", or "make Rev00" from an existing DOCX, see `references/docx-formatting-fixes.md`. This covers:

- Adding `pageBreakBefore` to H2 section headings (not sub-headings)
- Setting `cantSplit` on all table rows to prevent page-splitting
- Setting proportional percentage column widths per column count
- RevC03→Rev00 reset pattern (copy + format fixes, no metadata changes)
- Verification checks after fixes
- Charts vs images detection

**Pitfall:** Only add page breaks to section-level H2 headings, not sub-headings (H3 like "1.1", "2.1"). The divider paragraphs (all-caps section labels) also need breaks. `cantSplit` on every row means a tall table pushes entirely to the next page — this is correct per user request.

## DOCX Audit-and-Fix Workflow (non-SamayaDoc documents)

When the user says "check this [plan docx]" on a document that was NOT created via SamayaDoc, use `references/docx-audit-and-fix-workflow.md` for a systematic audit-and-fix pattern:

1. **Audit** — check heading styles (all "Normal"?), cantSplit on tables, RBS/category consistency across sections, stale timelines, missing project-specific risks (e.g., Mostadam)
2. **Fix** — apply Heading 1/2/3 styles by paragraph index, add cantSplit to all rows, rebuild taxonomy tables via XML row replacement, fix run-level text content, add missing rows
3. **Cross-reference** — compare DOCX content against the repo markdown version of the same plan (scoring scale, risk count, categories, EMV values, risk IDs). Also check related Excel registers against the plan's stated numbers.
4. **Present findings** — use a table with Arabic summaries for each point (one short line per finding, simple everyday Arabic, no symbols)
5. **Verify** — re-read and assert all fixes applied

See the reference file for complete code patterns including: table XML rebuild with width-per-column, run-level text replacement vs XML-level for split-run text, and adding new rows to existing tables.

## Related reference files

- `references/dc-submission-transmittal-pattern.md` — DC submission transmittal for submitting prequalification packages to CG via Aconex (cover document with attachments table)
- `references/docx-audit-and-fix-workflow.md` — Systematic audit and structural fix for existing DOCX (heading styles, cantSplit, table rebuilding via XML, content correction). Use when user says "check this [plan docx]" on non-SamayaDoc documents.
- `references/docx-formatting-fixes.md` — DOCX formatting fixes: page breaks before sections, prevent table splitting, set proportional column widths, RevC03→Rev00 reset pattern
- `references/docx-image-rendering-fix.md` — Fix for images disappearing after bulk DOCX edits: empty cNvPr name, missing noChangeAspect, AND RGBA->RGB conversion (Word on macOS does not render RGBA PNGs). Run after any page-break/table-width/symbol-cleanup pass.
- `references/cg-correspondence-best-practices.md` — CG correspondence strategy: don't ask logic questions, separate threads, align with NRS before sending, acknowledge without commitment, state commercial impact upfront. Derived from user corrections on email drafts to CG.
- `references/contract-grounded-sow-methodology.md` — Verifying SOW scope against contract (SoW + ER) before writing. Every scope statement must map to a contract clause; never invent tasks. Dispatch labors (Kimi/Codex/Claude) for cross-verification. Copy PDFs from OneDrive via AppleScript first, then extract text with PyMuPDF. See the "SOW contract-accuracy verification" section above.
- `references/onedrive-macos-workaround.md` — OneDrive macOS sandbox workaround via Finder AppleScript (essential when files lock after `mv`)
- `references/docx-generation-example.md` — Full working gen script with `set_table_widths()` + `get_col_widths()`
- `references/markdown-to-docx-pipeline.md` — Full-feature markdown-to-DOCX pipeline: cover page, styled tables, colour-coded P-I matrix, header/footer with Page X of Y, code blocks, blockquotes, lists. Use when source is a `.md` file and SamayaDoc is not available.
- `references/batch-md-to-docx-conversion.md` — Converting multiple MD deliverables to Samaya-branded DOCX in one script pass
- `references/microclimate-action-report-pattern.md` — Museum showcase microclimate control + T&H monitoring action reports. Connected vs individual showcase architecture, 7/8-section structure, cost presentation rules, SVG flowchart patterns for DOCX.
- `references/docx-editing-techniques.md` — Editing existing DOCX files (remove table rows, update paragraphs, save as R01). Use terminal heredoc, not execute_code sandbox.
- `references/svg-chart-embedding.md` — SVG chart creation, cairosvg rendering, Mac cairo fix, dual HTML/DOCX gen pattern
- `references/svg-embedding-docx-pattern.md` — SVG→PNG→DOCX embedding via cairosvg: working `add_svg_to_doc()` function, viewBox cropping rules, flowchart arrow routing, A4 sizing. Essential for any DOCX with embedded flowcharts.
- `references/subcontractor-creation-workflow.md` — End-to-end workflow for setting up a new subcontractor folder with SOW, docx, SitRep, and reference files
- `references/mep-scope-completeness.md` — Scope gaps checklist (earthing, ELV, existing-services survey, gallery env, commissioning role, fire completeness, CITC telecom clause, recovery programme pattern)
- `references/method-of-statement-pattern.md` — MOS generation pattern: PMBOK 11-section structure, doc ref pattern, column width tables per section, gen script skeleton, dual DOCX+HTML tracks, personnel verification protocol
- `references/comprehensive-mos-pattern.md` — Extended 15-section MOS for LiDAR scanning, heritage documentation — image-rich HTML-first with embedded photos, 4 scan rounds
- `references/samaya-html-print-template.md` — **HTML print-ready document design system**: CSS classes, cover page pattern, page shell, photo embedding, project folder template, weasyprint/Surge workflow
- `references/stakeholder-plan-docx-generation.md` — SMP DOCX generation: content extraction, SVG chart specs, personnel verification, revision history, common pitfalls
- `references/standalone-subcontractor-docx-pattern.md` — Creating standalone DOCX for subcontractors to submit TO Samaya (not Samaya-branded). Includes: subcontractor's own logo + color palette, day-based Gantt charts (not calendar dates), DMP Gate + RACI columns, SVG vs table flowchart patterns, third-party report handling ("use as guide only"), Oddy scope boundary, BIM coordination ownership split, and all helper functions. See the `When to use` section for the distinction.
- `references/sustainability-points-stripping.md` — Complete reference for stripping points-chasing / rating-tier language from sustainability documents. The ER mandates code compliance (Mostadam Manual + SBC 1001), not a rating tier. This reference documents every pattern to remove and what to replace it with, plus the verification checklist.
- `references/subcontractor-prequalification-package.md` — Prequalification package for subs lacking museum experience: letter, RACI, risk register, procurement routing, email template, drawing selection rules

## Reusable scripts

- `scripts/html-to-docx-converter.py` — CLI tool: `python3 html-to-docx-converter.py <input.html> <output.docx> [--strip-points] [--clean]`. Walks HTML body in order, maps h2/h3/h4/p/table/ul/ol/hr to SamayaDoc methods. Handles inline bold/italic, nested HTML in cells, Arabic text.
  - `--strip-points`: pre-processes HTML to remove all points-chasing / rating-tier language for sustainability documents (ER mandates code compliance, not a rating).
  - `--clean`: strips decorative symbols (§ · — – → × ° •) and AI-sounding phrases ("this strategy reads", "the highest-impact", "the biggest X lever", "reading note", "this is the X-defining rule"). Use for any document where the user wants plain engineering English with no AI fingerprint.
  - Edit config constants at the top of `main()` to set doc ref, project name, revision, etc.
