---
name: hermes-quality-assurance
description: Use before delivering ANY Hermes labor output (HTML, code, analysis) — runs cross-labor audit, HTML validation, and file-contamination checks
version: 1.5.1
author: agent
tags: [qa, quality-assurance, audit, html-validation, workflow]
triggers:
  - before delivering any deliverable produced by a labor (Claude Code, Kimi, etc.)
  - generated or edited HTML / A4 print pages
  - file looks contaminated with line-number prefixes
  - cross-labor audit needed (one labor checks another's output)
---

# Hermes Quality Assurance

QA protocol for all deliverables produced by labors (Claude Code, Kimi, etc.) — catch layout breaks, logic errors, and content contamination before delivery.

> **HARD RULE — NEVER deliver labor output without a QA pass.** Every Claude Code deliverable must clear Kimi audit (and `scripts/qa_check.py` for HTML) before it reaches the user.

## Workflow

```
Plan (agent-as-leader)
  └── Claude Code (execute heavy work — HTML gen, deep analysis, code)
        └── Kimi (MANDATORY audit of Claude output)
              ├── HTML/CSS structure check
              ├── Content accuracy / scope check
              ├── Layout validation (div balance, closing tags)
              └── File contamination check
        └── Fix issues found by Kimi
              └── Deliver
```

**Rule:** NEVER deliver output from Claude Code without Kimi QA check first.

## CRITICAL: File Contamination Pitfall (read_file → write_file)

`read_file()` returns content WITH line number prefixes like:
```
   123|<div class="sheet">
```

If this output is used directly as input to `write_file()`, the file becomes:
```
   123|<div class="sheet">
```

This breaks ALL browser rendering — the line numbers appear as visible text.

**Prevention:**
- Never pipe `read_file()` output → `write_file()`.
- Always use terminal `cat` or `subprocess.run(['cat', path])` to get raw file content.
- QA check: Verify first line of output does NOT match `^\s*\d+\|`.

**Fix if contaminated:**
```python
import re
c = re.sub(r'^\s*\d+\|', '', c, flags=re.MULTILINE)
```

## HTML QA Checklist

Don't hand-roll the checks — run the bundled script against every generated HTML before delivery:

```bash
python3 scripts/qa_check.py path/to/file.html [more.html ...]
```

Exits non-zero if any file has issues; prints a per-file pass/fail report. It checks:

| # | Check | Why |
|---|-------|-----|
| 1 | `<!DOCTYPE html>` present | rendering mode |
| 2 | `</html>` and `</body>` present | truncated output |
| 3 | `<div>` open/close balance | layout break |
| 4 | `table`/`thead`/`tbody` balance | table collapse |
| 5 | No line-number contamination | read_file pitfall |
| 6 | A4 print setup when class=sheet present | print overflow |
| 7 | Image/asset paths resolve correctly | broken images |
| 8 | TOC updated after page add/move/delete | stale page refs |
| 9 | Page IDs sequential 1..N | anchor link breaks |
| 10 | No broken `<section>` tags (`ection class="page"`) | regex replacement bug where `>` was omitted — the string `ection class="page"` (missing `<s` and `>`) should not appear in the output |
| 11 | All internal § references hyperlinked (`&sect;N` → `<a href="#sN">`) | broken navigation |
| 12 | Mobile UI interaction check | interactive elements work on mobile |
| 13 | Schedule / programme alignment (MOS, master plans with timelines) | dates misaligned with project reality |

### Full-Document Integrity After Targeted Patch

When Claude Code or another labor patches a single page/section of a large HTML file, perform these checks before delivery:

1. **Page count** — verify total pages haven't changed unexpectedly: `grep -c '<section class="page"' file.html`
2. **Section balance** — `grep -c '<section'` must equal `grep -c '</section>'`
3. **Key content pages** — check that BOQ, payment, terms, and other critical sections are present and not truncated
4. **Backup exists** — confirm a `.bak` copy was made before the edit (if not, this is a workflow failure)
5. **Footer page numbers** — verify all `Page <b>N</b> / M` footers are sequential 1..M with no gaps
6. **Deploy and preview** — check the live site at every page, not just the edited one
7. **Page height audit** — verify no page exceeds the A4 1123px boundary after the patch. Run in browser console: `Array.from(document.querySelectorAll('.page')).map((p,i) => i+1 + ':' + p.offsetHeight).join(', ')`. Any value > 1123 means clipped content.
8. **CSS isolation check** — if the patch injected a new `<style>` block, verify all selectors are scoped (e.g. `.p15-*` namespaced to their page). A bare `.page`, `.pf`, `.boq`, or `table` selector in an injected style block can override global CSS on all pages. Check: `grep -E '^\\s*\\.(page|pf|ph|boq|pay|toc|gantt|spec|docs|sec|stat|phase)\\b'` in the injected block.
9. **CSS stacking context check** — After a CSS rewrite that changes `display` (flex→block), `position`, or `z-index` on modal/overlay elements, verify interactive buttons are clickable and not shadowed by backdrop elements. Check `position: fixed` elements aren't overridden by lower-specificity base class rules.

**Pitfall:** A focused patch on page 15 can corrupt unrelated pages through CSS conflicts, overflow clipping (pages exceeding 1123px min-height), or accidental tag removal in surrounding content. The diff only shows what the labor *intended* to change, not what *actually broke*. **Always re-measure all page heights after any structural patch — don't assume pages you didn't edit still fit.**

**Pitfall — Subagent overwrites the whole file instead of patching:** Subagents with `patch()` may accidentally replace the entire file content if the old_string isn't unique or the match fails. Always verify file size and first/last 5 lines after a subagent edit. If the file shrank or the first line changed from `<!DOCTYPE html>` to something else, the subagent corrupted it.

**Pitfall — Regex `>>` double-close on section tags:** When post-processing HTML to add `data-page` attributes, a regex like `/<section[^>]*class="[^"]*page[^"]*"/g` matches only up to the closing `"` of the `class` attribute, NOT the full tag. If the replacement string adds `>` but the original `>` remains unconsumed by the regex, every section tag ends with `>>`. The browser parses this as broken markup and the text `ection class="page">` appears as visible content. **Check:** grep for `ection class="page"` (missing `<`) and `class="page">>` (double `>>`) in the final output — zero of either means tags are well-formed.

### Section Reference (§) Link Audit

In project documents with cross-references, all internal `§` references must be hyperlinked anchors — plain text § references break navigation in digital delivery.

**Check:** After any edit that adds, removes, or renames sections:
```python
import re
c = open('file.html').read()
# Count all internal § refs that have anchors
anchored_sections = ['1.2','1.5','3.1','5.1','7.0','8','9','10','11','12','13']
unlinked = 0
for sec in anchored_sections:
    for m in re.finditer(f'&sect;{re.escape(sec)}', c):
        pos = m.start()
        before_tag = c[:pos].rfind('<a ')
        after_tag = c[:pos].rfind('</a>')
        if before_tag <= after_tag:  # not inside a link
            # Skip external refs (ROADMAP §, ER §, SoW §, Contract §)
            before_text = c[max(0,pos-40):pos]
            if not re.search(r'(ROADMAP|ER\\s|SoW\\s|Contract\\s)', before_text):
                unlinked += 1
```

**Linking pattern** (invisible link — no visual change):
```html
<a href="#s7" style="text-decoration:none;color:inherit">§7.0</a>
```

**Mapping:** section IDs like `id="s7"` on an `<h2>` map to `#s7` for §7.0. Sub-sections like §12.2 use `id="s12-2"` → `href="#s12-2"`.

**Common miss:** When moving section references from body text to a separate "CRP §" column in a disposition table, re-wrap as links — don't leave them as plain `&sect;7.0`.

### Table Column Width Audit

Tables with explicit column widths must fit their actual content. A column that's too narrow wraps text into unreadable towers; one too wide wastes space.

**Check after setting column widths:**
```python
# For each column, measure the longest content string in chars
# At 0.4rem (~6.4px base), Inter regular: ~5.5px/char, bold: ~6px/char
# Include cell padding: 7px left + 7px right = 14px per cell
# Required_width = max_content_chars * char_width + 14
```

**Pitfall:** Monospace content (Aconex codes, doc numbers) is wider at ~5.5-6px/char than proportional text. A column set to 120px for "MOC-ASEER-SIC-1K0-PL-0029" (35 chars) needs at least 35*5.5+14 ≈ 207px.

### Profile/Prequalification Page Overflow Audit Pipeline

For A4 profile documents (Samaya Factory profile, prequalification books), use this 3-stage overflow audit after ANY layout change:

1. **Claude — Audit** (checks all pages for overflow/mismatches)
   - Check every `.page` section for `height: calc()` mismatches vs print content area (170mm = 210 - 22 top - 18 bottom)
   - Flag pages where content exceeds available height
   - Check for `overflow: visible` on `.page` that would bleed content into adjacent pages
   - Report each page as PASS, MARGINAL, or FAIL with exact line numbers

2. **Kimi — Fix** (applies CSS fixes to flagged pages)
   - Fix height calc mismatches (change 174mm calcs to 170mm)
   - Remove explicit `overflow: visible` on page-level elements
   - Add `1fr` flex rows where content might overflow
   - Add explicit heights to `background-image` elements inside flex containers

3. **Codex — Verify** (checks fixes are applied and TOC is correct)
   - Verify flagged pages are properly fixed
   - Check TOC (id="p2") entries match actual page IDs and numbers
   - Check for duplicate, missing, or stale page references
   - Verify no Aseer Museum or other restricted content appears
   - Verify no device/brand names in technical sections

**Key checks every time:**
- `grep -c 'overflow: visible'` on the main CSS to catch global page bleed
- `grep -E 'height: calc\\(210mm'` on CSS — verify values match print content area
- `grep -c 'فني|Artec|Spider|EinScan'` on HTML — verify no brand names in scanning sections

### A4 Page Height Enforcement

Never let content exceed the A4 page boundary (1123px at 96dpi). Use these techniques:

- **Flex containment for image-heavy pages:** apply min-height:0 on EVERY flex child with flex:1. Without it the child ignores parent height and blows past A4 boundary.
- **Image scaling:** use height:100% with object-fit:contain not height:auto inside flex containers. height:auto respects natural aspect ratio and overflows.
- **Layout budget:** account for header ~50px, footer ~40px, section title ~60px, note blocks ~40px when sizing variable content.
- **Verify with browser:** after each layout change, open in browser and check no page has a scrollbar.

### A4 Overflow Resolution: Page Split Workflow

When a page exceeds 1123px and compacting fonts/heights isn't enough, **split the page** (don't reduce content below readability):

1. **Identify the split point** — choose a natural break (end of a section, after a major table) where the overflow content can become its own page.
2. **Close the current page** — add `</section>` after the split point and start a new `<section class="page">` with its own header.
3. **Renumber all subsequent pages** — use Python with reverse-order replacement to avoid cascading:
   ```python
   # WRONG — cascading: 05→06→07→...→23
   for old in range(5, 23):
       c = c.replace(f"PAGE {old:02d}", f"PAGE {old+1:02d}")
   
   # RIGHT — reverse order to prevent cascade
   for old in range(22, 4, -1):
       c = c.replace(f"PAGE {old:02d}", f"PAGE {old+1:02d}")
   ```
4. **Update both footer numbers AND section comment markers** — both `<!-- ============== PAGE N ... -->` and `<span class="pg-num">PAGE N / M</span>` must be incremented consistently.
5. **Update total page count** in every footer from `M` to `M+1`.
6. **Verify all pages after the split** — run `Array.from(document.querySelectorAll('.page')).map((p,i) => i + ' ov=' + (p.scrollHeight > p.offsetHeight))` — every page must show `ov=false`.

**Pitfall — Cascading renumbering:** A simple sequential `replace()` loop creates a cascade: PAGE 05 → 06, then PAGE 06 → 07 (including the one you just created), ending with all pages showing the same number. Always iterate in **reverse order** (highest page number first) or use a single-pass regex substitution.

### Always Update the TOC

Any structural change — adding, removing, reordering pages, or renaming a section — requires an immediate TOC update:

1. Update page numbers (toc-page spans) to match new footer numbers
2. Update anchor targets (href=#page-N) to match new id=page-N values
3. Update section descriptions if scope changed
4. Verify TOC item count matches the number of TOC-entry sections
5. Verify all page IDs are sequential 1..N with no gaps

**Common failure:** shifting pages by inserting or deleting without updating TOC hrefs and page numbers by the same delta. The result is an off-by-one where one entry still points to old page numbers.

## Mandatory Self-Audit Before Delivery

**HARD RULE — Never present any output (HTML, analysis, code) to the user without a self-audit pass first.** This applies to your own direct work, not just delegated labor output.

### 🔴 Pitfall: Don't Trust PDF Document Metadata for Submission Status

A PDF that says "Rev A" and "Issued to CG" on its cover page does **NOT** mean it was actually submitted through the CDE (Aconex). The PDF may have been prepared as a submittal-ready package but never formally issued.

**Always cross-reference document metadata against the project register before asserting submission status:**

| What you see on the PDF | What may be true |
|---|---|
| "Rev A · Issued to CG" | Package was prepared and quality-checked, but never uploaded to Aconex |
| "Status: Issued to Employer" | Document was formatted for submission, awaiting PM approval |
| Formal TQ/RFI number assigned | Number was reserved/allocated but the TQ was never transmitted |

**Source-of-truth hierarchy for submission status:**
1. **Project register log** (e.g. RFI_Register.xlsx) — definitive: Status column shows Draft/Open/Answered/Closed
2. **Email / Aconex notification** — confirm transmission happened (a sent-item or DS form confirmation)
3. **PDF cover metadata** — **LEAST reliable** — may reflect what was *planned* not what was *sent*

**Verification pattern:**
```python
# Before asserting "RFI was sent", check the register
register = openpyxl.load_workbook('RFI_Register.xlsx')
sheet = register['Register']
for row in sheet.iter_rows(min_row=2, max_row=20):
    if row[0].value == 'RFI-003':
        status = row[14].value  # Status column (0-indexed: col O = index 14)
        if status in ('Draft', 'Open'):
            # NOT sent — do not report as issued
```

**User correction signal:** If you find PDFs with Rev numbers and Issued stamps and report them as "sent" — and the user says "they didnt send" — you fell for metadata vs reality. The file system has both the *prepared submittal package* and the *tracking register*. Check the register first.

- **Asset path verification:** When cloning/versioning an existing HTML file (e.g. Rev C01 → C02), check ALL `src="..."` and `href="..."` paths resolve relative to the new file's location. Assets may live in a sibling folder (`01_HTML/` → `04_Assets/`), not `assets/`. Grep for `src="` and `href="` and verify each path with `ls` or `test -f`.
- **Browser preview:** Open the file in browser (via `terminal open` or `browser_navigate`) and visually confirm:
  - Images/logo load (no broken image icons)
  - Page structure renders without visible layout breaks
  - Text is readable, no overlapping elements
- **Whitespace/content check:** Scan for placeholder text, stale date references, wrong revision numbers, or copy-paste artifacts from the source file.
- **Cross-verify status claims against source files:** When a status document (.md tracker, status summary) says a document was "submitted" or has a certain CG code, verify against the actual deliverables folder — check that the corresponding PDF/excel submission package exists with a matching date. Status trackers can be aspirational or prematurely written. Evidence files (PDFs, signed response sheets) are ground truth.

- **Use project register logs for definitive status:** The project register log (.xlsb/.xlsx) tracks every document revision, received date, replied date, and disposition code (A/B/C/D). It is more authoritative than status summaries. Read .xlsb files with pyxlsb: use datetime(1899, 12, 30) as the Excel epoch, iterate rows on the "Document Submittals" sheet, and cross-reference document codes against the table being verified. The register often reveals submissions marked "Under Review" in status files that actually received Code B (Approved as Noted) weeks earlier.

- **PDF cover metadata is NOT ground truth for submission status:** A PDF with "Rev A - Issued to CG" on page 1 may be a prepared package that was never formally transmitted via Aconex. The register status column (Draft/Open/Answered/Closed) is the definitive indicator. Only Aconex transmission confirmations or signed/dated response sheets are ground truth.

## Cross-Labor Audit Protocol

| Labor | Role | QA Responsibility |
|-------|------|-------------------|
| Claude Code | Main executor | Produces output, must self-check structure |
| Kimi | Auditor | HTML validation, content accuracy, scope compliance, layout check |
| Hermes (lead) | Workflow orchestrator | Assigns tasks, verifies Kimi audit passed before delivery |

**User's preferred variant for file generation tasks**
(User explicitly corrected: "always review your work use consultant"):
- **Codex = Plan** — creates structured execution plan
- **Claude = Execute** — does the actual work  
- **KIMI = QC** — reviews/validates the output before delivery
- Use this mapping when generating construction registers, HTML deliverables,
  or any file-based output.
- If Kimi times out (long prompts), do a manual domain review yourself rather
  than shipping un-audited work.

**Audit order for multi-labor workflows:**
1. Kimi runs QA first (fast pass — catches obvious breaks)
2. Fix issues found
3. Claude Code runs second (deep pass — complex logic review)
4. Fix issues found
5. Deliver with summary of what QA caught

## Skill Authoring QA

When creating/updating skills:
- Verify all terminal commands are syntactically valid
- Test any referenced file paths exist
- Check that numbered steps are sequential
- Ensure pitfalls section reflects actual failures from this session

## Report Writing Standards for Stakeholders

When writing reports (EV snapshots, status reports, contract studies) that go to decision-makers:

### Day-Snapshot Scope
- Reports are **snapshots**, not comprehensive studies. Strip contract structure, ER requirements, resource schedules, penalty clauses, workflow maps, obligation tracking.
- Core content only: what's delivered, what's paid, earned value, variance, outstanding, next steps.

### Stakeholder Language
- Every table cell and note must answer: **"What does this mean for the decision-maker?"**
- Replace technical jargon with stakeholder value:
  - ❌ `EXTRACTED` / `PDF ONLY` / `REF ONLY`
  - ✅ `PAYMENT BASIS — ALL FIGURES VERIFIED` / `DEFINES NRS VS SAMAYA RESPONSIBILITIES`
- No status labels that only an engineer understands. Every tag must be self-explanatory.
- Column header: use `Stakeholder Value` not `Status`.

### Template Preservation (HARD RULE)
- **NEVER regenerate an HTML file.** Always use `patch()` for targeted edits.
- Preserve the original layout, CSS, color scheme, and structure exactly as-is.
- The user corrected this explicitly — regenerating breaks the approved design.

### Brevity & Tone
- Short, direct sentences. No padding, no transitional filler.
- No hedging language (`arguably`, `essentially`, `notably`, `it is worth noting`).
- Use contractions where natural (`can't`, `doesn't`, `it's`, `we're`).
- Active voice over passive where possible.
- **Use HTML `<ul><li>` lists, not prose paragraphs.** Status notes, summaries, and key points must be scannable bullet lists. Never paragraph blocks.
- Keep paragraphs under 3-4 sentences.
- Present numbers plainly without dramatic lead-ins (`CV = -218K` not `a troubling variance of`).
- No bold flourishes in summaries. Clean presentation of data only.

### Invoice Language
- `HOLD` not `REJECT` for disputed invoices. `REJECT` implies final rejection; `HOLD` leaves the door open for partial payment after review.

### Status Sections: Facts Only, No Recommendations
- Status bullet lists state **facts only** — what was delivered, what was paid, what's due.
- Move payment recommendations (pay X, hold Y) to a separate decision section or remove entirely if the decision hasn't been made.
- A status note that says "pay ~45K, HOLD ~36K" is a recommendation, not a status fact. Strip it to "due 11 Jun".

### Remove Redundant Sections
- For a day-snapshot, every section must carry unique information.
- If a section repeats what's already stated elsewhere (assessment box repeats status list, data table is granular detail nobody asked for), **remove it**.
- The question to ask: "Does this help a stakeholder make a decision right now?" If no, cut it.

### Formal Labeling for Explanatory Blocks

When adding explanatory text blocks (table footnotes, spec-strip notes, callout boxes) in formal project documents:

- **Use formal category labels**, not conversational question-style headers.
  - ✅ `Purpose:` / `Contractual Position:` / `Scope:` / `Methodology:`
  - ❌ `What this table shows:` / `What stays the same:` / `Why X shows Y:`
- **Structure as scannable 2-3 line items** with bold labels, not a single dense paragraph.
- Each labeled line should be a complete, self-contained statement the reader can absorb in one glance.
- Labels must be **nouns or noun phrases** (Purpose, Scope, Principle, Finding) — not questions or conversational prompts.
- This applies specifically to **body content** (explanatory boxes, footnotes, info strips) in documents submitted to clients, consultants, or project management. Informational labels (`What this section covers`) are acceptable in internal or technical-reference sections.

Example — correct formal style:
```
Purpose: Maps communication touch-points per role. Coordination reference, not workload allocation.
Contractual Position: SAMAYA retains full contractual responsibility. Nothing here reduces that.
SAMAYA PD Volume (78%): PD role is the primary coordination node. Higher volume ≠ greater liability.
```

### Excel Register QA — Check for Residual Icons

When generating/modifying submittal register .xlsx files:

1. **Load each xlsx** with openpyxl and check all cell values for residual Unicode symbols:
```python
import openpyxl
icon_ranges = [(0x25A0,0x25FF), (0x2700,0x27BF), (0x1F300,0x1F9FF),
               (0x2600,0x26FF), (0x23F0,0x23FF)]
wb = openpyxl.load_workbook(fp)
for sn in wb.sheetnames:
    ws = wb[sn]
    for row in ws.iter_rows():
        for cell in row:
            v = str(cell.value or '')
            for c in v:
                cp = ord(c)
                for lo, hi in icon_ranges:
                    if lo <= cp <= hi:
                        print(f'ICON {sn} R{cell.row} C{cell.column}: U+{cp:04X}')
```

2. **Check stage header cell** (A1/A2 in each sheet) — must not contain ▲ or other prefix icons

3. **Check Remarks column** — no emoji status indicators (⏳✅🟡🟢🔴⚠️)

4. **Verify .py generator scripts** match the same standard — icons in .py code produce icons in .xlsx

### No Icons or Emoji in Formal Docs
- No emoji icons (⚠️ ✅ 🔴 📋 etc.) in formal project documents.
- Keep it clean — text-only status indicators.
- Use colored tag classes (`.tag.r`, `.tag.a`, `.tag.g`) for visual status instead.
- **Comprehensive Unicode ranges to scan for** when verifying icon-free documents:

```python
icon_ranges = [
    (0x25A0, 0x25FF),   # Geometric Shapes ■□▲▼◆○ etc
    (0x2600, 0x26FF),   # Misc Symbols ☀★☎☠☹⚠ etc
    (0x2700, 0x27BF),   # Dingbats ✀✁✂✓✗✘✙✚ etc
    (0x2B00, 0x2BFF),   # Misc Symbols and Arrows ⬤⭐ etc
    (0x1F000, 0x1FFFF), # Emoji 🟠🟡🟢🔴🟣 etc (includes 1F300-1F9FF)
    (0x2300, 0x23FF),   # Misc Technical ⌂⌃⌄⌅⏳ etc
    (0x2500, 0x257F),   # Box Drawing ─│┌┐└┘
    (0x2580, 0x259F),   # Block Elements ▀▄█▌▐
    (0xFE00, 0xFE0F),   # Variation Selectors
    (0x200D, 0x200D),   # Zero Width Joiner
]
```

Real catches from Aseer Museum session: U+2500 `─` (box drawing in Landscaping comments), U+2550 `═` (double line in Master script separators), U+2588 `█` (full block in Master legend), U+23F3 `⏳` (hourglass user explicitly called out), U+2705 `✅` (checkmark in dashboard data).

### Humanization Rules
When a humanization pass is requested, apply these specific changes:
- **Transitional phrases:** eliminate "In conclusion," "Furthermore," "Moreover," "It is worth noting that," "As we can see," "Let's delve into"
- **Formulaic structures:** remove "First... Second... Finally..." cadence
- **Hedging:** strip "arguably," "essentially," "importantly," "notably"
- **Self-referential meta:** delete "This report will explore...", "The purpose of this section is to..."
- **Verbosity:** trim academic/phrasings to direct statements
- **Contractions:** use don't, isn't, it's, we're, can't where natural
- **Active voice:** prefer active over passive
- **Paragraph length:** max 3-4 sentences
- **Number presentation:** plain without dramatic lead-ins ("CV = -218K" not "a troubling variance of")

### EV Bracket Calculation
- When calculating earned value percentages, use **actual drawing/submittal counts from project registers** — not estimates or judgement calls.
- Search for registers (XLSX logs, submittal trackers, drawing lists) and count actual items.
- A bracket like "specialist review = 115K" without precise supporting data will be questioned. Back it with register-level evidence.

## Data Integrity — Never Fabricate Source Data

**HARD RULE — Do not create, generate, or synthesize data that does not come from the source files provided by the user or discovered during research.**

This includes:
- **Thumbnails/swatches/images** — If the Excel/PPTX source has no image column, do not extract images from other sources (e.g. PPTX schedule slides) and present them as if they came from the Excel schedules. The user tracks provenance carefully.
- **Hotspot/material positions** — If the user provides a PPTX with annotated callouts, use the **actual callout positions** from the file. Do not hand-craft "reasonable-looking" positions.
- **Material descriptions** — Use only the description, finish, colour, supplier fields from the actual data files (Excel JSON, etc.). Do not supplement with data from other sources unless explicitly asked.

**Verification checklist before delivery:**
1. For every data point shown to the user, ask: "Did this come from a source file the user provided, or did I infer/generate it?"
2. If inferred/generated, either strip it or flag it clearly as "estimated / placeholder — replace with source data"
3. For hotspot positions on images: verify they came from a PPTX callout extraction, not manual estimation
4. For material swatches/thumbnails: only show if the source Excel/JSON data has an image field

**User correction signal:** If the user says "don't make from your side" or "this is not in the file", you fabricated data. Immediately remove it and apologize.

## Admin Mode / Editor Pattern

When building editor/CRUD features that should be hidden from regular users:

1. **Gate with URL parameter**: `?admin=1` activates admin mode
2. **Check in component**: `window.location.search.includes('admin=1') || sessionStorage.getItem('admin')==='1'`
3. **Store as state**: `useState(()=>window.location.search.includes('admin=1'))`
4. **Conditional render**: `{adminMode && <EditorPanel/>}`
5. **No visual cues** for non-admin users — the edit button, admin link, or any editor UI must not appear in the DOM at all

This avoids accidental activation, keeps the UI clean for end-users, and requires deliberate action to access admin features.

## Hotspot Editor Design Pattern

When building interactive material hotspot editors for architectural/3D render presentations:

### Core Interactions
| Action | Implementation |
|--------|---------------|
| **Click to add** | Click on image → record x/y as percentage of image dimensions → open material picker popup |
| **Drag to move** | mousedown on pin → track delta via onMouseMove → update x/y% using `(delta / imageRect) * 100` |
| **Hover to delete** | Show × button on pin hover → confirm → remove from array |
| **Save** | Serialize hotspot array to localStorage → reload on next visit |
| **Discard** | Keep a copy of original hotspots → restore on discard |

### Material Picker
- Search by code, category, description, element, supplier
- Category filter pills (Flooring, Walls, Ceilings, Stone...)
- Scrollable list showing code (gold), category badge, description, colour
- Keyboard navigation: up/down arrows, Enter to select, Escape to close

### Data Flow
```
materials.json (defaults) → getMaterials() (merged with localStorage customs)
  ↕ (CRUD via materialStore.ts)
localStorage (custom/overridden materials)

materials → EditorOverlay (material picker uses this)
  ↕ (save via onSave)
GalleryViewer → saveHotspots() → localStorage
```

### localStorage Keys Convention
- `aseer_hotspots_{galleryId}_{viewName}` — per-view hotspot overrides
- `aseer_custom_materials` — added/edited materials
- `aseer_hidden_materials` — codes of deleted default materials

## References

- `scripts/qa_check.py` — canonical HTML QA validator. Handles `.sheet`/`.page` layouts, accounts for cover sheets when counting footers, validates asset paths, detects `read_file()` line-number contamination, and accepts spaced CSS values such as `page-break-after: always`. Accepts one or more files; exit code 0 = all clean, 1 = issues found.
- `references/html-sheet-audit-notes.md` — patterns for validating multi-sheet A4 HTML documents: sheet counting with modifier classes, CSS whitespace normalization, continuation-sheet footer checks, and project-fact/role audits.
- `references/cumulative-disposition-table.md` — pattern for tracking review comments across multiple CG submission rounds in project documents. Use when building or editing CG Comment Disposition tables (summary + detailed).
