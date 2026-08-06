# Git Rebase + Post-Commit Hook Recovery

The `aseer-museum-pm` repo has a post-commit hook that auto-regenerates `06_Risk_System/webapp/src/index.html` after every commit. This creates a specific failure mode during `git pull --rebase`.

## Symptom: "interactive rebase in progress"

After `git pull --rebase origin main`, the hook fires on the rebased commit. `git status` shows:

```
interactive rebase in progress; onto 46031ca
Last command done (1 command done):
   pick cdaba50 # Email scan ...
```

And `git push` fails with a network error (red herring — the real blocker is the incomplete rebase).

## Fix

```bash
git rebase --continue
git push origin main
```

The rebase has no actual conflicts — the hook's dirty state was already handled by the rebase machinery. Just continue it.

## Why this happens

1. `git pull --rebase` applies your commit on top of `origin/main`
2. The post-commit hook fires, regenerating `index.html`
3. The rebase machinery sees the hook's side-effect as a modification, but it's not a conflict
4. `git rebase --continue` accepts the state and completes the rebase
5. The working tree is clean and pushable

## What NOT to do

- Do NOT `git checkout -- index.html` mid-rebase — this can lose the hook's output
- Do NOT `git stash` mid-rebase — the stash captures the rebase state and creates confusion
- Do NOT force-push — the rebase is clean, just incomplete

## Related: post-commit hook + `git stash` approach

When you need to pull with rebase and the hook has already fired on your own commit (before the rebase), use the stash approach:

```bash
git add <your files>
git commit -m "..."
git stash                              # save the post-commit dirty state
git fetch origin && git rebase origin/main
git stash pop                          # may conflict in index.html — accept theirs
git checkout --theirs 06_Risk_System/webapp/src/index.html  # if conflicted
git add 06_Risk_System/webapp/src/index.html
git commit -m "merge: accept remote index.html"
git push origin main
```

## When to use which

| Situation | Approach |
|-----------|----------|
| `git pull --rebase` left rebase in progress | `git rebase --continue` then push |
| Remote has new commits, need to rebase cleanly | Stash approach above |
| No remote divergence, just need to push | `git checkout -- index.html` then push |
