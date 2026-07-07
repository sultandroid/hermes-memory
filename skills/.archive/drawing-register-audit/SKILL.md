---
name: drawing-register-audit
description: Audit a drawing register (HTML or JSON) against filesystem files, update statuses, and cross-reference against contract scope. For Aseer Museum / Samaya BIM projects.
triggers:
  - "rescan drawings"
  - "update drawing status"
  - "audit drawing register"
  - "check NRS deliverables"
  - "drawing tree update"
  - "راجع ملفات المخططات"
  - "حدث حالة المخططات"
---

# Drawing Register Audit

Audit a project's drawing register against the actual files on disk, update the HTML status tree, and cross-reference against contract scope.

> **CRITICAL RULE: Never regenerate HTML from scratch.** Use `patch()` for targeted updates only — status markers, counters, dates, and revision numbers. User corrected this firmly. Preserve original layout/CSS/structure exactly.

## Workflow

### Phase 1: Extract register entries

Read the HTML file. Parse all drawing entries — each is a row like:
`<span class="mk XX">[&gt;&gt;]</span> A2742-XXXX Rev X Title text`

Extract: drawing_no, revision, title, current status (OK/>>/XX), status class (ok/pn/xx).

Use `python3` with regex to parse:
```python
import re
html_d = html.replace("&gt;",">").replace("&lt;","<").replace("&amp;","&")
entries = re.findall(r'<span class="mk (ok|pn|xx)">\[(OK|>>|XX)\]</span>\s+(A2742[\-A]+\d+)\s+Rev\s+([\w\-]+)\s+(.+)', html_d)
```

### Phase 2: Scan filesystem

Scan three locations for each drawing:
1. `06_Drawing_Source_Folders/` — active PDF/DWG files
2. `00_Stamped_CAD_Source/` — stamped DWG files
3. `02_Approved_Stamped_Packages/` — NRS-stamped PDFs
4. `05_Correspondence_Archive/` — old revisions / previous packages

Use `find` to build indexes. Key filename patterns:
- `A2742-XXXX.pdf` — source PDF (may have Rev suffix: `A2742-1200A.pdf`)
- `A2742-XXXX_NRS_stamped.pdf` — stamped PDF in approved packages
- `A2742-A-XXXX.pdf` — existing/demo/section drawings use "A" prefix naming
- `A2742-XXXX (1).pdf` — some files have parenthesized suffix

### Phase 3: Cross-reference

For each register entry:
1. **Stamped**: file in `02_Approved_Stamped_Packages/` → status OK
2. **Source PDF/DWG**: file in `06_Drawing_Source_Folders/` or `00_Stamped_CAD_Source/` → status >>
3. **Archive only**: file only in Correspondence Archive → status >> but note "old revision"
4. **No file anywhere**: status XX

### Phase 4: Update HTML (PATCH ONLY — never regenerate)

Use `patch()` for every change:

```python
# Status change
patch(path=html_path,
  old_string='<span class="mk xx">[XX]</span> A2742-1743',
  new_string='<span class="mk pn">[&gt;&gt;]</span> A2742-1743')

# Section header update
patch(path=html_path,
  old_string='1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>58 <span class="mk xx">[XX]</span>20',
  new_string='1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>78',
  replace_all=True)

# Summary counter
patch(path=html_path,
  old_string='class="num">167</div><div class="label">Pending',
  new_string='class="num">207</div><div class="label">Pending')
```

### Phase 5: Cross-reference against contract scope

After updating the drawing tree, check the contract responsibility matrix:
- `Contracts/NSR/Nissen SOW responsibilty matrix.pdf` — defines who creates vs reviews/approves/stamps
- Matrix has two column groups: **Samaya** (Design/Create/Shop drawing/Coordination) and **NRS** (Create/Coordination/Review/Approve/Stamp)
- NRS scope = IFC Stage 4 CAD package (interior architecture + scenography)
- Samaya scope = MEP, structure, lighting, AV, displays, graphics, etc. (NRS reviews/approves/stamps)

Extract matrix with PyMuPDF:
```python
import fitz
doc = fitz.open(path)
page = doc[0]
blocks = page.get_text("blocks")
for b in blocks:
    x, y = b[0], b[1]
    text = b[4].strip()
    print(f"({x:.0f},{y:.0f}) {text}")
```

### Phase 6: Present in workflow terms

Do NOT just report file counts. Present:
- What NRS must CREATE — has it been delivered?
- What NRS must REVIEW/APPROVE/STAMP — has that happened?
- What drawings exist only as old revisions?
- What items in NRS scope have no corresponding drawings?
- Workflow bottleneck (stamping, review turnaround, missing items)

## Pitfalls

- ⚠️ **Never regenerate the HTML.** User will correct you ("why you change the design/workflow"). Always use patch().
- ⚠️ **Naming variants**: drawings may use `A2742-XXXX` in register but `A2742-A-XXXX` or `A2742-XXXX (1)` on disk. Search with find + wildcards.
- ⚠️ **OneDrive stubs**: check actual file size with `ls -la` — 0-byte files are not real.
- ⚠️ **Old revisions**: files in `05_Correspondence_Archive/` count as delivered but may be outdated. Note this separately.
- ⚠️ **Section headers appear in 2 places** (summary disc-grid + tree section headers). Use `replace_all=True` or handle both.
- ⚠️ **Counter line is one long line** — use exact substring match, not multi-line.

## Reference

See `references/aseer-register-structure.md` for Aseer Museum register sections and file locations.
