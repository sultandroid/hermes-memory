# Cron-Driven Status-Only Repo Pattern

## When to Use

When you need a GitHub repo that auto-syncs project status from a local source (OneDrive, database, API) on a schedule. The repo contains **only `.md` files** — no scripts, no binaries, no generated artifacts.

## Architecture

```
~/aseer-museum-pm/          # Local clone (workdir for cron)
└── 00_Status/
    └── project_status.md   # The only tracked file

~/.hermes/scripts/
└── aseer-pm-status.py      # Update script (outside repo)
```

## Rules

1. **Scripts live in `~/.hermes/scripts/`** — never in the repo itself. The repo is for `.md` files only.
2. **Cron job references the script** via `script: <name>.py` — the cron runner executes it from `~/.hermes/scripts/`.
3. **`deliver: "local"`** — silent operation. No notifications to the user. The cron job updates the repo without spamming the chat.
4. **`workdir` set to the repo clone** — so `git add/commit/push` work from the right directory.

## Cron Setup

```bash
# Create the cron job
cronjob action=create \
  name="Project Status Sync" \
  schedule="0 6,10,14,18 * * *" \
  script="update_script.py" \
  deliver="local" \
  workdir="/Users/user/project-repo"
```

## Update Script Pattern

```python
#!/usr/bin/env python3
"""Daily update: extract from source → write .md → commit → push"""

import subprocess
from datetime import date
from pathlib import Path

REPO_DIR = Path.home() / "project-repo"
STATUS_FILE = REPO_DIR / "00_Status" / "status.md"
TODAY = date.today().isoformat()

# 1. Read source data (OneDrive, DB, API, file)
source = Path("/path/to/source.md").read_text()

# 2. Extract relevant sections
# 3. Write status file
STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
STATUS_FILE.write_text(content)

# 4. Commit and push (no binary files)
subprocess.run(["git", "add", str(STATUS_FILE)], cwd=REPO_DIR, check=True)
subprocess.run(["git", "commit", "-m", f"Update: auto {TODAY}", "--allow-empty"], cwd=REPO_DIR, check=True)
subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
```

## Pitfalls

- **Scripts in repo = user will ask you to remove them.** Keep the repo clean — only `.md` files tracked.
- **`deliver: "origin"` spams the user.** Always use `"local"` for silent cron jobs unless the user explicitly asks for notifications.
- **OneDrive EDEADLK** — When reading from OneDrive paths, the file may be locked. Use a fallback path or copy to `/tmp/` first.
- **`--allow-empty`** on commit prevents the cron job from failing when the content hasn't changed.
- **Multiple syncs per day** — the user may want 4× daily (06,10,14,18) rather than once. Ask or default to 4× for status repos.
