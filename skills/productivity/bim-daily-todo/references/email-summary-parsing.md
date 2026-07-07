# Aseer Email Summary Markdown Parsing

## Background

When the Aseer CSV register is OneDrive-locked (persistent `Errno 11`), the `Docs/Email Archive/مشروع متحف عسير الإقليمي/` folder contains Hermes-generated markdown summary files per email category. These are **often readable** when the CSV is not, because they are smaller, simpler files that OneDrive hydrates sooner.

## File Format

All markdown files share this structure:

```markdown
# CATEGORY — Arabic Name

**Project:** Aseer Regional Museum ( ASE ) | Ministry of Culture, KSA
**Generated:** 2026-05-28 17:07 by Hermes Agent
**Total entries:** N

---

## Entries

### 1. YYYY-MM-DD — Category Name
**File:** <email-filename.md>
**Doc Code:** `<CODE>`

### 2. YYYY-MM-DD — Category Name
**File:** <email-filename.md>
**Doc Code:** `<CODE>`
```

## Extraction Function

```python
import re, json
from datetime import datetime, timedelta

def parse_aseer_markdown_summary(filepath, days_back=30):
    """
    Parse a Hermes-generated Aseer email summary markdown file.

    Args:
        filepath: path to the .md summary file
        days_back: filter entries newer than this many days

    Returns:
        list of dicts: [{date, doc_code, subject, entry_num, category}, ...]
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract category from header
    cat_match = re.match(r'# (\w+) —', content)
    category = cat_match.group(1) if cat_match else 'UNKNOWN'

    # Extract total count
    total_match = re.search(r'\*\*Total entries:\*\*\s*(\d+)', content)
    total = int(total_match.group(1)) if total_match else 0

    # Extract entries
    entries = []
    current = {}
    entry_pattern = re.compile(
        r'###\s+(\d+)\.\s+(?:(\d{4}-\d{2}-\d{2})\s+—\s+)?(.+?)\n'
        r'\*\*File:\*\*\s*(.+?)\n'
        r'\*\*Doc Code:\*\*\s*`(.+?)`'
    )
    for match in entry_pattern.finditer(content):
        entry_num = int(match.group(1))
        date_str = match.group(2)
        subject = match.group(3).strip()
        filename = match.group(4).strip()
        doc_code = match.group(5).strip()

        date = None
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                pass

        if date and date >= datetime.now() - timedelta(days=days_back):
            entries.append({
                'entry_num': entry_num,
                'date': date,
                'date_str': date_str or 'unknown',
                'subject': subject,
                'filename': filename,
                'doc_code': doc_code if doc_code != '—' else '',
                'category': category
            })

    return {'category': category, 'total': total, 'entries': entries}
```

## Priority Classification (Markdown Version)

| Category | Doc Code Pattern | Priority |
|----------|----------------|----------|
| RFP | `Artec`, `Bluehaus`, `RFQ`, `Proposal`, `Quotation` | 🔴 HIGH |
| DOC | `HSE`, `FIRE`, `Emergency`, `Safety`, `Security`, `PL-0036`, `PL-0040` | 🔴 HIGH |
| DOC | `PL-`, `ZD-`, `SC-` (general plans) | 🟡 MEDIUM |
| DOC | `PQ-` (procurement/vendor) | 🟡 MEDIUM |
| REP | any | 🟢 LOW |

Date cutoff: entries older than 14 days are still included IF they are the latest revision of an ongoing thread (e.g., Artec RFQ spans May 25 back to Jan 2026 — include only the May 25 entry).

## Worked Example (June 4, 2026)

Files read:
- `RFP - مقترحات فنية.md`: 33 entries, **11 with dates** (9 from May 25, 1 from May 20, 1 from Apr 28)
- `DOC - تقديم مستندات.md`: 54 entries, **30 with dates** (May 18-25 range)
- `REP - التقارير والخطط.md`: 29 entries, **13 with dates** (May 10-25 range)

Key entries extracted:
- Artec Space Spider RFQ (May 25, RFP) — deduplicate 6 threads into 1 item
- Bluehaus MEP Design Services proposal (May 20, RFP)
- Project Communication Plan PL-0018 Rev.01 (May 25, DOC)
- Workers Welfare Plan PL-0037 (May 21, DOC)
- HSE SC-0035 Rev.01 (May 20, DOC)
- Fire Prevention PL-0036 (May 20, DOC)
- Security Plan PL-0040 (May 23, DOC)
- CCTV ZD-0038 (May 21, DOC)
- Projector Vendor PQ-0056 Rev.01 (May 23, DOC)
- Showcases ZD-0030 Rev.01 (May 23, DOC)
- Weekly Kickoff meeting (May 25, REP)
- Daily Report (May 23, REP)

## Filename Utility

The email attachments in `Email_Archive/_attachments/` and `Email_Archive/Attachments/` contain descriptive filenames that reveal content even when the files themselves are locked:

```bash
ls -lt '.../Attachments/' | head -20
# => MOC-MUS-ASE-1K0-PL-0018-REV01 REPLY.pdf     May 25
# => SI-CG-ASEER-007 Rev.02.pdf                   May 24
# => Daily Report 23-05-2026.pdf                  May 24
# => MOC-MUS-ASE-1KH-SC-0035 Rev.01.pdf           May 24
# => MOC-MUS-ASE-1KH-PL-0040.pdf                  May 24
```

Scrape names with: `ls -lt 'path/Attachments/' | awk '/\.pdf$/ {print $NF}'`
