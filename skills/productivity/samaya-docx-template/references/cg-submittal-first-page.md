# CG Submittal — First Page Layout & Conventions

## First Page Order

For CG-submittal documents, the first page must contain in order:

1. **Cover metadata table** (Document Reference, Contract, Employer, etc.)
2. **DC block** — QC table with Prepared by / Reviewed by / Approved by (actual names, not role titles)
3. **Revision history table** (Version, Date, Author, Changes)
4. Then the document body (TOC → sections)

Insert spacing between these tables (~6pt empty paragraph) for visual separation.

## DC Block Template

4-column table: empty | Prepared by | Reviewed by | Approved by
- Header row: navy fill `#1E293B`, white bold 9.5pt text
- 3 signature rows with "Name:" fields
- All cells: cantSplit, compact margins (28dxa top/bottom, 56dxa left/right)
- Alternating row shading (`#F1F5F9` / white)

## Revision History Entry Format

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Samaya Technical Office | Initial release |
| C01 | ... | ... | ... |
| REV00 | ... | Samaya Technical Office | REV00 - First issue for CG review |

REV00 entry must be client-appropriate — no internal formatting details. Use:
- ✅ "REV00 - First issue for CG review"
- ❌ "Format revision — unified table styles, halftone remarks, page breaks, removed internal references"

## TOC via Word Field

Replace static TOC text with a Word TOC field for auto-generated page numbers and hyperlinks:

```python
# Insert after "TABLE OF CONTENTS" heading
# Build as XML elements:
# fldChar begin → instrText "TOC \\o \"1-2\" \\h \\z \\u" → fldChar separate → placeholder text → fldChar end
```

After insertion, user must right-click the TOC in Word → Update Field → "Update entire table" to generate page numbers.

## Severity Scale — Project-Aligned Schedule Thresholds

When defining schedule impact thresholds, align them to the project's remaining duration:

| Rating | Schedule Impact (10-month project) |
|--------|-----------------------------------|
| Low | Less than 1 week |
| Medium | 1 - 2 weeks |
| High | 2 - 4 weeks |
| Very High | More than 4 weeks |

## Live Register Notes

Any table showing live register data must carry a halftone (9pt gray `#64748B`) note immediately after:

> *"Data shown is a snapshot from the live Project Risk Register, which is the authoritative source and updated weekly."*

Tables that need this: Current Risk Snapshot, Current Risk Distribution, Register Status Summary.

## Header Format

- Left: Samaya logo (1.0 inch wide)
- Right: "Aseer Regional Museum — Risk Management Plan" (8pt, `#64748B` Calibri)
- No doc ref, no revision number in header

## Footer Format

`Page X of Y` (Word PAGE/NUMPAGES fields) + `Samaya Investment Company`
