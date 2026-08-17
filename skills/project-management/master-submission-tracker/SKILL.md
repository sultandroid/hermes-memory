---
name: master-submission-tracker
title: Master Submission Tracker — Consolidated View Across All Specialists
description: Build and maintain a consolidated submission tracker that aggregates all specialist submissions into one source of truth. Covers the markdown tracker file, auto-update script from Outlook, visual dashboard HTML, and daily cron. Designed for multi-specialist projects where individual discipline plans exist but a cross-cutting view is needed.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [submission-tracker, submittal, cg-response, outlook-sync, dashboard, project-management]
    related_skills: [discipline-submission-plan, submittal-register-management, submission-plan-validator, project-risk-register]
---

# Master Submission Tracker

## When to Use

- User has multiple discipline-specific submission plans and asks for a **consolidated view** of all submissions across all specialists
- User asks to "track all submissions" or "make a system to track submissions"
- Need a single source of truth for what was submitted, CG response codes, and pending items
- User wants a visual dashboard (bar charts) showing status per specialist
- User wants auto-updates from Outlook email scanning

## Architecture

```
02_Schedule/
  {discipline}_submission_plan.md    ← Individual plans (one per specialist)
  submission_plan_risk_assessment.md ← Master schedule with dates
  submission_tracker.md              ← CONSOLIDATED TRACKER (this pattern)

00_Status/
  submissions_visual_status.html     ← Visual dashboard (bar charts per specialist)
  submittal_dashboard.html           ← Existing submittal dashboard (if any)

scripts/
  update_submission_tracker.py       ← Auto-update from Outlook

01_Registers/
  submittal_register.md              ← Existing submittal register (if any)
```

## Step 1 — Gather Data Sources

| Source | What to extract |
|--------|----------------|
| **Outlook SQLite** | CG response emails (Hossam Mabrouk, Maged Zamzam, Abdrabo Shahin) — doc ref + code |
| **Specialist submittal registers** (Excel) | Rawasin AV register, Exhibition Fit-Out register, etc. |
| **Existing repo registers** | `submittal_register.md`, `submission_plan_risk_assessment.md` |
| **Desktop files** | `Aseer_Deliverables_Submission_Schedule_v3.xlsx` (if accessible) |

## Step 2 — Create the Tracker Markdown

File: `02_Schedule/submission_tracker.md`

### Frontmatter

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: <data sources used>
---
```

### Sections

1. **Dashboard** — summary table (total, approved, revise, rejected, pending counts)
2. **Per-specialist sections** — one `## N. Discipline` per specialist, each with a table:

   | Ref | Subject | Submitted | CG Response | Code | Notes |

3. **Overdue Alerts** — items >14 days without CG response
4. **Source Files** — table linking to source Excel files

### Status Codes

| Code | Meaning |
|------|---------|
| **B** | Approved w/ Comments |
| **C** | Revise & Resubmit |
| **D** | Disapproved/Rejected |
| **DA** | Deemed Approved (>14d CG silent) |
| **U/UR** | Under Review |
| **S** | Submitted (no response yet) |
| **P** | Pending (not submitted) |
| **Final** | Final transmittal received |

## Step 3 — Create the Auto-Update Script

File: `scripts/update_submission_tracker.py`

### Key Logic

```python
# 1. Query Outlook SQLite for CG response emails (last 30 days)
#    Path: ~/Library/Group Containers/UBF8T346G9.Office/Outlook/.../Outlook.sqlite
#    Filter: sender LIKE '%Hossam%' (or other CG reviewers)
# 2. Extract doc ref from subject (MOC-MUS-ASE-XXXX-XX-XXXX)
# 3. Detect code from preview text using regex patterns
# 4. Match doc ref against tracker markdown table rows
# 5. Update code column if different
# 6. Update last_updated in frontmatter
```

### CG Code Detection Patterns

```python
CG_PATTERNS = [
    (r'(?:Approved|Code\s*[Aa])\s*(?:with\s*Comment)', 'B'),
    (r'Code\s*[Bb]', 'B'),
    (r'Code\s*[Cc]', 'C'),
    (r'Code\s*[Dd]', 'D'),
    (r'D[- ]Rejected', 'D'),
    (r'C[- ]Revise', 'C'),
    (r'Revise\s*and\s*Resubmit', 'C'),
]
```

### Cron Setup

```bash
cronjob action=create name=update-submission-tracker \
  schedule="0 7 * * *" \
  prompt="Run the submission tracker update script..." \
  workdir=/path/to/repo
```

## Step 4 — Create the Visual Dashboard

File: `00_Status/submissions_visual_status.html`

### Data Structure

```javascript
const SECTIONS = [
  {name:"1. Architecture (NRS)", total:11, approved:6, revise:3, rejected:0, review:2, submitted:0, pending:0},
  // ... one per specialist
];
```

### Layout

1. **KPI row** — Total, Approved, Revise, Rejected, Under Review, Pending
2. **Legend** — colour-coded status dots
3. **Section cards** — one per specialist, each with 6 horizontal bars (approved/revise/rejected/review/submitted/pending)
4. **Overall donut chart** — distribution across all statuses

### Deployment

```bash
surge --domain aseer-submissions-status.surge.sh ./00_Status/
```

## Step 5 — Link from Existing Dashboard

Add a link in the existing `submittal_dashboard.html` header:

```html
<a href="https://github.com/.../submission_tracker.md" target="_blank">📋 Tracker</a>
```

## Pitfalls

- **Tracker is a SUMMARY view, not the full deliverables register.** The master tracker records gateway submissions + CG response codes. The authoritative granular source is the CG `Design_Phase_Deliverables_Tracker_*.xlsx` (one sheet per discipline, real drawing numbers `MOC-ASE-...-DDD-XXXX`, per-deliverable status). When the user supplies this xlsx, do NOT treat the tracker as complete — sync the xlsx in (mirror sheets to `02_Schedule/design_phase_deliverables_register.md` or update tracker sections with real drawing numbers/statuses). Known thin sections vs the register: **Architecture** (tracker ~12 rows vs ~318 in register), **Showcases** (~4 vs ~65 drawing numbers), **Mech** (Code-C packages like HVAC as-built / Design Base Report / duct networks often missing). AV/Electrical are usually close.
- **Dashboard KPI block can be left empty.** The summary table (Total / Approved / Revise / Rejected / DA / Pending) is often all `—` even when per-specialist tables are fully populated. Populate it by counting rows per code across all sections — it's a template bug, not a data gap.
- **Check GitHub issues before answering repo-state questions.** Per AGENTS.md Rule 10, file a `known-issue` on `sultandroid/aseer-museum-pm` BEFORE fixing a tracker bug (empty KPIs, missing deliverables). When the user asks "do we have X on repo", run `gh issue list --repo sultandroid/aseer-museum-pm --state open` first and cross-reference — the answer may already be tracked as an issue.
- **Outlook DB locked** — the SQLite file may be locked by Outlook process. Queries still work but file operations fail.
- **OneDrive EDEADLK** — Excel files on OneDrive may throw "Resource deadlock avoided". Copy to `/Volumes/MIcro/Download/` first.
- **Tracker vs individual plans** — the master tracker records actual submission status. Individual plans define what should be submitted. They serve different purposes and both should be maintained.
- **Auto-update script scope** — only detects CG responses from Hossam Mabrouk emails by default. Other CG reviewers (Maged Zamzam, Abdrabo Shahin) are not scanned. Extend the sender filter if needed.
- **Visual dashboard data is hardcoded** — the HTML embeds the data statically. Regenerate when the tracker markdown changes significantly. The script does not auto-update the HTML.
- **AV submittal registers are large** — Rawasin's register has 35+ items. These go in a sub-table under the AV section, not mixed with gateway submissions.
- **Exhibition Fit-Out register** — also has many items (FO-xxx). Same treatment: sub-table under its section.

## Step 6 — Overdue / At-Risk Status Report (per-discipline, from the CG xlsx)

When the user asks "what's overdue in <discipline>" or "I need a system to track this tracker", build a **status report script** that parses the CG `Design_Phase_Deliverables_Tracker_*.xlsx` directly and classifies every deliverable by forecast date. This is the authoritative granular source — do NOT answer overdue questions from the summary `submission_tracker.md` alone.

- Script: `scripts/design_tracker_overdue.py` (committed to `sultandroid/aseer-museum-pm`). Auto-finds the newest matching xlsx across `~/.hermes/cache/documents`, `~/Desktop`, `~/Downloads`, OneDrive, and the repo; parses all 10 discipline sheets; buckets each item as 🔴 Overdue / 🟠 At-risk (≤3d) / 🟡 Upcoming (≤7d) / ✅ Done; prints a daily-ready report.
- Cron: `design-tracker-daily-status` (job `6c19cd75b518`, daily 08:00) runs the script and relays stdout verbatim. The report is informational — the cron must NOT modify files.
- **Scoping correction (learned):** when the user says "electrical submittals" in the AD Engineering context, they mean the **Electrical sheet of the Design Phase Deliverables Tracker** (AD's own submission plan), NOT section 4 of `submission_tracker.md`. Ask/confirm which source before answering overdue questions — the two disagree on statuses and granularity.

## Related Workflows

- `references/risk-review-workflow.md` — "next risk" pattern: navigate open risks by score, search Outlook for updates, update JSON, report changes. Used when the user says "next risk" or names a risk ID during a review session.
- `references/design-tracker-xlsx-parsing.md` — pitfalls for parsing the CG Design Phase Deliverables Tracker xlsx (corrupted sheet dimensions, trailing-space sheet names, trailing-period statuses, gitignored data file).
- `references/design-tracker-overdue-monitoring.md` — sheet structure + parsing pitfalls (trailing-space sheet names, `Submitted.` done-status, corrupted Electrical sheet dimension, 0-1 prep floats) and the **email cross-reference workflow**: after generating the overdue report, query Outlook for new Aconex `SIC.-WTRAN-000NNN` transmittals to see which overdue items got cleared, then update `submittal_register.md` and commit.
