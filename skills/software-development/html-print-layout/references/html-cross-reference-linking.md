# HTML Cross-Reference Linking

Bulk-convert all `§N.N` text references in an HTML document into clickable anchor links pointing to the correct section IDs.

## Technique

Use Python `re.sub()` with a closure that checks context before wrapping. **Must use `re.sub()` — do NOT use `str.replace()` in a loop**, which causes cascading renumbering (e.g., §12 → §12.5 gets linked first to `#s12`, then the `.5` suffix is orphaned outside the tag).

```python
import re

link_rules = [
    ('&sect;12\\.2', '#s12-2'),   # most specific first
    ('&sect;12\\.5', '#s12-5'),
    ('&sect;1\\.2',  '#s1-2'),
    ('&sect;7\\.0',  '#s7'),
    ('&sect;9',      '#s9'),
    ('&sect;13',     '#s13'),
    # ... etc
]

count = 0
for pattern, anchor in link_rules:
    def make_repl(m, anc=anchor):
        global count
        full = m.group(0)
        pos = m.start()
        # Skip if already inside an <a> tag
        before_tag = c[:pos].rfind('<a ')
        after_tag = c[:pos].rfind('</a>')
        if before_tag > after_tag:
            return full
        # Skip external document references
        before_text = c[max(0,pos-40):pos]
        if re.search(r'(ROADMAP|ER\\s|SoW\\s|Contract\\s)', before_text):
            return full
        count += 1
        return f'<a href="{anc}" style="text-decoration:none;color:inherit">{full}</a>'
    
    c = re.sub(pattern, make_repl, c)
```

## Key Rules

| Rule | Why |
|------|-----|
| **Most specific first** | `&sect;12\\.2` before `&sect;12` so `§12.2` links to `#s12-2` not `#s12` |
| **Skip already-linked** | Check no `<a ` tag opened without `</a>` closing before the match position |
| **Skip external refs** | `ROADMAP §`, `ER §`, `SoW §`, `Contract §` point to other documents, not internal anchors |
| **Inline style** | `style="text-decoration:none;color:inherit"` on the `<a>` to preserve visual appearance |
| **Use `re.sub()`, not `str.replace()`** | `str.replace()` in a loop cascades — PAGE 05→06, then 06→07, eventually all become the last number |

## Pitfall: Double-Wrapping from Successive Passes

If a first pass links `&sect;12` (matching the generic pattern before `&sect;12.5`), and a second pass tries to link `&sect;12.5` inside the already-wrapped `<a>` tag, you get:

```html
<a href="#s12">&sect;12</a>.5
```

The `.5` is orphaned outside the link. **Fix:** Run `re.sub()` in a single pass ordered from most specific to least specific pattern. The already-inside-`<a>` check (`before_tag > after_tag`) prevents re-wrapping.

### Cleanup if double-wrapping already occurred

```python
# Remove nested <a> tags
c = re.sub(r'<a href="([^"]+)"[^>]*><a href="([^"]+)"[^>]*>', r'<a href="\1">', c)
c = re.sub(r'</a></a>', '</a>', c)

# Fix orphaned suffixes like §12 + .5
c = re.sub(r'<a href="#s12"[^>]*>&sect;12</a>\.5', '<a href="#s12-5" style="text-decoration:none;color:inherit">&sect;12.5</a>', c)
```

## Anchor ID Inventory

Before linking, inventory all anchor IDs in the document:

```bash
grep -o 'id="[^"]*"' file.html | grep '^id="s' | sort -u
```

Map each to its section number. Sections without anchors get plain text.

## Verification

Count linked vs unlinked references (skipping external refs):

```python
anchored_sections = ['1.2','1.5','3.1','5.1','7.0','7.1','7.3','8','9','10','11','12','12.2','12.5','13']
linked = 0
unlinked = 0
for sec in anchored_sections:
    pattern = f'&sect;{re.escape(sec)}'
    for m in re.finditer(pattern, c):
        pos = m.start()
        before_tag = c[:pos].rfind('<a ')
        after_tag = c[:pos].rfind('</a>')
        if before_tag > after_tag:
            linked += 1
        else:
            before_text = c[max(0,pos-40):pos]
            if not re.search(r'(ROADMAP|ER\s|SoW\s|Contract\s)', before_text):
                unlinked += 1
print(f"Linked: {linked}, Unlinked: {unlinked}")
```

Run QA after linking to confirm no broken tags or double-wrapping.
