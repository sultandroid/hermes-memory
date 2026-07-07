# Reference-Driven Section Redesign (4-Agent Workflow)

Use when redesigning a profile section based on a third-party reference document (PDF, guide, standards doc).

## Workflow

### Phase 1 — Extract & Summarize (Kimi role)

Read the source document (PDF or other) and produce a 2-page bilingual (AR/EN) structured summary covering:
- Services / capabilities offered
- Technical specifications (materials, colors, dimensions)
- Process / methodology
- Quality standards
- Company info (if relevant)

**Output file**: `Guide/<GuideName>_Summary.md` — lives permanently as project reference.

**Extraction tools**:
- `pdftotext` for PDF text extraction
- Python for cleanup and structuring
- Format: bilingual tables + section headers

### Phase 2 — Build the Prompt (Codex role)

Based on the summary + current section HTML, write a comprehensive Claude prompt:
- Current section ID and line range
- Desired 2-page layout structure (what goes on each page)
- Key content points from the summary to include
- **Critical instruction**: Frame ALL content as Samaya's own capability — never copy third-party branding

### Phase 3 — Execute Redesign (Claude role)

Claude patches:
- `index.html` — replaces old section content with new 2-page spread
- Appropriate per-archetype CSS file — adds new component styles

**Mandatory Claude instructions**:
- "Do NOT create SVG placeholder images"
- "Use ONLY existing photos from assets/img/"
- "Verify each photo path exists on disk before writing"
- "Fabrication, assembly, and process photos: use existing workshop/machine images from assets/"
- "Preserve cover slogan: هندسة الفنّ. لصناعة الإرث. / Engineering Art. For Crafting Legacy."

### Phase 4 — Review (Kimi role)

**Critical checks**:

1. **No third-party branding leaked** — grep for the source document's company name, URLs, or trademarks in the modified section
2. **All photo paths resolve to existing files** — run the phantom path detection script. Claude invents non-existent paths like:
   - `06-qa-lab/` (should be `05-qa-lab/`)
   - `projects/material-samples/*.jpg` (doesn't exist at that path)
   - `real-quality-check.jpg`, `patina-work.jpg` (never were Samaya photos)
3. **Bilingual format** — Arabic primary, English secondary throughout
4. **TOC entries** — new sub-pages (p15b etc.) must have TOC entries; adjacent pages' entries preserved
5. **Footer numbers** — follow sibling pattern (p15 → "15", p15b → "15b")
6. **CSS height constraints undamaged** — `grep -c '210mm' v6/css/*.css` count unchanged

### Phantom Photo Path Detection Script

Run this AFTER any Claude content redesign:

```python
import re, os
BASE = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile"
with open(f"{BASE}/v6/index.html") as f: html = f.read()
paths = set()
for m in re.findall(r"url\\('([^']+)'\\)", html):
    paths.add(m)
missing = [p for p in paths if not os.path.exists(os.path.join(BASE, p)) and not p.startswith('data:')]
if missing:
    print(f"BROKEN PATHS ({len(missing)}):")
    for m in missing: print(f"  {m}")
```

For each broken path, search `assets/img/` for the actual file or replace with a different existing photo.

## Example: Wayfinding Page Redesign (v6.9)

- Source: `Vision_SignageWayfinding.pdf` (39 pages, Vision Branding)
- Summary: `Guide/Vision_SignageWayfinding_Summary.md` (198 lines, 2-page bilingual)
- Result: p15 → 2-page spread (p15 methodology + p15b sign types + specs)
- Issues caught: 9 phantom image paths, all fixed before deploy

## Output Files

- `Guide/<GuideName>_Summary.md` — permanent reference
- `index.html` — patched sections
- `css/<archetype>.css` — new component styles
