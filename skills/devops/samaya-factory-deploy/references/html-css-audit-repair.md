# HTML/CSS Audit & Repair on Production Documents

Systematic workflow for auditing and fixing HTML/CSS issues on deployed production documents (technical proposals, reports) hosted on samaya-factory.com.

## When To Use

- User provides a URL and asks you to "review HTML/CSS" or "fix issues"
- A production document has section numbering drift, broken page numbers, tag imbalance, or CSS issues
- The document is a multi-page A4 print-oriented HTML (typically technical proposals)

## Workflow

### 1. Source the File

Two approaches — use the one that matches the deployment pattern:

**SSH access** (preferred for large files):
```bash
# Copy from server
ssh -p 65002 u517606786@samaya-factory.com 'cat domains/samaya-factory.com/public_html/build/.../index.html' > /tmp/original.html

# Backup before modifying
ssh -p 65002 u517606786@samaya-factory.com 'cp .../index.html .../index.html.bak'
```

**curl** (for smaller files or read-only analysis):
```bash
curl -sL 'https://example.com/path' > /tmp/original.html
```

### 2. Audit Phase — What to Check

Use Python scripts to systematically check these issues:

| Check | Method |
|-------|--------|
| Tag balance | Count `<tag>` vs `</tag>` for `div`, `section`, `span`, `p`, `svg`, `table`, `tr`, `td`, `th`, `header`, `footer` |
| Section comment drift | Extract `<!-- SECTION N: -->` comments and compare to next `<h2>N.</h2>` |
| Footer page numbers | Extract all `pg-num` spans and verify sequential numbering |
| Inline style proliferation | Count `style="` attributes vs CSS classes |
| Duplicate IDs | Collect all `id="..."` and find duplicates |
| Print-specific CSS | Check `@page`, `break-after`, `page-break-inside` |
| Invalid HTML attributes | e.g. `width="auto"` on SVG, invalid entity references |
| Multiple `<style>` blocks | Count style blocks in `<head>` vs `<body>` |

**Key regex patterns:**
```python
# Tag balance
opens = len(re.findall(rf'<{tag}[\s>]', html))
closes = len(re.findall(rf'</{tag}>', html))

# Section drift
comments = re.finditer(r'<!--\s*SECTION (\d+):(.*?)-->', html)
# For each, check following h2: re.search(r'<h2[^>]*>(\d+)\.', rest)

# Footer numbers
re.findall(r'صفحة (\d+) / (\d+)', html)
```

### 3. Fix Phase — Programmatic Repair

Write a Python script that addresses all issues in one pass. Apply fixes in this order:

1. **Section comment numbering** — Match comment numbers to h2 content
2. **Missing comments** — Identify pages with no SECTION comment and add them
3. **Tag balance** — Stack-based orphaned close tag removal
4. **Style extraction** — Move inline styles to CSS classes, move `<style>` from body to head
5. **Page numbers** — Count all `.page` sections, assign absolute page numbers
6. **Structural fixes** — Add `<main>`, `<h1>`, meta description, fix invalid attributes
7. **CSS fixes** — `@page` Safari compatibility, CSS comment typos

#### Tag Balance Fix Pattern
```python
def balance_tags(html_str, tag_name):
    """Remove orphaned closing tags for a given tag."""
    pattern_open = re.compile(r'<' + re.escape(tag_name) + r'[\s>]')
    pattern_close = re.compile(r'</' + re.escape(tag_name) + r'>')
    lines = html_str.split('\n')
    open_stack = []
    lines_to_clean = {}
    for line_idx, line in enumerate(lines):
        opens = [(m.start(), m.end()) for m in pattern_open.finditer(line)]
        closes = [(m.start(), m.end()) for m in pattern_close.finditer(line)]
        for _ in opens: open_stack.append(('open', line_idx))
        for c_start, c_end in closes:
            if open_stack:
                open_stack.pop()
            else:
                lines_to_clean.setdefault(line_idx, []).append((c_start, c_end - c_start))
    for line_idx in sorted(lines_to_clean.keys(), reverse=True):
        line = lines[line_idx]
        for idx, length in sorted(lines_to_clean[line_idx], reverse=True):
            line = line[:idx] + line[idx+length:]
        lines[line_idx] = line
    return '\n'.join(lines)
```

#### Page Number Fix Pattern
```python
page_n = 0
for i, line in enumerate(lines):
    if re.search(r'<section[^>]*class="[^"]*page[^"]*"', line):
        page_n += 1
    if 'pg-num' in line and i > 50:  # skip CSS
        m = re.search(r'صفحة (\d+) / \d+', line)
        if m and int(m.group(1)) != page_n:
            lines[i] = line.replace(m.group(), f'صفحة {page_n} / 49')
```

### 4. Deploy Phase

```bash
# Upload fixed file
scp -P 65002 /tmp/fixed.html u517606786@samaya-factory.com:domains/samaya-factory.com/public_html/build/.../index.html

# Verify via HTTP
curl -sk 'https://samaya-factory.com/build/.../index.html' > /dev/null -w '%{http_code}'
```

### 5. Verification

Always verify the live page with automated checks:
- HTTP 200 status
- Tag balance on the live response
- Section comments 2, 15, 16 present
- Last footer = 49/49
- No `<style>` in `<body>`
- No duplicate IDs
- No `width="auto"` on SVG

## Converting Monolithic HTML to Page-Split Pipeline

When a monolithic HTML document (600KB+, 2800+ lines) needs to be made editable page-by-page without breaking structure:

### The Working Approach

Create a simple project with:
- `base.html` — template containing DOCTYPE, `<head>` with ALL inline CSS, and closing `</body></html>`. Contains `{{BODY}}` placeholder.
- `pages/` — one file per `<section class="page">` block
- `scripts/assemble.js` — simple concat (read files in order, join, replace `{{BODY}}`)
- `dist/index.html` — output

**Extraction method:**
```python
# 1. Find all <section class="page"> positions
page_starts = [m.start() for m in re.finditer(
    r'<section[^>]*class="[^"]*page[^"]*"[^>]*>', html)]
# 2. Find matching </section> for each
page_ends = [html.find('</section>', ps) + len('</section>') for ps in page_starts]
# 3. Split at page boundaries (not between pages)
head = html[:page_starts[0]]                    # template front
tail = html[page_ends[-1]:].strip()              # template back
# 4. Each page = html[page_starts[i]:page_ends[i]]
# 5. Inter-page SECTION comments come from gap[page_ends[i-1]:page_starts[i]]
```

### What NOT To Do (failed approaches)

| Approach | Why It Failed |
|----------|---------------|
| Placeholder system (`{{page_number}}`, `{{total_pages}}`) | When pages shift (continued pages split, gallery subsections added), numbers get out of sync. Re-rendering with correct numbers requires post-processing that breaks HTML tags. |
| Puppeteer page measurement | `file://` protocol causes unreliable page counting in headless Chrome. Falls back to static count anyway. |
| External CSS | Permissions issues on shared hosting (403 errors), caching problems, the user expects inline CSS like the original. |
| Regex post-processing that modifies HTML tags | Adding `data-page` attributes via regex replacement consumed the `>` from every `<section>` tag, producing `>>` — every page broke. |
| Auto-generated TOC | Requires page-break measurement which only Puppeteer can do, and Puppeteer is unreliable for this use case. |

### Key Rules for Stability

1. **Each `<section class="page">` is a concrete file** with a fixed position (01-cover.html, 02-document-control.html...). Page position never changes — only content within the page.
2. **Page numbers are hardcoded in footers** (`صفحة 2 / 49`). Since page position is fixed by filename, editing content doesn't shift page numbers.
3. **CSS stays inline** in `base.html` — same `<style>` block approach as the original monolithic file.
4. **The assemble script is a pure concat** — read files in order, join with `\n\n`, replace `{{BODY}}`. No rendering, no placeholders, no transformation.
5. **SECTION comments are preserved** by capturing the gap between `page_ends[i-1]` and `page_starts[i]` and prepending to each page file.
6. **The project lives in `~/Documents/`**, not `/tmp/`. The user explicitly corrected this — their project files must be in their Documents folder.

| Issue | Cause | Fix |
|-------|-------|-----|
| Section comments skip numbers | New pages added without updating comments | Match comments to h2 content |
| Footer page numbers wrong | Divider pages (PART X) added without updating footers | Count all .page sections and assign absolute numbers |
| Duplicate page number footers | Stray `<section class="page">` elements from incomplete tag closure | Balance tags first, then renumber |
| `@page` directive | "A4 portrait" syntax not supported in Safari | Use `size:210mm 297mm` |
| Cover SVG width="auto" | `<svg width="auto">` is invalid HTML | Remove `width` attribute or use numeric value |
| Duplicate id="arr" | Copy-paste of SVG elements | Rename second occurrence to "arr2" |

## Pitfalls

- Large files (600KB+) cause terminal output truncation — use `scp` or `cat` via SSH to a temp file, then read with Python `open()`
- `execute_code` tool has 50KB stdout cap — don't `print()` the full HTML; write to file instead
- When fixing tag balance, the order matters: fix orphaned closes BEFORE adding new content
- Page renumbering must happen AFTER all other structural changes (since section pages may shift)
- Verify the live page after deploy, not just the local copy
