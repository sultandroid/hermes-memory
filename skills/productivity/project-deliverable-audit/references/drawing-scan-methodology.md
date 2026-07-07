# Drawing Scan Methodology

## Naming Conventions

### A-Prefix (Existing/Demolition/Sections)
Drawings in sections 1100, 1150, 1350, 1500 use `A2742-A-XXXX` naming (e.g. `A2742-A-1100.pdf`) but the register lists them as `A2742-XXXX`. Always search for both patterns:

```python
# BARE search (exact match)
result = find ... -iname "*A2742-1100*"

# A-prefix search (alternative naming)
result = find ... -iname "*A2742-A-1100*"

# Broader fallback for (1) suffix:
result = find ... -iname "*1100*"
```

### Parenthesized Suffix (Duplicate Marker)
Some files have `(1)` in the name: `A2742-A-1100 (1).pdf`. This is a OneDrive duplicate marker or version copy — NOT a revision indicator. Search by drawing number alone.

### Revision Suffix in Filenames
- `A2742-1200A.pdf` = Rev A
- `A2742-1200B.pdf` = Rev B
- `A2742-1200C.pdf` = Rev C
- `A2742-1200 2.pdf` = duplicate copy, not a revision

## Status Determination Priority

1. File in `02_Approved_Stamped_Packages/` → `stamped`
2. File in `06_Drawing_Source_Folders/` → `source_pdf`
3. DWG in `00_Stamped_CAD_Source/` → `stamped_source`
4. Only in `05_Correspondence_Archive/` → `archive_only`
5. Nowhere → `missing`

## Section Header Count Updates

When updating section header counters (e.g. `>>:58 XX:20` → `>>:78`):

Match the exact text including HTML entities.
Use `replace_all=True` when the same header appears in both summary disc-grid and tree sections.

### Counter line format
```
├── 1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>58 <span class="mk xx">[XX]</span>20
```

### Update rules
- When all [XX] become [>>], remove the XX:N suffix entirely
- When adding new drawings to a section, update the >>:N count
- Keep section totals consistent across sheets

## RIBA Tree Updates

The RIBA Stages 4-6 Deliverable Tree references drawing status in:
- Sheet 1: Summary counters and Critical Gaps section
- Sheet 2: Category A items (A01-A10)
- Sheet 2: Category B items (B01-B08)

When updating, check:
1. "162/243 stamped, 69 pending, 12 never received" → update to new counts
2. A09/A10: change from `MISSING` to `PARTIAL` if drawings found
3. B06 External Details: update sheet count if new drawings added
4. B08 Painted Finishes: update if status changes
5. Critical Gaps section: remove A09-A10 line if resolved
6. Missing count in summary (17 → 15 if A09-A10 resolved)
