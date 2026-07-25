# CR Sheet Rules — Icons, Symbols, and Style

## No emoji, no AI symbols

CR sheets (xlsx) are formal project documents. They must NOT contain:
- Emoji/icons: ✅ ❌ ⚠️ 🔴 🟡 🟢 — use text labels: [done], [missing], [caution], High/Medium/Low
- Arrows: → ← ↑ ↓ ↔ — use words: "to", "from", "up", "down"
- Typographic marks: § · – — • — use Section, -, or just spaces

## openpyxl cleanup before save

When writing CR sheets with openpyxl, always run a cleanup pass on ALL string cell values before saving:

```python
import openpyxl

replace_map = {
    '\u2705': '[done]',
    '\u274c': '[missing]',
    '\u26a0': '[caution]',
    '\u2014': ' - ',
    '\u2013': ' - ',
    '\u2192': ' to ',
    '\u2190': ' from ',
}

for row in ws.iter_rows():
    for cell in row:
        if cell.value and isinstance(cell.value, str):
            for old, new in replace_map.items():
                if old in cell.value:
                    cell.value = cell.value.replace(old, new)
```

## Perform a full document review, not just CR items

When a subcontractor/specialist returns a deliverable with a CR sheet showing items as closed:

1. Check each CR item is actually closed (open the DOCX/PDF, verify the content changed)
2. Then do a SECOND PASS: review the entire document independently — look for:
   - Style issues (wrong font, wrong company name, "the Contractor" vs "Samaya")
   - Structural problems (duplicate appendices, section numbering conflicts)
   - Missing content (BIM LOD, code edition, cross-references to other plans)
   - Inconsistencies (CR says "added" but document doesn't show it)

The user will catch what you missed. A CR-only review is not enough — you must read the actual deliverable.

## Adding review columns to CR sheets

When adding a new column with review comments:

1. Add the column header with navy fill (#1E293B), white bold font
2. Use red (#B01E2F) 9pt italic font for comments
3. Prefix closed items with [done], in-progress with [in progress], rejected with [push-back]
4. Be specific — include section numbers and file paths where applicable
5. Add general notes at the bottom numbered 1..N

## Document reference verification

When a subcontractor uses their own document numbering (e.g., "AMA/SMP-01" instead of the project's MOC-MUS-ASE- prefix), flag it. The project standard is:
- Prefix: MOC-MUS-ASE-{Discipline}-{TYPE}-{####}
- This is non-negotiable for CG submissions
