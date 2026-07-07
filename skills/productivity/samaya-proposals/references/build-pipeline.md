# A4 Build Pipeline — Section Partial Architecture

For proposals over 500KB or 40+ pages where a monolithic HTML file becomes unmanageable.

## Folder Layout

```
project-root/
├── manifest.json          ← section registry
├── template.html          ← HTML5 skeleton with {{body}}
├── package.json           ← npm build:validate
├── styles/
│   └── a4.css             ← shared A4 print CSS
├── sections/
│   ├── cover.html         ← <section class="page page-cover">...</section>
│   ├── document-control.html
│   ├── av-led.html
│   ├── av-led-g1.html …   ← gallery subsections (children)
│   ├── part2-divider.html ← <section class="page page-divider">...</section>
│   └── ... (49+ partials)
├── scripts/
│   ├── build.js           ← render + post-process numbering
│   └── validate.js        ← 36 automated checks
└── dist/
    └── index.html         ← final assembled output
```

## Placeholder System

Each partial uses `{{placeholder}}` syntax for build-time substitution:

| Placeholder | Source | Example |
|------------|--------|---------|
| `{{section_number}}` | manifest → auto-assigned | `2` |
| `{{page_number}}` | build (post-process scan) | `5` |
| `{{total_pages}}` | build (count of .page elements) | `51` |
| `{{title_ar}}` | manifest | `ورقة ضبط الوثيقة` |
| `{{title_en}}` | manifest | `Document Control` |
| `{{short_title_ar}}` | manifest | `ضبط الوثيقة` |
| `{{chip_text}}` | hardcoded per section | `ضبط · CONTROL` |
| `{{doc_code}}` | manifest | `SMP-RCRC-TP-AR-001` |
| `{{rev}}` | manifest | `01` |
| `{{date}}` | manifest | `June 2026` |
| `{{toc_placeholder}}` | replaced in post-process | TOC table or static text |

## Build Process (2-pass)

**Pass 1 — Render:** Read manifest, read each partial, replace manifest-provided placeholders (`{{section_number}}`, `{{title_ar}}`, `{{chip_text}}`, etc.). Keep `{{page_number}}` and `{{total_pages}}` as literal placeholders.

**Pass 2 — Post-process numbering:**

```js
// 1. Count all .page sections (matches page, page-cover, page-divider)
const pageRegex = /<section[^>]*class="[^"]*page[^"]*"[^>]*>/g;
const actualPages = (finalHtml.match(pageRegex) || []).length;

// 2. Replace total_pages
finalHtml = finalHtml.replace(/\{\{total_pages\}\}/g, String(actualPages));

// 3. Add data-page attribute for positional tracking
let pageIdx = 0;
finalHtml = finalHtml.replace(pageRegex, (match) => {
  pageIdx++;
  const classMatch = match.match(/class="([^"]*)"/);
  return `<section class="${classMatch[1]}" data-page="${pageIdx}">`;
});

// 4. Line-by-line: replace {{page_number}} with current data-page value
const lines = finalHtml.split('\n');
let currentPage = 0;
for (let i = 0; i < lines.length; i++) {
  if (/data-page="(\d+)"/.test(lines[i])) {
    currentPage = parseInt(lines[i].match(/data-page="(\d+)"/)[1]);
  }
  if (/\{\{page_number\}\}/.test(lines[i])) {
    lines[i] = lines[i].replace(/\{\{page_number\}\}/g, String(currentPage));
  }
}
finalHtml = lines.join('\n');

// 5. Clean up data-page attributes
finalHtml = finalHtml.replace(/ data-page="\d+"/g, '');
```

## Section Numbering Rules

| Type | Page Number | Section Number |
|------|-------------|----------------|
| cover | 1 | (empty) |
| divider | (increment) | (empty) |
| content | increment | increment + 1 (offset for cover) |
| content (continued) | increment | same as previous |
| child subsection | increment | `parent.N` (e.g. `17.1`) |

## Critical Pitfalls

### The `>>` Bug
The section-tag regex MUST consume the closing `>` of the tag. The regex `/<section[^>]*class="[^"]*page[^"]*"/g` matches only up to the closing `"` of the class attribute, leaving `>` unconsumed. When the replacement adds its own `>`, the result is `>>` at the end of every section tag, breaking all page rendering.

**Fix:** Use `/<section[^>]*class="[^"]*page[^"]*"[^>]*>/g` — note the trailing `[^>]*>`.

### Preserving Original Class Values
When injecting `data-page`, extract the original class attribute and preserve it:
```js
const classMatch = match.match(/class="([^"]*)"/);
return `<section class="${classMatch[1]}" data-page="${pageIdx}">`;
```
Do NOT hardcode `class="page"` — this would lose `page-cover` and `page-divider` classes.

### Continued Pages in Manifest
When a section spans 2+ pages (same topic, split for A4 fit), mark the manifest entry with `"continued": true`. The second `<section class="page">` inside the same partial will get the same section number but an incremented page number.

### Multi-Section Partials
If a partial has multiple `<section class="page">` elements (from `<!-- PAGE BREAK -->` markers), the line-by-line scan handles this automatically — each section open increments the page counter, and the next `{{page_number}}` gets the new value.

## Validation Checks (36 total)

1. **File integrity:** exists, <800KB
2. **HTML structure:** DOCTYPE, lang="ar", charset, viewport, description, Google Fonts, CSS link, <main>
3. **Semantic HTML:** at least one `<h1>`, `<h2>`, `<header>`, `<footer>`, `<section>`
4. **CSS:** @page size: A4 (not A4 portrait), 210×297mm, page-break-after, box-sizing, print-color-adjust, -webkit-print-color-adjust, CSS variables
5. **Known issues:** no SVG width="auto", no @page size: A4 portrait
6. **Placeholders:** zero unfilled {{tokens}}
7. **Page structure:** section count == close count, footers present
8. **Page numbering:** footers found, last page = total, no duplicates, sequential
