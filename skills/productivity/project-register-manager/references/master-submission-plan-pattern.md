# Master Submission Plan Pattern

Generated from: Aseer Museum session, June 29, 2026
Location: `04_Registers/_scripts/Master_Submission_Plan.py`
Output: `04_Registers/Master Submission Plan/Master_Submission_Plan.xlsx`

## Structure (3 Sheets)

### Sheet 1: Master Plan
All packages ordered by submission date. Columns:
- Package name
- 50% / 1st Submission date
- 90% date
- 100% date
- IFC/AFC date
- Depends On (dependency chain text)
- Group (0-5 parallel track)
- Review Buffer (e.g., "7d after prior")
- Notes

**Formatting:**
- Date group headers (blue bars) between different submission dates
- Blue-shaded rows = parallel submissions (same date, no dependency)
- Freeze panes at header row

### Sheet 2: Dependency Network
What-blocks-what table with lag time. Columns:
- If THIS is delayed...
- ...it blocks (list of packages)
- Lag (time to impact)
- Parallel group
- Critical? (highlighted in pink for critical path)

### Sheet 3: Parallel Tracks
Chronological view by group (0-5). Columns:
- Date
- Track 0 — Foundation
- Track 1 — Structural-feed
- Track 2 — Arch-feed
- Track 3 — Late (needs Arch 90%)
- Track 4 — Client-dep
- Track 5 — IFC

## TRACKS Data Structure

```python
TRACKS = [
    ('Package Name', ['50%', '90%', '100%', 'IFC'],
     'Depends On Text', group_number, 'Notes'),
]
```

- group_number: 0-5 integer controlling parallel track
- Dates with 'TBC' are sorted last
- '—' means not applicable at that stage
- 7-day review buffer: `ad(date, 30+REVIEW)` where REVIEW=7

## Key Constants

```python
REVIEW = 7  # days for review buffer between dependent stages
def ad(d, n):
    return (datetime.strptime(d, '%d/%m/%Y') + timedelta(days=n)).strftime('%d/%m/%Y')
```

## Icon/Emoji Policy

The Master Plan script generates sheet names and headers with plain text. Verify no Unicode icons or emoji appear anywhere in the output before delivery.
