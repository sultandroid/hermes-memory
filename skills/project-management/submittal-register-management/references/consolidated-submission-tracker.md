# Consolidated Master Submission Tracker

Build a single markdown file that aggregates all specialist submissions into one place, with per-specialist sections, CG response codes, and overdue alerts. Auto-update via a Python script that scans Outlook for CG response emails.

## When to Use

- User asks for "all submissions in one place", "master tracker", "consolidated view"
- You have multiple specialists (Architecture, AV, MEP, Electrical, Structural, Lighting, Fit-Out, etc.) each with their own submissions
- CG responses arrive via email (Hossam Mabrouk) and need to be captured automatically
- The existing `submittal_register.md` is too flat or auto-generated and doesn't give per-specialist clarity

## Architecture

```
02_Schedule/submission_tracker.md     ← Master tracker (markdown, 16 sections)
scripts/update_submission_tracker.py  ← Auto-update script (scans Outlook)
00_Status/submissions_visual_status.html ← Visual dashboard (bar charts per section)
```

## Tracker File Structure

```markdown
---
last_updated: 2026-08-06
owner_agent: Hermes
status: active
source: Outlook email scan + specialist submittal registers
---

# Aseer Museum — Master Submission Tracker

> **Status codes:** A=Approved | B=Approved w/ comments | C=Revise & Resubmit | D=Disapproved | DA=Deemed Approved | U=Under Review | S=Submitted | P=Pending

## Dashboard

| Metric | Count |
|--------|:-----:|
| Total submissions tracked | — |
| Approved (Code A/B) | — |
| Revise & Resubmit (Code C) | — |
| Rejected (Code D) | — |
| Deemed Approved (DA) | — |
| Under Review / Pending | — |

## 1. Architecture (NRS)

| Ref | Subject | Submitted | CG Response | Code | Notes |
|-----|---------|-----------|-------------|------|-------|
| 1A0-1G-0001 Rev.01 | Arch DD Basement Floor — 50% Gateway | 11-Jul | 26-Jul | **B** | CG Code B |

## 2. AV / IT (Rawasin)
### 2.1 Design Gateway Submissions
### 2.2 AV Submittal Register (Rawasin)
### 2.3 AV Supplier Prequalifications

... repeat for all 16 specialists ...
```

## Data Sources to Integrate

| Source | What it provides |
|--------|-----------------|
| Outlook SQLite (Hossam Mabrouk emails) | CG response codes (B/C/D) per doc ref |
| Specialist's own submittal register (xlsx) | Full deliverable list per stage (50%/90%/100%/IFC) |
| Existing `submittal_register.md` | Historical CG responses |
| Existing per-discipline plans (`02_Schedule/*_submission_plan.md`) | Deliverable lists, dates, blockers |

## Auto-Update Script Pattern

```python
import re, sqlite3
from pathlib import Path

OUTLOOK_DB = Path.home() / "Library/Group Containers/.../Outlook.sqlite"
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
        SELECT m.Message_NormalizedSubject, m.Message_Preview,
               datetime(m.Message_TimeReceived, 'unixepoch', 'localtime')
        FROM Mail m
        WHERE m.Message_TimeReceived >= ?
          AND m.Message_SenderList LIKE '%Hossam%'
        ORDER BY m.Message_TimeReceived DESC
    """, (since_ts,))
    results = []
    for subject, preview, received in cursor.fetchall():
        doc_ref = re.search(r'(MOC-MUS-ASE-[\w-]+)', subject or '')
        code = None
        for pattern, label in CG_PATTERNS:
            if re.search(pattern, preview or '', re.IGNORECASE):
                code = label; break
        if doc_ref and code:
            results.append({'doc_ref': doc_ref.group(1), 'code': code, 'received': received})
    return results

def update_tracker(results):
    content = TRACKER.read_text()
    for r in results:
        pattern = re.escape(r['doc_ref']) + r'\s*\|.*?\|.*?\|.*?\|.*?\|'
        m = re.search(pattern, content, re.MULTILINE)
        if m:
            line = m.group(0)
            new_line = re.sub(
                r'(\|.*?\|.*?\|.*?\|.*?\|)\s*\*?\*?[A-Za-z]+\*?\*?\s*(\|)',
                rf'\1**{r["code"]}**\2', line
            )
            if new_line != line:
                content = content.replace(line, new_line)
    TRACKER.write_text(content)
```

## Cron Job

```bash
cronjob action=create \
  schedule="0 7 * * *" \
  name="update-submission-tracker" \
  prompt="Run update script, commit + push changes to GitHub" \
  workdir="/Users/mohamedessa/aseer-museum-pm"
```

## Visual Dashboard

Build a companion HTML page (`00_Status/submissions_visual_status.html`) with:
- 6 KPI cards (Total, Approved, Revise, Rejected, Under Review, Pending)
- 16 section cards, each with horizontal bar charts (pure CSS, no Chart.js needed for bars)
- Overall donut chart (Chart.js)
- Deploy to Surge.sh

See `data-dashboards` skill → `references/per-section-bar-chart-dashboard.md` for the bar chart pattern.

## Pitfalls

- **AV submittal register has 35+ items all Pending** — the Rawasin register shows everything as Pending because it's a forward plan, not a status tracker. Mark them Pending, not "Not Started".
- **CG emails may have multiple codes for the same doc ref** — a doc can go C→B (upgraded) or B→C (downgraded). The script picks the latest email by date.
- **OneDrive-locked xlsx files** — copy to `/Volumes/MIcro/Download/` first, then read with openpyxl. Do not read directly from OneDrive paths.
- **Tracker sections must be manually maintained** — the auto-update script only updates CG codes, it doesn't add/remove rows. Add new submissions manually.
- **Status code column is the 5th pipe-delimited field** — the regex `\|.*?\|.*?\|.*?\|.*?\|` captures 4 fields before the code. Verify column position matches your table layout.
- **Count statuses by parsing table rows** — use `re.finditer(r'^\|.*?\|\s*\*{0,2}([A-Za-z]+)\*{0,2}\s*\|', content, re.MULTILINE)` to extract codes from markdown tables. Filter out header rows (`| Ref |`) and separator rows (`|---|`).
