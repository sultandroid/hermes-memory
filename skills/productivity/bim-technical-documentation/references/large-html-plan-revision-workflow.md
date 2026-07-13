# Large HTML Plan Revision Workflow

When creating a new revision of a multi-page HTML plan document (SMP, DMP, BEP, Resource Plan, etc.) — typically 20+ pages, 2000+ lines, 250KB+.

## 1. Read the Source File

The 40K character limit on `read_file` means a 2500-line HTML file cannot be read in one call. Strategy:

```bash
# First, count lines
wc -l file.html
# 2456 lines, 286KB
```

Read in **200-line chunks** (this keeps each chunk well under 40K chars):

```python
read_file(path="...", offset=1, limit=200)
read_file(path="...", offset=201, limit=200)
# ... continue until offset+limit > total_lines
```

**Pitfall:** Some chunks may still exceed 40K if they contain dense table rows or SVG content. If a 200-line chunk fails, try 100-line chunks for that range.

## 2. Create the New Revision File

Copy the source to the target location first, then apply patches:

```bash
cp "source/Rev03_file.html" "target/Rev04_file.html"
```

**Output location:** `03_Plans/<category>/` — not `99_Archive/`. The Archive holds the previous revision; the active Plans directory gets the new one.

## 3. Apply Patches — Order Matters

Apply patches in this order to minimize conflicts:

### Phase 1: Global Replacements (use `replace_all=true`)
- Title tag: `Rev 03` → `Rev 04`
- All page headers: `SMP Rev 03` → `SMP Rev 04`
- All footers: `Rev 03` → `Rev 04`
- Date stamps: `2026-05-11` → `2026-07-03`

### Phase 2: Cover Page
- Revision number and description
- Date
- Cover description text (strip internal doc references per CG rules)

### Phase 3: TOC Page
- Snapshot card values (role counts, page counts)
- Section descriptions (e.g., "55 roles" → "61 roles")
- Compliance notice box

### Phase 4: Revision History (Section 1.1)
- Add new row for the new revision
- Keep descriptions brief — list changes, not internal rationale

### Phase 5: CG Comment Disposition (Section 1.4)
- Update disposition chip (e.g., "R1+R2" → "R1+R2+R3 CLOSED")
- Update section banner description
- Add new Round 3 cat-row + individual rows in the **same table** (never split rounds across separate tables)

### Phase 6: Content Sections (Sections 2-15)
- Update counts (role totals, interface counts, KPI counts)
- Add new stakeholders to registers (T1, T2, T3 tables)
- Add new interfaces to interface matrix
- Add new KPIs to monitoring table
- Add new governance notes (Value Map, Software Governance, etc.)

### Phase 7: Communication Plan
- Add new reports/meetings if applicable
- Update report counts in headers

### Phase 8: Final Verification
- All `PAGE XX / YY` footers sequential and total YY correct
- HTML comments (`<!-- PAGE XX · ... -->`) match actual page numbers
- TOC page references match new page numbers
- No orphaned section references
- All disposition chips updated

## 4. Patch Strategy for Large HTML

### Use `replace_all=true` for:
- Common patterns that appear identically in every page footer/header
- Document reference numbers
- Revision labels in disposition chips

### Use single `replace` for:
- Unique content blocks (tables, register entries, interface rows)
- Section-specific headers and banners
- Cover page text

### Handling Table Row Additions
When adding rows to an existing table (e.g., new stakeholders in T2 register):

1. Find the **last row** of the existing table section
2. Use that row + the closing `</tbody>` as the `old_string`
3. Insert new rows between the last row and `</tbody>`

Example:
```
old_string: "<tr>...last existing row...</tr>\n    </tbody>"
new_string: "<tr>...last existing row...</tr>\n      <tr>...new row...</tr>\n    </tbody>"
```

### Handling Page Number Updates
After adding content that pushes a page boundary, update ALL footers:

```bash
# Check current page count
grep -c 'PAGE' file.html
# Should match the /YY total in each footer
```

Use `replace_all=true` for the `/ 23` → `/ 24` update, but verify no unintended matches (e.g., a table cell containing "23").

## 5. Common Pitfalls

- **Nested `<section>` tags** — When patching page content, verify the replacement doesn't create nested `<section class="page">`. The old content already opens a `<section>`, and if your replacement also starts with `<section>`, you get invalid nesting.
- **TBC status suffix creep** — After adding new TBC stakeholders, verify no status commentary (`— pending`, `⚠ CRITICAL`) was appended. TBC = just TBC.
- **Page overflow** — Adding 3+ new table rows can push content past A4 height. Check with `grep -n '<section class="page"'` to count pages, then compare content density.
- **Replace-all on common numbers** — `replace_all=True` on `/ 23` can hit unintended targets (table cells, SVG text). Verify after.
- **OneDrive lock** — Never use `write_file` to overwrite a OneDrive-stored HTML file. Use `patch` only. If you already overwrote, recover with `ditto`.
