# Plan Status Update from Email — Workflow

When the user provides a list of project plans with their statuses and asks to "search for updates from emails", the workflow is:

## Phase 1 — Query Outlook by Plan Doc Codes

Search for each plan's document code (PL-XXXX, ZD-XXXX, SC-XXXX) and subject keywords (SMP, PEP, RMP, Fire Prevention, etc.) in Outlook SQLite.

**Canonical query pattern:**
```sql
SELECT m.Message_NormalizedSubject,
       datetime(m.Message_TimeReceived, 'unixepoch', '31 years') as received,
       substr(m.Message_Preview,1,300) as preview
FROM Mail m
WHERE (
  m.Message_NormalizedSubject LIKE '%SMP%'
  OR m.Message_NormalizedSubject LIKE '%PEP%'
  OR m.Message_NormalizedSubject LIKE '%RMP%'
  OR m.Message_NormalizedSubject LIKE '%Fire Prevention%'
  -- ... one LIKE per plan
)
ORDER BY m.Message_TimeReceived DESC
LIMIT 30;
```

**Epoch pitfall:** The active DB at `Data/Outlook.sqlite` uses Unix epoch. Always verify with the test query first. If the epoch is Mac (Jan 1 1904), use `datetime(col + 978307200, 'unixepoch')`.

## Phase 2 — Extract CG Codes from Preview

CG responses from Hossam Mabrouk follow a consistent pattern in `Message_Preview`:
```
Classification-ASE-External-DS-XXXX-XXXX
...
B - Approved with Comments       ← or "C - Revise and Resubmit"
REF. MOC-MUS-ASE-1XX-ZD-XXXX
```

Read the CG code directly from preview — no attachment extraction needed for Code B.

## Phase 3 — Map Status Changes

| Email Signal | Status Change |
|-------------|---------------|
| `B - Approved with Comments` | Code D → **Code B** |
| `C - Revise and Resubmit` | Code B → **Code C** (or stays Code C) |
| `Rev.02 submitted` | Previous Rev Code C → **Submitted 🟡** |
| `NRS query re receipt` | Submitted — still awaiting |

## Phase 4 — Cascade to 3 Files

Update these files in `aseer-museum-pm/08_Document_Index/`:

1. **`00_plan_tracker.md`** — the master tracker. Update:
   - `last_updated` date in YAML frontmatter
   - CG status, revision, and next action for each changed plan
   - Move plans between sections (e.g., Code D → Code B moves from "Needs Revision" to "Approved")
   - Summary stats at bottom (Code B count, Code D count, etc.)

2. **`obligation_matrix.md`** — the obligation matrix. Update:
   - `last_updated` date
   - CG status and next obligation for each changed plan
   - Move plans between sections

3. **`approved_plans.md`** — the approved plans index. Update:
   - `last_updated` and `owner_agent` in YAML frontmatter
   - Add new revision rows for plans that changed status
   - Update status codes and notes

## Phase 5 — Git Commit & Push

```bash
cd /Users/mohamedessa/aseer-museum-pm
git add 08_Document_Index/00_plan_tracker.md 08_Document_Index/obligation_matrix.md 08_Document_Index/approved_plans.md
git commit -m "update plan tracker: <summary of key changes>"
git pull --rebase origin main
git push origin main
```

**Pitfall — post-commit hook dirties index.html:** After commit, `git checkout -- 06_Risk_System/webapp/src/index.html` before push to discard the auto-generated copy. If remote has diverged, use stash approach.

## Plans Tracked (Aseer Museum)

| Category | Count | Plans |
|----------|-------|-------|
| ✅ Code B (Approved) | 16 | DMP, Stakeholder, Communication, HSE overarching, ERP, Heat Stress, Lifting Ops, Reward, Mobile Equipment, HSE Training, Temporary Electrical, Injury & Illness, BEP, Resource Management, Site Security, HSE Induction Training |
| 🔴 Code C (Revise & Resubmit) | 2 | Fire Prevention, Worker Welfare |
| 🔴 Code C Resubmitted | 1 | Environment & Waste |
| 🟡 Draft (Not Submitted) | 2 | Mobilization, PQP |
| 🟡 Submitted to CG (Awaiting) | 3 | RMP (Rev.01), SMP, PEP (Rev.02) |
| ⬜ Missing (Not Created) | 7 | Schedule, Cost, Change, Commissioning, Security, IT/AV, Training |
