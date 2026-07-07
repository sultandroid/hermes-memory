# Email Archive Search for Scope/Pricing Info

When searching for scope-of-work detail across Samaya BIM unit project folders, much of the information lives in archived email threads—not formal contract docs. This reference covers how to find and interpret them.

## Archive Location

Each project under `Bim Unit/<Project>/` has an `Email_Archive/` directory. There is also a global `_Unsorted_Emails/Email_Archive/` for uncategorised messages.

## File Format

Emails are stored as `.md` files with YAML frontmatter:

```markdown
# Subject line
- **Date:** ...
- **From:** ...
- **Archived:** ...
- **RecordID:** NNNNN
- **Attachments:** Yes (see Attachments folder)
---
Email body text...
```

## Key Signals to Search For

| Signal | What It Usually Means |
|--------|-----------------------|
| طلب تسعير (pricing request) | Scope definition per zone/floor — lists areas to quote |
| طلب عرض سعر (quotation request) | Similar to above, with expected breakdown |
| أمر شغل (work order) | Formal scope assignment for specific work package |
| طلب اصدار امر تشغيل (issue work order request) | Pre-work-order request with attached plans |
| مطلوب تسعيير (pricing required) | Scope items listed explicitly per zone |
| مستخلص رقم N (payment certificate #N) | Completed scope items — can reveal what was actually built |

## Detection: Corrupted vs Usable Files

Many archived emails are **zeroed-out** — the archiver captured YAML frontmatter but the body was not preserved. Two quick checks:

```bash
# Check file size — usable files are >400 bytes
stat -f%z filename.md

# Check if body exists (look for content after the --- separator)
grep -c "^[a-z]" filename.md  # non-zero = has body text
```

Files <300 bytes are almost always frontmatter-only (corrupted).
Files >400 bytes often have readable body content.

## Searching Technique

### By Subject Line (Fastest)
Email subjects are in the filename. List all that contain a keyword:

```bash
ls Email_Archive/ | grep -i "قران\|Quran\|تسعير\|scope\|عرض سعر"
```

### By Body Content
Search inside .md files that have body text:

```bash
# Search email bodies for floor/zone references
grep -rl "الدور الأول\|first floor\|قاعة\|مقهى\|مكتبة" Email_Archive/*.md 2>/dev/null
```

### By RecordID Chain
Emails in a thread share subject references. Find one, then search for its RecordID or subject prefix in other files:

```bash
grep -l "1311-Al Quran\|22047\|طلب تسعير" *_*.md
```

## Project Code References

| Code | Meaning |
|------|---------|
| 1311- | Mimar Interiors (MEK) project reference for Al Quran Exhibition |
| 22047- | Design Development drawing set for Al Quran Exhibition (MEK) |
| P00444 | Change order / variation for structural & MEP drawing modifications (Jabal Al-Noor) |

## Common Pitfalls

1. **Attachments not archived** — Most meaningful scope detail was in attached PDF/DWG/Excel files, not the email body. The archiver captures "Yes (see Attachments folder)" but those files may be missing or in a separate Attachments directory.
2. **Multiple naming conventions** — The same project may be called "متحف القران", "معرض القران الكريم", "Al Quran Exhibition", or "مبنى التفويج - جبل النور" in different emails. Search all variants.
3. **Corrupted >300 byte files** — Some files show size >300 but contain only null bytes (zeroed). Always `cat` a sample to verify content before relying on search results.
