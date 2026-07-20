---
name: project-status-publishing
description: Automate daily project status extraction from PROJECT_MEMORY.md and publish to a GitHub repo via cron. Covers Python extraction script, cron job setup, and OneDrive-safe file handling.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [project-status, github, cron, automation, status-report]
    related_skills: [project-initializer, aseer-document-control]
---

# Project Status Publishing — Automated Daily GitHub Updates

## When to Use

- User says "set up daily status updates to GitHub for [project]"
- User says "read this repo and update daily"
- User has a GitHub repo with a `00_Status/project_status.md` file that needs daily auto-updates
- User wants a cron job that extracts project status from PROJECT_MEMORY.md and publishes it

## Core Pattern

```
PROJECT_MEMORY.md (OneDrive) → Python extraction script → 00_Status/project_status.md → git commit + push → GitHub
                                                                                                    ↑
                                                                                              cron job (daily)
```

## Step 1: Clone the Repo

```bash
cd ~ && gh repo clone <owner>/<repo-name>
```

## Step 2: Create the Update Script

Create `update_status.py` in `~/.hermes/scripts/` — **NOT in the repo root**. The repo should contain only `.md` files (status, mapping, docs). Scripts live in `~/.hermes/scripts/` and are referenced by the cron job via the `script` parameter.

The script should:

1. **Read PROJECT_MEMORY.md** from OneDrive (primary + fallback paths)
2. **Extract sections by heading** using a `get_section()` function
3. **Filter table lines** for each section (Snapshot, Critical Issues, Milestones, Pending)
4. **Write `00_Status/project_status.md`** with YAML frontmatter
5. **Commit and push** to GitHub

### Key Python Pattern: Section Extraction

```python
def get_section(text, heading_pattern):
    """Get content between heading and next heading of same level."""
    lines = text.split("\n")
    in_section = False
    result = []
    for line in lines:
        if re.match(heading_pattern, line):
            in_section = True
            result.append(line)
            continue
        if in_section:
            if re.match(r"^## \d+\.", line) or re.match(r"^## [A-Z]", line):
                break
            result.append(line)
    return "\n".join(result)
```

### Key Python Pattern: Table Line Filtering

```python
# Milestones: green/approved items
milestone_lines = [l for l in sec0.split("\n") if l.startswith("|") and ("✅" in l or "🟢" in l)]

# Pending items: yellow/red/email items (exclude completed)
pending_lines = []
for line in sec0.split("\n"):
    if not line.startswith("|"):
        continue
    if any(m in line for m in ["✅", "🟢", "✔", "—old", "—"]):
        continue
    if any(m in line for m in ["🟡", "🔴", "📧", "📋"]):
        pending_lines.append(line)
```

### Key Python Pattern: Diff Detection + Telegram Summary

```python
# --- Diff against previous version ---
old_content = STATUS_FILE.read_text() if STATUS_FILE.exists() else ""
changes = []
if old_content and old_content != content:
    old_lines = set(old_content.split("\n"))
    new_lines = set(content.split("\n"))
    added = new_lines - old_lines
    for line in sorted(added):
        stripped = line.strip()
        if stripped and not stripped.startswith("---") and not stripped.startswith("#") and not stripped.startswith("|--") and not stripped.startswith("*Auto") and not stripped.startswith("last_") and not stripped.startswith("owner_") and not stripped.startswith("status:") and not stripped.startswith("source:"):
            changes.append(stripped)
elif not old_content:
    changes.append("First run — full status generated")

# --- Write ---
STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
STATUS_FILE.write_text(content)

# --- Git (only if content changed) ---
if old_content == content:
    print(f"📋 **Aseer PM Status — {TODAY} {NOW}**")
    print(f"📁 Repo: github.com/sultandroid/aseer-museum-pm")
    print("ℹ️ No changes since last run — skipped commit.")
    sys.exit(0)

subprocess.run(["git", "add", str(STATUS_FILE)], cwd=REPO_DIR, check=True)
subprocess.run(["git", "commit", "-m", f"Update status: auto {TODAY}"], cwd=REPO_DIR, check=True)

# --- Telegram summary ---
print(f"📋 **Aseer PM Status — {TODAY} {NOW}**")
print(f"📁 Repo: github.com/sultandroid/aseer-museum-pm")
print(f"{'✅ Pushed' if pushed else '❌ Push failed'}")
print("")
if changes:
    print("**🆕 Updates:**")
    for c in changes[:10]:
        c_short = c[:200] + "…" if len(c) > 200 else c
        print(f"• {c_short}")
    if len(changes) > 10:
        print(f"… and {len(changes)-10} more changes")
```

```python
import subprocess
from pathlib import Path

REPO_DIR = Path.home() / "<repo-name>"
STATUS_FILE = REPO_DIR / "00_Status" / "project_status.md"

subprocess.run(["git", "add", str(STATUS_FILE)], cwd=REPO_DIR, check=True)
subprocess.run(["git", "commit", "-m", f"Update status: auto {TODAY}", "--allow-empty"], cwd=REPO_DIR, check=True)

for branch in ["main", "master"]:
    result = subprocess.run(["git", "push", "origin", branch], cwd=REPO_DIR, capture_output=True, text=True)
    if result.returncode == 0:
        break
```

## Step 3: Set Up Cron Job

Use the `cronjob` tool with these parameters:

| Parameter | Value | Reason |
|-----------|-------|--------|
| `action` | `create` | |
| `name` | `{Project} Status Daily` | Human-readable name |
| `schedule` | `0 8 * * *` | Daily at 8 AM KSA (or as requested) |
| `prompt` | "Run the daily status update script at ~/.hermes/scripts/{script}.py. Report result." | Self-contained instruction |
| `workdir` | `~/<repo>` | Script runs from repo root |
| `script` | `{script}.py` | Path relative to `~/.hermes/scripts/` — keeps binaries out of the repo |
| `enabled_toolsets` | `["terminal"]` | Only needs terminal for git operations |

### Multi-run schedules

For 4× daily updates, use comma-separated hours: `0 6,10,14,18 * * *`

### Delivery modes

| `deliver` | Behaviour |
|-----------|-----------|
| `"local"` | Silent — runs, updates repo, no message to user |
| `"origin"` | Sends output to the current chat (Telegram, etc.) |

### Diff-based Telegram summary

When `deliver: "origin"`, the script should produce a Telegram-friendly summary:

```
📋 **Aseer PM Status — 2026-07-09 08:26**
📁 Repo: github.com/sultandroid/aseer-museum-pm
✅ Pushed

**🆕 Updates:**
• 🟢 AD ENGINEERING APPOINTED as MEP Designer
• ✅ Patinated Brass (MA-0007) — FINAL APPROVED
• 🟡 Structural Loading Plans (DD 50%)
```

Implementation: compare old file content vs new, extract added lines (skip frontmatter/headers/separators), print as bullet list capped at 10 items. If no changes, print "ℹ️ No changes since last run — skipped commit." and exit without committing.

## Step 4: Test the Script

```bash
cd ~/<repo> && python3 update_status.py
```

Verify:
- [ ] `00_Status/project_status.md` was written with today's date
- [ ] YAML frontmatter has correct `last_updated` and `owner_agent`
- [ ] All sections populated (Snapshot, Critical Issues, Milestones, Pending)
- [ ] Git commit + push succeeded
- [ ] GitHub shows the updated file

## Status File Format

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: PROJECT_MEMORY.md (auto-extracted YYYY-MM-DD)
---

# Project Status — {Project Name}

## Snapshot

{Project identity table from PROJECT_MEMORY.md Section 1}

## Critical Active Issues

{Issue table from PROJECT_MEMORY.md Section 3}

## Recent Milestones

{Approved/completed items from Section 0}

## Open Registers Summary

| Register | Status |
|----------|--------|
| Submittals / IFC | See PROJECT_MEMORY.md Section 5 |
| RFIs / TQs | See PROJECT_MEMORY.md Section 10 |
| NCRs | See PROJECT_MEMORY.md Section 10 |
| Site Instructions | See PROJECT_MEMORY.md Section 10 |

## Next Reviews / Deadlines

{Pending/in-progress items from Section 0}

---
*Auto-generated YYYY-MM-DD from PROJECT_MEMORY.md (last manual update: {date})*
```

## Pitfalls

- **OneDrive sync blocks file reads** — Use a fallback path if the primary PROJECT_MEMORY.md is locked. The `_Project_Memory/` subfolder copy is often more accessible than the root copy.
- **Section 0 table has no unique row pattern** — All rows start with `||`. When patching, include surrounding context. Better: regenerate the whole file from scratch each time.
- **Pending items may be empty** — If Section 0 has no 🟡/🔴/📧/📋 items, provide a fallback message rather than an empty section.
- **Branch name** — Try `main` first, fall back to `master`. The repo may use either.
- **GitHub auth** — Requires `gh` CLI to be authenticated. If push fails, check `gh auth status`.
- **Script language** — Prefer Python over bash for text extraction. Bash `awk`/`sed` is fragile with Unicode emoji markers (✅🟡🔴) and multi-line table cells.
- **Cron job workdir** — Always set `workdir` to the repo root so relative paths in the script resolve correctly.
- **Cron job enabled_toolsets** — Restrict to `["terminal"]` to minimize token overhead. The script only needs git operations.
- **Scripts outside repo** — Keep scripts in `~/.hermes/scripts/`, not in the repo. The repo should contain only `.md` files (status, mapping, docs). Reference scripts via the cron job's `script` parameter.
- **Empty commit on no-change** — Compare old vs new content before committing. If identical, skip the commit entirely (no `--allow-empty`). Print "No changes since last run" and exit.
- **Git rebase conflicts** — When the remote has diverged (e.g. another agent pushed), use `git fetch origin main && git rebase origin/main`. If conflicts arise in `00_Status/project_status.md`, skip the conflicting commit (`git rebase --skip`) — the auto-generated file is ephemeral and the latest version supersedes all prior ones.
- **Odoo task mapping** — When the user asks to link Odoo ↔ repo status, create `01_Odoo_Mapping/task_mapping.md` with the full task tree. Query Odoo for all project tasks with parent info, then organize by parent task with subtask tables. See `references/odoo-task-mapping.md` for the full pattern.
- **Manual one-shot discovery** — When the user asks "what's new" / "check the repo" / "what did you learn", use `references/manual-repo-discovery.md` for the structured git-log + file-reads workflow. Distinct from the automated cron-driven pattern — this is an interactive deep-dive.
- **Odoo-to-repo comparison audit** — When the user asks to verify the repo status file against live Odoo data, use `references/odoo-repo-comparison.md` for the full workflow: query Odoo, compute metrics, check hash, find discrepancies. Covers deadline mismatches, stale source dates, modified tasks, and discipline progress computation.
- **Existing sync script** — The `aseer-pm-status.py` script at `~/.hermes/scripts/aseer-pm-status.py` implements a bidirectional sync (PROJECT_MEMORY.md → Odoo + Odoo → repo). It uses timestamp-based direction detection, milestone text matching, and discipline progress computation. Reference it when the user asks to run the sync rather than build a new one.
