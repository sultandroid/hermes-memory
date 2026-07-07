# HTML-to-Word Content Sync

## When to use

A Word document (`.docx`) is the authoritative source, but an HTML render of the same document has drifted out of sync — different wording, extra content, wrong role names, stale cross-references, mismatched definitions. You need to align the HTML to the Word source without breaking the HTML markup, SVGs, or layout.

## Preconditions

- Both files exist and are known to be the same revision (same Rev code)
- Word file is `.docx` (not `.doc`)

## Pipeline

### Step 1: Extract Word text

Use zipfile + XML parsing (no `python-docx` required — the docx is a ZIP):

```python
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile("path/to/doc.docx") as z:
    xml_content = z.read("word/document.xml")

root = ET.fromstring(xml_content)
ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
paragraphs = root.findall(".//w:p", ns)

text_content = []
for p in paragraphs:
    texts = []
    for t in p.findall(".//w:t", ns):
        if t.text:
            texts.append(t.text)
    text_content.append("".join(texts))
```

This gives you every paragraph in order. Non-empty lines are the document body.

### Step 2: Read the HTML

Read the full HTML file. For files over 40KB, use `terminal` with `cat` or read section-by-section with `read_file` (offset/limit).

### Step 3: Compare section-by-section

Don't do a naive diff. Align on document structure:

| Section to check | Common drift patterns |
|-----------------|----------------------|
| **Introduction / Purpose** (Sec 2) | HTML editors expand introductory text, add explanatory detail not in Word |
| **Definitions** (Sec 2.3) | HTML adds extra descriptors ("Active throughout design phase", "Friday excluded", "causing schedule delay") |
| **Org chart / Role tables** (Sec 3) | Role names change (PM ↔ CM), Tier composition differs, HTML invents placeholder roles |
| **Milestone owners** (Sec 4) | Role substitutions in owner column (PM vs CM, PD vs PM) |
| **Role allocation tables** (Sec 5) | Row labels diverge, section cross-references change (Sec 8.3 vs 8.4) |
| **Location matrix** (Sec 6) | Role names differ, location notes expanded |
| **Induction steps** (Sec 7.1) | Step owners changed, content added (extra training items, mention of specific procedures) |
| **Sub-contractor tables** (Sec 7.3) | Extra descriptors in discipline column ("Cat A conservation"), integration mechanism details |
| **KPI wording** (Sec 8.2) | KPI names trimmed/expanded, source references diverge |

### Step 4: Apply corrections to HTML

Use targeted find-and-replace. The HTML has structured markup so each text string is usually unique within its context.

**Best practices:**
- Include enough surrounding HTML context to guarantee uniqueness (include `<td>`, `<tr>`, class names)
- For role renames (PM → CM), check if the HTML also has cards/divs with the old role name
- After bulk replacement, verify with grep that no stale references remain
- Check both **content** and **cross-references** (section numbers, document codes)

**Verification checklist:**
```bash
# Check removed items are gone
for term in "old text" "other old text"; do
  if grep -q "$term" file.html; then echo "STILL PRESENT: $term"; fi
done
# Check required items are present
for term in "new text" "other new text"; do
  if grep -q "$term" file.html; then echo "PRESENT: $term"; else echo "MISSING: $term"; fi
done
```

### Step 5: Final visual check

Open the HTML in a browser (via `browser_navigate`) and verify:
- No broken page layout from changed text lengths
- SVGs and tables render correctly
- Changed content reads naturally in context

## Pitfalls

- **Multiple matches**: A simple `<tr><td>Role Name</td>` pattern may match twice in the HTML (once in the role allocation table, once elsewhere). Always check count before replacing.
- **Unicode vs HTML entities**: `&amp;` vs `&`, `\u2014` vs `&mdash;`, `\u00b7` vs `&middot;`. Use the exact encoding present in the file.
- **Section cross-references**: When a section number shifts (e.g., 8.3 → 8.4), both the heading and any inline references to that section need updating. Check all occurrences.
- **HTML inserts not in Word**: The HTML may have self-contained additions (new roles, extra sub-contractors, expanded notes) that don't correspond to anything in the Word source. Remove them unless user confirms otherwise.
- **Word vs HTML has different lead text**: The Word may be concise, the HTML expanded. Align to the authoritative source (usually Word).
- **Visual-only content**: SVGs, phase strips, headcount curves — these are HTML-only and have no Word equivalent. Don't touch them.
