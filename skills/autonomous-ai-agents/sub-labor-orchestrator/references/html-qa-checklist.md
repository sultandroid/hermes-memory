# HTML Deliverable QA Checklist — Codex CLI Audit Reference

## Who This Is For
This is the **Codex CLI** quality checklist. Proven in 2026-05-29 training session against a ~77KB HTML deliverable tree. When Codex receives an HTML deliverable from Claude Code for QA audit, he checks every item below.

## Structural Integrity (10 Standard Checks)

| # | Check | Verification | Python snippet |
|---|-------|-------------|----------------|
| 1 | **DOCTYPE** | `<!DOCTYPE html>` present on line 1 | `c.startswith('<!DOCTYPE html>')` |
| 2 | **Tag balance** | Count `]'`, `'</div>'` — diff must be 0. Use regex `<div[>\s]` to catch both `<div>` and `<div class=...>` | `len(re.findall(r'<div[>\s]', c)) == c.count('</div>')` |
| 3 | **No line-number corruption** | First line must NOT start with spaces+digits+pipe | `bool(re.match(r'^\s*\d+\|', c.split('\\n')[0]))` → must be False |
| 4 | **Closing tags** | `</body>` and `</html>` must exist and be the last non-empty lines | `c.strip().endswith('</html>')` |
| 5 | **CSS @page** | Must set `size:A4 portrait; margin:0` | `'size:A4' in c and 'margin:0' in c` |
| 6 | **Sheet sizing** | `.sheet{width:210mm;min-height:297mm;overflow:hidden;page-break-after:always}` | Check each property present |
| 7 | **Logo paths** | Must use `../Docs/09_Registers/...` relative path. ALL 4 logos must resolve as existing files. | For each `src=...`, verify `Path(...).exists()` |
| 8 | **Font loading** | Calibri + Carlito from Google Fonts | `'fonts.googleapis.com' in c` |
| 9 | **Div balance per sheet** | Each `.sheet` div block should have balanced open/close count | Extract between sheet divs and count |
| 10 | **Content overflow risk** | `overflow:hidden` clips content taller than 297mm. For dense tables, consider explicit `height:297mm` or removing `overflow:hidden` | Visual check or Chrome headless render |

## Extended Checks (from real QA session)

### Entity encoding
```python
# Bare & in text content should be &amp;
import re
bare = re.findall(r'&(?!amp;|lt;|gt;|quot;|#39;|#[0-9]+;|#x[0-9a-fA-F]+;)', c)
if bare:
    print(f"Bare & found: {bare}")
```

### Trailing blank page
`sheet:last-of-type{page-break-after:auto}` prevents extra blank page after last sheet. Consider adding `break-after:page` alongside legacy `page-break-after:always`.

### Font portability
If the HTML must work offline, Carlito from Google Fonts won't load. Either:
- Embed fonts as `@font-face` with local files
- Or remove the remote dependency and use Calibri-only (which ships with macOS/Windows)

### Logo path fragility
Current path `../Docs/09_Registers/...` works from `Completed Tender Package From NRS/` folder. If the HTML is moved, logos break. For self-contained deliverables, copy logos to `_assets/logos/` alongside the HTML or use data URIs.

### Summary totals vs actual counts
Always verify:
```python
actual_items = len(re.findall(r'<td class="ref">[A-Z][0-9]+</td>', c))
dashboard_total = int(re.search(r'<b>TOTAL</b>.*?<b>(\d+)</b>', c, re.DOTALL).group(1))
assert actual_items == dashboard_total, f"Tree has {actual_items} items, dashboard says {dashboard_total}"
```

## Fixes for Common Issues

### Line-number corruption (most common bug)
Caused by piping `read_file()` output (which has line prefixes like `" 123|<div..."`) into `write_file()`.

```bash
python3 -c "import re; c=open('file.html').read(); c=re.sub(r'^\s*\d+\|', '', c, flags=re.MULTILINE); open('file.html','w').write(c)"
```

**Prevention:** NEVER pipe `read_file()` output to `write_file()`. Use `terminal cat` or `subprocess.run(['cat', path])` to get raw file content.

### Div mismatch
Most common cause: extra `<div>` without matching `</div>`, or missing `</div></body></html>` at file end.

```python
open_divs = len(re.findall(r'<div[>\s]', c))
close_divs = c.count('</div>')
print(f"open={open_divs} close={close_divs} diff={open_divs - close_divs}")
```

### Broken @page margins
Wrong: `@page { margin: 15mm 18mm }` alongside `.sheet { padding: 14mm 18mm }` — double margin causes content to be pushed off-page.
Correct: `@page { size: A4 portrait; margin: 0 }` with `.sheet { padding: 14mm 18mm }`. The padding IS the margin.

### Wrong logo paths
From `Completed Tender Package From NRS/` root, paths must go UP to Aseer-Museum root:
```html
../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/moc.png
../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/pmc_ace.png
../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/cg.png
../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/samaya.png
```
