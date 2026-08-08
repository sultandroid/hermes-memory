---
name: github-private-repo-discovery
description: "Find whether a GitHub issue/PR exists across a user's repos, and correctly handle private repos that return 404 to unauthenticated curl. Use when asked 'why can't I see issue #N' or 'is this issue in the repo'."
version: 1.0.0
author: hermes
platforms: [macos, linux]
metadata:
  hermes:
    tags: [github, issues, private-repo, gh-cli, discovery]
---

# GitHub Private-Repo Issue/PR Discovery

When asked "why can't I see issue #N in the repo?" or "is this issue/PR in the repo?", the most common root cause is a **private repo returning 404 to unauthenticated access** — not a genuinely missing issue.

## The core pitfall

A bare `curl -s https://api.github.com/repos/<owner>/<repo>/issues/<N>` (no token) returns **HTTP 404 for a private repo**, which is indistinguishable from a genuinely absent issue. This produced a real false negative: an issue was reported "doesn't exist" when it was simply in a private repo the user owns.

**Rule: never conclude "not found" from an unauthenticated curl 404.** Always use `gh` (which carries the authenticated token) first.

## Correct workflow

1. **Use `gh` first** — it authenticates as the logged-in user:
   ```bash
   gh issue view N --repo owner/repo
   gh pr view N --repo owner/repo
   ```
   If `gh auth status` shows an active account, `gh` is authoritative.

2. **If the user doesn't name the repo**, scan all their repos for the number:
   ```bash
   for repo in $(gh repo list <owner> --limit 100 --json name | python3 -c "import sys,json; [print(r['name']) for r in json.load(sys.stdin)]"); do
     code=$(gh api repos/<owner>/$repo/issues/N --jq '.number' 2>/dev/null && echo "FOUND in $repo" || echo "$repo: not here")
   done
   ```
   Or check HTTP status per repo with authenticated `gh api`:
   ```bash
   gh api repos/<owner>/$repo/issues/N -i 2>/dev/null | head -1   # HTTP/2 200 vs 404
   ```

3. **Only trust a 404 as "genuinely absent" after an authenticated check** (`gh` or `gh api` with token). Unauthenticated curl 404 is meaningless for private repos.

4. **Check both issues AND PRs** — the number may be a pull request, not an issue. `gh pr view N` separately.

## Pitfalls

- **`gh repo list` returns private repos too** (it's authenticated) — use it to enumerate, don't guess repo names.
- **A 404 from `gh` on a repo you own** usually means the number genuinely doesn't exist there — but still scan sibling repos before concluding.
- **Don't fabricate the repo name.** If the user says "the repo" but you have several, enumerate `gh repo list` and check each rather than assuming.
- **`curl` without `-H "Authorization: token ..."` is unauthenticated** — always prefer `gh` for private-repo lookups.
