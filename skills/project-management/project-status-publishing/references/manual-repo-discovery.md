# Manual Repo Discovery — What's New in a Project Repo

## When to use

User asks "what's new" / "check the repo" / "what did you learn" about a project repo (typically an `.md`-heavy project management repository, not a codebase). The goal is surface actionable intelligence from recent commits — not a raw git log.

## Workflow

### 1. Establish baseline

```bash
cd ~/<repo>
git log --oneline -20
git diff --stat HEAD~5..HEAD   # or HEAD~N..HEAD for the period
```

Scan the diff stat for clusters:
- New files appearing (registers, plans, command-center structures)
- Updated files (registers revised, plans edited)
- Deleted/archived files

### 2. Read the command center first

If the repo has a command center / master dashboard / plan tracker, read it before diving into individual files. It tells you the current canonical structure.

Targets in priority order:
- `00_Command_Center/master_dashboard.md` — operating model
- `08_Document_Index/00_plan_tracker.md` — plan approval status
- `00_Status/action_items.md` — current actions
- `01_Registers/` — risk register, submittal register, weekly report board

### 3. Drill into new or heavily-changed files

For each new file or file with >50 lines changed:
- Read the first 30-50 lines (frontmatter + opening sections)
- Read the findings/headlines section if one exists
- Read the gaps/risks/blockers section

File types and expected content:
| Pattern | What to expect |
|---------|---------------|
| `01_Registers/*` | Tables of risks, submittals, SORs, reports |
| `02_Schedule/*` | Submission plans, validation reports |
| `03_Plans/*/` | Plan documents, review emails, CR sheets |
| `10_Manager_Lanes/*/` | Dashboard per discipline manager |
| `Technical_Office/*` | Compliance systems, specialist management |
| `_skills/*` | In-repo skills for agent workflows |

### 4. Cross-reference against known gaps

Before reporting, check:
- New data that confirms or contradicts previously known blockers (e.g. schedule slippage numbers, contract value)
- New risks or treatments added to risk register
- New registers that fill previously-flagged gaps (e.g. weekly report board filling "no cash position data" gap)
- Plans moved from "draft" to "submitted" or "approved"
- Plans stuck at Code C/D that need escalation

### 5. Structure the findings report

Deliver as:
1. **Theme clusters** — group related changes (e.g. "Risk Management System overhauled", "Weekly Report Board — new data")
2. **Key findings per theme** — what was added, what it means
3. **Gaps/risks summary table** — new or updated blockers surfaced

Table format:
| Item | Status |
|------|--------|
| Description of gap | Current state / due date |

### 6. Priority reading order for a healthy repo check

| Step | What | Why |
|------|------|-----|
| 1 | `git log --oneline -20` | See the last 20 commits at a glance |
| 2 | `git diff --stat HEAD~5..HEAD` | See which files actually changed |
| 3 | `00_Command_Center/` files | Understand current operating model |
| 4 | `08_Document_Index/00_plan_tracker.md` | Know what's approved, drafted, or stuck |
| 5 | New/changed registers | Surface new data (weekly reports, risks, SORs) |
| 6 | New/changed plans | Check for revisions, CR sheets, reviews |
| 7 | Cross-reference findings against known blockers | Produce actionable table |

## Pitfalls

- **Don't just dump git log** — the user wants synthesis, not a raw commit list
- **Read frontmatter** — YAML frontmatter often contains `last_updated`, `owner_agent`, `source` that explain context
- **Check `.sync_state.json`** if present — shows last sync timestamps
- **Don't skip the plan tracker** — it's often the best aggregation of CG approval status
- **New directories (like `10_Manager_Lanes/`)** signal structural change — read the README first, then drill per-lane
- **Look at commit authors** — commits from `sultandroid` vs agents tell you who did what
