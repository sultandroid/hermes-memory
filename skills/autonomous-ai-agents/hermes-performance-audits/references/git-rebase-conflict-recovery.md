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
| Cron job reports `FAILED` / `provider timeout` / `idle for Ns` but the work was actually done | The LLM's final response timed out (idle limit ~600s) AFTER the git commit was made but BEFORE the push step ran. The commit exists locally, unpushed. | Check `git log -1` / `git status` first — do NOT redo the work. Then `git fetch origin && git rebase origin/main`, resolve conflicts, `git push`. |

## Recovery Sequence: "work done but push timed out" (preserve local commit)

When a cron job's LLM response timed out after committing but before pushing, the local commit is real work — do NOT discard it with `reset --hard`. Rebase it onto the remote instead:

```bash
# 1. Confirm the work is actually done (do NOT redo it)
git log -1 --format='%h %ci %s'          # shows the auto-commit
git status --short                        # clean = commit captured everything

# 2. Fetch and rebase local commit onto remote
git fetch origin
git log HEAD..origin/main --oneline        # see what the remote added
git rebase origin/main

# 3. Resolve conflicts (usually trivial — e.g. a date-stamp field)
#    Keep the cron job's value (today's date) over the remote's older value.
#    Edit the conflicted file, then:
git add <conflicted-file>
GIT_EDITOR=true git rebase --continue

# 4. Push
git push origin main
git log origin/main..HEAD --oneline        # empty = fully pushed
```

Key point: a `FAILED` cron status with a `provider timeout` / `idle for Ns` error does NOT mean the job's work failed. The commit may already exist locally. **Check `git log`/`git status` before re-running the job or redoing any work.**

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
