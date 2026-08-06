# Git Rebase Conflict Recovery for Cron Jobs

Patterns for recovering from git rebase conflicts, detached HEAD, and non-fast-forward push rejections during auto-sync cron jobs.

## Common Failure Modes

| Symptom | Root Cause | Quick Fix |
|---------|-----------|-----------|
| `rebase-merge directory already exists` | Previous rebase interrupted, not cleaned up | `rm -rf .git/rebase-merge` then retry |
| `detached HEAD` after rebase | Conflict resolution landed commit on detached HEAD | `git checkout <branch> && git reset --hard origin/<branch>` |
| `non-fast-forward` push | Local branch diverged from remote | `git fetch origin && git reset --hard origin/main` (nuclear — safe for auto-sync scripts) |
| `EDITOR unset` on rebase --continue | Non-interactive environment | `GIT_EDITOR=true git rebase --continue` |
| `Your branch and 'origin/main' have diverged` | Local commits not on remote | `git fetch origin && git reset --hard origin/main` |

## Recovery Sequence (for auto-sync scripts)

```bash
# 1. Clean up stale rebase state
rm -rf .git/rebase-merge 2>/dev/null

# 2. Fetch and reset to remote (safe for auto-sync — local changes are copies)
git fetch origin
git checkout main 2>/dev/null || true
git reset --hard origin/main

# 3. Apply local updates
cp ~/.hermes/memories/MEMORY.md MEMORY.md
# ... other copies ...

# 4. Commit and push
git add -A
git commit -m "Auto-sync $(date '+%Y-%m-%d %H:%M')"
git push origin main
```

## When to Use Each Approach

| Approach | When | Risk |
|----------|------|------|
| `git pull --rebase` | Manual work, want to preserve local commits | Low — preserves history |
| `git reset --hard origin/main` | Auto-sync scripts, local is a copy of source files | None — local changes are copies |
| `git checkout --theirs` + `git add` | Conflict resolution during rebase | Low — accepts remote version |
| `GIT_EDITOR=true git rebase --continue` | Non-interactive rebase completion | None — accepts default message |

## Prevention

- Always `git fetch origin` before `git pull --rebase` to detect divergence early
- For auto-sync scripts, prefer `git reset --hard origin/main` over rebase — simpler, fewer failure modes
- After `git commit`, check for post-commit hooks that dirty tracked files (e.g. auto-regeneration of index.html). Stash or checkout those files before the next `git pull --rebase`
