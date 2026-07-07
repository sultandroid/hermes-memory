# HTML → Samaya-branded DOCX conversion

## When to use

When a Samaya project document exists as a styled HTML file (CV-pack style, print-ready style, or framework-v1.0 style) and the user wants a `.docx` copy in the same folder. Examples seen in Aseer Museum:

- Sustainability Strategy HTML → DOCX (23 H2 sections, 29 tables, 25 body paragraphs, 5 images)
- BEP / SMP / DMP / Communication Plan deliverables

The HTML is usually rendered for browser/PDF; the DOCX is for issue control (Aconex, formal transmittal, copy-edit in Word).

## Conversion pattern (high-level)

1. Stage HTML to `/tmp/` (avoid OneDrive file-locking).
2. Strip `<script>` and `<style>` blocks.
3. Skip the cover page — find the first `<h2>` and start there. The cover is visually noisy and not useful in DOCX.
4. Walk top-level block elements in order: `<h2>`, `<h3>`, `<h4>`, `<p>`, `<table>`, `<ul>`/`<ol>`, `<hr>`.
5. For each block, find its matching close tag, then map to SamayaDoc methods:
   - `h2` → `add_h2(num, title)` (parse "1. Document Control" → `("1", "Document Control")`)
   - `h3/h4` → `add_h3(num, title)` / `add_body(..., bold=True)`
   - `p` → `add_rich_body()` with inline `<b>`/`<i>` segments preserved
   - `table` → `add_table(headers, rows)` with `<thead>` for headers and `<tbody>` for rows
   - `ul/ol` → bullet list via repeated `add_body("•  text")`
6. Save to `/tmp/`, then copy to OneDrive via AppleScript (NOT `cp` — produces zero-byte placeholder).
7. Verify via `xxd -l 4` that the file starts with `PK` (DOCX magic bytes) — confirms a real write.

## Working script template

See `scripts/html-to-docx-converter.py` for a full working implementation. Usage:

```bash
# Stage the HTML
cp "/path/to/source.html" /tmp/source.html
# Edit the script SRC_HTML / OUT_DOCX paths, then:
python3 /path/to/scripts/html-to-docx-converter.py
# Copy to OneDrive
osascript /path/to/scripts/copy_to_onedrive.scpt
```

## Critical pitfalls

### 1. Substring slicing off-by-one

When finding a closing tag after a start tag match, `re.search` returns offsets **within the substring you searched in**, not the absolute position. This is the #1 bug in ad-hoc HTML parsers:

```python
# WRONG — end_m.start() is offset within body[m.end():], not absolute
end_m = re.search(r'</p\s*>', body[m.end():], re.IGNORECASE)
items.append(('p', start, end, body[m.end():end_m.start() if end_m else m.end()]))
# ^^^ This slices an empty string. Result: all paragraph contents vanish silently.

# RIGHT — recompute absolute position
end_m = re.search(r'</p\s*>', body[m.end():], re.IGNORECASE)
if end_m:
    content_start = m.end()
    content_end = content_start + end_m.start()   # absolute
    end = content_start + end_m.end()
items.append(('p', start, end, body[content_start:content_end]))
```

**Symptom:** `Parsed N top-level items` looks correct, but `body_para_count` is 0 and the DOCX has section headers + tables but no intro paragraphs.

### 2. H2 number regex — sub-letters get dropped

Samaya documents use sub-lettered section numbers: `3.A`, `5.A`, `14.A`, `17.A`, `17.B`. The naive regex `\d+(?:\.\w+)?` matches "3" and drops the "A":

```python
# WRONG — drops the sub-letter into the title
m2 = re.match(r'^(\d+(?:\.\w+)?)\s*[.\)]\s*(.*)$', text)
# "3.A Consultant Framework" → num="3", title="A Consultant Framework"

# RIGHT — explicitly allow letters/digits after the dot
m2 = re.match(r'^(\d+(?:\.[A-Za-z0-9]+)?)\s*[.\)]\s*(.*)$', text)
# "3.A Consultant Framework" → num="3.A", title="Consultant Framework"
```

### 3. Nested `<table>` — track depth, not just the next close

Some Samaya HTMLs embed tables inside table cells for layout. The naive `<table>...</table>` greedy match will swallow the outer table's content. Track depth:

```python
depth = 1
pos = m.end()
while depth > 0:
    next_open = re.search(r'<table\b[^>]*>', body[pos:], re.IGNORECASE)
    next_close = re.search(r'</table\s*>', body[pos:], re.IGNORECASE)
    if not next_close: break
    if next_open and next_open.start() < next_close.start():
        depth += 1
        pos += next_open.end()
    else:
        depth -= 1
        pos += next_close.end()
```

### 4. `add_table()` col_widths_cm — DON'T pass

Per the main SKILL.md, the `col_widths_cm` parameter is broken in the current template (stores EMU as 'dxa', produces giant columns). If you need specific widths, call `set_table_widths()` after creation. For HTML conversion, default equal distribution is usually fine.

### 5. Cell text extraction — collapse whitespace, decode entities

HTML cells contain `<br>`, `&nbsp;`, `&sect;`, `&middot;` etc. Strip all tags first, then decode a known set of entities. Don't try to be exhaustive — `html.unescape()` is the easiest fallback if you don't need fine control:

```python
import html
cell_text = html.unescape(re.sub(r'<[^>]+>', ' ', cell_html))
cell_text = re.sub(r'\s+', ' ', cell_text).strip()
```

### 6. Inline formatting in `<p>` — preserve bold/italic

Most Samaya HTMLs use `<b>`, `<strong>`, `<i>`, `<em>` inline within paragraphs. Don't just call `add_body(text)` — build a segments list and call `add_rich_body()`:

```python
segments = html_to_inline_segments(content)   # walk with state machine
doc.add_rich_body(segments)
```

The state machine in `scripts/html-to-docx-converter.py` handles `<br>` as hard-break, ignores wrapper `<span>`/`<div>`, and decodes common entities.

### 7. OneDrive write — AppleScript only

`cp` to a OneDrive path on macOS produces a zero-byte placeholder. Always use Finder AppleScript `duplicate` with `with replacing`. After copy, verify with `xxd -l 4` — first 2 bytes must be `PK` (DOCX) or `%PDF` (PDF). All-zeros = placeholder, redo.

```applescript
tell application "Finder"
    set srcFile to POSIX file "/tmp/output.docx" as alias
    set destFolder to POSIX file "/path/to/OneDrive/folder/" as alias
    duplicate srcFile to destFolder with replacing
end tell
```

## Document anatomy — typical Samaya HTML

| Element | Count (Sustainability Strategy) | Notes |
|---------|-------------------------------|-------|
| H1 | 1 | Title strip, usually styled with subtitle below |
| H2 | 20–25 | Numbered sections (1, 2, 3...) plus sub-letters (3.A, 5.A, 14.A, 17.A, 17.B) |
| H3 | 0–5 | Subsection breaks |
| Body `<p>` | 20–30 | Section intro paragraphs (most content lives in tables) |
| Tables | 25–35 | Includes RACI matrices (35+ rows), compliance matrices, ER cross-references |
| Images | 3–8 | Usually on the cover page; skip in DOCX |
| Total words | 5,000–10,000 | |

## Verification after save

```python
from docx import Document
d = Document("output.docx")
print(f"Paragraphs: {len(d.paragraphs)} | Tables: {len(d.tables)}")
# Expect: paragraphs ≈ H2 + H3 + body `<p>` count from HTML
# Expect: tables = count of <table> elements in HTML
# Sample first H2 to confirm title preserved
print(d.paragraphs[0].text)
```

Then visually confirm in Word: H1 navy bold, H2 with bottom border, tables with navy header row, page numbers in footer, doc ref in footer-left.
