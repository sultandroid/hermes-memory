# Print-layout HTML Document — Page Extraction

When a document is one assembled HTML where page numbers are rendered by JS (`data-page-current`/`data-page-total`), raw HTML grep won't find page numbers. Use section headings as proxies.

## Pattern

```python
import re, requests

html = requests.get(url).text

# Find all <section class="page"> start positions
sections = list(re.finditer(r'<section\s+class="page[^"]*"[^>]*>', html))

for i, m in enumerate(sections):
    start = m.start()
    end = sections[i+1].start() if i + 1 < len(sections) else len(html)
    content = html[start:end]

    # Get heading to identify which page this is
    h = re.search(r'<h[12][^>]*>(.*?)</h[12]>', content, re.DOTALL)
    heading = re.sub(r'<[^>]+>', '', h.group(1)).strip()[:100] if h else '(no heading)'

    # Match by heading text pattern when you need a specific page
    if '34.' in heading or 'Assumptions, Exclusions' in heading:
        text = re.sub(r'<[^>]+>', '\n', content)
        text = re.sub(r'\n{3,}', '\n\n', text)
        print(text.strip())
        break

    # Fallback: count pages by order (section 0 = cover, section 1 = page 2, etc.)
    # Page N = section[N-1] (since section 0 is usually the cover)
```

## When to Use

- Document is one assembled `.html` with `<section class="page">` per page
- Page numbers are injected by JS (not in raw HTML)
- Need to find a specific page by section number or heading text
- The heading text contains the section number (e.g. "34. الافتراضات والاستثناءات")

## Pitfalls

- Cover page (section 0) has no heading or page number — skip manually
- RTL/Arabic headings extract correctly via regex but may show garbled in terminal — trust the pattern match, not the terminal display
- Some sections may be divider pages (dark banners) with no heading — these still count as pages for numbering purposes
- The first `<section>` found may be preceded by a `<style>` block — use `sections` (the regex match list), not `html.split()`
