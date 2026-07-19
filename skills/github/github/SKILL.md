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

### Repo Governance Workflows

For project coordination repos (not code repos), set up these 4 governance workflows to automate compliance, validation, and reporting:

| Workflow | Trigger | Purpose | Key Check |
|----------|---------|---------|-----------|
| `validate-constitution.yml` | Every push/PR to `main` | Verify agent compliance acknowledgment | Agent listed in `agent_compliance.md` |
| `validate-registers.yml` | Every commit to `01_Registers/` | Run register validation script | All `.md` files have required frontmatter |
| `generate-dashboard.yml` | Weekly cron (Sun 08:00 UTC) + manual | Auto-generate status dashboard | Runs sync-state-tracker + validate-registers + dashboard generator |
| `protect-readonly-folders.yml` | Every push/PR to `main` | Block modifications to protected folders | No changes to `00_Contracts/` |

#### Pattern: validate-constitution.yml

```yaml
name: Validate Constitution Compliance
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  validate-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check agent_compliance.md exists
        run: |
          if [ ! -f "09_Agent_Workspace/agent_compliance.md" ]; then
            echo "❌ agent_compliance.md not found"
            exit 1
          fi
      - name: Verify agent is registered
        run: |
          AUTHOR="${{ github.event.head_commit.author.name }}"
          if ! grep -qi "$AUTHOR" "09_Agent_Workspace/agent_compliance.md"; then
            echo "❌ Agent '$AUTHOR' not registered in compliance table"
            exit 1
          fi
      - name: Post PR comment if non-compliant
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## ❌ Constitution Compliance Failed\n\nAgent not registered in compliance table.'
            });
```

#### Pattern: validate-registers.yml

```yaml
name: Validate Registers
on:
  push:
    paths: [ '01_Registers/**' ]
  pull_request:
    paths: [ '01_Registers/**' ]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run register validation
        run: python scripts/validate-registers.py
      - name: Post PR comment with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('00_Command_Center/validation_report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## Register Validation\n\n' + report
            });
```

#### Pattern: generate-dashboard.yml

```yaml
name: Generate Weekly Dashboard
on:
  schedule:
    - cron: '0 8 * * 0'  # Sunday 08:00 UTC
  workflow_dispatch:
jobs:
  generate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run sync-state-tracker
        run: bash scripts/sync-state-tracker.sh
      - name: Run register validation
        run: python scripts/validate-registers.py
      - name: Generate dashboard
        run: python scripts/generate_dashboard.py
      - name: Commit and push
        run: |
          git add 00_Command_Center/ .sync_state.json
          git diff --cached --quiet || (
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git config user.name "github-actions[bot]"
            git commit -m "chore(dashboard): weekly auto-update"
            git push
          )
```

#### Pattern: protect-readonly-folders.yml

```yaml
name: Protect Read-Only Folders
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  protect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - name: Detect changes to protected folders
        run: |
          VIOLATIONS=""
          for folder in "00_Contracts"; do
            CHANGED=$(git diff --name-only HEAD^ HEAD -- "$folder/" 2>/dev/null || true)
            if [ -n "$CHANGED" ]; then
              VIOLATIONS="${VIOLATIONS}❌ Changes in ${folder}/:\n${CHANGED}\n"
            fi
          done
          if [ -n "$VIOLATIONS" ]; then
            echo -e "$VIOLATIONS"
            exit 1
          fi
          echo "✅ No protected folders modified"
```

#### Agent Compliance Register

Create `09_Agent_Workspace/agent_compliance.md` to track which agents have acknowledged the repo's CONSTITUTION.md:

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: CONSTITUTION.md
---

# Agent Compliance Register

| Agent | Acknowledged | Date | Commit | Notes |
|-------|-------------|------|--------|-------|
| Hermes | ✅ | YYYY-MM-DD | abc1234 | ORDER N — description |
| Claude | ✅ | YYYY-MM-DD | def5678 | Initial commit |

## Acknowledgment Procedure

Each agent must add their acknowledgment when first operating on the repo:
1. Add a row with agent name, date, and commit hash
2. Commit with message prefix `[COMPLIANCE]`
3. CI verifies this file contains the agent's acknowledgment
```

#### Pitfalls

- **Workflow YAML must be valid** — inline heredocs (`<< 'EOF'`) inside `run:` blocks can create YAML parsing errors if the heredoc content contains `---` (YAML document separator). Use Python scripts or separate script files instead of inline heredocs for complex content generation.
- **`fetch-depth: 2` required for diff checks** — `protect-readonly-folders.yml` needs the parent commit to compare against. `fetch-depth: 1` (shallow clone) won't have `HEAD^`.
- **Secrets for Telegram notifications** — if workflows notify via Telegram, store `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as GitHub secrets. The notification step should gracefully handle missing secrets (check `-n "$VAR"` before calling curl).
- **Workflow_dispatch inputs** — boolean inputs need `type: boolean` not `type: choice` with options. Choice inputs need `options:` array.
- **PR comments from workflows** — `actions/github-script@v7` can post comments on PRs. Use `github.rest.issues.createComment` (not `pullRequests`) — PRs are issues in the API.
- **Step summary** — use `$GITHUB_STEP_SUMMARY` for workflow output that appears in the GitHub UI. This is better than relying on PR comments for non-PR triggers (scheduled workflows, pushes to main).

### Repo Governance Files (CHANGELOG, VERSION, CONSTITUTION Amendment Log)

For project coordination repos (not code repos), maintain these 3 governance files at the repo root:

#### CHANGELOG.md

Tracks governance and structural changes to the repo itself (not file content changes):

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: git log; CONSTITUTION.md
---

# Repository Changelog

> Governance and structural changes to the repo.
> This tracks how the repo itself evolves — not file content changes.

| Date | Agent | Change | Rationale |
|------|-------|--------|-----------|
| YYYY-MM-DD | Agent | Description of change | Why it was done |
```

**Rules:**
- One row per structural/governance change (new script, new plan structure, new compliance rule)
- Do NOT track routine file content updates (register edits, status updates)
- Group by ORDER or feature, not by individual commit
- ISO date, agent name, concise change description, one-line rationale

#### VERSION.md

Tracks the repo's governance version using semver:

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: CONSTITUTION.md; CHANGELOG.md
---

# Repository Version

| Field | Value |
|-------|-------|
| **Repository Version** | 1.0.0 |
| **CONSTITUTION Version** | 1.0 |
| **Last Governance Review** | YYYY-MM-DD |
| **Next Review Due** | YYYY-MM-DD (quarterly) |

## Semver Policy

- **Major** — Breaking governance change (CONSTITUTION rewrite, entity isolation change)
- **Minor** — New governance feature (new script, new plan structure, new compliance rule)
- **Patch** — Fixes, clarifications, non-breaking additions
```

#### CONSTITUTION Amendment Log

Add an `Article X — Amendment Log` section to the repo's CONSTITUTION.md:

```markdown
## Article X — Amendment Log

| Version | Date | Change | Author | Rationale |
|---------|------|--------|--------|-----------|
| 1.0 | YYYY-MM-DD | Initial enactment | Agent | Establish governing rules |
| 1.0 | YYYY-MM-DD | Added version tracking header | Agent | Enable governance versioning |
```

Also add a version tracking header at the top of CONSTITUTION.md:
```markdown
**Version:** 1.0  
**Effective Date:** DD Month YYYY  
**Last Amended:** DD Month YYYY  
**Approver:** Name — Title  
```

### Agent Compliance Tracking

For repos governed by a CONSTITUTION, maintain these 3 files in `09_Agent_Workspace/`:

#### 1. agent_compliance.md (CI-checked)

```markdown
---
last_updated: YYYY-MM-DD
owner_agent: <agent name>
status: active
source: CONSTITUTION.md
---

# Agent Compliance Register

| Agent | Last Sign-Off | Constitution v | Skills | Active Tasks |
|-------|--------------|----------------|--------|--------------|
| Hermes | YYYY-MM-DD | 1.0 | DMP, Registers, CI/CD | ORDER N |
| Claude | YYYY-MM-DD | 1.0 | Registers, Aconex | — |
```

Checked by `validate-constitution.yml` on every push/PR to main.

#### 2. handoff_protocol.md

Standard procedure for task handoffs between agents:

| Field | Required | Description |
|-------|----------|-------------|
| Date | ✅ | ISO 8601 |
| From Agent | ✅ | Agent handing off |
| To Agent | ✅ | Agent receiving |
| Task | ✅ | Brief description |
| Status | ✅ | Complete / In Progress / Blocked / Pending |
| Files Touched | ✅ | List of files modified |
| Remaining Work | ✅ | What still needs doing |
| Blockers | ✅ | Issues blocking progress |

**Procedure:**
1. Document current state — update `last_updated` and `owner_agent` on all touched files, commit
2. Write handoff entry in `handoff_log.md` with all required fields
3. Set `owner_agent` in frontmatter of relevant files to the receiving agent
4. For urgent handoffs, flag with `URGENT`

#### 3. task_template.md

Standard template for creating new tasks:

```yaml
---
task_id: TASK-NNN
title: <Brief task title>
owner_agent: <Agent name>
status: pending | in_progress | completed | blocked | cancelled
priority: Critical | High | Medium | Low
created: YYYY-MM-DD
deadline: YYYY-MM-DD
source: <Source document or request>
---
```

Template sections: Description, Why, Scope (in/out), Plan References, Register References, Deliverables table, Steps checklist, Success Criteria, Dependencies.

### Frontmatter Audit & Fix Scripts

For repos with many `.md` files that need YAML frontmatter compliance, create two reusable scripts:

#### audit_frontmatter.py

```python
#!/usr/bin/env python3
"""Scan all .md files and report frontmatter compliance."""
import os, re, sys

TARGET_DIRS = ['00_Status/', '01_Registers/', '03_Plans/', '05_Comms/',
               '08_Document_Index/', 'Technical_Office/', '09_Agent_Workspace/',
               '00_Command_Center/', '02_Schedule/', '04_Cost/', '00_Project_Charter/']
REQUIRED_FIELDS = ['last_updated', 'owner_agent', 'status', 'source']
VALID_STATUSES = {'active', 'draft', 'superseded', 'closed', 'archived'}

results = {'total': 0, 'clean': 0, 'critical': [], 'medium': []}

for d in TARGET_DIRS:
    for root, dirs, files in os.walk(d):
        for f in files:
            if not f.endswith('.md'): continue
            path = os.path.join(root, f)
            results['total'] += 1
            content = open(path).read()
            
            if not content.startswith('---'):
                results['critical'].append(path)
                continue
            
            end = content.find('---', 3)
            fm = content[3:end] if end > 3 else content[3:]
            
            missing = [rf for rf in REQUIRED_FIELDS if rf not in fm]
            if missing:
                results['medium'].append((path, missing))
                continue
            
            status_match = re.search(r'^status:\s*(.+)$', fm, re.M)
            if status_match and status_match.group(1).strip() not in VALID_STATUSES:
                results['medium'].append((path, [f'invalid status: {status_match.group(1).strip()}']))
                continue
            
            results['clean'] += 1

print(f"Total: {results['total']}, Clean: {results['clean']}, "
      f"Critical: {len(results['critical'])}, Medium: {len(results['medium'])}")
```

#### fix_frontmatter.py

```python
#!/usr/bin/env python3
"""Auto-fix missing frontmatter in .md files."""
import os

DEFAULT_FM = '''---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: {source}
---
'''

for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith('.md'): continue
        path = os.path.join(root, f)
        content = open(path).read()
        if content.startswith('---'): continue
        
        source = path.lstrip('./')
        new_content = DEFAULT_FM.format(source=source) + content
        open(path, 'w').write(new_content)
        print(f"Fixed: {path}")
```

#### Pitfalls

- **Frontmatter audit scripts are reusable** — `audit_frontmatter.py` and `fix_frontmatter.py` can be dropped into any markdown-heavy repo. Update `TARGET_DIRS` and `REQUIRED_FIELDS` per project. The fix script adds `last_updated: YYYY-MM-DD` as a placeholder — the agent should update the actual date after running.
- **CHANGELOG vs git log** — CHANGELOG.md is for governance/structural changes only. Do NOT mirror every git commit. One row per ORDER or feature, not per commit.
- **CONSTITUTION amendment log** — every structural change to the CONSTITUTION gets a row. Routine content updates (fixing typos, clarifying existing rules) do not need amendment log entries — only changes that add/remove/modify articles or sections.

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

## Related Reference Files

| File | When to Use |
|------|-------------|
| `references/pmi-pmbok-repo-structure.md` | Creating a new project repo organized by PMI PMBOK knowledge areas |
| `references/cron-status-repo.md` | Setting up a cron-driven repo that auto-syncs `.md` status files from a local source — scripts outside repo, silent delivery, 4× daily schedule |

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
