# HTML-to-Content Extraction for DOCX Generation

## When to use

When the source content for a DOCX is a large HTML file (50KB+) stored on a **private network path** (OneDrive, local filesystem) that `web_extract` cannot read because it blocks private/internal network addresses.

## The problem

`web_extract(urls=["file:///path/to/file.html"])` returns:
```
Blocked: URL targets a private or internal network address
```

This happens for all `file://` URLs and any OneDrive/network share path. The browser tool also cannot navigate to `file://` URLs.

## Solution: html2text via terminal

```bash
# Install if needed
pip install html2text -q

# Extract to text file
python3 -c "
import html2text
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.body_width = 0  # no line wrapping
with open('/path/to/source.html', 'r') as f:
    html = f.read()
text = h.handle(html)
with open('/tmp/extracted_text.txt', 'w') as f:
    f.write(text)
print(f'Extracted {len(text)} chars')
"
```

### Key html2text settings

| Setting | Value | Why |
|---------|-------|-----|
| `body_width` | `0` | Prevents line wrapping at 80 chars — keeps table rows intact |
| `ignore_links` | `False` | Preserves URLs for reference documents |
| `ignore_images` | `False` | Preserves image alt text and paths |

### Alternative: direct file size check first

Before extracting, check the file size to decide if you need pagination:

```bash
wc -c "/path/to/source.html"
```

Files > 100KB will produce a large text output. Read it in chunks (200 lines at a time) via `read_file` with `offset` and `limit`.

## SMP merge workflow (RevC05 → repo SMP → DOCX)

When merging operational content from a consultant's HTML strategy document (e.g., RevC05 Sustainability Strategy) into a project plan (SMP markdown), then generating a formal DOCX:

### Step 1: Extract HTML content

Use html2text as above. The RevC05 HTML was 202KB → 1476 lines of extracted text.

### Step 2: Read both sources

- Read the existing repo SMP (markdown) in full
- Read the extracted HTML text in 200-300 line chunks
- Identify which sections from the HTML are NEW (not in the repo SMP) vs. UPDATES to existing sections

### Step 3: Identify new sections to merge

Typical new sections from a RevC05-style sustainability strategy that may not exist in a baseline SMP:

| New Section | Content |
|-------------|---------|
| Code Library with Edition Verification | Table of codes held/verified, edition status, DRM notes |
| Specialist Scope of Work | Engagement model, deliverables by stage, authority interface |
| Existing MEP Baseline | Current vs. upgrade target for chillers, pumps, AHUs, BMS, lighting |
| Procurement Specification per Material Category | 15+ material categories with thresholds, evidence, designer cert |
| Subcontractor Obligations Matrix | 10 subs + Samaya-wide + ITCA with credits and evidence |
| RACI Matrix | 8 Mostadam categories × 8 parties |
| BIM LOD 4 Sustainability Audit | 8-item checklist + 5 LOD 4 review items |
| Programme Sustainability Milestones | Day-based gates + reporting cadence |

### Step 4: Fix contradictions per ER/SoW only

When the HTML strategy document (RevC05) contains targets that differ from the contract (ER/SoW), the **contract wins**. Common contradictions in sustainability documents:

| Parameter | RevC05 (wrong) | ER/SoW (correct) | Fix |
|-----------|---------------|-------------------|-----|
| Waste diversion | ≥ 75% | ≥ 60% (SBC 1001 §8) | Change to 60% |
| Oddy aging period | 49-day (28d test + 21d age) | 14-day at 60°C (SoW §1.5, ER §2.4D) | Change to 14-day |

**Rule:** The RevC05 HTML is a *proposed* strategy document. The ER and SoW are the *contractual* requirements. Always prefer the contract values. Document the fix in the `conflict_resolution` YAML frontmatter and the revision log.

### Step 5: Write the updated SMP markdown

- Preserve the repo's YAML frontmatter (add conflict_resolution entries)
- Bump revision number
- Add new sections between existing ones using numbered gaps (e.g., §3.A after §3, §4.A after §4)
- Keep the repo's code-compliance framing (not points-chasing)
- Update the Table of Contents

### Step 6: Generate Samaya-branded DOCX

Use the `samaya-docx-template` skill's SamayaDoc class. Write a Python script that:

1. Imports `SamayaDoc` from the style guide path
2. Creates header with project name, doc ref, type, revision, date
3. Creates footer with doc number
4. Builds a cover page (spacers, title, project info table)
5. Adds each section using `add_h2()`, `add_h3()`, `add_body()`, `add_table()`
6. Saves to `/tmp/` then copies to OneDrive

**Key patterns for the gen script:**

- Cover page: use a 2-column table for project info (navy label + white value cells)
- Tables: use `col_widths_cm` parameter — sum to ~16.5cm for A4 portrait
- Bullet lists: use `add_body("- item text")` — there is no `add_bullet()` method
- Document control: add a revision history table at the end
- Closing statement: italic, medium gray, 10pt

### Step 7: Copy to OneDrive

```bash
cp /tmp/output.docx "/path/to/OneDrive/target/folder/"
```

## Pitfalls

- **html2text may not be installed** — always include `pip install html2text -q` in the command or use a try/except
- **Large HTML files** — the extracted text can be 80K+ chars. Read in chunks (200 lines at a time) via `read_file(offset=N, limit=200)`
- **RevC05 waste/aging values may be wrong** — the consultant's strategy document may propose targets that exceed contractual requirements. Always verify against ER/SoW before merging
- **DOCX generation script can be 500+ lines** — write it to a temp file first, then execute. Keep the script for reuse
- **SamayaDoc logo path** is hardcoded to OneDrive CloudStorage path. If running via terminal (TCC sandbox), the logo won't load — the fallback `[SAMAYA]` text appears instead. This is expected and acceptable
