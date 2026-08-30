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

## Multi-Authority Approval / Stamp Chains (e.g. Fire Alarm → Civil Defence + NRS)

Some submissions cannot go to the consultant until **multiple external authorities** approve + stamp first. On Aseer the pattern is the **Fire Alarm**: CG verbally approved (walls OK without calculation), but the **Civil Defence** opened a long amendment loop; after Civil Defence the package still needs **NRS** (National Research / design lead) stamp → consultant submission. ~3 days are consumed just collecting 3 stamps when run sequentially.

**Reusable coordination lessons (learned 2026-08-30):**

- **Triage the authority relationship BEFORE promising dates.** Civil Defence here treats the contractor as a *co-consultant*, not as the *owner/client* they'd normally be supportive of — so their review loops behave like another consultant's (expect revisions, not goodwill sign-off). Note which authorities behave which way so you don't promise "easy approval."
- **Acceleration = staggered parallel dispatch, not sequential.** Each authority reviews on a *different timeline*. Instead of waiting for A→B→C, dispatch the package to each authority as soon as *their portion* is stable (e.g. send Civil Defence the protection-strategy scope that won't change, send NRS the final layouts) so review windows overlap and the ~3-day stamp lag collapses. Applies to ANY multi-approver deliverable, not just Fire Alarm.
- A **verbal** "done/approved" from one authority is NOT an approval to submit — the remaining stamps still gate it.

## Per-Specialist Follow-up Tracker (user preference: "خليه فالريبو")

When the user gives you a **verbal status dump** of a discipline's submissions ("متابعة التقديمات / حالة الكهرباء — هذا اتقدم، هذا متأخر...") they want it **recorded in the repo**, not kept in chat or memory. Convention (established 2026-08-30, AD Engineering):

- File: `02_Schedule/{Specialist}/{Specialist}_{Discipline}_Tracker.md` — alongside the specialist's existing `README.md` / submission plan. Aseer example: `02_Schedule/AD_Engineering/AD_Engineering_Electrical_ICT_Tracker.md`.
- Structure: frontmatter (`last_updated`, `owner_agent: Hermes`, `status`, `source: <date> <channel> status call`), a **status legend** (✅ submitted / ⏳ in progress / ⚠️ delayed / 🔄 rework / 🤝 awaiting third-party), then a **one-row-per-package table**: `# | Package | Status | Detail / Next Step` capturing "who holds it + what the next action is" for each row.
- Mark **pressure points** (e.g. a submission stuck as Code C that keeps being pushed to the end of the tracker) and any **external dependency** (Civil Defence, NRS stamp, SBS site visit) so the blocker is explicit.
- Commit with a date-stamped message, per the user's always-include-the-date rule. Update the file incrementally as the user reports new status in follow-up turns (patch same file, commit again).
- This is a **live coordination log** — distinct from the CG `Design Phase Deliverables Tracker` (authoritative granular status) and the consolidated `submission_tracker.md` (gateway summary). Keep all three; they answer different questions.

## Capturing a subcontractor's EXCUSE LIST for the pressure meeting (2026-08-30, AD Engineering)

When a specialist repeatedly misses dates and offers blockers, add a **"Counter-arguments refuted"** section to their `{Specialist}_Tracker.md` (a dedicated `## {Specialist} Counter-arguments refuted — all excuses, nothing blocking` block). During the recovery call you debunk each stated blocker with the file evidence, then the section is your ammunition for the pressure meeting. Reusable refutation patterns that keep recurring with AD-type design consultants:

- **"Blocked waiting on X"** → check whether X was already delivered. Aseer case: AD claimed MC/CCTV was blocked on **power** — but power had **already been submitted**. Contradictory self-blocking = the strongest single debunk in the meeting.
- **"Need more info before I can draw"** → the **"work from the tender" directive**: the contractor (PM) instructs them to design from the contract/tender rather than stall for missing data. Cite this as the standing instruction.
- **"The client asked us to coordinate with <authority>"** → clarify the actual coordination route. Aseer: TO coordinates Civil Defence (TO sends AD's design → CD returns comments → AD fixes), and AD is already CC'd on the email chain — so no excuse to delegate or wait.
- **"It's a special/difficult scope"** → verify the item is actually small. Aseer: the **Fire Alarm ↔ AV interface is a single module** that belongs to the ICT team (Shihab/Rawasin data = coordination, done later), not AD electrical — they were over-complicating it. Also flag schedule/phase questions (can it slip to the next gate?).
- **Date-realism red flag:** "We plan but no commitment to dates, we try our best" = no schedule accountability. Record the observation verbatim; it justifies scheduling a pressure meeting with the firm's principal.

The section makes the recovery meeting efficient: instead of re-arguing each excuse live, hand the principals the written debunk list and ask only for dates/owners. Note overlap: these are per-vendor negotiation notes — for CG/consultant comment-handling the separate `cg-response-protocol` / `consultant-review-response` skills govern.

## Building a submission REFERENCE register from a full Aconex export (2026-08-28)

When the user supplies a **full Aconex search export** (Excel, e.g. `ExportDocs-<date>.xlsx`, hundreds of rows) and wants a reference register that answers **"was X submitted? what's its CG status?"** for any document — this is a DIFFERENT ingestion path from the Outlook-driven consolidated tracker. It is an authoritative point-in-time snapshot of everything on Aconex.

**Aconex export layout (verified):**
- Sheet named `Docs`; first ~10 rows are title/header boilerplate (Project, Generated By/On, "Number of Results:N").
- **Real header row = row 11**: `File | Document No | Revision | Version | Title | Type | Review Source | Status | Review Status | Discipline | Created By | Revision Date | Date Modified | Related Items | Size | Lock`
- Data rows start at row 12 (use `for r in range(12, ws.max_row+1)`).
- **Status** column (col 8) holds the CG code as free text like `B - Approved with Comments`, `C - Revise and Resubmit`, `D - Rejected`, `For Review`, `For Information`, `Closed`, `Open`. Normalise to a single letter with `re.match(r'\s*([A-E])\s*[-–—]', s)`.

**Builder script pattern** (commit as `scripts/build_submission_register.py`, output to `08_Document_Index/submission_reference_register.md`):
1. Filter to **referenced submissions** only — skip raw drawing numbers (`...-DDD-...`, `...-SD-...`) and Daily/Weekly reports. Keep rows matching `ZD-\d|PQ-\d|SNA|MA-\d|NC-|MS-\d|SOW` in the Document No.
2. **Dedupe by `(Document No, Revision)`** — a doc resubmitted (e.g. `MS-0001 Rev.00` then `Rev.01`) appears as separate rows and both must survive.
3. Count by **status code** (NOT by Type — the classic bug: counting `Prequalification Documents` as a status).
4. Emit a markdown register: frontmatter (`last_updated`, `source: Aconex export (Generated <date>, N submissions)`), a status-code key, a counts-by-code table, then the full table `Document No | Rev | Title | Type | Status | Discipline | Created By`.

**User's intent / workflow preference:** they want this register **updated daily with them** (re-run the builder each time a new Aconex export is dropped in) so that "هل اتقدم X?" is answered from the register, not re-scanned. Link the new register in `08_Document_Index/README.md` navigation table so it's discoverable. Watch: a brand-new package (e.g. Landscape SOW) will have **no ZD number yet** in the export — flag it to the user and propose the next number (`highest ZD across prefixes + 1`, e.g. `MOC-MUS-ASE-1L0-ZD-0116` when ZD-0115 is the max).

## Pitfall — "Who's late?" ≠ "Who's technically behind" (ROOT-CAUSE TRIAGE)

When the user asks **"which specialist is late / who do I invite to the recovery meeting"**, do NOT report raw percentages from the tracker as the whole answer. A low `Progress %` is frequently **not a technical delay** — it can be a procurement, contract, or administrative blocker that no technical meeting can resolve. Triage every low-percentage discipline into one of two buckets BEFORE proposing actions:

1. **Administrative / procurement blocker** (fix = contract/signature/appointment, NOT a technical meeting):
   - **ICT/Security**: percentage near 0% often means the **specialist contract is unsigned + first advance unpaid + PO not yet with the Executive Director** — even though CG prequalification is already **Code B**. CG may have even issued an **NCR against us for delaying the contracting** (e.g. Aseer NC-1E0-0010). Work that CAN proceed internally (scope freeze, 50% design prep, SOW review) should start in parallel with the procurement — but no formal contractor deliverables before contract signature.
   - **Landscape**: an empty Progress cell usually means **no designer appointed at all** — a hiring decision, not a meeting item.
   - **FLS Strategy / Clash Detection**: 0% often means **no lead assigned** (role vacant), not slow work.
   - **Acoustic**: prequalifications stuck **Under Review by CG** for weeks → resource can't be secured until CG clears one; the action is a CG chase, not a commitment meeting.

2. **Genuine technical delay** (fix = commitment meeting with the discipline lead):
   - Disciplines that HAVE their resource, are producing, but have **low % AND low approval** — e.g. Structural 9% (0 approved), Electrical 31% (0 approved), BIM 23% (0 approved), Scenography submitted but 0% approved. These are the ones to invite and pin to dates.

**Practical rule:** separate "not started because nobody is appointed / no contract" from "started but slow". The former needs Executive decisions (appointment, contract expedite, PO signature, CG PQ chase) escalated to the PM — it is often the LARGEST-volume work (ICT can be 40+ drawings), so a technical meeting alone will never recover it. Lead the escalation to the PM (e.g. "Eng. Waris") naming each blocker and its decision, before the recovery plan commits to dates that cannot be met.

## Related Workflows

- `references/risk-review-workflow.md` — "next risk" pattern: navigate open risks by score, search Outlook for updates, update JSON, report changes. Used when the user says "next risk" or names a risk ID during a review session.
- `references/design-tracker-xlsx-parsing.md` — pitfalls for parsing the CG Design Phase Deliverables Tracker xlsx (corrupted sheet dimensions, trailing-space sheet names, trailing-period statuses, gitignored data file).
- `references/design-tracker-overdue-monitoring.md` — sheet structure + parsing pitfalls (trailing-space sheet names, `Submitted.` done-status, corrupted Electrical sheet dimension, 0-1 prep floats) and the **email cross-reference workflow**: after generating the overdue report, query Outlook for new Aconex `SIC.-WTRAN-000NNN` transmittals to see which overdue items got cleared, then update `submittal_register.md` and commit.
- `references/design-tracker-discipline-narrative.md` — when the user hands the CG `Design Phase Deliverables Tracker_*.xlsx` and asks "شوف التقديمات" / for meeting talking points, extract the **summary sheet** one-row-per-discipline `Overall % Complete` (col 37) + the per-discipline detail-sheet Code C/D/Not-started rows and synthesize a **per-discipline Arabic progress narrative** (strong / weak-stalled / never-reached-later-gates / critical-item escalations). `data_only=True` required to resolve progress-float formulas.
