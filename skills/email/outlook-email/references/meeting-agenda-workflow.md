# Weekly Meeting Agenda from Email Open Points

When the user says "make excel agenda for meeting with [person] — add all open points":

## Source Data

Open points come from:
1. Recent inbox emails (last 3-7 days) — project submittals, CG responses, PO requests, CVs, schedules
2. Project folder emails (Asher Regional Museum, Zamzam Projects, etc.)
3. Flagged/pending items
4. CG consultant correspondence (response codes A/B/C/D)

## Grouping

Group open points by project. Standard projects for this user:

| Project | Section Label |
|---------|---------------|
| Aseer Regional Museum | ASEER MUSEUM |
| Hilton Samaya / Jabal Omar Museum | HILTON SAMAYA — JABAL OMAR |
| Al Galal & Al Jamal retail | AL GALAL & AL JAMAL |
| Zamzam Visitor Center | ZAMZAM VISITOR CENTER |
| Cross-project contracts/RFPs | CONTRACTS & PROCUREMENT |

## Excel Format

Use openpyxl with this styling:

| Element | Style |
|---------|-------|
| Title row (merged A1:G1) | Calibri 16pt bold, #0F172A, centered |
| Subtitle (A2:G2) | Calibri 10pt italic, #6B7280 |
| Header row (row 4) | Calibri 11pt bold white, fill #0F172A |
| Section headers | Calibri 12pt bold white, fill #1E40AF, merged A:G |
| Body rows | Calibri 10pt, alt fill #F8FAFC |
| Column widths | #=5, Project=20, Subject=60, From/Ref=30, Status=18, Priority=12, Action=35 |
| Critical status | Font red #DC2626 bold |
| Info/closed | Font green #059669 |
| Freeze panes | A5 |

### Columns

| # | Column | Content |
|---|--------|---------|
| A | # | Sequential per section |
| B | Project | Project name |
| C | Open Point / Subject | Clear description of the issue |
| D | From / Ref | Sender name and/or doc ref |
| E | Status | OPEN / CODE C / CODE B / FOR INFO / FLAGGED |
| F | Priority | Critical / High / Medium / Info |
| G | Action Required | What the user needs to do |

### Priority Labels

- **Critical** (#DC2626) — PO requests, task assignments, Code C rejections
- **High** (#EA580C) — Safety SORs, site protection, Code C, procurement
- **Medium** — Submittals for review, CVs, schedules, IRs, contracts
- **Info** — Code B, For Info, already approved

## Python Script Pattern

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ... build workbook with sections, items as list of tuples ...
# Save to: /Users/mohamedessa/Desktop/Meeting_Agenda_Open_Points_<date>.xlsx
```

Use `execute_code` or write `/tmp/create_agenda.py` and run via terminal. Save directly to Desktop so the user finds it immediately.