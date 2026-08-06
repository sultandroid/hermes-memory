# Master Submission Tracker — Consolidating All Specialists

## When to Use

The user asks to "track all submissions", "collect all submissions", "make a system to track submissions", or you have multiple specialist submittal registers and need a single source of truth with CG response codes, overdue alerts, and auto-update from Outlook.

## What to Build

| Artifact | Location | Purpose |
|----------|----------|---------|
| `submission_tracker.md` | `02_Schedule/` | Master tracker — 16+ specialist sections, CG codes, overdue alerts |
| `scripts/update_submission_tracker.py` | `scripts/` | Auto-update script — scans Outlook for CG responses, updates tracker |
| Cron job | Daily 07:00 | Runs script, commits + pushes changes |

## Data Sources to Collect

| Source | What to Extract |
|--------|---------------|
| **Outlook emails** (Hossam Mabrouk CG responses) | Doc ref, code (A/B/C/D), date, sender — scan last 30 days |
| **Specialist submittal registers** (OneDrive / Micro volume) | Deliverable lists, ref codes, stage columns (50%/90%/100%/IFC) |
| **Existing repo registers** (`01_Registers/submittal_register.md`) | Already-tracked submissions with CG codes |
| **Existing discipline plans** (`02_Schedule/*_submission_plan.md`) | Per-discipline deliverable registers, blockers, procurement status |
| **Master submission plan** (`02_Schedule/submission_plan_risk_assessment.md`) | Dates, parallel groups, dependencies |

## Tracker Structure — 16 Specialist Sections

1. **Architecture (NRS)** — DD Gateway submissions, Viz boards
2. **AV / IT (Rawasin)** — Design Gateway + Submittal Register (AV-xxx) + Supplier PQs
3. **MEP (AD Engineering)** — Design Basis, Assessment reports, Submittal Plans
4. **Electrical (TABCOMM / AD Engineering)** — Assessment reports (ZD-xxx), Submission Plans
5. **Structural** — DD Gateway, CVs, Assessment
6. **Lighting (Studio ZNA)** — Design Report, Philosophy, Layouts
7. **Exhibition Fit-Out** — FO-xxx deliverables (50%/90%/100%/IFC)
8. **Showcases (Glasbau Hahn)** — Presentation, Shop Drawings
9. **Graphics (Graphit)** — SoW, Schedule (client-blocked)
10. **Acoustic** — PQs (STUMIX, ACOUSTIEG, AME, JOCAVI, TransOrient)
11. **Setwork Suppliers** — PQs (Anaroque, Tannah, Saudi Emaar, BTT)
12. **Landscaping** — PQs (Evergreen, PINE), Concept/Design
13. **HSE Plans** — PL-xxx submittals (Security, Welfare, Fire, etc.)
14. **Integration / Management Plans** — DMP, BEP, RMP, PEP, etc.
15. **Prequalifications (cross-discipline)** — All PQ-xxx items
16. **IFC Packages** — IFC-0003 through IFC-0008

Plus: **Overdue Alerts** section (>14 days without CG response), **Source Files** table, **Dashboard** summary row.

## Auto-Update Script Pattern

```python
# scripts/update_submission_tracker.py
import re, sqlite3
from pathlib import Path
from datetime import datetime

OUTLOOK_DB = Path.home() / "Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
TRACKER = Path("02_Schedule/submission_tracker.md")

# CG response patterns in email previews
CG_PATTERNS = [
    (r'(?:Approved|Code\s*[Aa])\s*(?:with\s*Comment)', 'B'),
    (r'Code\s*[Bb]', 'B'),
    (r'Code\s*[Cc]', 'C'),
    (r'Code\s*[Dd]', 'D'),
    (r'D[- ]Rejected', 'D'),
    (r'C[- ]Revise', 'C'),
    (r'Revise\s*and\s*Resubmit', 'C'),
]

def scan_outlook(since_days=30):
    conn = sqlite3.connect(str(OUTLOOK_DB))
    cursor = conn.cursor()
    since_ts = int(datetime.now().timestamp()) - since_days * 86400
    cursor.execute("""
        SELECT m.Record_RecordID, m.Message_NormalizedSubject,
               m.Message_Preview, m.Message_SenderList,
               datetime(m.Message_TimeReceived, 'unixepoch', 'localtime')
        FROM Mail m
        WHERE m.Message_TimeReceived >= ?
          AND m.Message_SenderList LIKE '%Hossam%'
        ORDER BY m.Message_TimeReceived DESC
    """, (since_ts,))
    results = []
    for row in cursor.fetchall():
        sid, subject, preview, sender, received = row
        if not subject: continue
        m = re.search(r'(MOC-MUS-ASE-[\w-]+)', subject)
        if not m: continue
        doc_ref = m.group(1)
        code = None
        for pattern, label in CG_PATTERNS:
            if re.search(pattern, preview or '', re.IGNORECASE):
                code = label; break
        if doc_ref and code:
            results.append({'doc_ref': doc_ref, 'code': code,
                            'subject': subject.strip(), 'received': received})
    conn.close()
    return results

def update_tracker(results):
    content = TRACKER.read_text()
    for r in results:
        doc_ref, code = r['doc_ref'], r['code']
        pattern = re.escape(doc_ref) + r'\s*\|.*?\|.*?\|.*?\|.*?\|'
        m = re.search(pattern, content, re.MULTILINE)
        if m:
            line = m.group(0)
            parts = line.split('|')
            if len(parts) >= 6:
                current = parts[4].strip()
                if current != f'**{code}**' and current != code:
                    new_line = re.sub(
                        r'(\|.*?\|.*?\|.*?\|.*?\|)\s*\*?\*?[A-Za-z]+\*?\*?\s*(\|)',
                        rf'\1**{code}**\2', line)
                    content = content.replace(line, new_line)
    # Update frontmatter date
    today = datetime.now().strftime('%Y-%m-%d')
    content = re.sub(r'last_updated: \d{4}-\d{2}-\d{2}',
                     f'last_updated: {today}', content)
    TRACKER.write_text(content)
```

## Cron Job Setup

```bash
hermes cron create \
  --name "update-submission-tracker" \
  --schedule "0 7 * * *" \
  --workdir /path/to/repo \
  --prompt "Run the submission tracker update script: cd /path/to/repo && python3 scripts/update_submission_tracker.py. If there are changes, commit and push to GitHub with message 'auto: update submission tracker from CG emails'."
```

## Dashboard Link

Add a link from `submittal_dashboard.html` header to the tracker on GitHub:

```html
<a href="https://github.com/{owner}/{repo}/blob/main/02_Schedule/submission_tracker.md"
   target="_blank" style="color:var(--gold-light);font-size:12px;text-decoration:none;font-weight:500;">
   📋 Tracker
</a>
```

## Pitfalls

- **Outlook DB locked** — the SQLite file may be locked by Outlook process. Queries still work but file operations fail.
- **CG sends multiple codes for same doc** — some docs get Code C first, then upgraded to B later. Track the latest code by date.
- **Specialist registers use different formats** — AV register uses AV-xxx refs, Exhibition uses FO-xxx. Keep them in separate sections.
- **OneDrive files may be locked** — copy to Micro volume first before reading.
- **Doc ref matching** — the regex `MOC-MUS-ASE-[\w-]+` captures the full doc ref. Some subjects have leading spaces or special chars — strip them.
- **Tracker rows must have the doc ref in column 1** — the update script matches by doc ref in the first column of each row.
- **Frontmatter date** — always update `last_updated` after changes so the dashboard shows fresh data.
