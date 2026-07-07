---
name: github
description: "Complete GitHub workflow: authentication, repository management, pull requests, code review, issues, and CI/CD via `gh` CLI and `git`+`curl` fallbacks."
version: 2.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Git, PR, CI/CD, Issues, Code-Review, Repo-Management, Automation]
    related_skills: [requesting-code-review, simplify-code]
---

# GitHub Workflow

Complete guide for working with GitHub: auth setup, repo management, pull requests, code review, issues, releases, CI/CD, and secrets. Each section provides the `gh` CLI command first, then a `git`+`curl` fallback for machines without `gh`.

## Contents

1. [Authentication & Setup](#1-authentication--setup)
2. [Repository Management](#2-repository-management)
3. [Branch & Commit Workflow](#3-branch--commit-workflow)
4. [Pull Requests](#4-pull-requests)
5. [Code Review](#5-code-review)
6. [Issues Management](#6-issues-management)
7. [CI/CD & Actions](#7-cicd--actions)
8. [Releases & Secrets](#8-releases--secrets)

---

## 1. Authentication & Setup

### Detection Flow

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. `gh auth status` shows authenticated → use `gh` for everything
2. `gh` installed but not authenticated → use `gh auth login`
3. `gh` not installed → use git-only method

### Git-Only Auth (HTTPS with Personal Access Token)

```bash
# Configure credential caching
git config --global credential.helper store

# Set identity
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Test (will prompt for token once)
git ls-remote https://github.com/username/repo.git
```

### SSH Key Auth

```bash
# Generate key
ssh-keygen -t ed25519 -C "email@example.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub  # Add to GitHub: https://github.com/settings/keys

# Test
ssh -T git@github.com
```

### gh CLI Auth

```bash
gh auth login                    # Interactive browser login
echo "TOKEN" | gh auth login --with-token  # Token-based
gh auth setup-git                # Configure git to use gh
```

### Auth Detection Helper

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    # Extract from .hermes/.env or .git-credentials
    _env="${HERMES_HOME:-$HOME/.hermes}/.env"
    [ -f "$_env" ] && GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_env" | cut -d= -f2 | tr -d '\n\r')
    [ -z "$GITHUB_TOKEN" ] && GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  fi
fi

# Extract owner/repo
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | Use a personal access token as password |
| `permission denied` | Token lacks `repo` scope — regenerate with correct scopes |
| `authentication failed` | Run `git credential reject` then re-authenticate |
| SSH connection refused | Try SSH over HTTPS: add `Host github.com` with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |

---

## 2. Repository Management

### Cloning

```bash
# HTTPS
git clone https://github.com/owner/repo.git
# SSH
git clone git@github.com:owner/repo.git
# Shallow
git clone --depth 1 https://github.com/owner/repo.git
# With gh
gh repo clone owner/repo
```

### Creating Repos

```bash
# With gh
gh repo create my-project --public --clone
gh repo create my-project --private --description "..." --clone
gh repo create my-org/my-project --source . --public --push

# With curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name": "my-project", "private": false}'
```

### Forking & Syncing

```bash
gh repo fork owner/repo --clone

# Sync fork
git fetch upstream
git checkout main && git merge upstream/main && git push origin main
```

### Repository Settings

```bash
gh repo edit --description "..." --visibility public
gh repo edit --default-branch main --enable-wiki=false
```

### Branch Protection

```bash
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks": {"strict": true, "contexts": ["ci/test"]},
       "required_pull_request_reviews": {"required_approving_review_count": 1},
       "enforce_admins": false}'
```

---

## 3. Branch & Commit Workflow

### Branching

```bash
git checkout main && git pull origin main
git checkout -b feat/add-user-auth  # or fix/, refactor/, docs/, ci/
```

### Committing

```bash
git add src/auth.py
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing"
```

Conventional commit types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`.

### Pushing

```bash
git push -u origin HEAD
```

---

## 4. Pull Requests

### Creating PRs

```bash
# With gh
gh pr create --title "feat: add JWT auth" --body "## Summary\n..." \
  --draft --reviewer user1 --label "enhancement"

# With curl
BRANCH=$(git branch --show-current)
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{\"title\": \"feat: ...\", \"body\": \"## Summary\n...\",
       \"head\": \"$BRANCH\", \"base\": \"main\"}"
```

### Viewing PRs

```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
gh pr checks 123
```

### Merging

```bash
# Squash + delete branch (recommended)
gh pr merge --squash --delete-branch

# Auto-merge
gh pr merge --auto --squash --delete-branch

# With curl
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR/merge \
  -d '{"merge_method": "squash", "commit_title": "feat: ... (#123)"}'

# Clean up local branch
git checkout main && git pull origin main && git branch -D feature-branch
```

### CI Monitoring & Auto-Fix Loop

```bash
# Check CI
gh pr checks --watch
SHA=$(git rev-parse HEAD)

# Poll until done
for i in $(seq 1 20); do
  STATUS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] && break
  sleep 30
done
```

**Auto-fix loop:**
1. Check CI → identify failures
2. Read failure logs via `gh run view <RUN_ID> --log-failed` or download logs zip
3. Fix code with `patch`/`write_file`
4. `git add . && git commit -m "fix: ..." && git push`
5. Wait for CI → re-check
6. Repeat up to 3 attempts

---

## 5. Code Review

### Reviewing Local Changes (Pre-Push)

```bash
# Big picture
git diff main...HEAD --stat
git log main..HEAD --oneline

# Full diff
git diff main...HEAD

# File-by-file
git diff main...HEAD -- src/auth.py

# Common issues scan
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*="
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

### Reviewing a PR

```bash
# Check out PR locally
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Or with gh
gh pr checkout 123
```

### Posting Reviews

```bash
# Approve
gh pr review 123 --approve --body "LGTM!"
# Request changes
gh pr review 123 --request-changes --body "See inline comments."
# Comment
gh pr review 123 --comment --body "Some suggestions."

# Inline comments via API
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')
gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="Use parameterized queries." \
  -f path="src/auth.py" -f line=45 -f commit_id="$HEAD_SHA" -f side="RIGHT"
```

### Review Checklist

- **Correctness**: Does it do what it claims? Edge cases handled?
- **Security**: No hardcoded secrets, SQL injection, XSS?
- **Code Quality**: Clear naming, DRY, single responsibility?
- **Testing**: New code paths tested? Happy path + errors?
- **Performance**: No N+1 queries, appropriate caching?
- **Documentation**: Public APIs documented? README updated?

---

## 6. Issues Management

### Viewing Issues

```bash
gh issue list
gh issue list --state open --label "bug"
gh issue view 42
```

### Creating Issues

```bash
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description\n..." \
  --label "bug,backend" \
  --assignee "username"
```

### Managing Issues

```bash
# Labels
gh issue edit 42 --add-label "priority:high" --remove-label "needs-triage"

# Assignment
gh issue edit 42 --add-assignee username

# Comment
gh issue comment 42 --body "Investigated — root cause in auth middleware."

# Close/Reopen
gh issue close 42
gh issue reopen 42
```

### Issue Triage Workflow

1. List untriaged: `gh issue list --label "needs-triage" --state open`
2. Read and categorize each issue
3. Apply labels, priority, and assignee
4. Comment with triage notes

### Bulk Operations

```bash
# Close all issues with a specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"
```

---

## 7. CI/CD & Actions

### Workflows

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
```

### API Fallback

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows
```

---

## 8. Releases & Secrets

### Releases

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease
gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"
```

### Secrets (GitHub Actions)

```bash
gh secret set API_KEY --body "your-secret-value"
gh secret list
gh secret delete API_KEY
```

### Gists

```bash
gh gist create script.py --public --desc "Useful script"
```

---

## Quick Reference

| Action | gh | curl |
|--------|-----|------|
| Clone repo | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name` | `POST /user/repos` |
| List PRs | `gh pr list` | `GET /repos/o/r/pulls` |
| Create PR | `gh pr create` | `POST /repos/o/r/pulls` |
| Add comment | `gh pr comment N` | `POST /repos/o/r/issues/N/comments` |
| Merge PR | `gh pr merge` | `PUT /repos/o/r/pulls/N/merge` |
| List issues | `gh issue list` | `GET /repos/o/r/issues` |
| Create issue | `gh issue create` | `POST /repos/o/r/issues` |
| List workflows | `gh workflow list` | `GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `PUT /repos/o/r/actions/secrets/KEY` |
| Create release | `gh release create v1.0` | `POST /repos/o/r/releases` |

## Pitfalls

- **`gh` not installed**: All operations have `git`+`curl` fallbacks — no `gh` required.
- **Token expiry**: Personal access tokens expire. Set 90-day expiry or use fine-grained tokens.
- **Multiple accounts**: Use SSH with different keys per host alias in `~/.ssh/config`.
- **Credential persistence**: `git config --global credential.helper store` saves to `~/.git-credentials` in plaintext. Use `cache` instead for in-memory only.
- **GitHub API rate limits**: Unauthenticated: 60/hr. Authenticated: 5000/hr. Always include token.
