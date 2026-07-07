# HTML Proposal Page Separation — Clean Rebuild Pattern

## Problem
After repeated structural edits (removing duplicate Part 01/Part 02, expanding sections, renumbering pages), sections become mixed on shared pages. Patching individual section boundaries keeps breaking adjacent sections because the file structure is too damaged for targeted fixes.

## Signal
User says "pages broken from page 5", "section 15 floating in section 14", "fix page and break next page", "why alot of white pages". Targeted `<section>` wrap/unwrap patches fail repeatedly.

## Solution: Selective Strip-and-Rebuild (PREFERRED)

The blanket `re.sub` approach (page break before every h2) creates white pages for subsections, continuation headers, and part dividers. Use the SELECTIVE approach instead.

**CRITICAL SEQUENCE — must follow this exact order or operations cascade:**

1. Strip ALL section tags (remove every `<section class="page">` and `</section>`)
2. Rewrap the cover page (find first h2, wrap everything before it)
3. Add page breaks before qualifying h2s (main sections only, NOT continuations/part dividers)
4. Fix part dividers: add footers so they don't appear as blank white pages
5. Balance: remove orphan `</section>` tags until opens == closes

### Part Divider Blank Page Fix

Part dividers (الجزء الثاني, الثالث, الرابع, الخامس) appear as blank/white pages because their standalone `<section class="page">` contains only an h2 with no footer. The browser renders a blank-looking page with just one line of text.

**Fix:** Each part divider section needs a footer:

```python
# After step 4 above, add footers to part divider pages
for part_name in ['الجزء الثاني', 'الجزء الثالث', 'الجزء الرابع', 'الجزء الخامس']:
    # Find the section containing ONLY this part divider h2
    pattern = rf'(<section class="page">\s*<header.*?</header>\s*<h2>{part_name}.*?</h2>\s*)(</section>)'
    def add_footer(m):
        return m.group(1) + f'\n  <footer class="pg-footer"><span class="dc">SMP-RCRC-TP-AR-001 · Rev 01</span><span class="ctx">{part_name}</span><span class="pg-num">صفحة XX / 47</span></footer>\n' + m.group(2)
    h = re.sub(pattern, add_footer, h, count=1)
```

**Pitfall:** If the regex matches more than the intended section (e.g., `re.sub` with `count=1` still matches adjacent sections), the part divider's `</section>` gets duplicated and section balance breaks. Always verify `opens == closes` after this step.

### Continuation Detection Patterns

These h2 patterns should NOT start new pages:

```python
skip_patterns = [
    r'<h2>\s*الجزء\s',    # Part dividers (الجزء الثاني, الثالث, etc.)
    r'تابع',              # Continuation header (9. تابع)
    r'\(2/2\)',           # Page 2 of 2
    r'17\.1\.', r'17\.2\.', r'17\.3\.', r'17\.4\.',  # Subsection galleries
    r'17\.5\.', r'17\.6\.', r'17\.7\.', r'17\.8\.',
]
```

**Pitfall — `الجزء` substring false match**: The regex `r'<h2>الجزء'` matches any h2 containing those letters, including words like "الجزء" appearing in normal section titles. Use `r'<h2>\s*الجزء\s'` (with whitespace boundary) to match only the actual part divider headers. Test by checking which h2s get skipped before applying.

### After the Rebuild — What Remains Broken

The selective rebuild fixes section/page separation but does NOT fix:
- Page NUMBERING (all footer `صفحة X / Y` are reset — need separate renumber pass)
- H2 title overflow (some titles still too long for A4 — need CSS `word-wrap: break-word`)
- Duplicate page headers (if backup had them before strip, they persist in content)
- Chart placement (charts stay where they were in the original content)
- TOC page references (TOC becomes stale — regenerate after final numbering)

**Verification checklist after rebuild:**
1. `opens == closes` (section balance)
2. Part dividers have footers (not blank pages)
3. Continuations stay on parent page (not white pages)
4. H2 count matches original
