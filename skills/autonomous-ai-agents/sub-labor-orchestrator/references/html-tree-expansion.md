# HTML Deliverable Tree Expansion Pattern

Expanding a flat category into sub-deliverables (e.g., C01-C15 → 159 items with C01.01-C15.08 sub-items) requires a structured approach.

## The Pattern

1. **Define sub-items in Python** as a dict of tuples `(ref, name, note, desc, rag)`
2. **Generate HTML rows** using the same tree-connector conventions (`├──` / `└──` + `│   &ensp;` indentation)
3. **Insert into the HTML** by finding the category boundaries (e.g., `<!-- CATEGORY C -->` to `<!-- CATEGORY D -->`)
4. **Update all counters** — not just the category header, but every count in the document

## Python Code Pattern

```python
# Define parent metadata
parent_info = {"C01": {"name": "Showcase / Display Case Design", "rag": "b"}}

# Define sub-items per parent
c_subs = {"C01": [
    ("C01.01", "Design Brief &amp; Performance Spec", "description in parens", "Status text", "b"),
    # ...
]}

# Generate rows
rag_map = {"g": "OK", "a": "PARTIAL", "b": "PENDING", "r": "MISSING", "f": "FUTURE"}
all_rows = []
for c_ref, pi in parent_info.items():
    items = c_subs[c_ref]
    # Parent row with ├──
    tree_p = f"├── {c_ref} {pi['name']}<br>│   &ensp;(summary)"
    all_rows.append(f'<tr><td class="ref">{c_ref}</td><td class="tree">{tree_p}</td><td class="desc">N sub-deliverables</td><td class="stat"><span class="rag {pr}">{rag_map[pr]}</span></td></tr>')
    # Sub-items with │   ├──/└──
    for i, (sub_ref, name, note, desc, rag) in enumerate(items):
        is_last = (i == len(items) - 1)
        tree_sub = f"│   &ensp;{'└──' if is_last else '├──'} {sub_ref} {name}<br>│   &ensp;{'    &ensp;' if is_last else '│   &ensp;'}({note})"
        all_rows.append(f'<tr><td class="ref">{sub_ref}</td><td class="tree">{tree_sub}</td><td class="desc">{desc}</td><td class="stat"><span class="rag {rag}">{rag_map[rag]}</span></td></tr>')
```

## File Insertion

```python
# Read file
with open(path, "r") as f: content = f.read()

# Find section boundaries
c_start = content.find('<!-- ===== CATEGORY C ===== -->')
c_end = content.find('<!-- ===== CATEGORY D ===== -->')

# Replace rows between header and next category
header_snippet = content[c_start:c_start+500]
header_line_end = header_snippet.find('</td></tr>')
header_end = c_start + header_line_end + len('</td></tr>')

new_content = content[:header_end] + "\n" + expanded_html + "\n" + content[c_end:]

# Write
with open(path, "w") as f: f.write(new_content)
```

## Counter Updates (after expansion)

The expansion changes Stage 4 / Cat C totals. All document locations must be updated:
1. **Cat C header** (in the tree table)
2. **Sheet 1 summary counters**
3. **"About this Document" section**  
4. **Dashboard overall summary** — percentages + bar widths
5. **Stage 4 summary box** — item count + percentages + bar
6. **Category table** (Sheet 6) — C row + TOTAL row
7. **RAG legend** total count
8. **Stage 4 tree header** (e.g., "211 items")
9. **Cat C row description text** (e.g., "Expanded to 159 items")

Recalculate percentages: `count / new_total * 100`, round to nearest integer. Verify bar widths sum to 100%.

## Known Pitfalls

- **Escaped ampersands** — Use `&amp;` not `&` in HTML attributes and text content
- **Tree connector order** — Last sub-item uses `└──` and `    &ensp;`, all others use `├──` and `│   &ensp;`
- **Counter drift** — Every time item counts change, ALL counters in the document must be updated, not just the affected section
- **read_file contamination** — Do NOT use `read_file()` output (has line-number prefixes) as raw content for replacement. Use `open()` directly.
- **Patch tool limits** — For large sections (>100KB), Python string replacement is more reliable than `patch` tool's fuzzy matching
- **Category C is Stage 4** — Expanding Cat C only affects Stage 4 totals, not Stage 5 or Stage 6
