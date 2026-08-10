# Git Post-Commit Hook Auto-Regeneration Conflict Loop

## Symptom

The Aseer repo (`~/aseer-museum-pm`) has a **post-commit hook** that auto-rebuilds and redeploys the risk/lessons webapps after EVERY commit. This regenerates `06_Risk_System/webapp/src/index.html` and mutates `.sync_state.json`, `00_Command_Center/violations_log.md`, `99_Archive/adel_snapshots/file_list.txt`, etc. When pushing after register/email updates, this creates a recurring loop:

1. `git commit` → hook rebuilds webapp → files become dirty again
2. `git push` → rejected (remote has work, or "tip behind")
3. `git pull --rebase` → conflict in auto-generated files (`06_Risk_System/webapp/src/index.html`, `.sync_state.json`, `Technical_Office/Compliance_System/compliance_matrix.md`, `01_Registers/submittal_register.md`)
4. Every `git rebase --continue` re-fires the hook, dirtying files again → loop

This bit ~8 times in one session. The key is breaking the loop decisively.

## Robust Resolution Recipe

Work through these in order. **Always make the working tree fully clean before pulling/pushing.**

### 1. Commit ALL auto-generated changes first (break the loop)

The post-commit hook dirties files after each commit. Before pulling, commit those leftovers too, then pull.

```bash
cd ~/aseer-museum-pm
git add -A && git commit -m "Auto-sync: <what regenerated>" --no-verify   # --no-verify SKIPS the hook
```

Using `--no-verify` on the auto-sync commit stops the hook from re-firing on THAT commit, so the tree stays clean. (Hook still fires on your content commit — that's fine, commit its output next.)

### 2. If rebase has conflicts, resolve and keep the right side

For auto-generated files (webapp index.html, .sync_state.json, compliance_matrix.md), the **remote (theirs)** version is usually fine — it's just another agent/cron's output. Keep theirs:

```bash
git checkout --theirs .sync_state.json
git checkout --theirs 06_Risk_System/webapp/src/index.html
git checkout --theirs Technical_Office/Compliance_System/compliance_matrix.md
git add . && git commit -m "Resolve merge conflicts (accept theirs for auto-generated files)" --no-verify
```

For **manually-maintained registers** (submittal_register.md, specialist_register.md) you may need to merge: keep BOTH the remote row additions AND your new rows, removing the `<<<<<<<` / `=======` / `>>>>>>>` markers. Check the conflict first with `git diff --name-only --diff-filter=U` and `grep -n '<<<<<<<\|=======\|>>>>>>>' <file>`.

### 3. Rebase needs a non-interactive editor

The rebase pauses for commit-message editing. The post-commit hook can make `git rebase --continue` hang/timeout on the scp deploy step. Use:

```bash
GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git rebase --continue
```

Give it a generous timeout (90s+). The hook's scp failure (`dest open ... No such file or directory` for the LN webapp) is **non-fatal** — the rebase still completes; it just prints the scp error first.

### 4. Stale rebase state / interrupted rebase

If `git status` shows `HEAD (no branch)` and `.git/rebase-merge/` exists but `git rebase --continue` says "no rebase in progress":

```bash
rm -fr ".git/rebase-merge"
git rebase --abort 2>&1   # says "no rebase in progress" — fine
```

Then re-verify state: `git status -sb`. You may be "ahead N, behind M" with a clean tree — pull again.

### 5. Drop stale stashes

Repeated stash/pop cycles for auto-generated files leave noise. Once the working tree is clean and the branch is correct, drop the leftover auto-sync stashes:

```bash
git stash list
git stash drop "stash@{N}"   # one by one, oldest (auto-sync) entries
```

## Key insight

The post-commit hook means you can NEVER get a clean pull+push in one command — it re-dirties the tree after every commit. The pattern that works is:

```
commit content (hook fires, dirties tree)
→ git add -A + commit --no-verify (tree clean)
→ git pull --rebase (resolve conflicts if any)
→ git push
```

`--no-verify` is the lever that stops the loop — use it on the auto-sync commit so the tree stabilises. Do NOT use `--no-verify` to skip quality hooks you actually want; here it's specifically to stop the webapp-regeneration hook from re-dirtying after you've already captured its output.

## Aconex / register merge note

When merging `01_Registers/submittal_register.md` across agents, remote often adds rows you don't have (e.g. a TLC landscape offer, a new CG response). Preserve both sets of rows — dedup only if the same doc ref appears identically on both sides.
